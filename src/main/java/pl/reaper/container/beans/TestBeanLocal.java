package pl.reaper.container.beans;

import javax.ejb.Local;
import javax.jws.WebService;

@WebService
@Local
public interface TestBeanLocal {

    public String openPing();
    
    public String closePing();
}
