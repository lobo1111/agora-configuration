package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "settlement_log")
@XmlRootElement
public class SettlementLog implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "obligation_group_id", referencedColumnName = "id")
    @ManyToOne
    private ObligationGroup obligationGroup;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne
    private Community community;
    @Column(name = "total_income")
    private double totalIncome;
    @Column(name = "total_obligations")
    private double totalObligations;
    @Column(name = "settlement_balance")
    private double settlementBalance;
    @Column(name = "total_area")
    private double totalArea;
    @Column(name = "reference_rate")
    private double referenceRate;
    @ManyToMany
    @JoinTable(
        name = "settlement_log_payment", joinColumns =
    @JoinColumn(name = "settlement_id", referencedColumnName = "id"),
    inverseJoinColumns =
    @JoinColumn(name = "payment_id", referencedColumnName = "id"))
    private Collection<Payment> payments = new ArrayList<>();
    @Basic(optional = false)
    @NotNull
    @Column(name = "timestamp")
    @Temporal(TemporalType.TIMESTAMP)
    private Date timestamp = new Date();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public ObligationGroup getObligationGroup() {
        return obligationGroup;
    }

    public void setObligationGroup(ObligationGroup obligationGroup) {
        this.obligationGroup = obligationGroup;
    }

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public double getTotalIncome() {
        return totalIncome;
    }

    public void setTotalIncome(double totalIncome) {
        this.totalIncome = totalIncome;
    }

    public double getTotalObligations() {
        return totalObligations;
    }

    public void setTotalObligations(double totalObligations) {
        this.totalObligations = totalObligations;
    }

    public double getSettlementBalance() {
        return settlementBalance;
    }

    public void setSettlementBalance(double settlementBalance) {
        this.settlementBalance = settlementBalance;
    }

    public double getTotalArea() {
        return totalArea;
    }

    public void setTotalArea(double totalArea) {
        this.totalArea = totalArea;
    }

    public double getReferenceRate() {
        return referenceRate;
    }

    public void setReferenceRate(double referenceRate) {
        this.referenceRate = referenceRate;
    }

    public Collection<Payment> getPayments() {
        return payments;
    }

    public void setPayments(Collection<Payment> payments) {
        this.payments = payments;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}
