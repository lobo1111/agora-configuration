package pl.reaper.container.jython;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

public class JythonExecutor {

    private ScriptEngine engine;

    public JythonExecutor() throws Exception {
        engine = new ScriptEngineManager().getEngineByName("python");
        if(engine == null) {
            throw new Exception("Python scripting engine not found !");
        }
    }

    public String executeScript(String script) throws Exception {
        engine.eval(script);
        return String.valueOf(engine.get("output"));
    }
}
