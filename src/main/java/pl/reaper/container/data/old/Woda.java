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
@Table(name = "woda")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Woda.findAll", query = "SELECT w FROM Woda w")})
public class Woda implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "mieszkanie")
    private String mieszkanie;
    @Size(max = 256)
    @Column(name = "data")
    private String data;
    @Size(max = 256)
    @Column(name = "wskpop")
    private String wskpop;
    @Size(max = 256)
    @Column(name = "wskbie")
    private String wskbie;
    @Size(max = 256)
    @Column(name = "zuzycie")
    private String zuzycie;
    @Size(max = 256)
    @Column(name = "zuzyciew")
    private String zuzyciew;
    @Size(max = 256)
    @Column(name = "zaliczka")
    private String zaliczka;
    @Size(max = 256)
    @Column(name = "kwota")
    private String kwota;
    @Size(max = 256)
    @Column(name = "wodomierzId")
    private String wodomierzId;
    @Size(max = 256)
    @Column(name = "typ")
    private String typ;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Woda() {
    }

    public Woda(Integer id) {
        this.id = id;
    }

    public Woda(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getMieszkanie() {
        return mieszkanie;
    }

    public void setMieszkanie(String mieszkanie) {
        this.mieszkanie = mieszkanie;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public String getWskpop() {
        return wskpop;
    }

    public void setWskpop(String wskpop) {
        this.wskpop = wskpop;
    }

    public String getWskbie() {
        return wskbie;
    }

    public void setWskbie(String wskbie) {
        this.wskbie = wskbie;
    }

    public String getZuzycie() {
        return zuzycie;
    }

    public void setZuzycie(String zuzycie) {
        this.zuzycie = zuzycie;
    }

    public String getZuzyciew() {
        return zuzyciew;
    }

    public void setZuzyciew(String zuzyciew) {
        this.zuzyciew = zuzyciew;
    }

    public String getZaliczka() {
        return zaliczka;
    }

    public void setZaliczka(String zaliczka) {
        this.zaliczka = zaliczka;
    }

    public String getKwota() {
        return kwota;
    }

    public void setKwota(String kwota) {
        this.kwota = kwota;
    }

    public String getWodomierzId() {
        return wodomierzId;
    }

    public void setWodomierzId(String wodomierzId) {
        this.wodomierzId = wodomierzId;
    }

    public String getTyp() {
        return typ;
    }

    public void setTyp(String typ) {
        this.typ = typ;
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
        if (!(object instanceof Woda)) {
            return false;
        }
        Woda other = (Woda) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Woda[ id=" + id + " ]";
    }
    
}
