import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import CategoryView from "./components/CategoryView";
import EmailList from "./components/EmailList";
import EmailDetail from "./components/EmailDetail";
import QuotationPreview from "./components/QuotationPreview";
import POPreview from "./components/POPreview";
import InvoicePreview from "./components/InvoicePreview";
function App() {

  const [category, setCategory] = useState(null);
  const [sub, setSub] = useState(null);
  const [emailId, setEmailId] = useState(null);
  const [quotationEmail, setQuotationEmail] = useState(null);
  const [poEmail, setPoEmail] = useState(null)
  const [invoiceEmail, setInvoiceEmail] = useState(null)
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
        background: "#a0a0ab"
      }}>

        {!category && <Dashboard onSelectCategory={setCategory} />}

        {category && !sub &&
          <CategoryView
            category={category}
            onSelectSub={setSub}
            goBack={() => setCategory(null)}
          />
        }

        {category && sub && !emailId && 
          <EmailList
            category={category}
            sub={sub}
            goBack={() => setSub(null)}
            onOpenEmail={setEmailId}
          />
        }

        {emailId && !quotationEmail && !poEmail && !invoiceEmail &&
          <EmailDetail
            emailId={emailId}
            goBack={() => setEmailId(null)}
            onCreateQuotation={(id)=>{
              setQuotationEmail(id)
            }}
            onCreatePO={(id)=>{

              setPoEmail(id)
            }}
            onCreateInvoice={(id)=>{

              setInvoiceEmail(id)
            }}
          />
        }


        {quotationEmail &&
          <QuotationPreview
            emailId={quotationEmail}
            goBack={() => setQuotationEmail(null)}
          />
        }


        {poEmail &&
          <POPreview
            emailId={poEmail}
            goBack={() => setPoEmail(null)}
          />
        }


        {invoiceEmail &&
          <InvoicePreview
            emailId={invoiceEmail}
            goBack={() => setInvoiceEmail(null)}
          />
        }

      </div>

    </div>

  )
}

export default App