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
public class PropertyBean implements PropertyBeanLocal {
    
    @PersistenceContext
    EntityManager entityManager;
    @EJB
    DictionaryBeanLocal dictionary;

    @Override
    public String getProperty(String key) {
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
        CriteriaQuery<DictionaryType> query = criteriaBuilder.createQuery(DictionaryType.class);
        Root<DictionaryType> root = query.from(DictionaryType.class);
        Predicate predicate = criteriaBuilder.equal(root.get(DictionaryType_.type), "PROPERTIES");
        query.where(predicate);
        DictionaryType type = entityManager.createQuery(query).getSingleResult();
        return dictionary.getDictionaryValue(type, key);
    }
}
