package pl.reaper.container.beans;

import javax.ejb.Local;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Local
public interface JythonEngineHolderLocal {

    public ScriptEngineWrapper getJythonEngine();
}
