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
@Table(name = "kontrahenci")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Kontrahenci.findAll", query = "SELECT k FROM Kontrahenci k")})
public class Kontrahenci implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "idkontr")
    private String idkontr;
    @Size(max = 256)
    @Column(name = "nazwak")
    private String nazwak;
    @Size(max = 256)
    @Column(name = "kod")
    private String kod;
    @Size(max = 256)
    @Column(name = "ulica")
    private String ulica;
    @Size(max = 256)
    @Column(name = "nrbr")
    private String nrbr;
    @Size(max = 256)
    @Column(name = "nrmie")
    private String nrmie;
    @Size(max = 256)
    @Column(name = "nip")
    private String nip;
    @Size(max = 256)
    @Column(name = "rachunek")
    private String rachunek;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Kontrahenci() {
    }

    public Kontrahenci(Integer id) {
        this.id = id;
    }

    public Kontrahenci(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getIdkontr() {
        return idkontr;
    }

    public void setIdkontr(String idkontr) {
        this.idkontr = idkontr;
    }

    public String getNazwak() {
        return nazwak;
    }

    public void setNazwak(String nazwak) {
        this.nazwak = nazwak;
    }

    public String getKod() {
        return kod;
    }

    public void setKod(String kod) {
        this.kod = kod;
    }

    public String getUlica() {
        return ulica;
    }

    public void setUlica(String ulica) {
        this.ulica = ulica;
    }

    public String getNrbr() {
        return nrbr;
    }

    public void setNrbr(String nrbr) {
        this.nrbr = nrbr;
    }

    public String getNrmie() {
        return nrmie;
    }

    public void setNrmie(String nrmie) {
        this.nrmie = nrmie;
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
        if (!(object instanceof Kontrahenci)) {
            return false;
        }
        Kontrahenci other = (Kontrahenci) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Kontrahenci[ id=" + id + " ]";
    }
    
}
