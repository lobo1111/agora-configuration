package pl.reaper.agora.jpa.beans;

import javax.ejb.Remote;

@Remote
public interface PropertyBeanRemote {

    public String getProperty(String key);
    
}
