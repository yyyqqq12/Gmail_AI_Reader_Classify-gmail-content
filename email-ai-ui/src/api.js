import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getCategories = () => API.get("/api/email/categories");

export const getSubCategories = (category) =>
  API.get(`/api/email/category/${category}`);

export const getEmails = (category, sub) =>
  API.get(`/api/email/category/${category}/${sub}`);

export const getEmailDetail = (id) =>
  axios.get(`http://localhost:8000/api/email/detail/${id}`)

export const createQuotation = (id) =>
  axios.get(`http://localhost:8000/api/create-quotation/${id}`)

export const createPO = (id) =>
  axios.get(`http://localhost:8000/api/create-po/${id}`)

export const createInvoice = (id) =>
  axios.get(`http://localhost:8000/api/create-invoice/${id}`)