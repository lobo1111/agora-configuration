package pl.reaper.container.jython;

import java.io.PrintWriter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.script.ScriptException;
import org.python.core.Py;
import org.python.core.PyStringMap;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;
import pl.reaper.container.beans.DocumentStatusBeanLocal;
import pl.reaper.container.beans.PropertyBeanLocal;
import pl.reaper.container.data.Script;

public class ScriptEngineWrapper {

    private EntityManager entityManager;
    private EntityManager oldEntityManager;
    private PropertyBeanLocal propertyBean;
    private DocumentStatusBeanLocal documentStatusBean;
    private Map<String, Object> variables = new HashMap<>();
    private PythonInterpreter interpreter;

    public ScriptEngineWrapper() {
        PySystemState sys = Py.getSystemState();
        sys.add_classdir("/usr/java/devel/");
        interpreter = new PythonInterpreter(new PyStringMap(), sys);
        Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.INFO, "Jython engine created");
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

    public Object eval(String scriptName) throws ScriptException {
        Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
        interpreter.execfile(findScript(scriptName));
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

    private String findScript(String scriptName) {
        ScriptCache cache = new ScriptCache();
        if (!cache.inCache(scriptName)) {
            String scriptContent = "";
            List<Script> scriptChain = new DBScriptLoader(entityManager).loadScriptChain(scriptName);
            for (Script script : scriptChain) {
                variables.put("_scriptId", String.valueOf(script.getId()));
                scriptContent += new VariableParser(script.getScript() + "\n", variables).parse();
            }
            scriptContent += scriptChain.get(scriptChain.size() - 1).getOnInit();
            cache.cache(scriptName, scriptContent);
        }
        return "/opt/container/cache/" + scriptName + ".py";
    }
}
