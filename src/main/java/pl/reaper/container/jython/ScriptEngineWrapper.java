package pl.reaper.container.jython;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.script.Bindings;
import javax.script.Compilable;
import javax.script.CompiledScript;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import pl.reaper.container.beans.DocumentStatusBeanLocal;
import pl.reaper.container.beans.PropertyBeanLocal;
import pl.reaper.container.data.Script;

public class ScriptEngineWrapper {

    private EntityManager entityManager;
    private EntityManager oldEntityManager;
    private PropertyBeanLocal propertyBean;
    private DocumentStatusBeanLocal documentStatusBean;
    private Map<String, Object> variables = new HashMap<>();
    private ScriptEngine engine;

    public ScriptEngineWrapper() {
        engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.SEVERE, "Python engine not found");
        } else {
            engine.getContext().setWriter(new PrintWriter(System.out));
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.INFO, "Jython engine created");
        }
    }

    public Bindings getBinding() {
        Bindings binding = engine.createBindings();
        putMetaVars();
        binding.put("entityManager", entityManager);
        binding.put("oldEntityManager", oldEntityManager);
        binding.put("vars", variables);
        binding.put("properties", propertyBean);
        binding.put("documentStatusLoader", documentStatusBean);
        binding.put("outputAsString", new String());
        return binding;
    }

    private void putMetaVars() {
        variables.put("_threadId", Thread.currentThread().getId());
        variables.put("_threadName", Thread.currentThread().getName());
        variables.put("_uuid", UUID.randomUUID().toString());
    }

    public Object extractResult(CompiledScript script) {
        String result = (String) script.getEngine().get("outputAsString");
        if (result != null && !"".equals(result)) {
            return result;
        } else {
            return "<no output>";
        }
    }

    public Object eval(String scriptName) throws ScriptException {
        try {
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
            CompiledScript script = findScript(scriptName);
            script.eval(getBinding());
            return extractResult(script);
        } catch (ScriptException ex) {
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "";
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

    private CompiledScript findScript(String scriptName) throws ScriptException {
        CompiledScript compiledScript = ScriptCache.getFromCache(scriptName);
        if (compiledScript == null) {
            String scriptContent = "";
            List<Script> scriptChain = new DBScriptLoader(entityManager).loadScriptChain(scriptName);
            for (Script script : scriptChain) {
                variables.put("_scriptId", String.valueOf(script.getId()));
                scriptContent += new VariableParser(script.getScript() + "\n", variables).parse();
            }
            scriptContent += scriptChain.get(scriptChain.size() - 1).getOnInit();
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.INFO, scriptContent);
            Compilable compilingEngine = (Compilable) engine;
            compiledScript = compilingEngine.compile(scriptContent);
            ScriptCache.cache(scriptName, compiledScript);
        }
        return compiledScript;
    }
}