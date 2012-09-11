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
@Table(name = "zpk")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Zpk.findAll", query = "SELECT z FROM Zpk z")})
public class Zpk implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "nrwsp")
    private String nrwsp;
    @Size(max = 256)
    @Column(name = "konto")
    private String konto;
    @Size(max = 256)
    @Column(name = "idkontr")
    private String idkontr;
    @Size(max = 256)
    @Column(name = "bo_wn")
    private String boWn;
    @Size(max = 256)
    @Column(name = "bo_ma")
    private String boMa;
    @Size(max = 256)
    @Column(name = "m01_wn")
    private String m01Wn;
    @Size(max = 256)
    @Column(name = "m01_ma")
    private String m01Ma;
    @Size(max = 256)
    @Column(name = "anali")
    private String anali;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Zpk() {
    }

    public Zpk(Integer id) {
        this.id = id;
    }

    public Zpk(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getNrwsp() {
        return nrwsp;
    }

    public void setNrwsp(String nrwsp) {
        this.nrwsp = nrwsp;
    }

    public String getKonto() {
        return konto;
    }

    public void setKonto(String konto) {
        this.konto = konto;
    }

    public String getIdkontr() {
        return idkontr;
    }

    public void setIdkontr(String idkontr) {
        this.idkontr = idkontr;
    }

    public String getBoWn() {
        return boWn;
    }

    public void setBoWn(String boWn) {
        this.boWn = boWn;
    }

    public String getBoMa() {
        return boMa;
    }

    public void setBoMa(String boMa) {
        this.boMa = boMa;
    }

    public String getM01Wn() {
        return m01Wn;
    }

    public void setM01Wn(String m01Wn) {
        this.m01Wn = m01Wn;
    }

    public String getM01Ma() {
        return m01Ma;
    }

    public void setM01Ma(String m01Ma) {
        this.m01Ma = m01Ma;
    }

    public String getAnali() {
        return anali;
    }

    public void setAnali(String anali) {
        this.anali = anali;
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
        if (!(object instanceof Zpk)) {
            return false;
        }
        Zpk other = (Zpk) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Zpk[ id=" + id + " ]";
    }
    
}
