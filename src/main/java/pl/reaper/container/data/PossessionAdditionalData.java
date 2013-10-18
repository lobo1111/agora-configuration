package pl.reaper.container.data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Objects;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "possession_additional_data")
@XmlRootElement
public class PossessionAdditionalData implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Column(name = "declared_share")
    private double declaredShare;
    @Column(name = "declared_area")
    private double declaredArea;
    @Column(name = "people")
    private int people;
    @Column(name = "rooms")
    private int rooms;
    @Column(name = "hot_water")
    private double hotWater;
    @Column(name = "cold_water")
    private double coldWater;
    @OneToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "possession_id")
    private Possession possession;
    @JoinColumn(name = "account_id", referencedColumnName = "id")
    @OneToOne(optional = true)
    private Account account;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Account getAccount() {
        return account;
    }

    public void setAccount(Account account) {
        this.account = account;
    }

    public double getDeclaredArea() {
        return declaredArea;
    }

    public void setDeclaredArea(double declaredArea) {
        this.declaredArea = declaredArea;
    }

    public double getDeclaredShare() {
        return declaredShare;
    }

    public void setDeclaredShare(double declaredShare) {
        this.declaredShare = declaredShare;
    }

    public int getPeople() {
        return people;
    }

    public void setPeople(int people) {
        this.people = people;
    }

    public int getRooms() {
        return rooms;
    }

    public void setRooms(int rooms) {
        this.rooms = rooms;
    }

    public double getHotWater() {
        return hotWater;
    }

    public void setHotWater(double hotWater) {
        this.hotWater = hotWater;
    }

    public double getColdWater() {
        return coldWater;
    }

    public void setColdWater(double coldWater) {
        this.coldWater = coldWater;
    }

    public Possession getPossession() {
        return possession;
    }

    public void setPossession(Possession possession) {
        this.possession = possession;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 47 * hash + Objects.hashCode(this.id);
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final PossessionAdditionalData other = (PossessionAdditionalData) obj;
        if (!Objects.equals(this.id, other.id)) {
            return false;
        }
        return true;
    }
}
