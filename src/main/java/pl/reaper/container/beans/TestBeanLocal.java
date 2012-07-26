/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.reaper.container.beans;

import javax.ejb.Local;
import javax.jws.WebService;

/**
 *
 * @author tomek
 */
@WebService
@Local
public interface TestBeanLocal {

    String ping();
    
}
