package pl.reaper.container.beans;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.NonUniqueResultException;
import javax.persistence.PersistenceContext;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import pl.reaper.container.data.Dictionary;
import pl.reaper.container.data.DictionaryType;
import pl.reaper.container.data.Dictionary_;

@Stateless
public class DictionaryBean implements DictionaryBeanLocal {

    @PersistenceContext
    EntityManager entityManager;

    @Override
    public String getDictionaryValue(DictionaryType dictionaryType, String key) {
        try {
            CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
            CriteriaQuery<Dictionary> query = criteriaBuilder.createQuery(Dictionary.class);
            Root<Dictionary> root = query.from(Dictionary.class);
            Predicate dictionaryKeyPredicate = criteriaBuilder.equal(root.get(Dictionary_.key), key);
            Predicate dictionaryTypePredicate = criteriaBuilder.equal(root.get(Dictionary_.type), dictionaryType);
            query.where(dictionaryKeyPredicate, dictionaryTypePredicate);
            Dictionary result = entityManager.createQuery(query).getSingleResult();
            return result.getValue();
        } catch(NoResultException | NonUniqueResultException e) {
            Logger.getLogger(DictionaryBean.class.getName()).log(Level.WARNING, null, e);
            return null;
        }
    }
}
