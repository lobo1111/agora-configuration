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
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "obligation")
@XmlRootElement
public class Obligation implements Serializable {

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
    @JoinColumn(name = "contractor_id", referencedColumnName = "id")
    @ManyToOne
    private Company contractor;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "obligation")
    private Collection<ObligationLog> obligationLogs = new ArrayList<>();
    @OneToOne(mappedBy = "obligation", cascade = CascadeType.PERSIST)
    private ZakladowyPlanKont zpk;
    @JoinColumn(name = "obligation_group_id", referencedColumnName = "id")
    @ManyToOne
    private ObligationGroup obligationGroup;

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

    public Company getContractor() {
        return contractor;
    }

    public void setContractor(Company contractor) {
        this.contractor = contractor;
    }

    public Collection<ObligationLog> getObligationLogs() {
        return obligationLogs;
    }

    public void setObligationLogs(Collection<ObligationLog> obligationLogs) {
        this.obligationLogs = obligationLogs;
    }

    public ObligationGroup getObligationGroup() {
        return obligationGroup;
    }

    public void setObligationGroup(ObligationGroup obligationGroup) {
        this.obligationGroup = obligationGroup;
    }

    public ZakladowyPlanKont getZpk() {
        return zpk;
    }

    public void setZpk(ZakladowyPlanKont zpk) {
        this.zpk = zpk;
    }
}
