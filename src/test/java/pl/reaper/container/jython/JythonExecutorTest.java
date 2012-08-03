package pl.reaper.container.jython;

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
    public void testExecuteScript() throws Exception {
        System.out.println("simple jython test");
        ScriptLoader scriptLoader = new ScriptLoaderSimpleImpl();
        ScriptExecutor executor = new ScriptExecutor(scriptLoader, null);
        String expResult = "test";
        String result = executor.prepareAndExecuteScript("simple");
        assertEquals(expResult, result);
    }
}
