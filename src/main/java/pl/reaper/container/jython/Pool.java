package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.List;

public class Pool {
    private List<ScriptEngineWrapper> pool = new ArrayList<>();
    private List<ScriptEngineWrapper> working = new ArrayList<>();
    
    public boolean isEmpty() {
        return pool.isEmpty();
    }
    
    public ScriptEngineWrapper get() throws ScriptEnginePoolIsEmptyException {
        if(!pool.isEmpty()) {
            ScriptEngineWrapper engine = pool.remove(0);
            working.add(engine);
            return engine;
        } else {
            throw new ScriptEnginePoolIsEmptyException();
        }
    }
    
    public void release(ScriptEngineWrapper engine) throws UnknownScriptEngineException {
        if(working.remove(engine)) {
            pool.add(engine);
        } else {
            throw new UnknownScriptEngineException();
        }
    }
    
    public void put(ScriptEngineWrapper engine) {
        pool.add(engine);
    }

}
