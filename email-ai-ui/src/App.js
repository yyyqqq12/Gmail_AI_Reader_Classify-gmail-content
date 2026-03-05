import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import CategoryView from "./components/CategoryView";
import EmailList from "./components/EmailList";

function App() {

  const [category, setCategory] = useState(null);
  const [sub, setSub] = useState(null);

  return (

    <div style={{ display: "flex", height: "100vh" }}>

      <div style={{
        width: "250px",
        background: "#1e293b",
        color: "white",
        padding: "20px"
      }}>

        <h2>Email AI</h2>

        <button
          onClick={() => {
            setCategory(null)
            setSub(null)
          }}
          style={{
            marginTop: "20px",
            width: "100%",
            padding: "10px",
            background: "#334155",
            color: "white",
            border: "none",
            cursor: "pointer"
          }}
        >
          Dashboard
        </button>

      </div>

      <div style={{
        flex: 1,
        padding: "30px",
        background: "#f1f5f9"
      }}>

        {!category && <Dashboard onSelectCategory={setCategory} />}

        {category && !sub &&
          <CategoryView
            category={category}
            onSelectSub={setSub}
            goBack={() => setCategory(null)}
          />
        }

        {category && sub &&
          <EmailList
            category={category}
            sub={sub}
            goBack={() => setSub(null)}
          />
        }

      </div>

    </div>

  )
}

export default App