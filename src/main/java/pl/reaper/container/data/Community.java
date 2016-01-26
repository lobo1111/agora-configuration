package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.text.SimpleDateFormat;
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
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "community")
@XmlRootElement
public class Community implements Serializable {
    // @Max(value=?)  @Min(value=?)//if you know range of your decimal fields consider using these annotations to enforce field validation

    @Column(name = "area")
    private BigDecimal area;
    @JoinColumn(name = "company_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Company company;
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 150)
    @Column(name = "name")
    private String name;
    @Column(name = "in_date")
    @Temporal(javax.persistence.TemporalType.DATE)
    private Date inDate;
    @Column(name = "out_date")
    @Temporal(javax.persistence.TemporalType.DATE)
    private Date outDate;
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "community")
    private Collection<Possession> possessions = new ArrayList<>();
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "community")
    private Collection<ZakladowyPlanKont> zpks = new ArrayList<>();
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "community")
    private Collection<Contractor> obligations = new ArrayList<>();
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "community")
    private Collection<ElementCommunity> elements = new ArrayList<>();
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "community")
    private Collection<Counter> counters = new ArrayList<>();
    @JoinColumn(name = "default_account_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST)
    private Account defaultAccount;
    @JoinColumn(name = "repair_fund_account_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST)
    private Account repairFundAccount;

    public Community() {
    }

    public Community(Integer id) {
        this.id = id;
    }

    public Community(Integer id, String name) {
        this.id = id;
        this.name = name;
    }

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

    public Date getInDate() {
        return inDate;
    }

    public void setInDate(Date inDate) {
        this.inDate = inDate;
    }

    public Date getOutDate() {
        return outDate;
    }

    public void setOutDate(Date outDate) {
        this.outDate = outDate;
    }

    @XmlTransient
    public Collection<Possession> getPossessions() {
        return possessions;
    }

    public void setPossessions(Collection<Possession> possessions) {
        this.possessions = possessions;
    }

    public Collection<ZakladowyPlanKont> getZpks() {
        return zpks;
    }

    public void setZpks(Collection<ZakladowyPlanKont> zpks) {
        this.zpks = zpks;
    }

    public Collection<Contractor> getObligations() {
        return obligations;
    }

    public void setObligations(Collection<Contractor> obligations) {
        this.obligations = obligations;
    }

    public Collection<ElementCommunity> getElements() {
        return elements;
    }

    public void setElements(Collection<ElementCommunity> elements) {
        this.elements = elements;
    }

    public Account getDefaultAccount() {
        return defaultAccount;
    }

    public void setDefaultAccount(Account defaultAccount) {
        this.defaultAccount = defaultAccount;
    }

    public Account getRepairFundAccount() {
        return repairFundAccount;
    }

    public void setRepairFundAccount(Account repairFundAccount) {
        this.repairFundAccount = repairFundAccount;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    public Collection<Counter> getCounters() {
        return counters;
    }

    public void setCounters(Collection<Counter> counters) {
        this.counters = counters;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Community)) {
            return false;
        }
        Community other = (Community) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Community[ id=" + id + " ]";
    }

    public BigDecimal getArea() {
        return area;
    }

    public void setArea(BigDecimal area) {
        this.area = area;
    }

    public Company getCompany() {
        return company;
    }

    public void setCompany(Company company) {
        this.company = company;
    }

    public String getFormattedInDate() {
        return new SimpleDateFormat("dd-MM-yyyy").format(inDate);
    }

    public String getFormattedOutDate() {
        return new SimpleDateFormat("dd-MM-yyyy").format(outDate);
    }

    public String longDescription() {
        return "[name:" + name + "]"
                + "[company:" + company + "]";
    }
}
