package pl.reaper.container.beans;

import javax.ejb.Local;
import javax.script.CompiledScript;

@Local
public interface ScriptsLoaderLocal {

    public void init();

    public CompiledScript getScript(String name) throws Exception;
}
