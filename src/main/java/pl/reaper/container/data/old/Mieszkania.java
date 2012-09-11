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
@Table(name = "mieszkania")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Mieszkania.findAll", query = "SELECT m FROM Mieszkania m")})
public class Mieszkania implements Serializable {
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
    @Column(name = "winda")
    private String winda;
    @Size(max = 256)
    @Column(name = "inne")
    private String inne;
    @Size(max = 256)
    @Column(name = "mc1")
    private String mc1;
    @Size(max = 256)
    @Column(name = "mc2")
    private String mc2;
    @Size(max = 256)
    @Column(name = "mc3")
    private String mc3;
    @Size(max = 256)
    @Column(name = "mc4")
    private String mc4;
    @Size(max = 256)
    @Column(name = "mc5")
    private String mc5;
    @Size(max = 256)
    @Column(name = "mc6")
    private String mc6;
    @Size(max = 256)
    @Column(name = "mc7")
    private String mc7;
    @Size(max = 256)
    @Column(name = "mc8")
    private String mc8;
    @Size(max = 256)
    @Column(name = "mc9")
    private String mc9;
    @Size(max = 256)
    @Column(name = "mc10")
    private String mc10;
    @Size(max = 256)
    @Column(name = "mc11")
    private String mc11;
    @Size(max = 256)
    @Column(name = "mc12")
    private String mc12;
    @Size(max = 256)
    @Column(name = "typ")
    private String typ;
    @Size(max = 256)
    @Column(name = "fr")
    private String fr;
    @Size(max = 256)
    @Column(name = "fmc1")
    private String fmc1;
    @Size(max = 256)
    @Column(name = "fmc2")
    private String fmc2;
    @Size(max = 256)
    @Column(name = "fmc3")
    private String fmc3;
    @Size(max = 256)
    @Column(name = "fmc4")
    private String fmc4;
    @Size(max = 256)
    @Column(name = "fmc5")
    private String fmc5;
    @Size(max = 256)
    @Column(name = "fmc6")
    private String fmc6;
    @Size(max = 256)
    @Column(name = "fmc7")
    private String fmc7;
    @Size(max = 256)
    @Column(name = "fmc8")
    private String fmc8;
    @Size(max = 256)
    @Column(name = "fmc9")
    private String fmc9;
    @Size(max = 256)
    @Column(name = "fmc10")
    private String fmc10;
    @Size(max = 256)
    @Column(name = "fmc11")
    private String fmc11;
    @Size(max = 256)
    @Column(name = "fmc12")
    private String fmc12;
    @Size(max = 256)
    @Column(name = "fr_ile_lok")
    private String frIleLok;
    @Size(max = 256)
    @Column(name = "wodomierz")
    private String wodomierz;
    @Size(max = 256)
    @Column(name = "pozytek")
    private String pozytek;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Mieszkania() {
    }

    public Mieszkania(Integer id) {
        this.id = id;
    }

    public Mieszkania(Integer id, String md5) {
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

    public String getWinda() {
        return winda;
    }

    public void setWinda(String winda) {
        this.winda = winda;
    }

    public String getInne() {
        return inne;
    }

    public void setInne(String inne) {
        this.inne = inne;
    }

    public String getMc1() {
        return mc1;
    }

    public void setMc1(String mc1) {
        this.mc1 = mc1;
    }

    public String getMc2() {
        return mc2;
    }

    public void setMc2(String mc2) {
        this.mc2 = mc2;
    }

    public String getMc3() {
        return mc3;
    }

    public void setMc3(String mc3) {
        this.mc3 = mc3;
    }

    public String getMc4() {
        return mc4;
    }

    public void setMc4(String mc4) {
        this.mc4 = mc4;
    }

    public String getMc5() {
        return mc5;
    }

    public void setMc5(String mc5) {
        this.mc5 = mc5;
    }

    public String getMc6() {
        return mc6;
    }

    public void setMc6(String mc6) {
        this.mc6 = mc6;
    }

    public String getMc7() {
        return mc7;
    }

    public void setMc7(String mc7) {
        this.mc7 = mc7;
    }

    public String getMc8() {
        return mc8;
    }

    public void setMc8(String mc8) {
        this.mc8 = mc8;
    }

    public String getMc9() {
        return mc9;
    }

    public void setMc9(String mc9) {
        this.mc9 = mc9;
    }

    public String getMc10() {
        return mc10;
    }

    public void setMc10(String mc10) {
        this.mc10 = mc10;
    }

    public String getMc11() {
        return mc11;
    }

    public void setMc11(String mc11) {
        this.mc11 = mc11;
    }

    public String getMc12() {
        return mc12;
    }

    public void setMc12(String mc12) {
        this.mc12 = mc12;
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

    public String getFmc1() {
        return fmc1;
    }

    public void setFmc1(String fmc1) {
        this.fmc1 = fmc1;
    }

    public String getFmc2() {
        return fmc2;
    }

    public void setFmc2(String fmc2) {
        this.fmc2 = fmc2;
    }

    public String getFmc3() {
        return fmc3;
    }

    public void setFmc3(String fmc3) {
        this.fmc3 = fmc3;
    }

    public String getFmc4() {
        return fmc4;
    }

    public void setFmc4(String fmc4) {
        this.fmc4 = fmc4;
    }

    public String getFmc5() {
        return fmc5;
    }

    public void setFmc5(String fmc5) {
        this.fmc5 = fmc5;
    }

    public String getFmc6() {
        return fmc6;
    }

    public void setFmc6(String fmc6) {
        this.fmc6 = fmc6;
    }

    public String getFmc7() {
        return fmc7;
    }

    public void setFmc7(String fmc7) {
        this.fmc7 = fmc7;
    }

    public String getFmc8() {
        return fmc8;
    }

    public void setFmc8(String fmc8) {
        this.fmc8 = fmc8;
    }

    public String getFmc9() {
        return fmc9;
    }

    public void setFmc9(String fmc9) {
        this.fmc9 = fmc9;
    }

    public String getFmc10() {
        return fmc10;
    }

    public void setFmc10(String fmc10) {
        this.fmc10 = fmc10;
    }

    public String getFmc11() {
        return fmc11;
    }

    public void setFmc11(String fmc11) {
        this.fmc11 = fmc11;
    }

    public String getFmc12() {
        return fmc12;
    }

    public void setFmc12(String fmc12) {
        this.fmc12 = fmc12;
    }

    public String getFrIleLok() {
        return frIleLok;
    }

    public void setFrIleLok(String frIleLok) {
        this.frIleLok = frIleLok;
    }

    public String getWodomierz() {
        return wodomierz;
    }

    public void setWodomierz(String wodomierz) {
        this.wodomierz = wodomierz;
    }

    public String getPozytek() {
        return pozytek;
    }

    public void setPozytek(String pozytek) {
        this.pozytek = pozytek;
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
        if (!(object instanceof Mieszkania)) {
            return false;
        }
        Mieszkania other = (Mieszkania) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Mieszkania[ id=" + id + " ]";
    }
    
}
