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
@Table(name = "payment_scheduler_zpk")
@XmlRootElement
public class PaymentSchedulerZpk implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @JoinColumn(name = "payment_scheduler_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private PaymentScheduler paymentScheduler;
    @JoinColumn(name = "zpk_account_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST, optional = false)
    private ZakladowyPlanKont zpk;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public PaymentScheduler getPaymentScheduler() {
        return paymentScheduler;
    }

    public void setPaymentScheduler(PaymentScheduler paymentScheduler) {
        this.paymentScheduler = paymentScheduler;
    }

    public ZakladowyPlanKont getZpk() {
        return zpk;
    }

    public void setZpk(ZakladowyPlanKont zpk) {
        this.zpk = zpk;
    }
}
