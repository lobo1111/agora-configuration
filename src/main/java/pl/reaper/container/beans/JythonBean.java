package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.security.DenyAll;
import javax.annotation.security.PermitAll;
import javax.annotation.security.RolesAllowed;
import javax.ejb.Stateless;
import javax.jws.WebService;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import pl.reaper.container.jython.DBScriptLoader;
import pl.reaper.container.jython.ScriptExecutor;
import pl.reaper.container.jython.ScriptLoader;


@WebService(endpointInterface = "pl.reaper.container.beans.JythonBeanLocal")
@Stateless
public class JythonBean implements JythonBeanLocal {

    @PersistenceContext
    EntityManager entityManager;

    private ScriptLoader getLoader() {
        return new DBScriptLoader(entityManager);
    }

    @PermitAll
    @Override
    public String executeScript(String scriptName, Map variables) {
        ScriptLoader loader = getLoader();
        ScriptExecutor executor = new ScriptExecutor(loader, entityManager);
        return executor.prepareAndExecuteScript(scriptName, variables);
    }
}
