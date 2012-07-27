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
        System.out.println("executeScript");
        String script = "output = 'test'";
        JythonExecutor instance = new JythonExecutor();
        String expResult = "test";
        String result = instance.executeScript(script);
        assertEquals(expResult, result);
    }
}
