package pl.reaper.container.beans;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

@Stateless
public class TemplateBean implements TemplateBeanLocal {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    EntityManager entityManager;

    @Override
    public String getTemplate(String templateName) {
        return null;
    }
}
