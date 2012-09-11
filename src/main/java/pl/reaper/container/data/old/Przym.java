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
@Table(name = "przym")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Przym.findAll", query = "SELECT p FROM Przym p")})
public class Przym implements Serializable {
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
    @Column(name = "miesiac")
    private String miesiac;
    @Size(max = 256)
    @Column(name = "platnik")
    private String platnik;
    @Size(max = 256)
    @Column(name = "kul")
    private String kul;
    @Size(max = 256)
    @Column(name = "nrbr")
    private String nrbr;
    @Size(max = 256)
    @Column(name = "nrmie")
    private String nrmie;
    @Size(max = 256)
    @Column(name = "udzial")
    private String udzial;
    @Size(max = 256)
    @Column(name = "nrwsp")
    private String nrwsp;
    @Size(max = 256)
    @Column(name = "pow")
    private String pow;
    @Size(max = 256)
    @Column(name = "pow_co")
    private String powCo;
    @Size(max = 256)
    @Column(name = "osoby")
    private String osoby;
    @Size(max = 256)
    @Column(name = "zw_norma")
    private String zwNorma;
    @Size(max = 256)
    @Column(name = "cw_norma")
    private String cwNorma;
    @Size(max = 256)
    @Column(name = "czynsz")
    private String czynsz;
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
    @Column(name = "np")
    private String np;
    @Size(max = 256)
    @Column(name = "inne")
    private String inne;
    @Size(max = 256)
    @Column(name = "winda")
    private String winda;
    @Size(max = 256)
    @Column(name = "pozytek")
    private String pozytek;
    @Size(max = 256)
    @Column(name = "mc")
    private String mc;
    @Size(max = 256)
    @Column(name = "typ")
    private String typ;
    @Size(max = 256)
    @Column(name = "fr")
    private String fr;
    @Size(max = 256)
    @Column(name = "wodomierz")
    private String wodomierz;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Przym() {
    }

    public Przym(Integer id) {
        this.id = id;
    }

    public Przym(Integer id, String md5) {
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

    public String getMiesiac() {
        return miesiac;
    }

    public void setMiesiac(String miesiac) {
        this.miesiac = miesiac;
    }

    public String getPlatnik() {
        return platnik;
    }

    public void setPlatnik(String platnik) {
        this.platnik = platnik;
    }

    public String getKul() {
        return kul;
    }

    public void setKul(String kul) {
        this.kul = kul;
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

    public String getUdzial() {
        return udzial;
    }

    public void setUdzial(String udzial) {
        this.udzial = udzial;
    }

    public String getNrwsp() {
        return nrwsp;
    }

    public void setNrwsp(String nrwsp) {
        this.nrwsp = nrwsp;
    }

    public String getPow() {
        return pow;
    }

    public void setPow(String pow) {
        this.pow = pow;
    }

    public String getPowCo() {
        return powCo;
    }

    public void setPowCo(String powCo) {
        this.powCo = powCo;
    }

    public String getOsoby() {
        return osoby;
    }

    public void setOsoby(String osoby) {
        this.osoby = osoby;
    }

    public String getZwNorma() {
        return zwNorma;
    }

    public void setZwNorma(String zwNorma) {
        this.zwNorma = zwNorma;
    }

    public String getCwNorma() {
        return cwNorma;
    }

    public void setCwNorma(String cwNorma) {
        this.cwNorma = cwNorma;
    }

    public String getCzynsz() {
        return czynsz;
    }

    public void setCzynsz(String czynsz) {
        this.czynsz = czynsz;
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

    public String getNp() {
        return np;
    }

    public void setNp(String np) {
        this.np = np;
    }

    public String getInne() {
        return inne;
    }

    public void setInne(String inne) {
        this.inne = inne;
    }

    public String getWinda() {
        return winda;
    }

    public void setWinda(String winda) {
        this.winda = winda;
    }

    public String getPozytek() {
        return pozytek;
    }

    public void setPozytek(String pozytek) {
        this.pozytek = pozytek;
    }

    public String getMc() {
        return mc;
    }

    public void setMc(String mc) {
        this.mc = mc;
    }

    public String getTyp() {
        return typ;
    }

    public void setTyp(String typ) {
        this.typ = typ;
    }

    public String getFr() {
        return fr;
    }

    public void setFr(String fr) {
        this.fr = fr;
    }

    public String getWodomierz() {
        return wodomierz;
    }

    public void setWodomierz(String wodomierz) {
        this.wodomierz = wodomierz;
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
        if (!(object instanceof Przym)) {
            return false;
        }
        Przym other = (Przym) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Przym[ id=" + id + " ]";
    }
    
}
