package pl.reaper.container.data;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "community_default_contractor")
@XmlRootElement
public class CommunityDefaultContractor implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "company_id", referencedColumnName = "id")
    @ManyToOne
    private Company company;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "zpk_number")
    private String zpkNumber;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "zpk_description")
    private String zpkDescription;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Company getCompany() {
        return company;
    }

    public void setCompany(Company company) {
        this.company = company;
    }

    public String getZpkNumber() {
        return zpkNumber;
    }

    public void setZpkNumber(String zpkNumber) {
        this.zpkNumber = zpkNumber;
    }

    public String getZpkDescription() {
        return zpkDescription;
    }

    public void setZpkDescription(String zpkDescription) {
        this.zpkDescription = zpkDescription;
    }
}
