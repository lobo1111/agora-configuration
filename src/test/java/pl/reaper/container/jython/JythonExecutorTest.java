package pl.reaper.container.jython;

import java.util.HashMap;
import java.util.Map;
import org.junit.After;
import org.junit.AfterClass;
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

public class JythonExecutorTest {
    
    public JythonExecutorTest() {
    }
    
    @BeforeClass
    public static void setUpClass() {
    }
    
    @AfterClass
    public static void tearDownClass() {
    }
    
    @Before
    public void setUp() {
    }
    
    @After
    public void tearDown() {
    }

    @Test
    public void jythonSimpleScript() throws Exception {
        ScriptLoader scriptLoader = new ScriptLoaderSimpleImpl();
        ScriptExecutor executor = new ScriptExecutor(scriptLoader);
        String expResult = "test";
        String result = executor.prepareAndExecuteScript("simple", new HashMap<String, String>());
        assertEquals(expResult, result);
    }
    
    @Test
    public void jythonVariables() throws Exception {
        ScriptLoader scriptLoader = new ScriptLoaderSimpleImpl();
        ScriptExecutor executor = new ScriptExecutor(scriptLoader);
        String expResult = "customVarValue";
        Map<String, String> customVars = new HashMap<>();
        customVars.put("customVar", expResult);
        String result = executor.prepareAndExecuteScript("vars", customVars);
        assertEquals(expResult, result);
    }
}
