package pl.reaper.container.beans;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.Singleton;
import pl.reaper.container.jython.ScriptEngineNotFoundException;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Singleton
public class JythonEngineHolder implements JythonEngineHolderLocal {

    private List<ScriptEngineWrapper> pool = new ArrayList<>();
    private List<ScriptEngineWrapper> working = new ArrayList<>();
    private static final int initSize = 10;
    private static final int step = initSize / 3;

    public JythonEngineHolder() {
        addEngines(initSize);
    }

    @Override
    public ScriptEngineWrapper getJythonEngine() {
        if (pool.isEmpty()) {
            addEngines(step);
        }
        ScriptEngineWrapper engine = pool.remove(0);
        working.add(engine);
        return engine;
    }

    @Override
    public void releaseEngine(ScriptEngineWrapper engine) {
        if (working.contains(engine)) {
            working.remove(engine);
        } else {
            Logger.getLogger(JythonEngineHolder.class.getName()).log(Level.SEVERE, "Unknown engine !");
        }
        pool.add(engine);
    }

    private void addEngines(int size) {
        try {
            for (int i = 0; i < size; i++) {
                pool.add(new ScriptEngineWrapper());
            }
            Logger.getLogger(JythonEngineHolder.class.getName()).log(Level.INFO, "Engine pool increased({0})", size);
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(JythonEngineHolder.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
