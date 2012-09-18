package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;
import javax.jws.WebService;

@WebService
@Local
public interface JythonBeanLocal {

    public String executeScript(String scriptName, Map variables, boolean preservePrivilages);
    
}
