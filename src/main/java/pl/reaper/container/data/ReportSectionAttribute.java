package pl.reaper.container.data;

import java.io.Serializable;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.xml.bind.annotation.XmlRootElement;

@Entity
@Table(name = "report_section_attribute")
@XmlRootElement
public class ReportSectionAttribute implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @Column(name = "header_style")
    private String headerStyle;
    @Basic(optional = false)
    @Column(name = "column_style")
    private String columnStyle;
    @JoinColumn(name = "section_id", referencedColumnName = "id")
    @ManyToOne(optional = false)
    private ReportSection section;
    @Basic(optional = false)
    @Column(name = "attribute")
    private String attribute;
    @Basic(optional = false)
    @Column(name = "attribute_alias")
    private String attributeAlias;
    @Basic(optional = false)
    @Column(name = "attribute_order")
    private String attributeOrder;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getHeaderStyle() {
        return headerStyle;
    }

    public void setHeaderStyle(String headerStyle) {
        this.headerStyle = headerStyle;
    }

    public String getColumnStyle() {
        return columnStyle;
    }

    public void setColumnStyle(String columnStyle) {
        this.columnStyle = columnStyle;
    }

    public ReportSection getSection() {
        return section;
    }

    public void setSection(ReportSection section) {
        this.section = section;
    }

    public String getAttribute() {
        return attribute;
    }

    public void setAttribute(String attribute) {
        this.attribute = attribute;
    }

    public String getAttributeAlias() {
        return attributeAlias;
    }

    public void setAttributeAlias(String attributeAlias) {
        this.attributeAlias = attributeAlias;
    }

    public String getAttributeOrder() {
        return attributeOrder;
    }

    public void setAttributeOrder(String attributeOrder) {
        this.attributeOrder = attributeOrder;
    }
}
