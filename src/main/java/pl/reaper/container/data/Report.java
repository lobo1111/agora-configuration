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
    @Basic(optional = false)
    @Column(name = "css")
    private String css;
    @Basic(optional = false)
    @Column(name = "js")
    private String js;
    @Basic(optional = false)
    @Column(name = "on_init")
    private String onInit;
    @Basic(optional = false)
    @Column(name = "header_style")
    private String headerStyle;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "report")
    private Collection<ReportSection> sections = new ArrayList<>();
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "report")
    private Collection<ReportFilter> filters = new ArrayList<>();
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "report")
    private Collection<ReportFilterGroup> filterGroups = new ArrayList<>();

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

    public String getHeaderStyle() {
        return headerStyle;
    }

    public void setHeaderStyle(String headerStyle) {
        this.headerStyle = headerStyle;
    }

    public String getOnInit() {
        return onInit;
    }

    public void setOnInit(String onInit) {
        this.onInit = onInit;
    }

    public String getCss() {
        return css;
    }

    public void setCss(String css) {
        this.css = css;
    }

    public String getJs() {
        return js;
    }

    public void setJs(String js) {
        this.js = js;
    }

    public Collection<ReportSection> getSections() {
        return sections;
    }

    public void setSections(Collection<ReportSection> sections) {
        this.sections = sections;
    }

    public Collection<ReportFilter> getFilters() {
        return filters;
    }

    public void setFilters(Collection<ReportFilter> filters) {
        this.filters = filters;
    }

    public Collection<ReportFilterGroup> getFilterGroups() {
        return filterGroups;
    }

    public void setFilterGroups(Collection<ReportFilterGroup> filterGroups) {
        this.filterGroups = filterGroups;
    }
}
