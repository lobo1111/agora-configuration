package pl.reaper.container.beans;

import javax.annotation.security.DenyAll;
import javax.ejb.Local;
import javax.jws.WebService;

@WebService
@Local
public interface TestBeanLocal {

    @DenyAll
    public String ping();
}
