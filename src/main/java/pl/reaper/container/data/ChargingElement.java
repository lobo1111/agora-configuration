package pl.reaper.container.data;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "charging_element")
@XmlRootElement
public class ChargingElement implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @NotNull
    @Column(name = "key_value")
    private String key;
    @Basic(optional = false)
    @NotNull
    @Column(name = "name")
    private String name;
    @JoinColumn(name = "group_id", referencedColumnName = "id")
    @ManyToOne
    private Dictionary group;
    @Column(name = "value")
    private double value;
    @JoinColumn(name = "charging_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Charging charging;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Dictionary getGroup() {
        return group;
    }

    public void setGroup(Dictionary group) {
        this.group = group;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public Charging getCharging() {
        return charging;
    }

    public void setCharging(Charging charging) {
        this.charging = charging;
    }
}
