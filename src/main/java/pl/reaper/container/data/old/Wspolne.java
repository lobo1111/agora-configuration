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
import javax.persistence.Lob;
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
@Table(name = "wspolne")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Wspolne.findAll", query = "SELECT w FROM Wspolne w")})
public class Wspolne implements Serializable {
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
    @Column(name = "nazwa")
    private String nazwa;
    @Size(max = 256)
    @Column(name = "ulica")
    private String ulica;
    @Size(max = 256)
    @Column(name = "nrbr")
    private String nrbr;
    @Size(max = 256)
    @Column(name = "pow")
    private String pow;
    @Size(max = 256)
    @Column(name = "powd")
    private String powd;
    @Size(max = 256)
    @Column(name = "pows")
    private String pows;
    @Size(max = 256)
    @Column(name = "osoby")
    private String osoby;
    @Size(max = 256)
    @Column(name = "ilmie")
    private String ilmie;
    @Size(max = 256)
    @Column(name = "rach")
    private String rach;
    @Size(max = 256)
    @Column(name = "rachfr")
    private String rachfr;
    @Size(max = 256)
    @Column(name = "dataprz")
    private String dataprz;
    @Size(max = 256)
    @Column(name = "datawyl")
    private String datawyl;
    @Size(max = 256)
    @Column(name = "zarzad")
    private String zarzad;
    @Size(max = 256)
    @Column(name = "funrem")
    private String funrem;
    @Size(max = 256)
    @Column(name = "funremjak")
    private String funremjak;
    @Size(max = 256)
    @Column(name = "nip")
    private String nip;
    @Size(max = 256)
    @Column(name = "regon")
    private String regon;
    @Size(max = 256)
    @Column(name = "kod")
    private String kod;
    @Lob
    @Size(max = 65535)
    @Column(name = "uchwala")
    private String uchwala;
    @Size(max = 256)
    @Column(name = "nr_uchwaly")
    private String nrUchwaly;
    @Size(max = 256)
    @Column(name = "datazebrania")
    private String datazebrania;
    @Size(max = 256)
    @Column(name = "godz_zebrania")
    private String godzZebrania;
    @Size(max = 256)
    @Column(name = "mkId")
    private String mkId;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 255)
    @Column(name = "md5")
    private String md5;

    public Wspolne() {
    }

    public Wspolne(Integer id) {
        this.id = id;
    }

    public Wspolne(Integer id, String md5) {
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

    public String getNazwa() {
        return nazwa;
    }

    public void setNazwa(String nazwa) {
        this.nazwa = nazwa;
    }

    public String getUlica() {
        return ulica;
    }

    public void setUlica(String ulica) {
        this.ulica = ulica;
    }

    public String getNrbr() {
        return nrbr;
    }

    public void setNrbr(String nrbr) {
        this.nrbr = nrbr;
    }

    public String getPow() {
        return pow;
    }

    public void setPow(String pow) {
        this.pow = pow;
    }

    public String getPowd() {
        return powd;
    }

    public void setPowd(String powd) {
        this.powd = powd;
    }

    public String getPows() {
        return pows;
    }

    public void setPows(String pows) {
        this.pows = pows;
    }

    public String getOsoby() {
        return osoby;
    }

    public void setOsoby(String osoby) {
        this.osoby = osoby;
    }

    public String getIlmie() {
        return ilmie;
    }

    public void setIlmie(String ilmie) {
        this.ilmie = ilmie;
    }

    public String getRach() {
        return rach;
    }

    public void setRach(String rach) {
        this.rach = rach;
    }

    public String getRachfr() {
        return rachfr;
    }

    public void setRachfr(String rachfr) {
        this.rachfr = rachfr;
    }

    public String getDataprz() {
        return dataprz;
    }

    public void setDataprz(String dataprz) {
        this.dataprz = dataprz;
    }

    public String getDatawyl() {
        return datawyl;
    }

    public void setDatawyl(String datawyl) {
        this.datawyl = datawyl;
    }

    public String getZarzad() {
        return zarzad;
    }

    public void setZarzad(String zarzad) {
        this.zarzad = zarzad;
    }

    public String getFunrem() {
        return funrem;
    }

    public void setFunrem(String funrem) {
        this.funrem = funrem;
    }

    public String getFunremjak() {
        return funremjak;
    }

    public void setFunremjak(String funremjak) {
        this.funremjak = funremjak;
    }

    public String getNip() {
        return nip;
    }

    public void setNip(String nip) {
        this.nip = nip;
    }

    public String getRegon() {
        return regon;
    }

    public void setRegon(String regon) {
        this.regon = regon;
    }

    public String getKod() {
        return kod;
    }

    public void setKod(String kod) {
        this.kod = kod;
    }

    public String getUchwala() {
        return uchwala;
    }

    public void setUchwala(String uchwala) {
        this.uchwala = uchwala;
    }

    public String getNrUchwaly() {
        return nrUchwaly;
    }

    public void setNrUchwaly(String nrUchwaly) {
        this.nrUchwaly = nrUchwaly;
    }

    public String getDatazebrania() {
        return datazebrania;
    }

    public void setDatazebrania(String datazebrania) {
        this.datazebrania = datazebrania;
    }

    public String getGodzZebrania() {
        return godzZebrania;
    }

    public void setGodzZebrania(String godzZebrania) {
        this.godzZebrania = godzZebrania;
    }

    public String getMkId() {
        return mkId;
    }

    public void setMkId(String mkId) {
        this.mkId = mkId;
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
        if (!(object instanceof Wspolne)) {
            return false;
        }
        Wspolne other = (Wspolne) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.old.Wspolne[ id=" + id + " ]";
    }
    
}
