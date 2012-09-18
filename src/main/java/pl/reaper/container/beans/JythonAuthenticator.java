package pl.reaper.container.beans;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;

@Stateless
public class JythonAuthenticator implements JythonAuthenticatorLocal {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;

    @Override
    public boolean isUserInRole(String userName, String groupName) {
        Query query = entityManager.createQuery(String.format("SELECT count(s) FROM UserGroup s WHERE s.user.login = '%s' and s.name = %s", userName, groupName));
        return query.getSingleResult() == 1;
    }
}
