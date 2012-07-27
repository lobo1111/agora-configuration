package pl.reaper.container.jython;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

public class JythonExecutor {

    private ScriptEngine engine;

    public JythonExecutor() {
        engine = new ScriptEngineManager().getEngineByName("python");
    }

    public String executeScript(String script) throws Exception {
        engine.put("output", -1);
        engine.eval(script);
        return (String) engine.get("output");
    }
}
