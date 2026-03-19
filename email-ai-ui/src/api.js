import axios from "axios";

const API = axios.create({
  baseURL: "http://115.187.22.224:8182"
});

export const getCategories = () => API.get("/api/email/categories");

export const getSubCategories = (category) =>
  API.get(`/api/email/category/${category}`);

export const getEmails = (category, sub) =>
  API.get(`/api/email/category/${category}/${sub}`);

export const getEmailDetail = (id) =>
  axios.get(`http://115.187.22.224:8182/api/email/detail/${id}`)

export const createQuotation = (id) =>
  axios.get(`http://115.187.22.224:8182/api/create-quotation/${id}`)

export const createPO = (id) =>
  axios.get(`http://115.187.22.224:8182/api/create-po/${id}`)

export const createInvoice = (id) =>
  axios.get(`http://115.187.22.224:8182/api/create-invoice/${id}`)