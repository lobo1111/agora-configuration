package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Remote;
import javax.jws.WebService;

@WebService
@Remote
public interface JythonBeanRemote {

    public String secureScriptExecution(String scriptName, Map variables);
}
