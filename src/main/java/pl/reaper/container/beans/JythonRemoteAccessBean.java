package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.jws.WebService;

@WebService(endpointInterface = "pl.reaper.container.beans.JythonRemoteAccessBeanLocal")
@Stateless
public class JythonRemoteAccessBean implements JythonRemoteAccessBeanLocal {

    @EJB
    private JythonBeanLocal jythonBean;

    @Override
    public String call(String scriptName, Map parameters) {
        return jythonBean.executeScript(scriptName, parameters, true);
    }

    @Override
    public String simpleCall(String scriptName) {
        return call(scriptName, new HashMap<String, String>());
    }
}
