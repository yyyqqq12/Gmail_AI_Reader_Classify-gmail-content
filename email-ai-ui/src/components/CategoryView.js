import React, { useEffect, useState } from "react";
import { getSubCategories } from "../api";
import Loading from "./Loading";

function CategoryView({ category, onSelectSub, goBack }) {

  const [subs, setSubs] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    setLoading(true);

    getSubCategories(category).then((res) => {
      setSubs(res.data);
      setLoading(false);
    });

  }, [category]);

  if (loading) {
    return <Loading />;
  }

  return (
    <div>

      {/* BACK BUTTON */}
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

      <h2>{category}</h2>

      {Object.keys(subs).map((sub) => (
        <div
          key={sub}
          style={{
            border: "1px solid gray",
            margin: "10px",
            padding: "10px",
            cursor: "pointer",
          }}
          onClick={() => onSelectSub(sub)}
        >
          {sub} ({subs[sub]})
        </div>
      ))}

    </div>
  );
}

export default CategoryView;