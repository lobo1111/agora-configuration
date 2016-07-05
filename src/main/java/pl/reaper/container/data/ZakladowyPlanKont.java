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
    @Basic(optional = true)
    @Column(name = "label")
    private String label;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST)
    private Community community;
    @JoinColumn(name = "type_id", referencedColumnName = "id")
    @ManyToOne
    private Dictionary type;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @OneToOne(cascade = CascadeType.PERSIST)
    private Possession possession;
    @OneToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name = "contractor_id", referencedColumnName = "id")
    private Contractor contractor;
    @OneToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name = "account_id", referencedColumnName = "id")
    private Account account;
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "zpk")
    private Collection<ZpkBalance> zpkBalances = new ArrayList<>();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
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

    public Contractor getContractor() {
        return contractor;
    }

    public void setContractor(Contractor contractor) {
        this.contractor = contractor;
    }

    public Account getAccount() {
        return account;
    }

    public void setAccount(Account account) {
        this.account = account;
    }

    public Collection<ZpkBalance> getZpkBalances() {
        return zpkBalances;
    }

    public ZpkBalance getCurrentBalance() {
        for (ZpkBalance balance : zpkBalances) {
            if (balance.getBookingPeriod().isDefaultPeriod()) {
                return balance;
            }
        }
        return null;
    }

    public void setZpkBalances(Collection<ZpkBalance> zpkBalances) {
        this.zpkBalances = zpkBalances;
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
                + "[obligation:" + contractor + "]";
    }
}
