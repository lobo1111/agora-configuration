package pl.reaper.container.beans;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import pl.reaper.container.data.DocumentStatus;
import pl.reaper.container.data.DocumentStatus_;

@Stateless
public class DocumentStatusBean implements DocumentStatusBeanLocal {

    @PersistenceContext
    private EntityManager entityManager;
    private static final String UNKNOWN = "UNKNOWN";

    @Override
    public DocumentStatus getStatus(String status) {
        try {
            CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
            CriteriaQuery<DocumentStatus> query = criteriaBuilder.createQuery(DocumentStatus.class);
            Root<DocumentStatus> root = query.from(DocumentStatus.class);
            Predicate predicate = criteriaBuilder.equal(root.get(DocumentStatus_.status), status);
            query.where(predicate);
            return entityManager.createQuery(query).getSingleResult();
        } catch (Exception e) {
            return loadUnknownStatus();
        }
    }

    private DocumentStatus loadUnknownStatus() {
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
        CriteriaQuery<DocumentStatus> query = criteriaBuilder.createQuery(DocumentStatus.class);
        Root<DocumentStatus> root = query.from(DocumentStatus.class);
        Predicate predicate = criteriaBuilder.equal(root.get(DocumentStatus_.status), UNKNOWN);
        query.where(predicate);
        return entityManager.createQuery(query).getSingleResult();
    }
}
