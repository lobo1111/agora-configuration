package pl.reaper.container.beans;

import java.util.Map;
import javax.ejb.Local;

@Local
public interface JythonBeanLocal {

    public String executeScript(String scriptName, Map variables);
    
}
