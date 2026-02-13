import { useState, useEffect } from "react";
import "./AdminPage.css";

export default function AdminPage() {
  
  const [dailyLimit, setDailyLimit] = useState("");
  const [txnLimit, setTxnLimit] = useState("");
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState("");
  const [balance, setBalance] = useState(null);

  const [beneficiaries, setBeneficiaries] = useState([]);

  const [amount, setAmount] = useState("");
  const [operation, setOperation] = useState("credit");

  /* =======================
     FETCH CUSTOMERS
  ======================= */
  useEffect(() => {
    fetch("/api/admin/customers", {
      method: "GET",
      headers: { Authorization: "Basic " + btoa("admin:pass") },
    })
      .then(res => res.json())
      .then(data => setCustomers(data));
  }, []);

  /* =======================
     LOAD CUSTOMER DETAILS
  ======================= */
  const loadCustomer = async (customerId) => {
    setSelectedCustomer(customerId);

    const res = await fetch(
      `/api/admin/customer/${customerId}`,
      {  method: "GET",
         headers: { Authorization: "Basic " + btoa("admin:pass") } }
    );
    const data = await res.json();

    setBalance(data.balance);
    setBeneficiaries(data.beneficiaries);
  };

  /* =======================
     CREDIT / DEBIT
  ======================= */
  const updateBalance = async () => {
    await fetch("/api/admin/wallet", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Basic " + btoa("admin:pass"),
      },
      body: JSON.stringify({
        customer_id: selectedCustomer,
        amount: Number(amount),
        type: operation,
      }),
    });

    alert("Balance updated");
    loadCustomer(selectedCustomer);
    setAmount("");
  };

  /* =======================
   DELETE BENEFICIARY
======================= */
const deleteBeneficiary = async (beneficiaryId) => {
  const confirmDelete = window.confirm(
    "Are you sure you want to delete this beneficiary?"
  );
  if (!confirmDelete) return;

  await fetch(
    `/api/admin/beneficiary/${beneficiaryId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: "Basic " + btoa("admin:pass"),
      },
    }
  );

  alert(" Beneficiary deleted");
  loadCustomer(selectedCustomer); // refresh list
};


  /* =======================
     EXISTING FUNCTIONS
  ======================= */
  const uploadFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    await fetch("/api/admin/upload", {
      method: "POST",
      headers: { Authorization: "Basic " + btoa("admin:pass") },
      body: form,
    });

    alert("File uploaded");
  };

  const saveLimits = async () => {
    await fetch("/api/admin/limits", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Basic " + btoa("admin:pass"),
      },
      body: JSON.stringify({
        daily_limit: Number(dailyLimit),
        per_transaction_limit: Number(txnLimit),
      }),
    });

    alert(" Limits updated");
    setDailyLimit("");
    setTxnLimit("");
  };

  return (
    <div className="admin-container">
      <h2 className="admin-title">🏦 Admin Control Panel</h2>

      {/* Upload */}
      <div className="admin-card">
        <h3>📄 Upload Sanctions / Rules</h3>
        <input type="file" onChange={uploadFile} />
      </div>

      {/* Limits */}
      <div className="admin-card">
        <h3>💰 Transfer Limits</h3>

        <div className="input-group">
          <label>Daily Limit</label>
          <input
            type="number"
            value={dailyLimit}
            onChange={(e) => setDailyLimit(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Per Transaction</label>
          <input
            type="number"
            value={txnLimit}
            onChange={(e) => setTxnLimit(e.target.value)}
          />
        </div>

        <button className="save-btn" onClick={saveLimits}>Save</button>
      </div>

      {/* CUSTOMER MANAGEMENT */}
      <div className="admin-card">
        <h3>👤 Customer Management</h3>

        <select onChange={(e) => loadCustomer(e.target.value)}>
          <option>Select Customer</option>
          {customers.map(c => (
            <option key={c.user_id} value={c.user_id}>{c.user_id}</option>
          ))}
        </select>

        {balance !== null && (
          <p className="balance">Balance: ₹{balance}</p>
        )}
      </div>

      {/* BENEFICIARIES */}
      {/* BENEFICIARIES */}
{beneficiaries.length > 0 && (
  <div className="admin-card">
    <h3>🏦 Beneficiaries</h3>
    <ul className="list">
      {beneficiaries.map(b => (
        <li key={b.id} className="beneficiary-row">
          <span>
            {b.name} — {b.bank}
          </span>

          <button
            className="delete-btn"
            onClick={() => deleteBeneficiary(b.id)}
          >
            ❌
          </button>
        </li>
      ))}
    </ul>
  </div>
)}


      {/* CREDIT / DEBIT */}
      {selectedCustomer && (
        <div className="admin-card">
          <h3>➕➖ Credit / Debit</h3>

          <select onChange={(e) => setOperation(e.target.value)}>
            <option value="credit">Credit</option>
            <option value="debit">Debit</option>
          </select>

          <input 
            type="number"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />

          <button className="save-btn" onClick={updateBalance}>
            Execute
          </button>
        </div>
      )}
    </div>
  );
}
