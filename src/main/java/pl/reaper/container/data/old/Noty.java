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
@Table(name = "noty")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Noty.findAll", query = "SELECT n FROM Noty n")})
public class Noty implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "platnik")
    private String platnik;
    @Size(max = 256)
    @Column(name = "mieszkanie")
    private String mieszkanie;
    @Size(max = 256)
    @Column(name = "data")
    private String data;
    @Size(max = 256)
    @Column(name = "nota")
    private String nota;
    @Size(max = 256)
    @Column(name = "kwota")
    private String kwota;
    @Size(max = 256)
    @Column(name = "symbol")
    private String symbol;
    @Size(max = 256)
    @Column(name = "idtypu")
    private String idtypu;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Noty() {
    }

    public Noty(Integer id) {
        this.id = id;
    }

    public Noty(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getPlatnik() {
        return platnik;
    }

    public void setPlatnik(String platnik) {
        this.platnik = platnik;
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

    public String getNota() {
        return nota;
    }

    public void setNota(String nota) {
        this.nota = nota;
    }

    public String getKwota() {
        return kwota;
    }

    public void setKwota(String kwota) {
        this.kwota = kwota;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getIdtypu() {
        return idtypu;
    }

    public void setIdtypu(String idtypu) {
        this.idtypu = idtypu;
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
        if (!(object instanceof Noty)) {
            return false;
        }
        Noty other = (Noty) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Noty[ id=" + id + " ]";
    }
    
}
