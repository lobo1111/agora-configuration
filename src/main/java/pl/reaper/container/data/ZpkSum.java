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
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "zpk_sum")
@XmlRootElement
public class ZpkSum implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private int id;
    @JoinColumn(name = "zpk_id", referencedColumnName = "id")
    @OneToOne(cascade = CascadeType.PERSIST, optional = false)
    private ZakladowyPlanKont zpk;
    @JoinColumn(name = "booking_period_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private BookingPeriod bookingPeriod;
    @Column(name = "number_prefix")
    private String numberPrefix;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public ZakladowyPlanKont getZpk() {
        return zpk;
    }

    public void setZpk(ZakladowyPlanKont zpk) {
        this.zpk = zpk;
    }

    public BookingPeriod getBookingPeriod() {
        return bookingPeriod;
    }

    public void setBookingPeriod(BookingPeriod bookingPeriod) {
        this.bookingPeriod = bookingPeriod;
    }

    public String getNumberPrefix() {
        return numberPrefix;
    }

    public void setNumberPrefix(String numberPrefix) {
        this.numberPrefix = numberPrefix;
    }
}
