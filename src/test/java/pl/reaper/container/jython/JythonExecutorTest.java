package pl.reaper.container.jython;

import java.util.HashMap;
import java.util.Map;
import static org.junit.Assert.*;
import org.junit.Test;

public class JythonExecutorTest {
    
    @Test
    public void jythonSimpleScript() throws Exception {
        ScriptLoader scriptLoader = new ScriptLoaderSimpleImpl();
        ScriptExecutor executor = new ScriptExecutor();
        executor.setLoader(scriptLoader);
        executor.setEngineBuilder(ScriptEngineWrapper.getInstance().init());
        String expResult = "test";
        String result = executor.fire("simple", null);
        assertEquals(expResult, result);
    }
    
    @Test
    public void jythonVariables() throws Exception {
        ScriptLoader scriptLoader = new ScriptLoaderSimpleImpl();
        ScriptExecutor executor = new ScriptExecutor();
        executor.setLoader(scriptLoader);
        executor.setEngineBuilder(ScriptEngineWrapper.getInstance().init());
        String expResult = "customVarValue";
        Map<String, String> customVars = new HashMap<>();
        customVars.put("customVar", expResult);
        String result = executor.fire("vars", customVars);
        assertEquals(expResult, result);
    }
}
