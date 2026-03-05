import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getCategories = () => API.get("/api/email/categories");

export const getSubCategories = (category) =>
  API.get(`/api/email/category/${category}`);

export const getEmails = (category, sub) =>
  API.get(`/api/email/category/${category}/${sub}`);