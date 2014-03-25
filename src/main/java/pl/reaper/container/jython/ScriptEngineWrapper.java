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
import pl.reaper.container.beans.PropertyBeanLocal;
import pl.reaper.container.beans.ScriptsLoaderLocal;

public class ScriptEngineWrapper {

    private EntityManager entityManager;
    private PropertyBeanLocal propertyBean;
    private Map<String, Object> variables = new HashMap<>();
    private ScriptEngine engine;
    private ScriptsLoaderLocal loader;

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
        binding.put("vars", variables);
        binding.put("properties", propertyBean);
        return binding;
    }

    private void putMetaVars() {
        variables.put("_threadId", Thread.currentThread().getId());
        variables.put("_threadName", Thread.currentThread().getName());
        variables.put("_uuid", UUID.randomUUID().toString());
    }

    public Object extractResult(Bindings binding) {
        Object output = ((Map<String, Object>) binding.get("vars")).get("output");
        if (output != null) {
            return (String) output;
        } else {
            return "<no output>";
        }
    }

    public Object eval(String scriptName) throws ScriptException {
        try {
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.INFO, "Variables:\n" + variablesAsString());
            CompiledScript script = findScript(scriptName);
            Bindings binding = getBinding();
            script.eval(binding);
            return extractResult(binding);
        } catch (ScriptException ex) {
            Logger.getLogger(ScriptEngineWrapper.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "";
    }

    public ScriptEngineWrapper setLoader(ScriptsLoaderLocal loader) {
        this.loader = loader;
        return this;
    }

    public ScriptEngineWrapper setEntityManager(EntityManager entityManager) {
        this.entityManager = entityManager;
        return this;
    }

    public ScriptEngineWrapper setPropertyBean(PropertyBeanLocal propertyBean) {
        this.propertyBean = propertyBean;
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

    private String variablesAsString() {
        StringBuilder builder = new StringBuilder();
        for (String key : variables.keySet().toArray(new String[0])) {
            builder.append(key).append("=").append(variables.get(key)).append("\n");
        }
        return builder.toString();
    }

    private CompiledScript findScript(String scriptName) throws ScriptException {
        return loader.getScript(scriptName);
    }
}