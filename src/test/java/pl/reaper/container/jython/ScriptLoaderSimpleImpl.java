package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.List;
import pl.reaper.container.data.Script;

public class ScriptLoaderSimpleImpl implements ScriptLoader {

    @Override
    public List<Script> loadScriptChain(String name) {
        List<Script> chain = new ArrayList<>();
        if ("init".equals(name)) {
        } else if("simple".equals(name)) {
            chain.add(getSimpleScript(name));
        } else if("vars".equals(name)) {
            chain.add(getVarsScript(name));
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

    private Script getVarsScript(String name) {
        Script simple = new Script();
        simple.setName(name);
        simple.setScript("output.setResult(customVar)");
        simple.setOnInit("");
        return simple;
    }
}
