package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.PostConstruct;
import javax.annotation.security.PermitAll;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.jws.WebService;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.script.ScriptException;
import pl.reaper.container.jython.ScriptEngineWrapper;
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
    private ScriptEngineWrapper engineBuilder;

    @PostConstruct
    public void initScripting() {
        engineBuilder = new ScriptEngineWrapper()
                .setDocumentStatusBean(documentStatusBean)
                .setEntityManager(entityManager)
                .setOldEntityManager(oldEntityManager)
                .setPropertyBean(propertyBean);
    }

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
            String output = "";
            engineBuilder.resetVariables().addVariables(variables);
            output = (String) engineBuilder.eval(scriptName);
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, output.length() > 256 ? output.substring(0, 256) : output);
            return output;
        } catch (ScriptException ex) {
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "";
    }

    @Override
    public boolean ping() {
        return true;
    }
}
