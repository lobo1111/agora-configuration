package pl.reaper.container.jython;

import java.util.List;
import pl.reaper.container.data.Script;

public interface ScriptLoader {

    public List<Script> loadScriptChain(String name);
    
    public List<Script> loadBaseScripts();
}
