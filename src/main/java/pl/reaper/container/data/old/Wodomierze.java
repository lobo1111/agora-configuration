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
@Table(name = "wodomierze")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Wodomierze.findAll", query = "SELECT w FROM Wodomierze w")})
public class Wodomierze implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "wodomierzId")
    private String wodomierzId;
    @Size(max = 256)
    @Column(name = "mieszkanie")
    private String mieszkanie;
    @Size(max = 256)
    @Column(name = "wodomierz")
    private String wodomierz;
    @Size(max = 256)
    @Column(name = "data_legalizacji")
    private String dataLegalizacji;
    @Size(max = 256)
    @Column(name = "data_montazu")
    private String dataMontazu;
    @Size(max = 256)
    @Column(name = "zamontowany")
    private String zamontowany;
    @Size(max = 256)
    @Column(name = "adres")
    private String adres;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Wodomierze() {
    }

    public Wodomierze(Integer id) {
        this.id = id;
    }

    public Wodomierze(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getWodomierzId() {
        return wodomierzId;
    }

    public void setWodomierzId(String wodomierzId) {
        this.wodomierzId = wodomierzId;
    }

    public String getMieszkanie() {
        return mieszkanie;
    }

    public void setMieszkanie(String mieszkanie) {
        this.mieszkanie = mieszkanie;
    }

    public String getWodomierz() {
        return wodomierz;
    }

    public void setWodomierz(String wodomierz) {
        this.wodomierz = wodomierz;
    }

    public String getDataLegalizacji() {
        return dataLegalizacji;
    }

    public void setDataLegalizacji(String dataLegalizacji) {
        this.dataLegalizacji = dataLegalizacji;
    }

    public String getDataMontazu() {
        return dataMontazu;
    }

    public void setDataMontazu(String dataMontazu) {
        this.dataMontazu = dataMontazu;
    }

    public String getZamontowany() {
        return zamontowany;
    }

    public void setZamontowany(String zamontowany) {
        this.zamontowany = zamontowany;
    }

    public String getAdres() {
        return adres;
    }

    public void setAdres(String adres) {
        this.adres = adres;
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
        if (!(object instanceof Wodomierze)) {
            return false;
        }
        Wodomierze other = (Wodomierze) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Wodomierze[ id=" + id + " ]";
    }
    
}
