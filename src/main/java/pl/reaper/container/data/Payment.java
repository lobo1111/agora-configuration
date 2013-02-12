package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
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
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "payment")
@XmlRootElement
public class Payment implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Possession possession;
    @JoinColumn(name = "type_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Dictionary type;
    @JoinColumn(name = "status_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Dictionary status;
    @Column(name = "income")
    private BigDecimal income;
    @Basic(optional = true)
    @Size(min = 0, max = 255)
    @Column(name = "description")
    private String description;
    @Column(name = "booked")
    private boolean booked;
    @Column(name = "create_day")
    @Temporal(TemporalType.TIMESTAMP)
    private Date createDay;
    @Column(name = "booking_day")
    @Temporal(TemporalType.TIMESTAMP)
    private Date bookingDay;
    @JoinColumn(name = "balance_id", referencedColumnName = "id")
    @ManyToOne(optional = true)
    private ZpkBalance zpkBalance;
    @JoinColumn(name = "account_id", referencedColumnName = "id")
    @ManyToOne(optional = true)
    private Account account;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public Dictionary getType() {
        return type;
    }

    public void setType(Dictionary type) {
        this.type = type;
    }

    public Dictionary getStatus() {
        return status;
    }

    public void setStatus(Dictionary status) {
        this.status = status;
    }

    public BigDecimal getIncome() {
        return income;
    }

    public void setIncome(BigDecimal income) {
        this.income = income;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public boolean isBooked() {
        return booked;
    }

    public void setBooked(boolean booked) {
        this.booked = booked;
    }

    public Date getCreateDay() {
        return createDay;
    }

    public void setCreateDay(Date createDay) {
        this.createDay = createDay;
    }

    public Date getBookingDay() {
        return bookingDay;
    }

    public void setBookingDay(Date bookingDay) {
        this.bookingDay = bookingDay;
    }

    public ZpkBalance getZpkBalance() {
        return zpkBalance;
    }

    public void setZpkBalance(ZpkBalance zpkBalance) {
        this.zpkBalance = zpkBalance;
    }

    public Account getAccount() {
        return account;
    }

    public void setAccount(Account account) {
        this.account = account;
    }
}
