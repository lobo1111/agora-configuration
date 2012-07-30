package pl.reaper.container.jython;

import java.util.List;

public class ScriptLoaderSimpleImpl implements ScriptLoader {

    @Override
    public void loadScriptChain(String name, List<Script> chain) {
        if ("init".equals(name)) {
        } else {
            chain.add(getSimpleScript(name));
        }
    }

    private Script getSimpleScript(String name) {
        Script simple = new Script();
        simple.setName(name);
        simple.setScript("output.setResult('test')");
        simple.setOnInit("");
        return simple;
    }
}
