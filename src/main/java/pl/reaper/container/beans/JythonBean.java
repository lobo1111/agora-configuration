package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.Resource;
import javax.annotation.security.PermitAll;
import javax.ejb.EJB;
import javax.ejb.SessionContext;
import javax.ejb.Stateless;
import javax.jws.WebService;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import pl.reaper.container.jython.DBScriptLoader;
import pl.reaper.container.jython.ScriptEngineNotFoundException;
import pl.reaper.container.jython.ScriptEngineWrapper;
import pl.reaper.container.jython.ScriptExecutor;
import pl.reaper.container.jython.ScriptLoader;
import pl.reaper.container.ws.wrappers.MapWrapper;

@WebService(endpointInterface = "pl.reaper.container.beans.JythonBeanRemote")
@Stateless
public class JythonBean implements JythonBeanLocal, JythonBeanRemote {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;
    @PersistenceContext(name = "agora_old_erp", unitName = "agora_old_erp")
    private EntityManager oldEntityManager;
    @EJB
    private PropertyBeanLocal propertyBean;
    @EJB
    private DocumentStatusBeanLocal documentStatusBean;
    @EJB
    private JythonAuthenticatorLocal authenticator;
    @Resource
    private SessionContext ctx;

    @PermitAll
    @Override
    public String secureScriptExecution(String scriptName, MapWrapper variables) {
        return executeScript(scriptName, variables.map, true);
    }

    @PermitAll
    @Override
    public String simpleSecureScriptExecution(String scriptName) {
        return executeScript(scriptName, new HashMap<String, String>(), true);
    }

    @Override
    public String executeScript(String scriptName, Map variables, boolean preservePrivilages) {
        try {
            ScriptLoader scriptLoader = getScriptLoader();
            ScriptEngineWrapper engineBuilder = getScriptEngine();
            ScriptExecutor executor = getScriptExecutor(scriptLoader, engineBuilder, preservePrivilages);
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

    private ScriptExecutor getScriptExecutor(ScriptLoader scriptLoader, ScriptEngineWrapper engineBuilder, boolean preservePrivilages) {
        ScriptExecutor executor = new ScriptExecutor();
        executor.setLoader(scriptLoader);
        executor.setEngineBuilder(engineBuilder);
        executor.setSessionContext(ctx);
        executor.setPreservePrivilages(preservePrivilages);
        executor.setAuthenticator(authenticator);
        return executor;
    }

    @Override
    public boolean ping() {
        return true;
    }
}
