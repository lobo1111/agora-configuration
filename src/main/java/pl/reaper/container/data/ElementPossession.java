package pl.reaper.container.data;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "element_possession")
@XmlRootElement
public class ElementPossession implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Possession possession;
    @JoinColumn(name = "element_id", referencedColumnName = "id")
    @ManyToOne(optional = false, cascade = CascadeType.PERSIST)
    private Element element;
    @JoinColumn(name = "element_community_id", referencedColumnName = "id")
    @ManyToOne(optional = false, cascade = CascadeType.PERSIST)
    private ElementCommunity elementCommunity;
    @Column(name = "override_parent_value")
    private boolean overrideParentValue;
    @Column(name = "value")
    private double localValue;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public Element getElement() {
        return element;
    }

    public void setElement(Element element) {
        this.element = element;
    }

    public ElementCommunity getElementCommunity() {
        return elementCommunity;
    }

    public void setElementCommunity(ElementCommunity elementCommunity) {
        this.elementCommunity = elementCommunity;
    }

    public boolean isOverrideParentValue() {
        return overrideParentValue;
    }

    public void setOverrideParentValue(boolean overrideParentValue) {
        this.overrideParentValue = overrideParentValue;
    }

    public double calculateGlobalValue() {
        if (isOverrideParentValue()) {
            return localValue;
        } else {
            return elementCommunity != null ? elementCommunity.calculateGlobalValue() : element.getGlobalValue();
        }
    }

    public double getLocalValue() {
        return localValue;
    }

    public void setLocalValue(double localValue) {
        this.localValue = localValue;
    }

    public Dictionary getGroup() {
        return element.getGroup();
    }

    public String getName() {
        return element.getName();
    }
}
