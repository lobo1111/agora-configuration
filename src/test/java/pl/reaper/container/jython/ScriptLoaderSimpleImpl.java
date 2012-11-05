package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Dictionary;
import java.util.List;
import pl.reaper.container.data.Script;

public class ScriptLoaderSimpleImpl implements ScriptLoader {
    
    private static final String OUTPUT = ""
            + "\nclass Output:"
            + "\n\t_result = ''"
            + "\n\tdef getResult(self):"
            + "\n\t\treturn self._result"
            + "\n\tdef setResult(self, result):"
            + "\n\t\tself._result = result"
            + "\n\tdef appendResult(self, result):"
            + "\n\t\tself._result += result";
    
    private static final String OUTPUT_INIT = ""
            + "\noutput = Output()";

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
        simple.setScript(OUTPUT + OUTPUT_INIT);
        simple.setOnInit("output.setResult('test')");
        simple.setAllowedGroups((Collection)new ArrayList<Dictionary>());
        return simple;
    }

    private Script getVarsScript(String name) {
        Script simple = new Script();
        simple.setName(name);
        simple.setScript(OUTPUT + OUTPUT_INIT);
        simple.setOnInit("print vars\noutput.setResult(vars.get('customVar'))");
        simple.setAllowedGroups((Collection)new ArrayList<Dictionary>());
        return simple;
    }

}
