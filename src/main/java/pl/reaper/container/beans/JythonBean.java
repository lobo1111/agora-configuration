package pl.reaper.container.beans;

import java.util.logging.Level;
import java.util.logging.Logger;
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
            Logger.getLogger(JythonBean.class.getCanonicalName()).log(Level.INFO, "Executing script: {0}", script);
            String result = String.valueOf(executor.executeScript(script));
            Logger.getLogger(JythonBean.class.getCanonicalName()).log(Level.INFO, "Script result: {0}", result);
            return result;
        } catch (Exception ex) {
            Logger.getLogger(JythonBean.class.getCanonicalName()).log(Level.SEVERE, "Script execution error: ", ex);
            return ex.getMessage();
        }
    }
}
