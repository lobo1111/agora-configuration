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
        System.out.println("!!!!!!!!!" + groupName);
        System.out.println("!!!!!!!!!" + userName);
        Query query = entityManager.createQuery("SELECT count(s) FROM UserGroup s WHERE s.user.login = :userName and s.name = :groupName")
                .setParameter("userName", userName)
                .setParameter("groupName", groupName);
        Object result = query.getSingleResult();
        System.out.println(result);
        return result == 1;
    }
}
