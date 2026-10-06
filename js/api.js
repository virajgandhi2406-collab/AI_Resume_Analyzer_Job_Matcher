/**
 * ResumePulse AI - Unified API Client Service
 */

class ApiService {
  constructor() {
    const saved = localStorage.getItem("resumepulse_api_base");
    if (saved) {
      this.baseUrl = saved;
    } else if (
      window.location.protocol.startsWith("http") &&
      window.location.hostname !== "localhost" &&
      window.location.hostname !== "127.0.0.1"
    ) {
      this.baseUrl = `${window.location.origin}/api/v1`;
    } else {
      this.baseUrl = "http://localhost:8000/api/v1";
    }
  }

  setBaseUrl(url) {
    this.baseUrl = url.replace(/\/$/, "");
    if (!this.baseUrl.endsWith("/api/v1")) {
      this.baseUrl += "/api/v1";
    }
    localStorage.setItem("resumepulse_api_base", this.baseUrl);
  }

  async _request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {};

    if (!(options.body instanceof FormData)) {
      defaultHeaders["Content-Type"] = "application/json";
    }

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        let errMessage = `HTTP ${response.status} ${response.statusText}`;
        try {
          const errData = await response.json();
          if (errData.detail) {
            errMessage = typeof errData.detail === "string" ? errData.detail : JSON.stringify(errData.detail);
          }
        } catch (e) {
          // fallback to status text
        }
        throw new Error(errMessage);
      }
      return await response.json();
    } catch (err) {
      console.error(`API Error on [${url}]:`, err);
      throw err;
    }
  }

  // Dashboard & Analytics
  async getDashboardSummary() {
    return this._request("/analytics/dashboard-summary");
  }

  // Resumes & ATS
  async uploadResume(file, provider = "auto") {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("ai_provider", provider);
    return this._request("/resumes/upload", {
      method: "POST",
      body: formData,
    });
  }

  async analyzeResumeText(rawText, targetTitle = "", provider = "auto") {
    return this._request("/resumes/analyze-text", {
      method: "POST",
      body: JSON.stringify({
        raw_text: rawText,
        target_job_title: targetTitle,
        ai_provider: provider,
      }),
    });
  }

  async getAllResumes() {
    return this._request("/resumes/");
  }

  async getResume(id) {
    return this._request(`/resumes/${id}`);
  }

  getResumePdfUrl(id) {
    return `${this.baseUrl}/resumes/${id}/export-pdf`;
  }

  // Jobs
  async getJobs(params = {}) {
    const query = new URLSearchParams();
    if (params.search) query.append("search", params.search);
    if (params.location) query.append("location", params.location);
    if (params.workplace_type) query.append("workplace_type", params.workplace_type);
    if (params.experience_level) query.append("experience_level", params.experience_level);
    
    const qs = query.toString() ? `?${query.toString()}` : "";
    return this._request(`/jobs/${qs}`);
  }

  async createJob(jobData) {
    return this._request("/jobs/", {
      method: "POST",
      body: JSON.stringify(jobData),
    });
  }

  // Match Engine
  async matchSingle(matchPayload) {
    return this._request("/match/match-single", {
      method: "POST",
      body: JSON.stringify(matchPayload),
    });
  }

  async batchMatchAll(resumeId) {
    return this._request(`/match/batch-match/${resumeId}`, {
      method: "POST",
    });
  }

  // AI Copilot Tools
  async generateCoverLetter(payload) {
    return this._request("/ai-tools/cover-letter", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  async optimizeBullets(bulletPoints, targetRole = "Software Engineer", provider = "auto") {
    return this._request("/ai-tools/optimize-bullets", {
      method: "POST",
      body: JSON.stringify({
        bullet_points: bulletPoints,
        target_role: targetRole,
        ai_provider: provider,
      }),
    });
  }

  async generateInterviewPrep(payload) {
    return this._request("/ai-tools/interview-prep", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  async generateCareerRoadmap(targetRole, currentSkills = []) {
    return this._request("/ai-tools/career-roadmap", {
      method: "POST",
      body: JSON.stringify({
        target_role: targetRole,
        current_skills: currentSkills,
      }),
    });
  }

  // Tracker Kanban
  async getApplications(status = null) {
    const qs = status ? `?status_filter=${status}` : "";
    return this._request(`/tracker/${qs}`);
  }

  async createApplication(appData) {
    return this._request("/tracker/", {
      method: "POST",
      body: JSON.stringify(appData),
    });
  }

  async updateApplication(id, appData) {
    return this._request(`/tracker/${id}`, {
      method: "PUT",
      body: JSON.stringify(appData),
    });
  }

  async deleteApplication(id) {
    return this._request(`/tracker/${id}`, {
      method: "DELETE",
    });
  }
}

const api = new ApiService();
