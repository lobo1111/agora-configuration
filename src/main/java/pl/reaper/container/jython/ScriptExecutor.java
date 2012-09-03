package pl.reaper.container.jython;

import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import pl.reaper.container.beans.PropertyBeanLocal;
import pl.reaper.container.data.Script;

public class ScriptExecutor {

    private ScriptLoader loader;
    private EntityManager entityManager;
    private PropertyBeanLocal propertyBean;

    public ScriptExecutor(ScriptLoader loader) {
        this.loader = loader;
    }

    public void setEntityManager(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    public void setPropertyBean(PropertyBeanLocal propertyBean) {
        this.propertyBean = propertyBean;
    }
    
    private List<Script> loadScriptChain(String name) throws ScriptEngineNotFoundException {
        List<Script> initChain = loader.loadBaseScripts();
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Base scripts loaded({0})", Arrays.deepToString(initChain.toArray(new Script[initChain.size()])));
        List<Script> scriptChain = loader.loadScriptChain(name);
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script chain loaded({0})", Arrays.deepToString(scriptChain.toArray(new Script[scriptChain.size()])));
        initChain.addAll(scriptChain);
        return initChain;
    }

    private Object executeScripts(List<Script> scripts, Map variables) {
        String wholeScript = "";
        ScriptEngine engine = null;
        Object result = null;
        putMetaVars(variables);
        try {
            engine = getEngine(variables);
            for (Script script : scripts) {
                variables.put("_scriptId", script.getId());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Initializing script {0}...", script.getName());
                String evaluatedScript = evalVariables(script.getScript(), variables);
                wholeScript += evaluatedScript + "\n";
                engine.eval(evaluatedScript);
                if (script.getBase() != null && script.getBase() == true) {
                    evaluatedScript = evalVariables(script.getOnInit(), variables);
                    wholeScript += evaluatedScript + "\n";
                    engine.eval(evaluatedScript);
                }
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
            }
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing final script...");
            String evaluatedScript = evalVariables(scripts.get(scripts.size() - 1).getOnInit(), variables);
            wholeScript += evaluatedScript + "\n";
            engine.eval(evaluatedScript);
            result = extractResult(engine);
        } catch (ScriptEngineNotFoundException | ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, "Script execution exception[[" + wholeScript + "]]", ex);
            result = ex.getMessage();
        }
        return result;
    }

    public String prepareAndExecuteScript(String name, Map variables) {
        try {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing script: {0}", name);
            String result = String.valueOf(executeScripts(loadScriptChain(name), variables));
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script executed, result: {0}", result);
            return result;
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, ex.getMessage(), ex);
            return ex.getMessage();
        }
    }

    private ScriptEngine getEngine(Map variables) throws ScriptEngineNotFoundException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            throw new ScriptEngineNotFoundException("Python engine not found");
        }
        prepareEngine(engine, variables);
        return engine;
    }

    private void prepareEngine(ScriptEngine engine, Map variables) {
        engine.getContext().setWriter(new PrintWriter(System.out));
        engine.put("entityManager", entityManager);
        engine.put("vars", variables);
        engine.put("properties", propertyBean);
    }

    private Object extractResult(ScriptEngine engine) {
        try {
            String result = (String) engine.eval("output.getResult()");
            if (result != null && !"".equals(result)) {
                return result;
            }
        } catch (ScriptException ex) {
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "<no output>";
    }

    private void putMetaVars(Map variables) {
        variables.put("_threadId", Thread.currentThread().getId());
        variables.put("_threadName", Thread.currentThread().getName());
        variables.put("_uuid", UUID.randomUUID().toString());
    }

    private String evalVariables(String script, Map variables) {
        VariableParser parser = new VariableParser(script, variables);
        return parser.parse();
    }
}
