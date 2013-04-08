package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Local
public interface ScriptCompilatorLocal {

    public ScriptEngineWrapper compileScript(String scriptName, Map variables);
}
