package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;
import javax.jws.WebService;

@WebService
@Local
public interface JythonRemoteAccessBeanLocal {

    public String simpleCall(String scriptName);

    public String call(String scriptName, Map parameters);
}
