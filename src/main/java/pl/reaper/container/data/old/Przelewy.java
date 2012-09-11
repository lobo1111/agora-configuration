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
@Table(name = "przelewy")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Przelewy.findAll", query = "SELECT p FROM Przelewy p")})
public class Przelewy implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "idprzelewu")
    private String idprzelewu;
    @Size(max = 256)
    @Column(name = "nazwap")
    private String nazwap;
    @Size(max = 256)
    @Column(name = "idodb")
    private String idodb;
    @Size(max = 256)
    @Column(name = "idzlec")
    private String idzlec;
    @Size(max = 256)
    @Column(name = "kwota")
    private String kwota;
    @Size(max = 256)
    @Column(name = "tytulem")
    private String tytulem;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Przelewy() {
    }

    public Przelewy(Integer id) {
        this.id = id;
    }

    public Przelewy(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getIdprzelewu() {
        return idprzelewu;
    }

    public void setIdprzelewu(String idprzelewu) {
        this.idprzelewu = idprzelewu;
    }

    public String getNazwap() {
        return nazwap;
    }

    public void setNazwap(String nazwap) {
        this.nazwap = nazwap;
    }

    public String getIdodb() {
        return idodb;
    }

    public void setIdodb(String idodb) {
        this.idodb = idodb;
    }

    public String getIdzlec() {
        return idzlec;
    }

    public void setIdzlec(String idzlec) {
        this.idzlec = idzlec;
    }

    public String getKwota() {
        return kwota;
    }

    public void setKwota(String kwota) {
        this.kwota = kwota;
    }

    public String getTytulem() {
        return tytulem;
    }

    public void setTytulem(String tytulem) {
        this.tytulem = tytulem;
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
        if (!(object instanceof Przelewy)) {
            return false;
        }
        Przelewy other = (Przelewy) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Przelewy[ id=" + id + " ]";
    }
    
}
