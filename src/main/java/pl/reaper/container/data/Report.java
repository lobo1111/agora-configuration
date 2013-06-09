package pl.reaper.container.data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "report")
@XmlRootElement
public class Report implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @Column(name = "name")
    private String name;
    @JoinColumn(name = "community_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Community community;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "report")
    private Collection<ReportSection> sections = new ArrayList<>();
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "report")
    private Collection<ReportAttribute> attributes = new ArrayList<>();
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "report")
    private Collection<ReportFilter> filters = new ArrayList<>();

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

    public Community getCommunity() {
        return community;
    }

    public void setCommunity(Community community) {
        this.community = community;
    }

    public Collection<ReportSection> getSections() {
        return sections;
    }

    public void setSections(Collection<ReportSection> sections) {
        this.sections = sections;
    }

    public Collection<ReportAttribute> getAttributes() {
        return attributes;
    }

    public void setAttributes(Collection<ReportAttribute> attributes) {
        this.attributes = attributes;
    }

    public Collection<ReportFilter> getFilters() {
        return filters;
    }

    public void setFilters(Collection<ReportFilter> filters) {
        this.filters = filters;
    }
}
