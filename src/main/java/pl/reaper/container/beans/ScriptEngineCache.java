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
import pl.reaper.container.jython.ScriptEngineNotFoundException;
import pl.reaper.container.jython.ScriptEngineWrapper;

@Singleton
public class ScriptEngineCache implements ScriptEngineCacheLocal {

    private Map<String, ScriptEngineWrapper> cache = new HashMap<>();
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
        return cache.get(scriptName);
    }

    @Override
    public void put(String scriptName, ScriptEngineWrapper scriptEngineWrapper) {
        cache.put(scriptName, scriptEngineWrapper);
    }

    @Override
    public boolean contains(String scriptName) {
        return cache.containsKey(scriptName);
    }

    @Override
    public Object init(String ScriptName, Map variables) {
        try {
            ScriptEngineWrapper engine = getScriptEngine();
            Object output = compilator.compile(engine, ScriptName, variables);
            put(ScriptName, engine);
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
}
