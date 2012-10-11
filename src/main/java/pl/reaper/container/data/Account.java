package pl.reaper.container.data;

import java.io.Serializable;
import java.util.Collection;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

@Entity
@Table(name = "account")
@XmlRootElement
public class Account implements Serializable {

    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "id")
    private Integer id;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 150)
    @Column(name = "name")
    private String name;
    @Basic(optional = false)
    @NotNull
    @Size(min = 1, max = 150)
    @Column(name = "number")
    private String number;
    @Basic(optional = false)
    @Column(name = "type")
    private String type;
    @OneToMany(mappedBy = "parrentAccount")
    private Collection<Account> childAccounts;
    @JoinColumn(name = "bank_id", referencedColumnName = "id")
    @ManyToOne
    private Bank bank;
    @JoinColumn(name = "parrent_account_id", referencedColumnName = "id")
    @ManyToOne
    private Account parrentAccount;
    @ManyToMany
    @JoinTable(
        name = "possession_account", joinColumns =
    @JoinColumn(name = "account_id", referencedColumnName = "id"),
    inverseJoinColumns =
    @JoinColumn(name = "possession_id", referencedColumnName = "id"))
    private Collection<Possession> possessions;

    public Account() {
    }

    public Account(Integer id) {
        this.id = id;
    }

    public Account(Integer id, String name, String number) {
        this.id = id;
        this.name = name;
        this.number = number;
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

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    @XmlTransient
    public Collection<Account> getChildAccounts() {
        return childAccounts;
    }

    public void setChildAccounts(Collection<Account> childAccounts) {
        this.childAccounts = childAccounts;
    }

    public Account getParrentAccount() {
        return parrentAccount;
    }

    public void setParrentAccount(Account parrentAccount) {
        this.parrentAccount = parrentAccount;
    }

    public Collection<Possession> getPossessions() {
        return possessions;
    }

    public void setPossessions(Collection<Possession> possessions) {
        this.possessions = possessions;
    }

    public Bank getBank() {
        return bank;
    }

    public void setBank(Bank bank) {
        this.bank = bank;
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
        if (!(object instanceof Account)) {
            return false;
        }
        Account other = (Account) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "pl.reaper.container.data.Account[ id=" + id + " ]";
    }
}
