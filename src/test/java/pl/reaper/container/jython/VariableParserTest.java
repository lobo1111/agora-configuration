package pl.reaper.container.jython;

import java.util.HashMap;
import java.util.Map;
import org.junit.Test;
import static org.junit.Assert.*;

public class VariableParserTest {
    String simpleText = "[:toInsert]";
    String simpleTextResult = "inserted";
    String noVariablesText = "jakis tekst";
    String noVariablesTextResult = "jakis tekst";
    String missingVariableText = "[:variableNotFound]";
    String missingVariableTextResult = "[:variableNotFound]";
    String missingVariableNameText = "przed [:] po";
    String missingVariableNameTextResult = "przed [:] po";
    String combo = simpleText + noVariablesText + missingVariableText + missingVariableNameText;
    String comboResult = simpleTextResult + noVariablesTextResult + missingVariableTextResult + missingVariableNameTextResult;
    Map<String, String> variables = new HashMap<>();
    
    public VariableParserTest() {
        variables.put("toInsert", "inserted");
    }

    @Test
    public void simpleTextParse() {
        VariableParser instance = new VariableParser(simpleText, variables);
        String expResult = simpleTextResult;
        String result = instance.parse();
        assertEquals(expResult, result);
    }
    
    @Test
    public void noVariablesTextParse() {
        VariableParser instance = new VariableParser(noVariablesText, variables);
        String expResult = noVariablesTextResult;
        String result = instance.parse();
        assertEquals(expResult, result);
    }
    
    @Test
    public void missingVariableTextParse() {
        VariableParser instance = new VariableParser(missingVariableText, variables);
        String expResult = missingVariableTextResult;
        String result = instance.parse();
        assertEquals(expResult, result);
    }
    
    @Test
    public void missingVariableNameTextParse() {
        VariableParser instance = new VariableParser(missingVariableNameText, variables);
        String expResult = missingVariableNameTextResult;
        String result = instance.parse();
        assertEquals(expResult, result);
    }
    
    @Test
    public void comboParse() {
        VariableParser instance = new VariableParser(combo, variables);
        String expResult = comboResult;
        String result = instance.parse();
        assertEquals(expResult, result);
    }
}
