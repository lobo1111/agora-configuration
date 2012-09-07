package pl.reaper.container.beans;

import javax.ejb.Local;

@Local
public interface DocumentStatusBeanLocal {

    public int getStatus(String status);

}
