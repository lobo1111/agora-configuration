package pl.reaper.container.beans;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.EJB;
import javax.ejb.Singleton;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.script.ScriptEngineManager;
import pl.reaper.container.jython.Pool;
import pl.reaper.container.jython.ScriptEngineNotFoundException;
import pl.reaper.container.jython.ScriptEnginePoolIsEmptyException;
import pl.reaper.container.jython.ScriptEngineWrapper;
import pl.reaper.container.jython.UnknownScriptEngineException;

@Singleton
public class ScriptEngineCache implements ScriptEngineCacheLocal {

    private Map<String, Pool> cache = new HashMap<>();
    private ScriptEngineManager engineManager;
    @EJB
    private ScriptCompilatorLocal compilator;
    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;
    @PersistenceContext(name = "agora_old_erp", unitName = "agora_old_erp")
    private EntityManager oldEntityManager;
    @EJB
    private PropertyBeanLocal propertyBean;
    @EJB
    private DocumentStatusBeanLocal documentStatusBean;

    public ScriptEngineCache() {
        engineManager = new ScriptEngineManager();
    }

    @Override
    public ScriptEngineWrapper get(String scriptName) {
        try {
            return cache.get(scriptName).get();
        } catch (ScriptEnginePoolIsEmptyException ex) {
            Logger.getLogger(ScriptEngineCache.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    @Override
    public boolean contains(String scriptName) {
        return cache.containsKey(scriptName) && !cache.get(scriptName).isEmpty();
    }

    @Override
    public Object init(String scriptName, Map variables) {
        try {
            ScriptEngineWrapper engine = getScriptEngine();
            Object output = compilator.compile(engine, scriptName, variables);
            addToPool(scriptName, engine);
            return output;
        } catch (ScriptEngineNotFoundException ex) {
            Logger.getLogger(ScriptEngineCache.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    @Override
    public ScriptEngineManager getEngineManager() {
        return engineManager;
    }

    private ScriptEngineWrapper getScriptEngine() throws ScriptEngineNotFoundException {
        ScriptEngineWrapper engineBuilder = new ScriptEngineWrapper(getEngineManager())
                .setDocumentStatusBean(documentStatusBean)
                .setEntityManager(entityManager)
                .setOldEntityManager(oldEntityManager)
                .setPropertyBean(propertyBean)
                .init();
        return engineBuilder;
    }

    private void addToPool(String scriptName, ScriptEngineWrapper engine) {
        if(cache.containsKey(scriptName)) {
            cache.get(scriptName).put(engine);
        } else {
            Pool pool = new Pool(scriptName);
            pool.put(engine);
            cache.put(scriptName, pool);
        }
    }

    @Override
    public void releaseEngine(String scriptName, ScriptEngineWrapper engine) {
        try {
            cache.get(scriptName).release(engine);
        } catch (UnknownScriptEngineException ex) {
            Logger.getLogger(ScriptEngineCache.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
