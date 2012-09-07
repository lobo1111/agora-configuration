package pl.reaper.container.beans;

import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import pl.reaper.container.data.DictionaryType;
import pl.reaper.container.data.DictionaryType_;

@Stateless
public class DocumentStatusBean implements DocumentStatusBeanLocal {

    @PersistenceContext
    private EntityManager entityManager;
    private static final String UNKNOWN = "UNKNOWN";
    @EJB
    DictionaryBeanLocal dictionary;

    @Override
    public int getStatus(String status) {
        try {
            CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
            CriteriaQuery<DictionaryType> query = criteriaBuilder.createQuery(DictionaryType.class);
            Root<DictionaryType> root = query.from(DictionaryType.class);
            Predicate predicate = criteriaBuilder.equal(root.get(DictionaryType_.type), "DOCUMENT_STATUS");
            query.where(predicate);
            DictionaryType type = entityManager.createQuery(query).getSingleResult();
            return dictionary.getDictionary(type, status).getId();
        } catch (Exception e) {
            return loadUnknownStatus();
        }
    }

    private int loadUnknownStatus() {
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
            CriteriaQuery<DictionaryType> query = criteriaBuilder.createQuery(DictionaryType.class);
            Root<DictionaryType> root = query.from(DictionaryType.class);
            Predicate predicate = criteriaBuilder.equal(root.get(DictionaryType_.type), "DOCUMENT_STATUS");
            query.where(predicate);
            DictionaryType type = entityManager.createQuery(query).getSingleResult();
            return dictionary.getDictionary(type, UNKNOWN).getId();
    }
}
