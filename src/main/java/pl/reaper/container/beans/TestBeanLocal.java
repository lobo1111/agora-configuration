package pl.reaper.container.beans;

import javax.annotation.security.RolesAllowed;
import javax.ejb.Local;
import javax.jws.WebService;

@WebService
@Local
public interface TestBeanLocal {

    @RolesAllowed("administrators") 
    public String ping();
}
