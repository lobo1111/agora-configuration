package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import pl.reaper.container.jython.scripts.Output;

public class ScriptExecutor {
    private ScriptLoader loader;
    
    public ScriptExecutor(ScriptLoader loader) {
        this.loader = loader;
    }

    private List<Script> loadScriptChain(String name) throws ScriptNotFoundException {
        ArrayList<Script> chain = new ArrayList<>();
        loader.loadScriptChain("init", chain);
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Base scripts loaded({0})", Arrays.deepToString(chain.toArray(new Script[chain.size()])));
        loader.loadScriptChain(name, chain);
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script chain loaded({0})", Arrays.deepToString(chain.toArray(new Script[chain.size()])));
        return chain;
    }

    private Object executeScripts(List<Script> scripts) throws ScriptException {
        try {
            ScriptEngine engine = getEngine();
            String finalScript = "";
            for (Script script : scripts) {
                finalScript = initScript(finalScript, script, engine);
            }
            engine.eval(finalScript);
            return extractResult(engine);
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, ex.getMessage(), ex);
            return ex.getMessage();
        }
    }

    public String prepareAndExecuteScript(String name) {
        try {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing script: {0}", name);
            String result = String.valueOf(executeScripts(loadScriptChain(name)));
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script executed, result: {0}", result);
            return result;
        } catch (ScriptNotFoundException | ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, ex.getMessage(), ex);
            return ex.getMessage();
        }
    }

    private ScriptEngine getEngine() throws ScriptEngineNotFoundException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if(engine == null) {
            throw new ScriptEngineNotFoundException("Python engine not found");
        }
        prepareEngine(engine);
        return engine;
    }

    private void prepareEngine(ScriptEngine engine) {
        engine.put("output", new Output());
    }

    private Object extractResult(ScriptEngine engine) {
        Output output = (Output)engine.get("output");
        if(output != null && output.getResult() != null && !"".equals(output.getResult())) {
            return output.getResult();
        } else {
            return "<no output>";
        }
    }

    private String initScript(String finalScript, Script script, ScriptEngine engine) throws ScriptException {
        finalScript += script.getScript();
        engine.eval(finalScript + "\n" + script.getOnInit());
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
        return finalScript;
    }
}
