package pl.reaper.container.beans;

import javax.ejb.Local;

@Local
public interface JythonAuthenticatorLocal {

    boolean isUserInRole(String userName, String groupName);
    
}
