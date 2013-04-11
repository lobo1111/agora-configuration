package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;
import javax.script.ScriptEngineManager;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Local
public interface ScriptEngineCacheLocal {

    public ScriptEngineWrapper get(String scriptName);

    public boolean contains(String scriptName);

    public Object init(String ScriptName, Map variables);

    public ScriptEngineManager getEngineManager();

    public void releaseEngine(String scriptName, ScriptEngineWrapper engine);
}
