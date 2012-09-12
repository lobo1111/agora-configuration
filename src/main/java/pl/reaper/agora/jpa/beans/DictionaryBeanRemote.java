package pl.reaper.agora.jpa.beans;

import javax.ejb.Remote;
import pl.reaper.agora.jpa.Dictionary;
import pl.reaper.agora.jpa.DictionaryType;

@Remote
public interface DictionaryBeanRemote {
    
    public Dictionary getDictionary(DictionaryType dictionaryType, String key);

    public String getDictionaryValue(DictionaryType dictionaryType, String key);

}
