package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.List;
import pl.reaper.container.data.Script;

public class ScriptLoaderSimpleImpl implements ScriptLoader {

    @Override
    public List<Script> loadScriptChain(String name) {
        List<Script> chain = new ArrayList<>();
        if ("init".equals(name)) {
        } else {
            chain.add(getSimpleScript(name));
        }
        return chain;
    }

    private Script getSimpleScript(String name) {
        Script simple = new Script();
        simple.setName(name);
        simple.setScript("output.setResult('test')");
        simple.setOnInit("");
        return simple;
    }
}
