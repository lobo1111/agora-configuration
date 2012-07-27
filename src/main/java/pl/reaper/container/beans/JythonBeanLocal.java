package pl.reaper.container.beans;

import javax.ejb.Local;
import javax.jws.WebService;

@WebService
@Local
public interface JythonBeanLocal {

    public String executeScript(String script);
    
}
