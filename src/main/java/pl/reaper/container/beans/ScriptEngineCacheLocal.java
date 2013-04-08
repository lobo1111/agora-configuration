package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;
import javax.script.ScriptEngineManager;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Local
public interface ScriptEngineCacheLocal {

    public ScriptEngineWrapper get(String scriptName, Map variables);

    public ScriptEngineManager getEngineManager();
}
