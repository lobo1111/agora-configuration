package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Date;
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
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "document_position")
@XmlRootElement
public class DocumentPosition implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @Column(name = "type")
    private String type;
    @ManyToOne
    @JoinColumn(name = "document_id", referencedColumnName = "id")
    private Document document;
    @ManyToOne
    @JoinColumn(name = "account_id", referencedColumnName = "id")
    private Account account;
    @ManyToOne
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    private BookingPeriod bookingPeriod;
    @ManyToOne
    @JoinColumn(name = "zpk_debit_id", referencedColumnName = "id")
    private ZakladowyPlanKont zpkDebit;
    @ManyToOne
    @JoinColumn(name = "zpk_credit_id", referencedColumnName = "id")
    private ZakladowyPlanKont zpkCredit;
    @Column(name = "month")
    private String month;
    @Column(name = "description")
    private String description;
    @Column(name = "client_name")
    private String clientName;
    @Column(name = "value")
    private BigDecimal value;
    @Column(name = "booked")
    private boolean booked;
    @Column(name = "booked_at")
    @Temporal(TemporalType.DATE)
    private Date bookedAt;
    @Column(name = "canceled")
    private boolean canceled;
    @Column(name = "canceled_at")
    @Temporal(TemporalType.DATE)
    private Date canceledAt;
    @Column(name = "created_at")
    @Temporal(TemporalType.DATE)
    private Date createdAt;
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "documentPosition")
    private List<DocumentPositionAttribute> attributes = new ArrayList<>();

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Document getDocument() {
        return document;
    }

    public void setDocument(Document document) {
        this.document = document;
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

    public ZakladowyPlanKont getZpkDebit() {
        return zpkDebit;
    }

    public void setZpkDebit(ZakladowyPlanKont zpkDebit) {
        this.zpkDebit = zpkDebit;
    }

    public ZakladowyPlanKont getZpkCredit() {
        return zpkCredit;
    }

    public void setZpkCredit(ZakladowyPlanKont zpkCredit) {
        this.zpkCredit = zpkCredit;
    }

    public String getMonth() {
        return month;
    }

    public void setMonth(String month) {
        this.month = month;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getClientName() {
        return clientName;
    }

    public void setClientName(String clientName) {
        this.clientName = clientName;
    }

    public BigDecimal getValue() {
        return value;
    }

    public void setValue(BigDecimal value) {
        this.value = value;
    }

    public boolean isBooked() {
        return booked;
    }

    public void setBooked(boolean booked) {
        this.booked = booked;
    }

    public Date getBookedAt() {
        return bookedAt;
    }

    public void setBookedAt(Date bookedAt) {
        this.bookedAt = bookedAt;
    }

    public boolean isCanceled() {
        return canceled;
    }

    public void setCanceled(boolean canceled) {
        this.canceled = canceled;
    }

    public Date getCanceledAt() {
        return canceledAt;
    }

    public void setCanceledAt(Date canceledAt) {
        this.canceledAt = canceledAt;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public List<DocumentPositionAttribute> getAttributes() {
        return attributes;
    }

    public void setAttributes(List<DocumentPositionAttribute> attributes) {
        this.attributes = attributes;
    }

    public DocumentPositionAttribute addAttribute(String name, String value) {
        DocumentPositionAttribute attr = new DocumentPositionAttribute();
        attr.setDocumentPosition(this);
        attr.setName(name);
        attr.setValue(value);
        this.getAttributes().add(attr);
        return attr;
    }
}
