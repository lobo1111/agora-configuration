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
@Table(name = "wsp640")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Wsp640.findAll", query = "SELECT w FROM Wsp640 w")})
public class Wsp640 implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "naz")
    private String naz;
    @Size(max = 256)
    @Column(name = "pco")
    private String pco;
    @Size(max = 256)
    @Column(name = "kco")
    private String kco;
    @Size(max = 256)
    @Column(name = "co")
    private String co;
    @Size(max = 256)
    @Column(name = "pzw")
    private String pzw;
    @Size(max = 256)
    @Column(name = "kzw")
    private String kzw;
    @Size(max = 256)
    @Column(name = "zw")
    private String zw;
    @Size(max = 256)
    @Column(name = "pns")
    private String pns;
    @Size(max = 256)
    @Column(name = "kns")
    private String kns;
    @Size(max = 256)
    @Column(name = "ns")
    private String ns;
    @Size(max = 256)
    @Column(name = "wynik")
    private String wynik;
    @Size(max = 256)
    @Column(name = "nrwsp")
    private String nrwsp;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Wsp640() {
    }

    public Wsp640(Integer id) {
        this.id = id;
    }

    public Wsp640(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNaz() {
        return naz;
    }

    public void setNaz(String naz) {
        this.naz = naz;
    }

    public String getPco() {
        return pco;
    }

    public void setPco(String pco) {
        this.pco = pco;
    }

    public String getKco() {
        return kco;
    }

    public void setKco(String kco) {
        this.kco = kco;
    }

    public String getCo() {
        return co;
    }

    public void setCo(String co) {
        this.co = co;
    }

    public String getPzw() {
        return pzw;
    }

    public void setPzw(String pzw) {
        this.pzw = pzw;
    }

    public String getKzw() {
        return kzw;
    }

    public void setKzw(String kzw) {
        this.kzw = kzw;
    }

    public String getZw() {
        return zw;
    }

    public void setZw(String zw) {
        this.zw = zw;
    }

    public String getPns() {
        return pns;
    }

    public void setPns(String pns) {
        this.pns = pns;
    }

    public String getKns() {
        return kns;
    }

    public void setKns(String kns) {
        this.kns = kns;
    }

    public String getNs() {
        return ns;
    }

    public void setNs(String ns) {
        this.ns = ns;
    }

    public String getWynik() {
        return wynik;
    }

    public void setWynik(String wynik) {
        this.wynik = wynik;
    }

    public String getNrwsp() {
        return nrwsp;
    }

    public void setNrwsp(String nrwsp) {
        this.nrwsp = nrwsp;
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
        if (!(object instanceof Wsp640)) {
            return false;
        }
        Wsp640 other = (Wsp640) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Wsp640[ id=" + id + " ]";
    }
    
}
