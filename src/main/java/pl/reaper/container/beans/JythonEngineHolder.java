package pl.reaper.container.beans;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.Singleton;
import pl.reaper.container.jython.ScriptEngineNotFoundException;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Singleton
public class JythonEngineHolder implements JythonEngineHolderLocal {

    private ScriptEngineWrapper engineBuilder;

    public JythonEngineHolder() {
        try {
            this.engineBuilder = new ScriptEngineWrapper();
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(JythonEngineHolder.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    @Override
    public ScriptEngineWrapper getJythonEngine() {
        return engineBuilder;
    }
}
