package pl.reaper.container.beans;

import javax.annotation.security.RolesAllowed;
import javax.ejb.Stateless;
import javax.jws.WebService;
import pl.reaper.container.jython.JythonExecutor;

@WebService(endpointInterface = "pl.reaper.container.beans.JythonBeanLocal")
@Stateless
public class JythonBean implements JythonBeanLocal {

    @RolesAllowed("administrators")
    @Override
    public String executeScript(String script) {
        try {
            JythonExecutor executor = new JythonExecutor();
            return executor.executeScript(script);
        } catch (Exception ex) {
            return ex.getMessage();
        }
    }
}
