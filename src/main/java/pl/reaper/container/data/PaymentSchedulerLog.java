package pl.reaper.container.data;

import java.io.Serializable;
import java.util.Date;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "payment_scheduler_log")
@XmlRootElement
public class PaymentSchedulerLog implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @JoinColumn(name = "payment_scheduler_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private PaymentScheduler paymentScheduler;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 20)
    @Column(name = "fired_month")
    private String firedMonth;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 20)
    @Column(name = "fired_year")
    private String firedYear;
    @Basic(optional = false)
    @NotNull
    @Column(name = "timestamp")
    @Temporal(TemporalType.TIMESTAMP)
    private Date timestamp = new Date();

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

    public String getFiredMonth() {
        return firedMonth;
    }

    public void setFiredMonth(String firedMonth) {
        this.firedMonth = firedMonth;
    }

    public String getFiredYear() {
        return firedYear;
    }

    public void setFiredYear(String firedYear) {
        this.firedYear = firedYear;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}
