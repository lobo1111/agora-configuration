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
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "script")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "Script.findAll", query = "SELECT s FROM Script s"),
    @NamedQuery(name = "Script.findById", query = "SELECT s FROM Script s WHERE s.id = :id"),
    @NamedQuery(name = "Script.findByName", query = "SELECT s FROM Script s WHERE s.name = :name"),
    @NamedQuery(name = "Script.findByBase", query = "SELECT s FROM Script s WHERE s.base = :base")})
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
    @Column(name = "base")
    private Boolean base;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "script")
    private Collection<ScriptScheduler> scriptSchedulers;
    @OneToMany(mappedBy = "parent")
    private Collection<Script> dependentScripts;
    @JoinColumn(name = "parent", referencedColumnName = "id")
    @ManyToOne
    private Script parent;

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

    public Boolean getBase() {
        return base;
    }

    public void setBase(Boolean base) {
        this.base = base;
    }

    @XmlTransient
    public Collection<ScriptScheduler> getScriptSchedulers() {
        return scriptSchedulers;
    }

    public void setScriptSchedulers(Collection<ScriptScheduler> scriptSchedulers) {
        this.scriptSchedulers = scriptSchedulers;
    }

    @XmlTransient
    public Collection<Script> getDependantScripts() {
        return dependentScripts;
    }

    public void setDependantScripts(Collection<Script> dependentScripts) {
        this.dependentScripts = dependentScripts;
    }

    public Script getParent() {
        return parent;
    }

    public void setParent(Script parent) {
        this.parent = parent;
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
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Script[ id=" + id + " ]";
    }
    
}
