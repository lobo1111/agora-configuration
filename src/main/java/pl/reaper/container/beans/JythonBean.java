package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import pl.reaper.container.jython.DBScriptLoader;
import pl.reaper.container.jython.ScriptExecutor;
import pl.reaper.container.jython.ScriptLoader;


@Stateless
public class JythonBean implements JythonBeanLocal {

    @PersistenceContext
    EntityManager entityManager;

    private ScriptLoader getLoader(EntityManager entityManager) {
        return new DBScriptLoader(entityManager);
    }

    @Override
    public String executeScript(String scriptName, Map variables) {
        ScriptLoader loader = getLoader(entityManager);
        ScriptExecutor executor = new ScriptExecutor(loader, entityManager);
        String result = executor.prepareAndExecuteScript(scriptName, variables);
        return result;
    }
}
