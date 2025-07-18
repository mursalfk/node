import React, { useState } from 'react';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchEmails = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch("http://localhost:5000/api/fetch-emails", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          date_from: dateFrom || null,
          date_to: dateTo || null,
        }),
      });
      const data = await response.json();
      if (data.success) {
        setEmails(data.emails);
      } else {
        setError(data.error || "Unknown error");
      }
    } catch (err) {
      setError("❌ Network Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>📩 Project NODE Dashboard</h1>
      <input type="email" placeholder="Gmail" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="App Password" value={password} onChange={e => setPassword(e.target.value)} />
      <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)} />
      <input type="date" value={dateTo} onChange={e => setDateTo(e.target.value)} />
      <button onClick={fetchEmails}>Fetch Emails</button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {emails.map((mail, idx) => (
          <li key={idx}>
            <strong>{mail.subject}</strong> [{mail.date}]
            <p>{mail.body}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
