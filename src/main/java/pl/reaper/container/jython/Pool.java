package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import pl.reaper.container.beans.JythonBean;

public class Pool {

    private List<ScriptEngineWrapper> pool = new ArrayList<>();
    private List<ScriptEngineWrapper> working = new ArrayList<>();
    private final String scriptName;

    public Pool(String scriptName) {
        this.scriptName = scriptName;
        Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, "Pool for " + scriptName + " created.");
    }

    public boolean isEmpty() {
        return pool.isEmpty();
    }

    public ScriptEngineWrapper get() throws ScriptEnginePoolIsEmptyException {
        if (!pool.isEmpty()) {
            ScriptEngineWrapper engine = pool.remove(0);
            working.add(engine);
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, "Pool(" + scriptName + ") - engine reserved(" + engine + ")");
            return engine;
        } else {
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, "Pool(" + scriptName + ") - can't get engine from empty pool !");
            throw new ScriptEnginePoolIsEmptyException();
        }
    }

    public void release(ScriptEngineWrapper engine) throws UnknownScriptEngineException {
        if (engine != null) {
            Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, "Pool(" + scriptName + ") - engine released(" + engine + ")");
            working.remove(engine);
            pool.add(engine);
        }
    }

    public void put(ScriptEngineWrapper engine) {
        Logger.getLogger(JythonBean.class.getName()).log(Level.SEVERE, "Pool(" + scriptName + ") - engine created(" + engine + ")");
        pool.add(engine);
    }
}
