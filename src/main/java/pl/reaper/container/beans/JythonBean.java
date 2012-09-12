package pl.reaper.container.beans;

import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import pl.reaper.agora.jpa.beans.DocumentStatusBeanRemote;
import pl.reaper.agora.jpa.beans.PropertyBeanRemote;
import pl.reaper.container.jython.*;


@Stateless
public class JythonBean implements JythonBeanLocal {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;
    @PersistenceContext(name = "agora_old_erp", unitName = "agora_old_erp")
    private EntityManager oldEntityManager;
    @EJB
    private PropertyBeanRemote propertyBean;
    @EJB
    private DocumentStatusBeanRemote documentStatusBean;

    @Override
    public String executeScript(String scriptName, Map variables) {
        try {
            ScriptLoader scriptLoader = getScriptLoader();
            ScriptEngineWrapper engineBuilder = getScriptEngine();
            ScriptExecutor executor = getScriptExecutor(scriptLoader, engineBuilder);
            return executor.fire(scriptName, variables);
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    private ScriptLoader getScriptLoader() {
        ScriptLoader scriptLoader = new DBScriptLoader(entityManager);
        return scriptLoader;
    }

    private ScriptEngineWrapper getScriptEngine() throws ScriptEngineNotFoundException {
        ScriptEngineWrapper engineBuilder = new ScriptEngineWrapper()
                .setDocumentStatusBean(documentStatusBean)
                .setEntityManager(entityManager)
                .setOldEntityManager(oldEntityManager)
                .setPropertyBean(propertyBean)
                .init();
        return engineBuilder;
    }

    private ScriptExecutor getScriptExecutor(ScriptLoader scriptLoader, ScriptEngineWrapper engineBuilder) {
        ScriptExecutor executor = new ScriptExecutor();
        executor.setLoader(scriptLoader);
        executor.setEngineBuilder(engineBuilder);
        return executor;
    }
}
