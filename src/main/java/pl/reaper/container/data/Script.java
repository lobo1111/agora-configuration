package pl.reaper.container.data;

import java.io.Serializable;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.Lob;
import javax.persistence.ManyToMany;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "script")
@XmlRootElement
public class Script implements Serializable {

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
    @Column(name = "script")
    private String script;
    @Lob
    @Size(max = 65535)
    @Column(name = "on_init")
    private String onInit;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "script")
    private Collection<ScriptScheduler> scriptSchedulers;
    @ManyToMany
    @JoinTable(name = "script_dependency",
    joinColumns =
    @JoinColumn(name = "script_id", referencedColumnName = "id"),
    inverseJoinColumns =
    @JoinColumn(name = "dependency", referencedColumnName = "id"))
    private Collection<Script> dependencies;
    @OneToMany
    @JoinTable(name = "script_security",
    inverseJoinColumns =
    @JoinColumn(name = "dictionary_id", referencedColumnName = "id"))
    private Collection<Dictionary> allowedGroups;

    public Script() {
    }

    public Script(Integer id) {
        this.id = id;
    }

    public Script(Integer id, String name) {
        this.id = id;
        this.name = name;
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

    public String getScript() {
        return script;
    }

    public void setScript(String script) {
        this.script = script;
    }

    public String getOnInit() {
        return onInit;
    }

    public void setOnInit(String onInit) {
        this.onInit = onInit;
    }

    @XmlTransient
    public Collection<ScriptScheduler> getScriptSchedulers() {
        return scriptSchedulers;
    }

    public void setScriptSchedulers(Collection<ScriptScheduler> scriptSchedulers) {
        this.scriptSchedulers = scriptSchedulers;
    }

    @XmlTransient
    public Collection<Script> getDependencies() {
        return dependencies;
    }

    public void setDependencies(Collection<Script> dependencies) {
        this.dependencies = dependencies;
    }

    public Collection<Dictionary> getAllowedGroups() {
        return allowedGroups;
    }

    public void setAllowedGroups(Collection<Dictionary> allowedGroups) {
        this.allowedGroups = allowedGroups;
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
        if (!(object instanceof Script)) {
            return false;
        }
        Script other = (Script) object;
        if (!this.name.equals(other.name)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Script[ id=" + id + " ]";
    }
}
