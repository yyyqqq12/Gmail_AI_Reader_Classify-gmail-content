import React, { useEffect, useState } from "react";
import { getCategories } from "../api";
import axios from "axios";
import Loading from "./Loading";

function Dashboard({ onSelectCategory }) {

  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(false);

  // Load categories from database
  const loadCategories = async () => {

    setLoading(true);

    const res = await getCategories();

    setCategories(res.data);

    setLoading(false);
  };

  // Load emails from Gmail → save to DB
  const loadEmails = async () => {

    setLoading(true);

    await axios.get("http://localhost:8000/api/load-emails");

    await loadCategories();   // refresh categories after loading emails

    setLoading(false);
  };


  const reloadEmails = async () => {

    setLoading(true)

    await axios.get("http://localhost:8000/api/reload-emails")

    await loadCategories()

    setLoading(false)
  }

  useEffect(() => {
    loadCategories();
  }, []);

  if (loading) {
    return <Loading />;
  }

  return (
    <div>

      <h1>Email Dashboard</h1>

      {/* Load Gmail Button */}
      

      <button
        onClick={loadEmails}
        style={btnBlue}
      >
        Load New Emails
      </button>

      <button
        onClick={reloadEmails}
        style={btnRed}
      >
        Delete and Reload All Emails
      </button>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, 260px)",
          gap: "20px",
          marginTop: "20px"
        }}
      >

        {Object.keys(categories).map((cat) => (

          <div
            key={cat}
            onClick={() => onSelectCategory(cat)}
            style={{
              background: "white",
              borderRadius: "10px",
              padding: "15px",
              boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
              cursor: "pointer"
            }}
          >

            <h3>{cat}</h3>

            <p
              style={{
                fontSize: "24px",
                color: "#2563eb",
                wordBreak: "break-word"
              }}
            >
              {categories[cat]}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}
const btnBlue = {
  padding: "10px 30px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "6px",
  marginRight: "10px",
  marginBottom: "20px",
  cursor: "pointer"
};

const btnRed = {
  padding: "10px 30px",
  background: "#ef4444",
  color: "white",
  border: "none",
  borderRadius: "6px",
  marginBottom: "20px",
  cursor: "pointer"
};
export default Dashboard;