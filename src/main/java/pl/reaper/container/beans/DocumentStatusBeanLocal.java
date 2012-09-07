package pl.reaper.container.beans;

import javax.ejb.Local;
import pl.reaper.container.data.Dictionary;

@Local
public interface DocumentStatusBeanLocal {

    public Dictionary getStatus(String status);

}
