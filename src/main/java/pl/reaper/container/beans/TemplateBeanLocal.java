/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.reaper.container.beans;

import javax.ejb.Local;

/**
 *
 * @author tomek
 */
@Local
public interface TemplateBeanLocal {

    String getTemplate(String templateName);
    
}
