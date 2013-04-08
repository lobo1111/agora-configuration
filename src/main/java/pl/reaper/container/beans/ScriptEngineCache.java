package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import javax.ejb.EJB;
import javax.ejb.Singleton;
import javax.script.ScriptEngineManager;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Singleton
public class ScriptEngineCache implements ScriptEngineCacheLocal {

    private Map<String, ScriptEngineWrapper> cache = new HashMap<>();
    private ScriptEngineManager engineManager;
    @EJB
    private ScriptCompilatorLocal compilator;

    public ScriptEngineCache() {
        engineManager = new ScriptEngineManager();
    }

    @Override
    public ScriptEngineWrapper get(String scriptName, Map variables) {
        if (!cache.containsKey(scriptName)) {
            cache.put(scriptName, compilator.compileScript(scriptName, variables));
        }
        ScriptEngineWrapper engine = cache.get(scriptName);
        engine.resetVariables()
                .addVariables(variables);
        return engine;
    }

    @Override
    public ScriptEngineManager getEngineManager() {
        return engineManager;
    }
}
