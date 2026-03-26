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
  API.get(`/api/email/detail/${id}`)

export const createQuotation = (id) =>
  API.get(`/api/create-quotation/${id}`)

export const createPO = (id) =>
  API.get(`/api/create-po/${id}`)

export const createInvoice = (id) =>
  API.get(`/api/create-invoice/${id}`)