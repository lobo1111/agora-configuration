package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.Collections;
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

    private EntityManager entityManager;

    public DBScriptLoader(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Override
    public List<Script> loadScriptChain(String name) {
        List<Script> chain = new ArrayList<>();
        try {
            Script script = loadScript(name);
            while (!chain.contains(script) && script != null) {
                chain.add(script);
                script = script.getParent();
            }
        } catch (NoResultException ex) {
            Logger.getLogger(DBScriptLoader.class.getName()).log(Level.WARNING, "Can't find script " + name, ex);
        }
        Collections.reverse(chain);
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

    @Override
    public List<Script> loadBaseScripts() {
        List<Script> allBaseScripts = new ArrayList<>();
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
        CriteriaQuery<Script> query = criteriaBuilder.createQuery(Script.class);
        Root<Script> root = query.from(Script.class);
        Predicate baseScriptPredicate = criteriaBuilder.equal(root.get(Script_.base), true);
        Predicate hasNoParentPredicate = criteriaBuilder.isNull(root.get(Script_.parent));
        query.where(baseScriptPredicate, hasNoParentPredicate);
        List<Script> baseScriptsWithoutParents = entityManager.createQuery(query).getResultList();
        for(Script base: baseScriptsWithoutParents) {
            allBaseScripts.addAll(loadScriptChain(base.getName()));
        }
        return allBaseScripts;
    }
}
