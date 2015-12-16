package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.annotation.security.PermitAll;
import javax.ejb.EJB;
import javax.ejb.SessionContext;
import javax.ejb.Stateless;
import javax.ejb.TransactionManagement;
import javax.ejb.TransactionManagementType;
import javax.jws.WebService;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.transaction.UserTransaction;
import javax.ws.rs.Path;
import pl.reaper.container.jython.ScriptEngineWrapper;
import pl.reaper.container.ws.wrappers.MapWrapper;

@WebService(endpointInterface = "pl.reaper.container.beans.JythonBeanRemote")
@Stateless
@Path("/JythonBeanService")
@TransactionManagement(TransactionManagementType.BEAN)
public class JythonBean implements JythonBeanLocal, JythonBeanRemote {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;
    @EJB
    private PropertyBeanLocal propertyBean;
    @EJB
    private ScriptsLoaderLocal loaderBean;
    @Resource
    private SessionContext context;
    private ScriptEngineWrapper engineBuilder;

    @PostConstruct
    public void initScripting() {
        engineBuilder = new ScriptEngineWrapper()
                .setEntityManager(entityManager)
                .setPropertyBean(propertyBean)
                .setLoader(loaderBean)
                .setContext(context);
    }

    @PermitAll
    @Override
    @Path("/JythonBean")
    public String secureScriptExecution(String scriptName, MapWrapper variables) {
        return executeScript(scriptName, variables.map);
    }

    @PermitAll
    @Override
    public String simpleSecureScriptExecution(String scriptName) {
        return executeScript(scriptName, new HashMap<String, String>());
    }

    @Override
    public String executeScript(String scriptName, Map variables) {
        try {
            String output = "";
            engineBuilder.resetVariables().addVariables(variables);
            output = (String) engineBuilder.eval(scriptName);
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, output.length() > 256 ? output.substring(0, 256) : output);
            return output;
        } catch (Exception ex) {
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "";
    }

    @Override
    public boolean ping() {
        return true;
    }
}
