package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import pl.reaper.container.data.Script;
import pl.reaper.container.data.Script_;

public class DBScriptLoader implements ScriptLoader {

    private final EntityManager entityManager;

    public DBScriptLoader(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Override
    public List<Script> loadScriptChain(String name) {
        List<Script> chain = new ArrayList<>();
        try {
            chain = loadScriptChain(loadScript(name));
        } catch (NoResultException ex) {
            Logger.getLogger(DBScriptLoader.class.getName()).log(Level.WARNING, "Can't find script " + name, ex);
        }
        Logger.getLogger(DBScriptLoader.class.getName()).log(Level.INFO, "Script chain loaded({0})", Arrays.deepToString(chain.toArray(new Script[chain.size()])));
        return chain;
    }

    public List<Script> loadScriptChain(Script script) {
        List<Script> chain = new ArrayList<>();
        getDependencies(chain, script);
        return chain;
    }

    private Script loadScript(String name) throws NoResultException {
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
        CriteriaQuery<Script> query = criteriaBuilder.createQuery(Script.class);
        Root<Script> root = query.from(Script.class);
        Predicate predicate = criteriaBuilder.equal(root.get(Script_.name), name);
        query.where(predicate);
        return entityManager.createQuery(query).getSingleResult();
    }

    private void getDependencies(List<Script> chain, Script script) {
        for (Script dependency : script.getDependencies()) {
            getDependencies(chain, dependency);
        }
        if (!chain.contains(script)) {
            chain.add(script);
        }
    }
}
