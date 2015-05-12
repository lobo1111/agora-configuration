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
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "bank_note")
@XmlRootElement
public class BankNote implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "possession_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Possession possession;
    @JoinColumn(name = "element_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Element element;
    @Column(name = "note_value")
    private double noteValue;
    @Column(name = "description")
    private String description;
    @Column(name = "created_at")
    @Temporal(javax.persistence.TemporalType.DATE)
    private Date createdAt;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    public Element getElement() {
        return element;
    }

    public void setElement(Element element) {
        this.element = element;
    }

    public double getNoteValue() {
        return noteValue;
    }

    public void setNoteValue(double noteValue) {
        this.noteValue = noteValue;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

}
