import React, { useEffect, useState } from "react"
import { getEmailDetail } from "../api"
import Loading from "./Loading"


function EmailDetail({
    emailId,
    goBack,
    onCreateQuotation,
    onCreatePO,
    onCreateInvoice
    }) {

    const [email, setEmail] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {

        const fetch = async () => {

        try {
            const res = await getEmailDetail(emailId)
            setEmail(res.data)
        } catch (err) {
            console.error(err)
        }

        setLoading(false)
        }

        fetch()

    }, [emailId])

    if (loading) return <Loading />

    // ----- actions -----

    const createQuotation = () => {
        onCreateQuotation(emailId)
        }

    const createPO = () => {
        onCreatePO(emailId)
        }

    const createInvoice = () => {
        onCreateInvoice(emailId)
        }



  return (

    <div>

      {/* Back button */}
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

      <h2>{email.subject}</h2>

      <p><b>Sender:</b> {email.sender}</p>
      <p><b>Date:</b> {email.date}</p>

      {/* ACTION BUTTONS */}

      <div style={{
        marginTop: "20px",
        marginBottom: "20px",
        display: "flex",
        gap: "10px",
        flexWrap: "wrap"
      }}>

        <button style={btnBlue} onClick={createQuotation}>
          Create Quotation
        </button>

        <button style={btnGreen} onClick={createPO}>
          Create Purchase Order
        </button>

        <button style={btnPurple} onClick={createInvoice}>
          Create Invoice
        </button>


      </div>

      {/* Email Body */}

      <div
        style={{
          padding: "20px",
          background: "white",
          borderRadius: "10px",
          whiteSpace: "pre-wrap",
          boxShadow: "0 4px 10px rgba(0,0,0,0.08)"
        }}
      >
        {email.body}
      </div>

    </div>
  )
}

const btnBlue = {
  padding: "10px 15px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
}

const btnGreen = {
  padding: "10px 15px",
  background: "#16a34a",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
}

const btnPurple = {
  padding: "10px 15px",
  background: "#7c3aed",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
}



export default EmailDetail