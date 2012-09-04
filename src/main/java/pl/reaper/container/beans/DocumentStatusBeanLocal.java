/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.reaper.container.beans;

import javax.ejb.Local;
import pl.reaper.container.data.DocumentStatus;

/**
 *
 * @author tomek
 */
@Local
public interface DocumentStatusBeanLocal {

    DocumentStatus getStatus(String status);
    
}
