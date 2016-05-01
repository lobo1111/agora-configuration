package pl.reaper.container.data;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "owner")
@XmlRootElement
public class Owner implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "address_id", referencedColumnName = "id")
    @ManyToOne(optional = true)
    private Address address;
    @JoinColumn(name = "company_id", referencedColumnName = "id")
    @ManyToOne(optional = true, cascade = CascadeType.PERSIST)
    private Company company;
    @JoinColumn(name = "person_id", referencedColumnName = "id")
    @ManyToOne(optional = true, cascade = CascadeType.PERSIST)
    private Person person;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne
    private Possession possession;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public Company getCompany() {
        return company;
    }

    public void setCompany(Company company) {
        this.company = company;
    }

    public Person getPerson() {
        return person;
    }

    public void setPerson(Person person) {
        this.person = person;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public boolean isCompany() {
        return company != null;
    }

    public boolean isPerson() {
        return person != null;
    }

    public String getName() {
        if (isCompany()) {
            return company.getName();
        } else if (isPerson()) {
            return person.getFirstName() + " " + person.getLastName();
        } else {
            return "";
        }
    }

    public String longDescription() {
        String description = "[name:" + getName() + "]";
        if (getPerson() != null) {
            description += "[person:" + getPerson().longDescription() + "]";
        }
        if (getCompany() != null) {
            description += "[company:" + getCompany().longDescription() + "]";
        }
        return description;
    }
}
