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
@Table(name = "administrowanie")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Administrowanie.findAll", query = "SELECT a FROM Administrowanie a")})
public class Administrowanie implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "Nr_Faktury")
    private String nrFaktury;
    @Size(max = 256)
    @Column(name = "Data_Faktury")
    private String dataFaktury;
    @Size(max = 256)
    @Column(name = "IdWsp")
    private String idWsp;
    @Size(max = 256)
    @Column(name = "Miesiac")
    private String miesiac;
    @Size(max = 256)
    @Column(name = "Cena")
    private String cena;
    @Size(max = 256)
    @Column(name = "Ilosc")
    private String ilosc;
    @Size(max = 256)
    @Column(name = "VAT")
    private String vat;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Administrowanie() {
    }

    public Administrowanie(Integer id) {
        this.id = id;
    }

    public Administrowanie(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNrFaktury() {
        return nrFaktury;
    }

    public void setNrFaktury(String nrFaktury) {
        this.nrFaktury = nrFaktury;
    }

    public String getDataFaktury() {
        return dataFaktury;
    }

    public void setDataFaktury(String dataFaktury) {
        this.dataFaktury = dataFaktury;
    }

    public String getIdWsp() {
        return idWsp;
    }

    public void setIdWsp(String idWsp) {
        this.idWsp = idWsp;
    }

    public String getMiesiac() {
        return miesiac;
    }

    public void setMiesiac(String miesiac) {
        this.miesiac = miesiac;
    }

    public String getCena() {
        return cena;
    }

    public void setCena(String cena) {
        this.cena = cena;
    }

    public String getIlosc() {
        return ilosc;
    }

    public void setIlosc(String ilosc) {
        this.ilosc = ilosc;
    }

    public String getVat() {
        return vat;
    }

    public void setVat(String vat) {
        this.vat = vat;
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
        if (!(object instanceof Administrowanie)) {
            return false;
        }
        Administrowanie other = (Administrowanie) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Administrowanie[ id=" + id + " ]";
    }
    
}
