package pl.reaper.container.beans;

import javax.ejb.Local;
import pl.reaper.container.data.Dictionary;
import pl.reaper.container.data.DictionaryType;

@Local
public interface DictionaryBeanLocal {
    
    public Dictionary getDictionary(DictionaryType dictionaryType, String key);

    public String getDictionaryValue(DictionaryType dictionaryType, String key);

}
