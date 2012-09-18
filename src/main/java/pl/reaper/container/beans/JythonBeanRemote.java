package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Remote;

@Remote
public interface JythonBeanRemote {
    public String secureScriptExecution(String scriptName, Map variables);
}
