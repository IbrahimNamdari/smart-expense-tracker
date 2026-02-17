import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // آدرس FastAPI تو
});

export const getExpenses = () => api.get("/expenses/");
export const getSummary = () => api.get("/expenses/summary/");
export const addExpenseAI = (text: string) => api.post(`/expenses/ai/?text_input=${text}`);
