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
@Table(name = "obr")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Obr.findAll", query = "SELECT o FROM Obr o")})
public class Obr implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Size(max = 256)
    @Column(name = "gr_rodz")
    private String grRodz;
    @Size(max = 256)
    @Column(name = "nrwsp")
    private String nrwsp;
    @Size(max = 256)
    @Column(name = "nr_dok")
    private String nrDok;
    @Size(max = 256)
    @Column(name = "nr_poz")
    private String nrPoz;
    @Size(max = 256)
    @Column(name = "dat_dok")
    private String datDok;
    @Size(max = 256)
    @Column(name = "konto_wn")
    private String kontoWn;
    @Size(max = 256)
    @Column(name = "konto_ma")
    private String kontoMa;
    @Size(max = 256)
    @Column(name = "wartosc")
    private String wartosc;
    @Size(max = 256)
    @Column(name = "nr_fakt")
    private String nrFakt;
    @Size(max = 256)
    @Column(name = "dat_fakt")
    private String datFakt;
    @Size(max = 256)
    @Column(name = "opis")
    private String opis;
    @Size(max = 256)
    @Column(name = "co")
    private String co;
    @Size(max = 256)
    @Column(name = "cw")
    private String cw;
    @Size(max = 256)
    @Column(name = "zw")
    private String zw;
    @Size(max = 256)
    @Column(name = "ns")
    private String ns;
    @Size(max = 256)
    @Column(name = "in")
    private String in;
    @Size(max = 256)
    @Column(name = "nrdok")
    private String nrdok;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Obr() {
    }

    public Obr(Integer id) {
        this.id = id;
    }

    public Obr(Integer id, String md5) {
        this.id = id;
        this.md5 = md5;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getGrRodz() {
        return grRodz;
    }

    public void setGrRodz(String grRodz) {
        this.grRodz = grRodz;
    }

    public String getNrwsp() {
        return nrwsp;
    }

    public void setNrwsp(String nrwsp) {
        this.nrwsp = nrwsp;
    }

    public String getNrDok() {
        return nrDok;
    }

    public void setNrDok(String nrDok) {
        this.nrDok = nrDok;
    }

    public String getNrPoz() {
        return nrPoz;
    }

    public void setNrPoz(String nrPoz) {
        this.nrPoz = nrPoz;
    }

    public String getDatDok() {
        return datDok;
    }

    public void setDatDok(String datDok) {
        this.datDok = datDok;
    }

    public String getKontoWn() {
        return kontoWn;
    }

    public void setKontoWn(String kontoWn) {
        this.kontoWn = kontoWn;
    }

    public String getKontoMa() {
        return kontoMa;
    }

    public void setKontoMa(String kontoMa) {
        this.kontoMa = kontoMa;
    }

    public String getWartosc() {
        return wartosc;
    }

    public void setWartosc(String wartosc) {
        this.wartosc = wartosc;
    }

    public String getNrFakt() {
        return nrFakt;
    }

    public void setNrFakt(String nrFakt) {
        this.nrFakt = nrFakt;
    }

    public String getDatFakt() {
        return datFakt;
    }

    public void setDatFakt(String datFakt) {
        this.datFakt = datFakt;
    }

    public String getOpis() {
        return opis;
    }

    public void setOpis(String opis) {
        this.opis = opis;
    }

    public String getCo() {
        return co;
    }

    public void setCo(String co) {
        this.co = co;
    }

    public String getCw() {
        return cw;
    }

    public void setCw(String cw) {
        this.cw = cw;
    }

    public String getZw() {
        return zw;
    }

    public void setZw(String zw) {
        this.zw = zw;
    }

    public String getNs() {
        return ns;
    }

    public void setNs(String ns) {
        this.ns = ns;
    }

    public String getIn() {
        return in;
    }

    public void setIn(String in) {
        this.in = in;
    }

    public String getNrdok() {
        return nrdok;
    }

    public void setNrdok(String nrdok) {
        this.nrdok = nrdok;
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
        if (!(object instanceof Obr)) {
            return false;
        }
        Obr other = (Obr) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Obr[ id=" + id + " ]";
    }
    
}
