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
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "internal_document_definition")
@XmlRootElement
public class InternalDocumentDefinition implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Community community;
    @JoinColumn(name = "credit_zpk_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private ZakladowyPlanKont creditZpk;
    @JoinColumn(name = "debit_zpk_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private ZakladowyPlanKont debitZpk;
    @Column(name = "name")
    private String name;

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

    public ZakladowyPlanKont getCreditZpk() {
        return creditZpk;
    }

    public void setCreditZpk(ZakladowyPlanKont creditZpk) {
        this.creditZpk = creditZpk;
    }

    public ZakladowyPlanKont getDebitZpk() {
        return debitZpk;
    }

    public void setDebitZpk(ZakladowyPlanKont debitZpk) {
        this.debitZpk = debitZpk;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

}
