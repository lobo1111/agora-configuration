package pl.reaper.agora.jpa.beans;

import javax.ejb.Remote;
import pl.reaper.agora.jpa.Dictionary;

@Remote
public interface DocumentStatusBeanRemote {

    public Dictionary getStatus(String status);

}
