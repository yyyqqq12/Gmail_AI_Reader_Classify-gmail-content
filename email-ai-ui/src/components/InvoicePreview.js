import React, { useEffect, useState } from "react"
import { createInvoice } from "../api"
import Loading from "./Loading"

function InvoicePreview({ emailId, goBack }) {

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {

    const fetch = async () => {

      const res = await createInvoice(emailId)

      setData(res.data.invoice)

      setLoading(false)
    }

    fetch()

  }, [emailId])

  if (loading) return <Loading />

  const buyer = data.buyer || {}
  const items = data.line_items || []

  return (

    <div>

      <button onClick={goBack}>← Back</button>

      <h2>Invoice Preview</h2>

      <p><b>Buyer:</b> {buyer.name}</p>
      <p><b>Email:</b> {buyer.email}</p>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>Description</th>
            <th>Qty</th>
            <th>Unit Price</th>
          </tr>
        </thead>

        <tbody>

          {items.map((item, i) => (

            <tr key={i}>
              <td>{item.item_desc}</td>
              <td>{item.qty}</td>
              <td>{item.unit_price}</td>
            </tr>

          ))}

        </tbody>

      </table>

      <br/>

      <button style={{background:"#16a34a",color:"white",padding:"10px"}}>
        Generate Invoice
      </button>

    </div>
  )
}

export default InvoicePreview