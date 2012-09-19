package pl.reaper.container.beans;

import javax.ejb.Local;

@Local
public interface TemplateBeanLocal {

    public String getTemplate(String templateName);
    
}
