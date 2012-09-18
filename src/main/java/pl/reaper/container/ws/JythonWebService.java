package pl.reaper.container.ws;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.security.RolesAllowed;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.jws.WebMethod;
import javax.jws.WebService;
import pl.reaper.container.beans.JythonBeanLocal;

@Stateless
@WebService(serviceName = "JythonWebService")
public class JythonWebService {
    @EJB
    private JythonBeanLocal jythonBean;

    @WebMethod
    public String call(String scriptName) {
        return callWithParameters(scriptName, new HashMap<String, String>());
    }
    
    @RolesAllowed("all")
    @WebMethod
    public String callWithParameters(String scriptName, Map parameters) {
        return jythonBean.executeScript(scriptName, parameters, true);
    }
}
