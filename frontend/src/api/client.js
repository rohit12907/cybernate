// ======================================
// CYBERMATE API CLIENT
// ======================================

import axios from "axios";

// Backend URL
const API = axios.create({
  // Vite proxies /api to FastAPI. Override this for deployed environments.
  baseURL: import.meta.env.VITE_API_URL || "/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ======================================
// REQUEST INTERCEPTOR
// ======================================

API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("cybermate_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ======================================
// RESPONSE INTERCEPTOR
// ======================================

API.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);

    if (error.response?.status === 401) {
      localStorage.removeItem("cybermate_token");
    }

    return Promise.reject(error);
  }
);

// ======================================
// DASHBOARD APIs
// ======================================

export const getDashboardStats = async () => {
  const response = await API.get("/dashboard/stats");
  return response.data;
};

export const getThreats = async () => {
  const response = await API.get("/threats");
  return response.data;
};

export const getHealth = async () => {
  const response = await API.get("/health");
  return response.data;
};

export const ingestLog = async (log) => {
  const response = await API.post("/log", log);
  return response.data;
};

export async function reset() {
  const res = await fetch(
    "http://localhost:8000/api/reset",
    {
      method: "DELETE"
    }
  );

  if (!res.ok) {
    throw new Error("Reset failed");
  }

  return res.json();
}

export const sendAlert = async (alert) => {
  const response = await API.post("/alert/send", alert);
  return response.data;
};

export const getThreatById = async (id) => {
  const response = await API.get(`/threats/${id}`);
  return response.data;
};

export const getLiveFeed = async () => {
  const response = await API.get("/live-feed");
  return response.data;
};

export const getAlertHistory = async () => {
  const response = await API.get("/alerts");
  return response.data;
};

// ======================================
// URL ANALYZER
// ======================================

export const scanURL = async (url) => {
  const response = await API.post("/scan/url", {
    url,
  });

  return response.data;
};

// ======================================
// IP ANALYZER
// ======================================

export const scanIP = async (ip) => {
  const response = await API.post("/scan/ip", {
    ip,
  });

  return response.data;
};

// ======================================
// HASH ANALYZER
// ======================================

export const scanHash = async (hash) => {
  const response = await API.post("/scan/hash", {
    hash,
  });

  return response.data;
};

// ======================================
// CSV LOG ANALYSIS
// ======================================

export const uploadLogFile = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post(
    "/upload/logs",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

// ======================================
// FORENSIC IMAGE ANALYSIS
// ======================================

export const uploadImage = async (file) => {
  const formData = new FormData();

  formData.append("image", file);

  const response = await API.post(
    "/upload/image",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

// ======================================
// AUTH APIs
// ======================================

export const login = async (email, password) => {
  const response = await API.post("/auth/login", {
    email,
    password,
  });

  return response.data;
};

export const register = async (userData) => {
  const response = await API.post(
    "/auth/register",
    userData
  );

  return response.data;
};

// ======================================
// PIPELINE APIs
// ======================================

export const startSimulation = async () => {
  const response = await API.post(
    "/pipeline/start"
  );

  return response.data;
};

export const getPipelineStatus = async () => {
  const response = await API.get(
    "/pipeline/status"
  );

  return response.data;
};

// ======================================
// EXPORT INSTANCE
// ======================================

export default API;
