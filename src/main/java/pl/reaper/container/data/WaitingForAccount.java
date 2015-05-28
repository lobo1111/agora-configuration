package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
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
import javax.persistence.Temporal;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "waiting_for_account")
@XmlRootElement
public class WaitingForAccount implements Serializable {

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
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private BookingPeriod bookingPeriod;
    @Column(name = "settled")
    private boolean settled;
    @Column(name = "comment")
    private String comment;
    @Column(name = "created_at")
    @Temporal(javax.persistence.TemporalType.DATE)
    private Date createdAt;
    @Column(name = "value")
    private double value;
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "waitingForAccount")
    private Collection<WaitingForAccountSettlement> settlements = new ArrayList<>();

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

    public BookingPeriod getBookingPeriod() {
        return bookingPeriod;
    }

    public void setBookingPeriod(BookingPeriod bookingPeriod) {
        this.bookingPeriod = bookingPeriod;
    }

    public boolean isSettled() {
        return settled;
    }

    public void setSettled(boolean settled) {
        this.settled = settled;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public Collection<WaitingForAccountSettlement> getSettlements() {
        return settlements;
    }

    public void setSettlements(Collection<WaitingForAccountSettlement> settlements) {
        this.settlements = settlements;
    }

}
