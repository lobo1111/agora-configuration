package pl.reaper.container.jython;

import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.script.ScriptException;
import org.python.util.PythonInterpreter;
import pl.reaper.container.beans.DocumentStatusBeanLocal;
import pl.reaper.container.beans.PropertyBeanLocal;

public class ScriptEngineWrapper {

    private EntityManager entityManager;
    private EntityManager oldEntityManager;
    private PropertyBeanLocal propertyBean;
    private DocumentStatusBeanLocal documentStatusBean;
    private Map<String, Object> variables = new HashMap<>();
    private PythonInterpreter interpreter;
    private String lastExecuted;

    public ScriptEngineWrapper() {
        interpreter = new PythonInterpreter();
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Jython engine created");
        lastExecuted = "";
        putMetaVars();
    }

    public ScriptEngineWrapper init() {
        interpreter.setOut(new PrintWriter(System.out));
        interpreter.setErr(new PrintWriter(System.out));
        interpreter.set("entityManager", entityManager);
        interpreter.set("oldEntityManager", oldEntityManager);
        interpreter.set("vars", variables);
        interpreter.set("properties", propertyBean);
        interpreter.set("documentStatusLoader", documentStatusBean);
        return this;
    }

    private void putMetaVars() {
        variables.put("_threadId", Thread.currentThread().getId());
        variables.put("_threadName", Thread.currentThread().getName());
        variables.put("_uuid", UUID.randomUUID().toString());
    }

    public Object extractResult(PythonInterpreter interpreter) {
        String result = interpreter.eval("output.getResult()").asString();
        if (result != null && !"".equals(result)) {
            return result;
        }
        return "<no output>";
    }

    public Object eval(String script) throws ScriptException {
        lastExecuted += (script = new VariableParser(script, variables).parse()) + "\n";
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
        interpreter.eval(script);
        return extractResult(interpreter);
    }

    public Object eval() throws ScriptException {
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
        interpreter.eval(lastExecuted);
        return extractResult(interpreter);
    }

    public ScriptEngineWrapper setEntityManager(EntityManager entityManager) {
        this.entityManager = entityManager;
        return this;
    }

    public ScriptEngineWrapper setPropertyBean(PropertyBeanLocal propertyBean) {
        this.propertyBean = propertyBean;
        return this;
    }

    public ScriptEngineWrapper setDocumentStatusBean(DocumentStatusBeanLocal documentStatusBean) {
        this.documentStatusBean = documentStatusBean;
        return this;
    }

    public ScriptEngineWrapper addVariables(Map toAdd) {
        if (toAdd != null) {
            variables.putAll(toAdd);
        }
        return this;
    }

    public ScriptEngineWrapper resetVariables() {
        variables.clear();
        putMetaVars();
        return this;
    }

    public ScriptEngineWrapper addVariable(String key, Object value) {
        if (key != null) {
            variables.put(key, value);
        }
        return this;
    }

    public String getLastExecuted() {
        return lastExecuted;
    }

    public ScriptEngineWrapper setOldEntityManager(EntityManager oldEntityManager) {
        this.oldEntityManager = oldEntityManager;
        return this;
    }

    private String variablesAsString() {
        StringBuilder builder = new StringBuilder();
        for (String key : variables.keySet().toArray(new String[0])) {
            builder.append(key).append("=").append(variables.get(key)).append("\n");
        }
        return builder.toString();
    }
}
