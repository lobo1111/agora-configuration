package pl.reaper.container.beans;

import javax.ejb.Local;

@Local
public interface DocumentStatusBeanLocal {

    public String getStatus(String status);

}
