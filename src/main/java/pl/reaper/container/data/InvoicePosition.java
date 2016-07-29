package pl.reaper.container.data;

import java.io.Serializable;
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
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "invoice_position")
@XmlRootElement
public class InvoicePosition implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @ManyToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name = "invoice_id", referencedColumnName = "id")
    private Invoice invoice;
    @Column(name = "position")
    private int position;
    @Column(name = "name")
    private String name;
    @ManyToOne
    @JoinColumn(name = "tax_id", referencedColumnName = "id")
    private Dictionary tax;
    @Column(name = "volume")
    private double volume;
    @Column(name = "unit_value_net")
    private double unitValueNet;
    @Column(name = "value_net")
    private double valueNet;
    @Column(name = "value_gross")
    private double valueGross;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Invoice getInvoice() {
        return invoice;
    }

    public void setInvoice(Invoice invoice) {
        this.invoice = invoice;
    }

    public int getPosition() {
        return position;
    }

    public void setPosition(int position) {
        this.position = position;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Dictionary getTax() {
        return tax;
    }

    public void setTax(Dictionary tax) {
        this.tax = tax;
    }

    public double getVolume() {
        return volume;
    }

    public void setVolume(double volume) {
        this.volume = volume;
    }

    public double getValueNet() {
        return valueNet;
    }

    public void setValueNet(double valueNet) {
        this.valueNet = valueNet;
    }

    public double getValueGross() {
        return valueGross;
    }

    public void setValueGross(double valueGross) {
        this.valueGross = valueGross;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 67 * hash + this.id;
        return hash;
    }

    public double getUnitValueNet() {
        return unitValueNet;
    }

    public void setUnitValueNet(double unitValueNet) {
        this.unitValueNet = unitValueNet;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final InvoicePosition other = (InvoicePosition) obj;
        if (this.id != other.id) {
            return false;
        }
        return true;
    }

}
