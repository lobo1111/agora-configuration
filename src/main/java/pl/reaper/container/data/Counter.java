package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
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
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "counter")
@XmlRootElement
public class Counter implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Column(name = "serial_number")
    private String serialNumber;
    @Column(name = "seal")
    private String seal;
    @JoinColumn(name = "type_id", referencedColumnName = "id")
    @ManyToOne
    private Dictionary type;
    @Column(name = "installation")
    @Temporal(TemporalType.DATE)
    private Date installation;
    @Column(name = "decomission")
    @Temporal(TemporalType.DATE)
    private Date decomission;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne
    private Community community;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne
    private Possession possession;
    @JoinColumn(name = "parent_counter_id", referencedColumnName = "id")
    @ManyToOne
    private Counter parent;
    @JoinColumn(name = "replacement_of", referencedColumnName = "id")
    @ManyToOne
    private Counter replacementOf;
    @OneToMany(mappedBy = "parent", cascade = CascadeType.PERSIST)
    private Collection<Counter> children = new ArrayList<>();
    @OneToMany(mappedBy = "counter", cascade = CascadeType.PERSIST)
    private Collection<CounterStatus> statuses = new ArrayList<>();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getSeal() {
        return seal;
    }

    public void setSeal(String seal) {
        this.seal = seal;
    }

    public Counter getReplacementOf() {
        return replacementOf;
    }

    public void setReplacementOf(Counter replacementOf) {
        this.replacementOf = replacementOf;
    }

    public String getSerialNumber() {
        return serialNumber;
    }

    public void setSerialNumber(String serialNumber) {
        this.serialNumber = serialNumber;
    }

    public Dictionary getType() {
        return type;
    }

    public void setType(Dictionary type) {
        this.type = type;
    }

    public Date getInstallation() {
        return installation;
    }

    public void setInstallation(Date installation) {
        this.installation = installation;
    }

    public Date getDecomission() {
        return decomission;
    }

    public void setDecomission(Date decomission) {
        this.decomission = decomission;
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

    public Counter getParent() {
        return parent;
    }

    public void setParent(Counter parent) {
        this.parent = parent;
    }

    public Collection<Counter> getChildren() {
        return children;
    }

    public void setChildren(ArrayList<Counter> children) {
        this.children = children;
    }

    public Collection<CounterStatus> getStatuses() {
        return statuses;
    }

    public void setStatuses(ArrayList<CounterStatus> statuses) {
        this.statuses = statuses;
    }

}
