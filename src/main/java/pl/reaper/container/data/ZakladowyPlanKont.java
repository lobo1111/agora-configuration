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
import javax.validation.constraints.Size;
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
    @Size(min = 1, max = 150)
    @Column(name = "number")
    private String number;
    @Basic(optional = true)
    @Size(min = 0, max = 255)
    @Column(name = "description")
    private String description;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne
    private Community community;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST)
    private Possession possession;
    @OneToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name = "obligation_id", referencedColumnName = "id")
    private Obligation obligation;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "zpk")
    private Collection<ZpkBalance> zpkBalances = new ArrayList<>();
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "zpk")
    private Collection<ZpkSum> zpkSums;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "zpk")
    private Collection<AutoPayment> autoPayments = new ArrayList<>();
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "zpk")
    private Collection<AutoPaymentOrder> autoPaymentOrders = new ArrayList<>();
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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
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

    public Collection<AutoPayment> getAutoPayments() {
        return autoPayments;
    }

    public void setAutoPayments(Collection<AutoPayment> autoPayments) {
        this.autoPayments = autoPayments;
    }

    public Collection<AutoPaymentOrder> getAutoPaymentOrders() {
        return autoPaymentOrders;
    }

    public void setAutoPaymentOrders(Collection<AutoPaymentOrder> autoPaymentOrders) {
        this.autoPaymentOrders = autoPaymentOrders;
    }

    public Collection<ObligationGroup> getObligationGroups() {
        return obligationGroups;
    }

    public void setObligationGroups(Collection<ObligationGroup> obligationGroups) {
        this.obligationGroups = obligationGroups;
    }

    public Collection<ZpkSum> getZpkSums() {
        return zpkSums;
    }

    public void setZpkSums(Collection<ZpkSum> zpkSums) {
        this.zpkSums = zpkSums;
    }

    public String longDescription() {
        return "[number:" + number + "]"
                + "[description:" + description + "]";
    }
}
