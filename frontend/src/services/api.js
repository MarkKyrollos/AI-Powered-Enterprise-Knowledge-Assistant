import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: API_BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  register: (email, password) =>
    api.post("/api/auth/register", { email, password }),
  login: (email, password) => {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);
    return api.post("/api/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },
  me: () => api.get("/api/auth/me"),
};

export const documentsApi = {
  upload: (file, onUploadProgress) => {
    const form = new FormData();
    form.append("file", file);
    return api.post("/api/documents/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress,
    });
  },
  list: () => api.get("/api/documents"),
  remove: (id) => api.delete(`/api/documents/${id}`),
};

export const chatApi = {
  ask: (question, documentIds) =>
    api.post("/api/chat", { question, document_ids: documentIds || null }),
  history: () => api.get("/api/chat/history"),
  clearHistory: () => api.delete("/api/chat/history"),
};

export default api;
