package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Collection;
import java.util.Date;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "incoming_payment_document")
@XmlRootElement
public class IncomingPaymentDocument implements Serializable {
    @Basic(optional = false)
    @Column(name = "status")
    private String status;
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 255)
    @Column(name = "sender")
    private String sender;
    @Column(name = "dateFrom")
    @Temporal(TemporalType.DATE)
    private Date dateFrom;
    @Column(name = "dateTo")
    @Temporal(TemporalType.DATE)
    private Date dateTo;
    @Size(max = 255)
    @Column(name = "accountNumber")
    private String accountNumber;
    @Size(max = 255)
    @Column(name = "extractNumber")
    private String extractNumber;
    // @Max(value=?)  @Min(value=?)//if you know range of your decimal fields consider using these annotations to enforce field validation
    @Column(name = "income")
    private BigDecimal income;
    @Column(name = "spending")
    private BigDecimal spending;
    @Column(name = "positionCounter")
    private Integer positionCounter;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "document")
    private Collection<IncomingPaymentDocumentPosition> incomingPaymentDocumentPositionCollection;

    public IncomingPaymentDocument() {
    }

    public IncomingPaymentDocument(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getSender() {
        return sender;
    }

    public void setSender(String sender) {
        this.sender = sender;
    }

    public Date getDateFrom() {
        return dateFrom;
    }

    public void setDateFrom(Date dateFrom) {
        this.dateFrom = dateFrom;
    }

    public Date getDateTo() {
        return dateTo;
    }

    public void setDateTo(Date dateTo) {
        this.dateTo = dateTo;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        this.accountNumber = accountNumber;
    }

    public String getExtractNumber() {
        return extractNumber;
    }

    public void setExtractNumber(String extractNumber) {
        this.extractNumber = extractNumber;
    }

    public BigDecimal getIncome() {
        return income;
    }

    public void setIncome(BigDecimal income) {
        this.income = income;
    }

    public BigDecimal getSpending() {
        return spending;
    }

    public void setSpending(BigDecimal spending) {
        this.spending = spending;
    }

    public Integer getPositionCounter() {
        return positionCounter;
    }

    public void setPositionCounter(Integer positionCounter) {
        this.positionCounter = positionCounter;
    }

    @XmlTransient
    public Collection<IncomingPaymentDocumentPosition> getIncomingPaymentDocumentPositionCollection() {
        return incomingPaymentDocumentPositionCollection;
    }

    public void setIncomingPaymentDocumentPositionCollection(Collection<IncomingPaymentDocumentPosition> incomingPaymentDocumentPositionCollection) {
        this.incomingPaymentDocumentPositionCollection = incomingPaymentDocumentPositionCollection;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof IncomingPaymentDocument)) {
            return false;
        }
        IncomingPaymentDocument other = (IncomingPaymentDocument) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.IncomingPaymentDocument[ id=" + id + " ]";
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
    
}
