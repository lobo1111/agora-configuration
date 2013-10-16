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
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "zpk")
@XmlRootElement
public class ZakladowyPlanKont implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @NotNull
    @Column(name = "number")
    private String number;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne
    private Community community;
    @JoinColumn(name = "type_id", referencedColumnName = "id")
    @ManyToOne
    private Dictionary type;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @OneToOne(cascade = CascadeType.PERSIST)
    private Possession possession;
    @OneToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name = "obligation_id", referencedColumnName = "id")
    private Obligation obligation;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "zpk")
    private Collection<ZpkBalance> zpkBalances = new ArrayList<>();
    @ManyToMany
    @JoinTable(
            name = "obligation_group_zpk", joinColumns =
    @JoinColumn(name = "zpk_id", referencedColumnName = "id"),
    inverseJoinColumns =
    @JoinColumn(name = "obligation_group_id", referencedColumnName = "id"))
    private Collection<ObligationGroup> obligationGroups = new ArrayList<>();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public Obligation getObligation() {
        return obligation;
    }

    public void setObligation(Obligation obligation) {
        this.obligation = obligation;
    }

    public Collection<ZpkBalance> getZpkBalances() {
        return zpkBalances;
    }

    public void setZpkBalances(Collection<ZpkBalance> zpkBalances) {
        this.zpkBalances = zpkBalances;
    }

    public Collection<ObligationGroup> getObligationGroups() {
        return obligationGroups;
    }

    public void setObligationGroups(Collection<ObligationGroup> obligationGroups) {
        this.obligationGroups = obligationGroups;
    }

    public Dictionary getType() {
        return type;
    }

    public void setType(Dictionary type) {
        this.type = type;
    }

    public String longDescription() {
        return "[number:" + number + "]"
                + "[type:" + type + "]"
                + "[community:" + community + "]"
                + "[possession:" + possession + "]"
                + "[obligation:" + obligation + "]";
    }
}
