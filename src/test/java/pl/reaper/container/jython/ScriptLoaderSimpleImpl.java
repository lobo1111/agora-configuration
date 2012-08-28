package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.List;
import pl.reaper.container.data.Script;

public class ScriptLoaderSimpleImpl implements ScriptLoader {
    
    private static final String OUTPUT = "from pl.reaper.container.jython.scripts import OutputInterface"
            + "\nclass Output(OutputInterface):"
            + "\n\t_result = ''"
            + "\n\tdef getResult(self):"
            + "\n\t\treturn self._result"
            + "\n\tdef setResult(self, result):"
            + "\n\t\tself._result = result"
            + "\n\tdef appendResult(self, result):"
            + "\n\t\tself._result += result";

    @Override
    public List<Script> loadScriptChain(String name) {
        List<Script> chain = new ArrayList<>();
        if("simple".equals(name)) {
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
        simple.setScript("output.setResult(vars.get('customVar'))");
        simple.setOnInit("");
        return simple;
    }

    @Override
    public List<Script> loadBaseScripts() {
        Script s = new Script();
        s.setBase(true);
        s.setName("output");
        s.setOnInit("output = Output()");
        s.setParent(null);
        s.setScript(OUTPUT);
        List<Script> l = new ArrayList<>();
        l.add(s);
        return l;
    }
}
