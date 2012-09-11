/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.reaper.container.data.old;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;

/**
 *
 * @author tomek
 */
@Entity
@Table(name = "dodatki")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Dodatki.findAll", query = "SELECT d FROM Dodatki d")})
public class Dodatki implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "nr_decyzji")
    private String nrDecyzji;
    @Size(max = 256)
    @Column(name = "platnik")
    private String platnik;
    @Size(max = 256)
    @Column(name = "dat_od")
    private String datOd;
    @Size(max = 256)
    @Column(name = "dat_do")
    private String datDo;
    @Size(max = 256)
    @Column(name = "kwota")
    private String kwota;
    @Size(max = 256)
    @Column(name = "kw")
    private String kw;
    @Size(max = 256)
    @Column(name = "CzyZawieszony")
    private String czyZawieszony;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Dodatki() {
    }

    public Dodatki(Integer id) {
        this.id = id;
    }

    public Dodatki(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNrDecyzji() {
        return nrDecyzji;
    }

    public void setNrDecyzji(String nrDecyzji) {
        this.nrDecyzji = nrDecyzji;
    }

    public String getPlatnik() {
        return platnik;
    }

    public void setPlatnik(String platnik) {
        this.platnik = platnik;
    }

    public String getDatOd() {
        return datOd;
    }

    public void setDatOd(String datOd) {
        this.datOd = datOd;
    }

    public String getDatDo() {
        return datDo;
    }

    public void setDatDo(String datDo) {
        this.datDo = datDo;
    }

    public String getKwota() {
        return kwota;
    }

    public void setKwota(String kwota) {
        this.kwota = kwota;
    }

    public String getKw() {
        return kw;
    }

    public void setKw(String kw) {
        this.kw = kw;
    }

    public String getCzyZawieszony() {
        return czyZawieszony;
    }

    public void setCzyZawieszony(String czyZawieszony) {
        this.czyZawieszony = czyZawieszony;
    }

    public String getMd5() {
        return md5;
    }

    public void setMd5(String md5) {
        this.md5 = md5;
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
        if (!(object instanceof Dodatki)) {
            return false;
        }
        Dodatki other = (Dodatki) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Dodatki[ id=" + id + " ]";
    }
    
}
