package pl.reaper.container.beans;

import javax.ejb.Local;

@Local
public interface TemplateBeanLocal {

    String getTemplate(String templateName);
    
}
