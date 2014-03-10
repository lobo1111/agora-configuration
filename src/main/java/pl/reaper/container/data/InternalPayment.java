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
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "internal_payment")
@XmlRootElement
public class InternalPayment implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @ManyToOne
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    private BookingPeriod bookingPeriod;
    @Column(name = "created_date")
    @Temporal(TemporalType.DATE)
    private Date createdDate;
    @Column(name = "booked_date")
    @Temporal(TemporalType.DATE)
    private Date bookedDate;
    @ManyToOne
    @JoinColumn(name = "credit_zpk_id", referencedColumnName = "id")
    private ZakladowyPlanKont creditZpk;
    @ManyToOne
    @JoinColumn(name = "debit_zpk_id", referencedColumnName = "id")
    private ZakladowyPlanKont debitZpk;
    @Column(name = "booked")
    private boolean booked;
    @Column(name = "credit")
    private double credit;
    @Column(name = "debit")
    private double debit;
    @Column(name = "comment")
    private String comment;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public BookingPeriod getBookingPeriod() {
        return bookingPeriod;
    }

    public void setBookingPeriod(BookingPeriod bookingPeriod) {
        this.bookingPeriod = bookingPeriod;
    }

    public Date getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(Date createdDate) {
        this.createdDate = createdDate;
    }

    public Date getBookedDate() {
        return bookedDate;
    }

    public void setBookedDate(Date bookedDate) {
        this.bookedDate = bookedDate;
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

    public boolean isBooked() {
        return booked;
    }

    public void setBooked(boolean booked) {
        this.booked = booked;
    }

    public double getCredit() {
        return credit;
    }

    public void setCredit(double credit) {
        this.credit = credit;
    }

    public double getDebit() {
        return debit;
    }

    public void setDebit(double debit) {
        this.debit = debit;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }
}
