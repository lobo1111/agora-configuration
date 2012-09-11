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
@Table(name = "platnicy")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Platnicy.findAll", query = "SELECT p FROM Platnicy p")})
public class Platnicy implements Serializable {
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
    @Column(name = "nazwisko")
    private String nazwisko;
    @Size(max = 256)
    @Column(name = "imie")
    private String imie;
    @Size(max = 256)
    @Column(name = "nazwa")
    private String nazwa;
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
    @Column(name = "kod")
    private String kod;
    @Size(max = 256)
    @Column(name = "dat_od")
    private String datOd;
    @Size(max = 256)
    @Column(name = "dat_do")
    private String datDo;
    @Size(max = 256)
    @Column(name = "nip")
    private String nip;
    @Size(max = 256)
    @Column(name = "bo")
    private String bo;
    @Size(max = 256)
    @Column(name = "wplaty")
    private String wplaty;
    @Size(max = 256)
    @Column(name = "noty")
    private String noty;
    @Size(max = 256)
    @Column(name = "odsetki")
    private String odsetki;
    @Size(max = 256)
    @Column(name = "ods")
    private String ods;
    @Size(max = 256)
    @Column(name = "umorzenia")
    private String umorzenia;
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
    @Column(name = "uwagi")
    private String uwagi;
    @Size(max = 256)
    @Column(name = "fbo")
    private String fbo;
    @Size(max = 256)
    @Column(name = "fwplaty")
    private String fwplaty;
    @Size(max = 256)
    @Column(name = "fnoty")
    private String fnoty;
    @Size(max = 256)
    @Column(name = "fodsetki")
    private String fodsetki;
    @Size(max = 256)
    @Column(name = "fods")
    private String fods;
    @Size(max = 256)
    @Column(name = "fumorzenia")
    private String fumorzenia;
    @Size(max = 256)
    @Column(name = "fmc")
    private String fmc;
    @Size(max = 256)
    @Column(name = "fbow")
    private String fbow;
    @Size(max = 256)
    @Column(name = "bo1")
    private String bo1;
    @Size(max = 256)
    @Column(name = "fbo1")
    private String fbo1;
    @Size(max = 256)
    @Column(name = "rach")
    private String rach;
    @Size(max = 256)
    @Column(name = "windykacja")
    private String windykacja;
    @Size(max = 256)
    @Column(name = "tel")
    private String tel;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Platnicy() {
    }

    public Platnicy(Integer id) {
        this.id = id;
    }

    public Platnicy(Integer id, String md5) {
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

    public String getNazwisko() {
        return nazwisko;
    }

    public void setNazwisko(String nazwisko) {
        this.nazwisko = nazwisko;
    }

    public String getImie() {
        return imie;
    }

    public void setImie(String imie) {
        this.imie = imie;
    }

    public String getNazwa() {
        return nazwa;
    }

    public void setNazwa(String nazwa) {
        this.nazwa = nazwa;
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

    public String getKod() {
        return kod;
    }

    public void setKod(String kod) {
        this.kod = kod;
    }

    public String getDatOd() {
        return datOd;
    }

    public void setDatOd(String datOd) {
        this.datOd = datOd;
    }

    public String getDatDo() {
        return datDo;
    }

    public void setDatDo(String datDo) {
        this.datDo = datDo;
    }

    public String getNip() {
        return nip;
    }

    public void setNip(String nip) {
        this.nip = nip;
    }

    public String getBo() {
        return bo;
    }

    public void setBo(String bo) {
        this.bo = bo;
    }

    public String getWplaty() {
        return wplaty;
    }

    public void setWplaty(String wplaty) {
        this.wplaty = wplaty;
    }

    public String getNoty() {
        return noty;
    }

    public void setNoty(String noty) {
        this.noty = noty;
    }

    public String getOdsetki() {
        return odsetki;
    }

    public void setOdsetki(String odsetki) {
        this.odsetki = odsetki;
    }

    public String getOds() {
        return ods;
    }

    public void setOds(String ods) {
        this.ods = ods;
    }

    public String getUmorzenia() {
        return umorzenia;
    }

    public void setUmorzenia(String umorzenia) {
        this.umorzenia = umorzenia;
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

    public String getUwagi() {
        return uwagi;
    }

    public void setUwagi(String uwagi) {
        this.uwagi = uwagi;
    }

    public String getFbo() {
        return fbo;
    }

    public void setFbo(String fbo) {
        this.fbo = fbo;
    }

    public String getFwplaty() {
        return fwplaty;
    }

    public void setFwplaty(String fwplaty) {
        this.fwplaty = fwplaty;
    }

    public String getFnoty() {
        return fnoty;
    }

    public void setFnoty(String fnoty) {
        this.fnoty = fnoty;
    }

    public String getFodsetki() {
        return fodsetki;
    }

    public void setFodsetki(String fodsetki) {
        this.fodsetki = fodsetki;
    }

    public String getFods() {
        return fods;
    }

    public void setFods(String fods) {
        this.fods = fods;
    }

    public String getFumorzenia() {
        return fumorzenia;
    }

    public void setFumorzenia(String fumorzenia) {
        this.fumorzenia = fumorzenia;
    }

    public String getFmc() {
        return fmc;
    }

    public void setFmc(String fmc) {
        this.fmc = fmc;
    }

    public String getFbow() {
        return fbow;
    }

    public void setFbow(String fbow) {
        this.fbow = fbow;
    }

    public String getBo1() {
        return bo1;
    }

    public void setBo1(String bo1) {
        this.bo1 = bo1;
    }

    public String getFbo1() {
        return fbo1;
    }

    public void setFbo1(String fbo1) {
        this.fbo1 = fbo1;
    }

    public String getRach() {
        return rach;
    }

    public void setRach(String rach) {
        this.rach = rach;
    }

    public String getWindykacja() {
        return windykacja;
    }

    public void setWindykacja(String windykacja) {
        this.windykacja = windykacja;
    }

    public String getTel() {
        return tel;
    }

    public void setTel(String tel) {
        this.tel = tel;
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
        if (!(object instanceof Platnicy)) {
            return false;
        }
        Platnicy other = (Platnicy) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Platnicy[ id=" + id + " ]";
    }
    
}
