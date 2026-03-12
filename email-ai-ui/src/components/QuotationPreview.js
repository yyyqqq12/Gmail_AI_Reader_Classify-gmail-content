import React, { useEffect, useState } from "react"
import { createQuotation } from "../api"
import Loading from "./Loading"

function QuotationPreview({ emailId, goBack }) {

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {

    const fetch = async () => {

      const res = await createQuotation(emailId)

      setData(res.data.quotation)

      setLoading(false)
    }

    fetch()

  }, [emailId])

  if (loading) return <Loading />

  const buyer = data.buyer || {}
  const items = data.line_items || []

  return (

    <div>

      <button onClick={goBack}>
        ← Back
      </button>

      <h2>Quotation Preview</h2>

      <h3>Buyer</h3>

      <p><b>Company:</b> {buyer.buyer_company_name}</p>
      <p><b>Name:</b> {buyer.buyer_name}</p>
      <p><b>Email:</b> {buyer.buyer_email}</p>
      <p><b>Contact:</b> {buyer.buyer_contact}</p>

      <h3>Items</h3>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>Product Code</th>
            <th>Description</th>
            <th>Qty</th>
            <th>Unit Price</th>
          </tr>
        </thead>

        <tbody>

          {items.map((item, i) => (

            <tr key={i}>

              <td>{item.product_code}</td>
              <td>{item.item_desc}</td>
              <td>{item.qty}</td>
              <td>{item.unit_price_myr}</td>

            </tr>

          ))}

        </tbody>

      </table>

      <br />

      <button style={{background:"#2563eb",color:"white",padding:"10px"}}>
        Generate Quotation
      </button>

    </div>
  )
}

export default QuotationPreview