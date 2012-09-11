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
@Table(name = "dane")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Dane.findAll", query = "SELECT d FROM Dane d")})
public class Dane implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "nazwa1")
    private String nazwa1;
    @Size(max = 256)
    @Column(name = "nazwa2")
    private String nazwa2;
    @Size(max = 256)
    @Column(name = "adres")
    private String adres;
    @Size(max = 256)
    @Column(name = "tel")
    private String tel;
    @Size(max = 256)
    @Column(name = "NIP")
    private String nip;
    @Size(max = 256)
    @Column(name = "rachunek")
    private String rachunek;
    @Size(max = 256)
    @Column(name = "poczta")
    private String poczta;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Dane() {
    }

    public Dane(Integer id) {
        this.id = id;
    }

    public Dane(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNazwa1() {
        return nazwa1;
    }

    public void setNazwa1(String nazwa1) {
        this.nazwa1 = nazwa1;
    }

    public String getNazwa2() {
        return nazwa2;
    }

    public void setNazwa2(String nazwa2) {
        this.nazwa2 = nazwa2;
    }

    public String getAdres() {
        return adres;
    }

    public void setAdres(String adres) {
        this.adres = adres;
    }

    public String getTel() {
        return tel;
    }

    public void setTel(String tel) {
        this.tel = tel;
    }

    public String getNip() {
        return nip;
    }

    public void setNip(String nip) {
        this.nip = nip;
    }

    public String getRachunek() {
        return rachunek;
    }

    public void setRachunek(String rachunek) {
        this.rachunek = rachunek;
    }

    public String getPoczta() {
        return poczta;
    }

    public void setPoczta(String poczta) {
        this.poczta = poczta;
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
        if (!(object instanceof Dane)) {
            return false;
        }
        Dane other = (Dane) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Dane[ id=" + id + " ]";
    }
    
}
