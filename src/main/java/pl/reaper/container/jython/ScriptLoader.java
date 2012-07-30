package pl.reaper.container.jython;

import java.util.List;

public interface ScriptLoader {

    public void loadScriptChain(String name, List<Script> chain);
}
