package pl.reaper.container.beans;

import java.io.StringWriter;
import java.util.List;
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
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.VelocityEngine;
import pl.reaper.container.data.Template;
import pl.reaper.container.data.TemplateVariable;
import pl.reaper.container.data.Template_;

@Stateless
public class TemplateBean implements TemplateBeanLocal {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    EntityManager entityManager;

    @Override
    public String getTemplate(String templateName) {
        try {
            Template template = findTemplate(templateName);   
            return parseTemplate(template);
        } catch (Exception ex) {
            Logger.getLogger(TemplateBean.class.getName()).log(Level.SEVERE, null, ex);
            return "";
        }
    }

    private Template findTemplate(String templateName) {
        try {
            CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
            CriteriaQuery<Template> query = criteriaBuilder.createQuery(Template.class);
            Root<Template> root = query.from(Template.class);
            Predicate predicate = criteriaBuilder.equal(root.get(Template_.name), templateName);
            query.where(predicate);
            return entityManager.createQuery(query).getSingleResult();
        } catch (NoResultException | NonUniqueResultException e) {
            Logger.getLogger(DictionaryBean.class.getName()).log(Level.WARNING, "Template[" + templateName + "] not found", e);
            return null;
        }
    }

    private String parseTemplate(Template template) throws Exception {
       VelocityEngine ve = new VelocityEngine();
       ve.init();
       VelocityContext context = new VelocityContext();
       for(TemplateVariable var: template.getTemplateVariableCollection()) {
           context.put(var.getName(), loadData(var.getData()));
       }
       StringWriter writer = new StringWriter();
       ve.evaluate(context, writer, template.getName(), template.getSource());
       return writer.toString();
    }

    private List loadData(String data) {
        return entityManager.createQuery(data).getResultList();
    }
}
