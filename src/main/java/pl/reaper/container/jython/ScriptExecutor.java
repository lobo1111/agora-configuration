package pl.reaper.container.jython;

import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import pl.reaper.container.data.Script;
import pl.reaper.container.jython.scripts.Output;

public class ScriptExecutor {

    private ScriptLoader loader;
    private EntityManager entityManager;

    public ScriptExecutor(ScriptLoader loader, EntityManager entityManager) {
        this.loader = loader;
        this.entityManager = entityManager;
    }

    private List<Script> loadScriptChain(String name) throws ScriptEngineNotFoundException {
        List<Script> initChain = loader.loadScriptChain("init");
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Base scripts loaded({0})", Arrays.deepToString(initChain.toArray(new Script[initChain.size()])));
        List<Script> scriptChain = loader.loadScriptChain(name);
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script chain loaded({0})", Arrays.deepToString(scriptChain.toArray(new Script[scriptChain.size()])));
        initChain.addAll(scriptChain);
        return initChain;
    }

    private Object executeScripts(List<Script> scripts, Map variables) {
        String finalScript = "";
        ScriptEngine engine = null;
        Object result = null;
        try {
            engine = getEngine(variables);
            for (Script script : scripts) {
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Initializing script {0}...", script.getName());
                finalScript += "\n" + script.getScript();
                engine.eval(finalScript);
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
            }
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing final script...");
            engine.eval(finalScript + "\n" + scripts.get(scripts.size() - 1).getOnInit());
            result = extractResult(engine);
        } catch (ScriptEngineNotFoundException | ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, "Script content:\n[[" + finalScript + "]]", ex);
            result = ex.getMessage();
        }
        return result;
    }

    public String prepareAndExecuteScript(String name, Map variables) {
        try {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing script: {0}", name);
            String result = String.valueOf(executeScripts(loadScriptChain(name), variables));
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script executed, result: {0}", result);
            return result;
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, ex.getMessage(), ex);
            return ex.getMessage();
        }
    }

    private ScriptEngine getEngine(Map variables) throws ScriptEngineNotFoundException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            throw new ScriptEngineNotFoundException("Python engine not found");
        }
        prepareEngine(engine, variables);
        return engine;
    }

    private void prepareEngine(ScriptEngine engine, Map variables) {
        engine.getContext().setWriter(new PrintWriter(System.out));
        engine.put("output", new Output());
        engine.put("entityManager", entityManager);
        addVariables(variables, engine);
    }

    private Object extractResult(ScriptEngine engine) {
        Output output = (Output) engine.get("output");
        if (output != null && output.getResult() != null && !"".equals(output.getResult())) {
            return output.getResult();
        } else {
            return "<no output>";
        }
    }

    private void addVariables(Map variables, ScriptEngine engine) {
        Iterator varsIterator = variables.keySet().iterator();
        while (varsIterator.hasNext()) {
            String key = (String) varsIterator.next();
            String value = (String) variables.get(key);
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Variables set: {0}={1}", new Object[]{key, value});
            engine.put("pre_" + key, value);
        }
    }

}
