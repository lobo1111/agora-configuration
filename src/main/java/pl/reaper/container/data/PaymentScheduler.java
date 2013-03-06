package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "payment_scheduler")
@XmlRootElement
public class PaymentScheduler implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "name")
    private String name;
    @Column(name = "active")
    private boolean active;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 20)
    @Column(name = "day")
    private String day;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Community community;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "paymentScheduler")
    private Collection<PaymentSchedulerTemplate> paymentSchedulerTemplates = new ArrayList<>();
    @ManyToMany
    @JoinTable(
        name = "payment_scheduler_zpk", joinColumns =
    @JoinColumn(name = "payment_scheduler_id", referencedColumnName = "id"),
    inverseJoinColumns =
    @JoinColumn(name = "zpk_account_id", referencedColumnName = "id"))
    private Collection<PaymentSchedulerZpk> zpks = new ArrayList<>();

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public String getDay() {
        return day;
    }

    public void setDay(String day) {
        this.day = day;
    }

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public Collection<PaymentSchedulerTemplate> getPaymentSchedulerTemplates() {
        return paymentSchedulerTemplates;
    }

    public void setPaymentSchedulerTemplates(Collection<PaymentSchedulerTemplate> paymentSchedulerTemplates) {
        this.paymentSchedulerTemplates = paymentSchedulerTemplates;
    }

    public Collection<PaymentSchedulerZpk> getZpks() {
        return zpks;
    }

    public void setZpks(Collection<PaymentSchedulerZpk> zpks) {
        this.zpks = zpks;
    }
}
