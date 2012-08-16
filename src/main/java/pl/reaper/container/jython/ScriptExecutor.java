package pl.reaper.container.jython;

import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;
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

    private Object executeScripts(List<Script> scripts) {
        String finalScript = "";
        try {
            ScriptEngine engine = getEngine();
            for (Script script : scripts) {
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Initializing script {0}...", script.getName());
                finalScript += "\n" + script.getScript();
                engine.eval(finalScript);
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
            }
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing final script...");
            engine.eval(finalScript + "\n" + scripts.get(scripts.size() - 1).getOnInit());
            return extractResult(engine);
        } catch (ScriptEngineNotFoundException | ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, "Script content:\n[[" + finalScript + "]]", ex);
            return ex.getMessage();
        }
    }

    public String prepareAndExecuteScript(String name) {
        try {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing script: {0}", name);
            String result = String.valueOf(executeScripts(loadScriptChain(name)));
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script executed, result: {0}", result);
            return result;
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, ex.getMessage(), ex);
            return ex.getMessage();
        }
    }

    private ScriptEngine getEngine() throws ScriptEngineNotFoundException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            throw new ScriptEngineNotFoundException("Python engine not found");
        }
        prepareEngine(engine);
        return engine;
    }

    private void prepareEngine(ScriptEngine engine) {
        engine.getContext().setWriter(new PrintWriter(System.out));
        engine.put("output", new Output());
        engine.put("entityManager", entityManager);
    }

    private Object extractResult(ScriptEngine engine) {
        Output output = (Output) engine.get("output");
        if (output != null && output.getResult() != null && !"".equals(output.getResult())) {
            return output.getResult();
        } else {
            return "<no output>";
        }
    }
}
