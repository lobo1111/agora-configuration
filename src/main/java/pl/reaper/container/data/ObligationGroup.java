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
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "obligation_group")
@XmlRootElement
public class ObligationGroup implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "name")
    private String name;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne
    private Community community;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "obligationGroup")
    private Collection<Obligation> obligations = new ArrayList<>();
    @ManyToMany
    @JoinTable(
            name = "obligation_group_zpk", joinColumns =
            @JoinColumn(name = "obligation_group_id", referencedColumnName = "id"),
            inverseJoinColumns =
            @JoinColumn(name = "zpk_id", referencedColumnName = "id"))
    private Collection<ZakladowyPlanKont> zpks = new ArrayList<>();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public Collection<Obligation> getObligations() {
        return obligations;
    }

    public void setObligations(Collection<Obligation> obligations) {
        this.obligations = obligations;
    }

    public Collection<ZakladowyPlanKont> getZpks() {
        return zpks;
    }

    public void setZpks(Collection<ZakladowyPlanKont> zpks) {
        this.zpks = zpks;
    }
}
