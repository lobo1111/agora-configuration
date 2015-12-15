package pl.reaper.container.data;

import java.io.Serializable;
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
@Table(name = "document")
@XmlRootElement
public class Document implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @Column(name = "type")
    private String type;
    @ManyToOne
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    private Community community;
    @ManyToOne
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    private Possession possession;
    @ManyToOne
    @JoinColumn(name = "contractor_id", referencedColumnName = "id")
    private Contractor contractor;
    @Column(name = "created_at")
    @Temporal(TemporalType.DATE)
    private Date createdAt;
    @Column(name = "closed")
    private boolean closed;
    @Column(name = "closed_at")
    @Temporal(TemporalType.DATE)
    private Date closedAt;
    @Column(name = "canceled")
    private boolean canceled;
    @Column(name = "canceled_at")
    @Temporal(TemporalType.DATE)
    private Date canceledAt;
    @Column(name = "description")
    private String description;
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "document")
    private List<DocumentAttribute> attributes = new ArrayList<>();
    @OneToMany(cascade = CascadeType.PERSIST, mappedBy = "document")
    private List<DocumentPosition> positions = new ArrayList<>();

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

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public Contractor getContractor() {
        return contractor;
    }

    public void setContractor(Contractor contractor) {
        this.contractor = contractor;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public boolean isClosed() {
        return closed;
    }

    public void setClosed(boolean closed) {
        this.closed = closed;
    }

    public Date getClosedAt() {
        return closedAt;
    }

    public void setClosedAt(Date closedAt) {
        this.closedAt = closedAt;
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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<DocumentAttribute> getAttributes() {
        return attributes;
    }

    public void setAttributes(List<DocumentAttribute> attributes) {
        this.attributes = attributes;
    }

    public List<DocumentPosition> getPositions() {
        return positions;
    }

    public void setPositions(List<DocumentPosition> positions) {
        this.positions = positions;
    }

    public DocumentAttribute putAttribute(String name, String value) {
        DocumentAttribute attr = getAttribute(name);
        attr = attr == null ? new DocumentAttribute() : attr;
        attr.setDocument(this);
        attr.setName(name);
        attr.setValue(value);
        if (!getAttributes().contains(attr)) {
            getAttributes().add(attr);
        }
        return attr;
    }

    public DocumentAttribute getAttribute(String name) {
        for (DocumentAttribute attr : attributes) {
            if (attr.getName().equals(name)) {
                return attr;
            }
        }
        return null;
    }
}
