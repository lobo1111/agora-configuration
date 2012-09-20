package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Remote;
import javax.jws.WebService;
import pl.reaper.container.ws.wrappers.MapWrapper;

@WebService
@Remote
public interface JythonBeanRemote {

    public String secureScriptExecution(String scriptName, MapWrapper variables);
    
    public String simpleSecureScriptExecution(String scriptName);
    
    public boolean ping();
}
