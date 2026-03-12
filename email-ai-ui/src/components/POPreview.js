import React, { useEffect, useState } from "react"
import { createPO } from "../api"
import Loading from "./Loading"

function POPreview({ emailId, goBack }) {

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {

    const fetch = async () => {

      const res = await createPO(emailId)

      setData(res.data.po)

      setLoading(false)
    }

    fetch()

  }, [emailId])

  if (loading) return <Loading />

  const supplier = data.supplier || {}
  const items = data.line_items || []

  return (

    <div>

      <button onClick={goBack}>← Back</button>

      <h2>Purchase Order Preview</h2>

      <h3>Supplier</h3>

      <p><b>Company:</b> {supplier.company}</p>
      <p><b>Email:</b> {supplier.email}</p>
      <p><b>Contact:</b> {supplier.contact}</p>

      <h3>Items</h3>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>Product Code</th>
            <th>Description</th>
            <th>Qty</th>
          </tr>
        </thead>

        <tbody>

          {items.map((item, i) => (

            <tr key={i}>

              <td>{item.product_code}</td>
              <td>{item.item_desc}</td>
              <td>{item.qty}</td>

            </tr>

          ))}

        </tbody>

      </table>

      <br/>

      <button style={{background:"#2563eb",color:"white",padding:"10px"}}>
        Generate PO
      </button>

    </div>
  )
}

export default POPreview