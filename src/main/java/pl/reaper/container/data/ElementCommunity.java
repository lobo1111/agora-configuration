package pl.reaper.container.data;

import java.io.Serializable;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "element_community")
@XmlRootElement
public class ElementCommunity implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne(optional = false, cascade = CascadeType.PERSIST)
    private Community community;
    @JoinColumn(name = "element_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Element element;
    @Column(name = "override_parent_value")
    private boolean overrideParentValue;
    @Column(name = "value")
    private double globalValue;
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "elementCommunity")
    private Collection<ElementPossession> possessionsElements;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public Element getElement() {
        return element;
    }

    public void setElement(Element element) {
        this.element = element;
    }

    public boolean isOverrideParentValue() {
        return overrideParentValue;
    }

    public void setOverrideParentValue(boolean overrideParentValue) {
        this.overrideParentValue = overrideParentValue;
    }

    public double getGlobalValue() {
        return globalValue;
    }

    public void setGlobalValue(double globalValue) {
        this.globalValue = globalValue;
    }

    public Collection<ElementPossession> getPossessionsElements() {
        return possessionsElements;
    }

    public void setPossessionsElements(Collection<ElementPossession> possessionsElements) {
        this.possessionsElements = possessionsElements;
    }
}
