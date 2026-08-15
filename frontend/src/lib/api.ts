export const API_BASE_URL = "http://localhost:8000/api";

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // Read token from localStorage
  let token = null;
  if (typeof window !== "undefined") {
    token = localStorage.getItem("access_token");
  }

  // Set up headers
  const headers = new Headers(options.headers || {});
  
  // Always include auth token if available
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  // If the body is JSON, set Content-Type
  // (Don't set it for FormData so the browser can automatically set the boundary)
  if (options.body && typeof options.body === "string" && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle Unauthorized responses
  if (response.status === 401 && typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  }

  return response;
}
