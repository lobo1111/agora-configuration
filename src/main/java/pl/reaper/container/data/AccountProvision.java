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
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "account_provision")
@XmlRootElement
public class AccountProvision implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "account_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Account account;
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private BookingPeriod bookingPeriod;
    @JoinColumn(name = "internal_payment_id", referencedColumnName = "id")
    @OneToOne
    private InternalPayment internalPayment;
    @Column(name = "provision_value")
    private double provisionValue;
    @Column(name = "created_at")
    @Temporal(javax.persistence.TemporalType.DATE)
    private Date createdAt;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 12)
    @Column(name = "month")
    private String month;

    public String getMonth() {
        return month;
    }

    public void setMonth(String month) {
        this.month = month;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Account getAccount() {
        return account;
    }

    public void setAccount(Account account) {
        this.account = account;
    }

    public BookingPeriod getBookingPeriod() {
        return bookingPeriod;
    }

    public void setBookingPeriod(BookingPeriod bookingPeriod) {
        this.bookingPeriod = bookingPeriod;
    }

    public InternalPayment getInternalPayment() {
        return internalPayment;
    }

    public void setInternalPayment(InternalPayment internalPayment) {
        this.internalPayment = internalPayment;
    }

    public double getProvisionValue() {
        return provisionValue;
    }

    public void setProvisionValue(double provisionValue) {
        this.provisionValue = provisionValue;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

}
