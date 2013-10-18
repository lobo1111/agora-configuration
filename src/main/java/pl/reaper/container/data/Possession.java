package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "possession")
@XmlRootElement
public class Possession implements Serializable {
    // @Max(value=?)  @Min(value=?)//if you know range of your decimal fields consider using these annotations to enforce field validation

    @Column(name = "area")
    private BigDecimal area = new BigDecimal(0);
    @Column(name = "share")
    private BigDecimal share = new BigDecimal(0);
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Community community;
    @JoinColumn(name = "address_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Address address;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "possession")
    private Collection<Owner> owners = new ArrayList<>();
    @OneToOne(cascade = CascadeType.PERSIST, fetch = FetchType.EAGER, mappedBy = "possession")
    private PossessionAdditionalData additionalData = new PossessionAdditionalData();
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "possession")
    private Collection<ElementPossession> elements;
    @OneToOne(cascade = CascadeType.ALL, mappedBy = "possession")
    private ZakladowyPlanKont zpk = new ZakladowyPlanKont();

    public Possession() {
    }

    public Possession(Integer id) {
        this.id = id;
    }

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

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public Collection<Owner> getOwners() {
        return owners;
    }

    public void setOwners(Collection<Owner> owners) {
        this.owners = owners;
    }

    public Collection<ElementPossession> getElements() {
        return elements;
    }

    public void setElements(Collection<ElementPossession> elements) {
        this.elements = elements;
    }

    public ZakladowyPlanKont getZpk() {
        return zpk;
    }

    public void setZpk(ZakladowyPlanKont zpk) {
        this.zpk = zpk;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Possession)) {
            return false;
        }
        Possession other = (Possession) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Possession[ id=" + id + " ]";
    }

    public BigDecimal getArea() {
        return area;
    }

    public void setArea(BigDecimal area) {
        this.area = area;
    }

    public BigDecimal getShare() {
        return share;
    }

    public void setShare(BigDecimal share) {
        this.share = share;
    }

    public PossessionAdditionalData getAdditionalData() {
        return additionalData;
    }

    public void setAdditionalData(PossessionAdditionalData additionalData) {
        this.additionalData = additionalData;
    }

    public String longDescription() {
        return "[area:" + area + "]"
                + "[share:" + share + "]"
                + "[community:" + community + "]"
                + "[address:" + address + "]";
    }

    public String getFullAddress() {
        return address.getFullAddress();
    }
}
