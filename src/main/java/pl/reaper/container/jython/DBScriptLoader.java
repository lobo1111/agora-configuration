package pl.reaper.container.jython;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.SessionContext;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import javax.script.ScriptException;
import pl.reaper.container.data.Script;
import pl.reaper.container.data.Script_;
import pl.reaper.container.data.UserGroup;

public class DBScriptLoader implements ScriptLoader {

    private final EntityManager entityManager;
    private final SessionContext context;

    public DBScriptLoader(EntityManager entityManager, SessionContext context) {
        this.entityManager = entityManager;
        this.context = context;
    }

    @Override
    public List<Script> loadScriptChain(String name) throws ScriptException {
        List<Script> chain = new ArrayList<>();
        try {
            chain = loadScriptChain(loadScript(name));
        } catch (NoResultException ex) {
            Logger.getLogger(DBScriptLoader.class.getName()).log(Level.WARNING, "Can't find script " + name, ex);
        }
        Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script chain loaded({0})", Arrays.deepToString(chain.toArray(new Script[chain.size()])));
        return chain;
    }

    public List<Script> loadScriptChain(Script script) throws ScriptException {
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

    private void getDependencies(List<Script> chain, Script script) throws ScriptException {
        checkSecurity(script);
        for (Script dependency : script.getDependencies()) {
            getDependencies(chain, dependency);
        }
        if (!chain.contains(script)) {
            chain.add(script);
        }
    }

    private void checkSecurity(Script script) throws ScriptException {
        for (UserGroup group : script.getAllowedGroups()) {
            if (context.isCallerInRole(group.getName())) {
                return;
            }
        }
        throw new ScriptException("You are not authorized to execute this script[id:" + script.getId() + "][name:" + script.getName() + "]");
    }
}
