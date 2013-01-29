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
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "company")
@XmlRootElement
public class Company implements Serializable {

    @OneToMany(cascade = CascadeType.ALL, mappedBy = "company")
    private Collection<Community> communities;
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @Size(min = 1, max = 150)
    @Column(name = "nip")
    private String nip;
    @Basic(optional = false)
    @Size(min = 1, max = 150)
    @Column(name = "regon")
    private String regon;
    @Size(max = 150)
    @Column(name = "www")
    private String www;
    @Size(max = 150)
    @Column(name = "email")
    private String email;
    @Size(max = 150)
    @Column(name = "phone_number_1")
    private String phoneNumber1;
    @Size(max = 150)
    @Column(name = "phone_number_2")
    private String phoneNumber2;
    @Size(max = 150)
    @Column(name = "phone_number_3")
    private String phoneNumber3;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 150)
    @Column(name = "name")
    private String name;
    @JoinColumn(name = "address_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Address address;
    @ManyToMany
    @JoinTable(
        name = "possession_company", joinColumns =
    @JoinColumn(name = "company_id", referencedColumnName = "id"),
    inverseJoinColumns =
    @JoinColumn(name = "possession_id", referencedColumnName = "id"))
    private Collection<Possession> possessions;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "possession")
    private Collection<ZakladowyPlanKont> zpks;

    public Company() {
    }

    public Company(Integer id) {
        this.id = id;
    }

    public Company(Integer id, String nip, String regon, String name) {
        this.id = id;
        this.nip = nip;
        this.regon = regon;
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNip() {
        return nip;
    }

    public void setNip(String nip) {
        this.nip = nip;
    }

    public String getRegon() {
        return regon;
    }

    public void setRegon(String regon) {
        this.regon = regon;
    }

    public String getWww() {
        return www;
    }

    public void setWww(String www) {
        this.www = www;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhoneNumber1() {
        return phoneNumber1;
    }

    public void setPhoneNumber1(String phoneNumber1) {
        this.phoneNumber1 = phoneNumber1;
    }

    public String getPhoneNumber2() {
        return phoneNumber2;
    }

    public void setPhoneNumber2(String phoneNumber2) {
        this.phoneNumber2 = phoneNumber2;
    }

    public String getPhoneNumber3() {
        return phoneNumber3;
    }

    public void setPhoneNumber3(String phoneNumber3) {
        this.phoneNumber3 = phoneNumber3;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
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

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Company)) {
            return false;
        }
        Company other = (Company) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Company[ id=" + id + " ]";
    }

    @XmlTransient
    public Collection<Community> getCommunityCollection() {
        return communities;
    }

    public void setCommunityCollection(Collection<Community> communityCollection) {
        this.communities = communityCollection;
    }

    public String longDescription() {
        return "[name:" + name + "]"
                + "[regon:" + regon + "]"
                + "[www:" + www + "]"
                + "[nip:" + nip + "]"
                + "[email:" + email + "]"
                + "[phone1:" + phoneNumber1 + "]"
                + "[phone2:" + phoneNumber2 + "]"
                + "[phone3:" + phoneNumber3 + "]"
                + "[address:" + address + "]";
    }
}
