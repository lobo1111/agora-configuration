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
@Table(name = "possession_auto_payment_order")
@XmlRootElement
public class PossessionAutoPaymentOrder implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST)
    private Possession possession;
    @JoinColumn(name = "zpk_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private ZakladowyPlanKont zpk;
    @Basic(optional = false)
    @Column(name = "payment_order")
    private int order;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public ZakladowyPlanKont getZpk() {
        return zpk;
    }

    public void setZpk(ZakladowyPlanKont zpk) {
        this.zpk = zpk;
    }

    public int getOrder() {
        return order;
    }

    public void setOrder(int order) {
        this.order = order;
    }
}
