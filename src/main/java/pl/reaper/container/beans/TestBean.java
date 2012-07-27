package pl.reaper.container.beans;

import javax.annotation.security.RolesAllowed;
import javax.ejb.Stateless;
import javax.jws.WebService;

@WebService(endpointInterface = "pl.reaper.container.beans.TestBeanLocal")
@Stateless
public class TestBean implements TestBeanLocal {

    @RolesAllowed("management")
    @Override
    public String openPing() {
        return "pong";
    }
    
    @RolesAllowed("management")
    @Override
    public String closePing() {
        return "pong";
    }
}
