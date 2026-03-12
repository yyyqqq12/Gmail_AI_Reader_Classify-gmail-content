import React, { useEffect, useState } from "react";
import { getEmails } from "../api";
import Loading from "./Loading";

function EmailList({ category, sub, goBack, onOpenEmail }) {

  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const fetchEmails = async () => {

      setLoading(true);

      try {
        const res = await getEmails(category, sub);
        setEmails(res.data);
      } catch (error) {
        console.error("Error fetching emails:", error);
      }

      setLoading(false);
    };

    fetchEmails();

  }, [category, sub]);

  // 🔄 Show loading spinner
  if (loading) {
    return <Loading />;
  }

  return (
    <div>

      {/* Back Button */}
      <button
        onClick={goBack}
        style={{
          padding: "8px 15px",
          background: "#e2e8f0",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          marginBottom: "20px"
        }}
      >
        ← Back
      </button>

      <h2 style={{ marginBottom: "20px" }}>
        {category} → {sub}
      </h2>

      <div style={{
        background: "white",
        borderRadius: "10px",
        boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
        
      }}>

        <div style={{
          maxHeight: "70vh",
          overflowY: "auto"
        }}>
      

        <table
          style={{
            width: "100%",
            borderCollapse: "collapse"
          }}
        >
        
          <thead style={{ background: "#f1f5f9" }}>
            <tr>
              <th style={thStyle}>Subject</th>
              <th style={thStyle}>Sender</th>
              <th style={thStyle}>Date</th>
            </tr>
          </thead>

          <tbody>

            {emails.length === 0 ? (
              <tr>
                <td colSpan="3" style={{
                  textAlign: "center",
                  padding: "20px",
                  color: "#64748b"
                }}>
                  No emails found
                </td>
              </tr>
            ) : (
              emails.map((e, i) => (
                <tr
                  key={i}
                  onClick={() => onOpenEmail(e.id)}
                  style={{
                    borderTop: "1px solid #e2e8f0",
                    cursor: "pointer"
                  }}
                  onMouseEnter={e => e.currentTarget.style.background="#f8fafc"}
                  onMouseLeave={e => e.currentTarget.style.background="white"}
                >
                  <td style={tdStyle}>{e.subject}</td>
                  <td style={tdStyle}>{e.sender}</td>
                  <td style={tdStyle}>{e.date}</td>
                </tr>
              ))
            )}

          </tbody>
        </table>
      </div>
      </div>

    </div>
  );
}

// Simple reusable styles
const thStyle = {
  padding: "12px",
  textAlign: "left",
  fontWeight: "600",
  position: "sticky",
  top: 0,
  background: "#f1f5f9",
  zIndex: 1
};

const tdStyle = {
  padding: "12px"
};

export default EmailList;