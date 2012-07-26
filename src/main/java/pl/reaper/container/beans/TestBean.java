package pl.reaper.container.beans;

import javax.annotation.security.DenyAll;
import javax.ejb.Stateless;
import javax.jws.WebService;

@WebService(endpointInterface = "pl.reaper.container.beans.TestBeanLocal")
@Stateless
public class TestBean implements TestBeanLocal {

    @DenyAll
    @Override
    public String ping() {
        return "pong";
    }
}
