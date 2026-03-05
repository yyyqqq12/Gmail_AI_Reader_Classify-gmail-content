import React from "react";

function Loading() {

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "200px",
      flexDirection: "column"
    }}>
      
      <div style={{
        border: "6px solid #e2e8f0",
        borderTop: "6px solid #2563eb",
        borderRadius: "50%",
        width: "40px",
        height: "40px",
        animation: "spin 1s linear infinite"
      }} />

      <p style={{marginTop: "30px", color:"#64748b"}}>
        Loading emails...
      </p>

      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>

    </div>
  );
}

export default Loading;