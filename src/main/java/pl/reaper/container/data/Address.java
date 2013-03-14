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
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "address")
@XmlRootElement
public class Address implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 150)
    @Column(name = "street")
    private String street;
    @Size(max = 150)
    @Column(name = "house_number")
    private String houseNumber;
    @Size(max = 150)
    @Column(name = "flat_number")
    private String flatNumber;
    @Size(max = 6)
    @Column(name = "postal_code")
    private String postalCode;
    @Size(max = 150)
    @Column(name = "city")
    private String city;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "address")
    private Collection<Person> persons;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "address")
    private Collection<Possession> possessions;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "address")
    private Collection<Company> companies;

    public Address() {
    }

    public Address(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getStreet() {
        return street;
    }

    public void setStreet(String street) {
        this.street = street;
    }

    public String getHouseNumber() {
        return houseNumber;
    }

    public void setHouseNumber(String houseNumber) {
        this.houseNumber = houseNumber;
    }

    public String getFlatNumber() {
        return flatNumber;
    }

    public void setFlatNumber(String flatNumber) {
        this.flatNumber = flatNumber;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(String postalCode) {
        this.postalCode = postalCode;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    @XmlTransient
    public Collection<Person> getPersons() {
        return persons;
    }

    public void setPersons(Collection<Person> persons) {
        this.persons = persons;
    }

    @XmlTransient
    public Collection<Possession> getPossessions() {
        return possessions;
    }

    public void setPossessions(Collection<Possession> possessions) {
        this.possessions = possessions;
    }

    @XmlTransient
    public Collection<Company> getCompanies() {
        return companies;
    }

    public void setCompanies(Collection<Company> companies) {
        this.companies = companies;
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
        if (!(object instanceof Address)) {
            return false;
        }
        Address other = (Address) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Address[ id=" + id + " ]";
    }

    public String longDescription() {
        return "[id:" + id + "]"
                + "[street:" + street + "]"
                + "[houseNumber:" + houseNumber + "]"
                + "[flatNumber:" + flatNumber + "]"
                + "[postalCode:" + postalCode + "]"
                + "[city:" + city + "]";
    }
}
