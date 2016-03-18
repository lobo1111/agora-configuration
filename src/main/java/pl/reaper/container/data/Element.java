package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
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
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "element")
@XmlRootElement
public class Element implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Column(name = "key_value")
    private String key;
    @Basic(optional = false)
    @NotNull
    @Column(name = "name")
    private String name;
    @JoinColumn(name = "group_id", referencedColumnName = "id")
    @ManyToOne
    private Dictionary group;
    @JoinColumn(name = "element_algorithm_id", referencedColumnName = "id")
    @ManyToOne
    private Dictionary algorithm;
    @Column(name = "global_value")
    private double globalValue;
    @Column(name = "default_element")
    private boolean defaultElement;
    @OneToMany(mappedBy = "element")
    private Collection<ElementCommunity> communityElements = new ArrayList<>();
    @OneToMany(mappedBy = "element")
    private Collection<ElementPossession> possessionElements = new ArrayList<>();

    public boolean isDefaultElement() {
        return defaultElement;
    }

    public void setDefaultElement(boolean defaultElement) {
        this.defaultElement = defaultElement;
    }

    public Dictionary getAlgorithm() {
        return algorithm;
    }

    public void setAlgorithm(Dictionary algorithm) {
        this.algorithm = algorithm;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Dictionary getGroup() {
        return group;
    }

    public void setGroup(Dictionary group) {
        this.group = group;
    }

    public double getGlobalValue() {
        return globalValue;
    }

    public double calculateGlobalValue() {
        return globalValue;
    }

    public void setGlobalValue(double globalValue) {
        this.globalValue = globalValue;
    }

    public Collection<ElementCommunity> getCommunityElements() {
        return communityElements;
    }

    public void setCommunityElements(Collection<ElementCommunity> communityElements) {
        this.communityElements = communityElements;
    }

    public Collection<ElementPossession> getPossessionElements() {
        return possessionElements;
    }

    public void setPossessionElements(Collection<ElementPossession> possessionElements) {
        this.possessionElements = possessionElements;
    }
}
