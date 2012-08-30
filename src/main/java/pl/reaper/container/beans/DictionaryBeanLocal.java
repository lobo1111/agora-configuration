package pl.reaper.container.beans;

import javax.ejb.Local;
import pl.reaper.container.data.DictionaryType;

@Local
public interface DictionaryBeanLocal {

    public String getDictionaryValue(DictionaryType dictionaryType, String key);

}
