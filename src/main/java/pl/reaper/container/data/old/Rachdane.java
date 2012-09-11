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
@Table(name = "rachdane")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Rachdane.findAll", query = "SELECT r FROM Rachdane r")})
public class Rachdane implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "nrrach")
    private String nrrach;
    @Size(max = 256)
    @Column(name = "idtowaru")
    private String idtowaru;
    @Size(max = 256)
    @Column(name = "ilosc")
    private String ilosc;
    @Size(max = 256)
    @Column(name = "cena")
    private String cena;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Rachdane() {
    }

    public Rachdane(Integer id) {
        this.id = id;
    }

    public Rachdane(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNrrach() {
        return nrrach;
    }

    public void setNrrach(String nrrach) {
        this.nrrach = nrrach;
    }

    public String getIdtowaru() {
        return idtowaru;
    }

    public void setIdtowaru(String idtowaru) {
        this.idtowaru = idtowaru;
    }

    public String getIlosc() {
        return ilosc;
    }

    public void setIlosc(String ilosc) {
        this.ilosc = ilosc;
    }

    public String getCena() {
        return cena;
    }

    public void setCena(String cena) {
        this.cena = cena;
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
        if (!(object instanceof Rachdane)) {
            return false;
        }
        Rachdane other = (Rachdane) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Rachdane[ id=" + id + " ]";
    }
    
}
