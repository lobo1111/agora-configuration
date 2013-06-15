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
@Table(name = "report_section")
@XmlRootElement
public class ReportSection implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @JoinColumn(name = "report_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private Report report;
    @JoinColumn(name = "parent_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private ReportSection parent;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "parent")
    private Collection<ReportSection> children;
    @Basic(optional = true)
    @Column(name = "query")
    private String query;
    @Basic(optional = false)
    @Column(name = "section_order")
    private String sectionOrder;
    @Basic(optional = false)
    @Column(name = "show_header")
    private boolean showHeader;
    @Basic(optional = true)
    @Column(name = "title")
    private String title;
    @Basic(optional = false)
    @Column(name = "show_title")
    private boolean showTitle;
    @Basic(optional = true)
    @Column(name = "title_style")
    private String titleStyle;
    @Basic(optional = true)
    @Column(name = "table_style")
    private String tableStyle;
    @Basic(optional = true)
    @Column(name = "row_style")
    private String rowStyle;
    @Column(name = "native_query")
    private boolean nativeQuery;
    @OneToMany(cascade = CascadeType.ALL, mappedBy = "section")
    private Collection<ReportSectionAttribute> attributes = new ArrayList<>();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Report getReport() {
        return report;
    }

    public void setReport(Report report) {
        this.report = report;
    }

    public ReportSection getParent() {
        return parent;
    }

    public void setParent(ReportSection parent) {
        this.parent = parent;
    }

    public Collection<ReportSection> getChildren() {
        return children;
    }

    public void setChildren(Collection<ReportSection> children) {
        this.children = children;
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public String getTableStyle() {
        return tableStyle;
    }

    public void setTableStyle(String tableStyle) {
        this.tableStyle = tableStyle;
    }

    public String getSectionOrder() {
        return sectionOrder;
    }

    public void setSectionOrder(String sectionOrder) {
        this.sectionOrder = sectionOrder;
    }

    public boolean isShowHeader() {
        return showHeader;
    }

    public void setShowHeader(boolean showHeader) {
        this.showHeader = showHeader;
    }

    public String getRowStyle() {
        return rowStyle;
    }

    public void setRowStyle(String rowStyle) {
        this.rowStyle = rowStyle;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public boolean isShowTitle() {
        return showTitle;
    }

    public void setShowTitle(boolean showTitle) {
        this.showTitle = showTitle;
    }

    public String getTitleStyle() {
        return titleStyle;
    }

    public void setTitleStyle(String titleStyle) {
        this.titleStyle = titleStyle;
    }

    public boolean isNativeQuery() {
        return nativeQuery;
    }

    public void setNativeQuery(boolean nativeQuery) {
        this.nativeQuery = nativeQuery;
    }

    public Collection<ReportSectionAttribute> getAttributes() {
        return attributes;
    }

    public void setAttributes(Collection<ReportSectionAttribute> attributes) {
        this.attributes = attributes;
    }
}
