package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
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
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "payment_scheduler_template")
@XmlRootElement
public class PaymentSchedulerTemplate implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @JoinColumn(name = "payment_scheduler_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private PaymentScheduler paymentScheduler;
    @Column(name = "amount")
    private BigDecimal amount;
    @Basic(optional = true)
    @Size(min = 0, max = 255)
    @Column(name = "description")
    private String description;
    @JoinColumn(name = "type_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Dictionary type;
    @Column(name = "auto_book")
    private boolean autoBook;

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

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Dictionary getType() {
        return type;
    }

    public void setType(Dictionary type) {
        this.type = type;
    }

    public boolean isAutoBook() {
        return autoBook;
    }

    public void setAutoBook(boolean autoBook) {
        this.autoBook = autoBook;
    }

}
