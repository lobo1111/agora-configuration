package pl.reaper.container.data;

import java.io.Serializable;
import java.util.Date;
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
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "payment_rent")
@XmlRootElement
public class PaymentRent implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne(optional = true)
    private Possession possession;
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private BookingPeriod bookingPeriod;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 12)
    @Column(name = "month")
    private String month;
    @Column(name = "timestamp")
    @Temporal(TemporalType.TIMESTAMP)
    private Date timestamp;
    @Column(name = "repair_fund")
    private boolean repairFund;
    @OneToOne(cascade = CascadeType.PERSIST, fetch = FetchType.EAGER, mappedBy = "paymentRent")
    private PaymentRentDetails paymentRentDetails = new PaymentRentDetails();
    @OneToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name = "internal_payment_id", referencedColumnName = "id")
    private InternalPayment internalPayment;

    public InternalPayment getInternalPayment() {
        return internalPayment;
    }

    public void setInternalPayment(InternalPayment internalPayment) {
        this.internalPayment = internalPayment;
    }

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

    public BookingPeriod getBookingPeriod() {
        return bookingPeriod;
    }

    public void setBookingPeriod(BookingPeriod bookingPeriod) {
        this.bookingPeriod = bookingPeriod;
    }

    public String getMonth() {
        return month;
    }

    public void setMonth(String month) {
        this.month = month;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public boolean isRepairFund() {
        return repairFund;
    }

    public void setRepairFund(boolean repairFund) {
        this.repairFund = repairFund;
    }

    public PaymentRentDetails getPaymentRentDetails() {
        return paymentRentDetails;
    }

    public void setPaymentRentDetails(PaymentRentDetails paymentRentDetails) {
        this.paymentRentDetails = paymentRentDetails;
    }

    public double calculateValue() {
        return paymentRentDetails.getValue();
    }
}
