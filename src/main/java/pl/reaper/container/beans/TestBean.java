/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.reaper.container.beans;

import javax.ejb.Stateless;
import javax.jws.WebService;

/**
 *
 * @author tomek
 */
@WebService(endpointInterface = "pl.reaper.container.beans.TestBeanLocal")
@Stateless
public class TestBean implements TestBeanLocal {

    @Override
    public String ping() {
        return "pong";
    }

    // Add business logic below. (Right-click in editor and choose
    // "Insert Code > Add Business Method")

}
