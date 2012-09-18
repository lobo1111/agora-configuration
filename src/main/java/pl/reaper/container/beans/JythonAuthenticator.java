package pl.reaper.container.beans;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import pl.reaper.container.data.UserGroup;
import pl.reaper.container.data.UserGroup_;

@Stateless
public class JythonAuthenticator implements JythonAuthenticatorLocal {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;

    @Override
    public boolean isUserInRole(String userName, String groupName) {
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
        CriteriaQuery query = criteriaBuilder.createQuery();
        Root<UserGroup> root = query.from(UserGroup.class);
        Predicate groupNameCriteria = criteriaBuilder.equal(root.get(UserGroup_.name), groupName);
        Predicate userNameCriteria = criteriaBuilder.equal(root.get(UserGroup_.user), userName);
        query.where(groupNameCriteria, userNameCriteria);
        query.select(criteriaBuilder.count(root));
        TypedQuery<Long> q = this.entityManager.createQuery(query);
        return q.getSingleResult() == 1;
    }
}
