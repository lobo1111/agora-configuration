package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Local
public interface ScriptCompilatorLocal {

    public Object compile(ScriptEngineWrapper engineBuilder, String scriptName, Map variables);
}
