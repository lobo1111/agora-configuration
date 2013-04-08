package pl.reaper.container.beans;

import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.script.ScriptException;
import pl.reaper.container.data.Script;
import pl.reaper.container.jython.DBScriptLoader;
import pl.reaper.container.jython.ScriptEngineNotFoundException;
import pl.reaper.container.jython.ScriptEngineWrapper;
import pl.reaper.container.jython.ScriptExecutor;
import pl.reaper.container.jython.ScriptLoader;

@Stateless
public class ScriptCompilator implements ScriptCompilatorLocal {

    @EJB
    private ScriptEngineCacheLocal cache;
    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;
    @PersistenceContext(name = "agora_old_erp", unitName = "agora_old_erp")
    private EntityManager oldEntityManager;
    @EJB
    private PropertyBeanLocal propertyBean;
    @EJB
    private DocumentStatusBeanLocal documentStatusBean;

    @Override
    public ScriptEngineWrapper compileScript(String scriptName, Map variables) {
        try {
            ScriptEngineWrapper engineBuilder = getScriptEngine();
            List<Script> chain = getScriptLoader().loadScriptChain(scriptName);
            engineBuilder.addVariables(variables);
            for (Script script : chain) {
                engineBuilder.addVariable("_scriptId", script.getId());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Initializing script {0}...", script.getName());
                engineBuilder.eval(script.getScript());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
            }
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing final script...");
            engineBuilder.eval(chain.get(chain.size() - 1).getOnInit());
            return engineBuilder;
        } catch (ScriptException | ScriptEngineNotFoundException ex) {
            Logger.getLogger(ScriptCompilator.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    private ScriptLoader getScriptLoader() {
        ScriptLoader scriptLoader = new DBScriptLoader(entityManager);
        return scriptLoader;
    }

    private ScriptEngineWrapper getScriptEngine() throws ScriptEngineNotFoundException {
        ScriptEngineWrapper engineBuilder = new ScriptEngineWrapper(cache.getEngineManager())
                .setDocumentStatusBean(documentStatusBean)
                .setEntityManager(entityManager)
                .setOldEntityManager(oldEntityManager)
                .setPropertyBean(propertyBean)
                .init();
        return engineBuilder;
    }
}
