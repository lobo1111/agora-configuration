/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package pl.reaper.container.data;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
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
@Table(name = "script_scheduler")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "ScriptScheduler.findAll", query = "SELECT s FROM ScriptScheduler s"),
    @NamedQuery(name = "ScriptScheduler.findById", query = "SELECT s FROM ScriptScheduler s WHERE s.id = :id"),
    @NamedQuery(name = "ScriptScheduler.findByName", query = "SELECT s FROM ScriptScheduler s WHERE s.name = :name"),
    @NamedQuery(name = "ScriptScheduler.findByEnabled", query = "SELECT s FROM ScriptScheduler s WHERE s.enabled = :enabled"),
    @NamedQuery(name = "ScriptScheduler.findBySchedule", query = "SELECT s FROM ScriptScheduler s WHERE s.schedule = :schedule")})
public class ScriptScheduler implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 45)
    @Column(name = "name")
    private String name;
    @Lob
    @Size(max = 65535)
    @Column(name = "command")
    private String command;
    @Basic(optional = false)
    @NotNull
    @Column(name = "enabled")
    private boolean enabled;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 45)
    @Column(name = "schedule")
    private String schedule;
    @JoinColumn(name = "id_script", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Script idScript;

    public ScriptScheduler() {
    }

    public ScriptScheduler(Integer id) {
        this.id = id;
    }

    public ScriptScheduler(Integer id, String name, boolean enabled, String schedule) {
        this.id = id;
        this.name = name;
        this.enabled = enabled;
        this.schedule = schedule;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCommand() {
        return command;
    }

    public void setCommand(String command) {
        this.command = command;
    }

    public boolean getEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getSchedule() {
        return schedule;
    }

    public void setSchedule(String schedule) {
        this.schedule = schedule;
    }

    public Script getIdScript() {
        return idScript;
    }

    public void setIdScript(Script idScript) {
        this.idScript = idScript;
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
        if (!(object instanceof ScriptScheduler)) {
            return false;
        }
        ScriptScheduler other = (ScriptScheduler) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.ScriptScheduler[ id=" + id + " ]";
    }
    
}
