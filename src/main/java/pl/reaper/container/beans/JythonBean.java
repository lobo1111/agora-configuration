package pl.reaper.container.beans;

import javax.annotation.security.RolesAllowed;
import javax.ejb.Stateless;
import javax.jws.WebService;
import pl.reaper.container.jython.ScriptExecutor;
import pl.reaper.container.jython.ScriptLoader;


@WebService(endpointInterface = "pl.reaper.container.beans.JythonBeanLocal")
@Stateless
public class JythonBean implements JythonBeanLocal {

    @RolesAllowed("administrators")
    @Override
    public String executeScript(String scriptName) {
        ScriptLoader loader = getLoader();
        ScriptExecutor executor = new ScriptExecutor(loader);
        return executor.prepareAndExecuteScript(scriptName);
    }

    private ScriptLoader getLoader() {
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
