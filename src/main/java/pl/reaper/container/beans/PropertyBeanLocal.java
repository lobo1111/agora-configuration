package pl.reaper.container.beans;

import javax.ejb.Local;

@Local
public interface PropertyBeanLocal {

    public String getProperty(String key);
    
}
