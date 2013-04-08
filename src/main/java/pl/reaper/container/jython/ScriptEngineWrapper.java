package pl.reaper.container.jython;

import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import pl.reaper.container.beans.DocumentStatusBeanLocal;
import pl.reaper.container.beans.PropertyBeanLocal;

public class ScriptEngineWrapper {

    private EntityManager entityManager;
    private EntityManager oldEntityManager;
    private PropertyBeanLocal propertyBean;
    private DocumentStatusBeanLocal documentStatusBean;
    private Map<String, Object> variables;
    private ScriptEngine engine;
    private String lastExecuted;

    public ScriptEngineWrapper(ScriptEngineManager engineManager) throws ScriptEngineNotFoundException {
        engine = engineManager.getEngineByName("python");
        if (engine == null) {
            throw new ScriptEngineNotFoundException("Python engine not found");
        }
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Jython engine created");
        lastExecuted = "";
        putMetaVars();
    }

    public ScriptEngineWrapper init() {
        engine.getContext().setWriter(new PrintWriter(System.out));
        engine.put("entityManager", entityManager);
        engine.put("oldEntityManager", oldEntityManager);
        engine.put("vars", variables);
        engine.put("properties", propertyBean);
        engine.put("documentStatusLoader", documentStatusBean);
        return this;
    }

    private void putMetaVars() {
        variables = new HashMap<>();
        variables.put("_threadId", Thread.currentThread().getId());
        variables.put("_threadName", Thread.currentThread().getName());
        variables.put("_uuid", UUID.randomUUID().toString());
    }

    public Object extractResult(ScriptEngine engine) {
        try {
            String result = (String) engine.eval("output.getResult()");
            if (result != null && !"".equals(result)) {
                return result;
            }
        } catch (ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Output not found");
        }
        return "<no output>";
    }

    public Object eval(String script) throws ScriptException {
        lastExecuted += (script = new VariableParser(script, variables).parse()) + "\n";
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
        engine.eval(script);
        return extractResult(engine);
    }

    public Object eval() throws ScriptException {
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
        engine.eval("\nprint vars('_uuid')\n");
        return extractResult(engine);
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
        for(String key: variables.keySet()) {
            builder.append(key).append("=").append(variables.get(key)).append("\n");
        }
        return builder.toString();
    }
}
