package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "zpk_balance")
@XmlRootElement
public class ZpkBalance implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @Column(name = "credit")
    private double credit;
    @Column(name = "debit")
    private double debit;
    @Column(name = "start_credit")
    private double startCredit;
    @Column(name = "start_debit")
    private double startDebit;
    @JoinColumn(name = "zpk_id", referencedColumnName = "id")
    @ManyToOne(cascade = CascadeType.PERSIST, optional = false)
    private ZakladowyPlanKont zpk;
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private BookingPeriod bookingPeriod;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "zpkBalance")
    private List<Payment> payments = new ArrayList<>();

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
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

    public double getStartCredit() {
        return startCredit;
    }

    public void setStartCredit(double startCredit) {
        this.startCredit = startCredit;
    }

    public double getStartDebit() {
        return startDebit;
    }

    public void setStartDebit(double startDebit) {
        this.startDebit = startDebit;
    }

    public ZakladowyPlanKont getZpk() {
        return zpk;
    }

    public void setZpk(ZakladowyPlanKont zpk) {
        this.zpk = zpk;
    }

    public BookingPeriod getBookingPeriod() {
        return bookingPeriod;
    }

    public void setBookingPeriod(BookingPeriod bookingPeriod) {
        this.bookingPeriod = bookingPeriod;
    }

    public List<Payment> getPayments() {
        return payments;
    }

    public void setPayments(List<Payment> payments) {
        this.payments = payments;
    }

    public String longDescription() {
        return "[credit:" + credit + "]"
                + "[debit:" + debit + "]"
                + "[startCredit:" + startCredit + "]"
                + "[startDebit:" + startDebit + "]";
    }
}
