package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.security.PermitAll;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.jws.WebService;
import javax.script.ScriptException;
import pl.reaper.container.jython.ScriptEngineWrapper;
import pl.reaper.container.ws.wrappers.MapWrapper;

@WebService(endpointInterface = "pl.reaper.container.beans.JythonBeanRemote")
@Stateless
public class JythonBean implements JythonBeanLocal, JythonBeanRemote {

    @EJB
    private ScriptEngineCacheLocal cache;

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
        String output = "";
        try {
            if (cache.contains(scriptName)) {
                ScriptEngineWrapper engineBuilder = cache.get(scriptName);
                engineBuilder.resetVariables().addVariables(variables);
                output = (String) engineBuilder.eval();
            } else {
                output = (String) cache.init(scriptName, variables);
            }
        } catch (ScriptException ex) {
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, null, ex);
        }
        Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, output.substring(0, 256));
        return output;
    }

    @Override
    public boolean ping() {
        return true;
    }
}
