package pl.reaper.container.jython;

import java.util.List;
import javax.script.ScriptException;
import pl.reaper.container.data.Script;

public interface ScriptLoader {

    public List<Script> loadScriptChain(String name);
}
