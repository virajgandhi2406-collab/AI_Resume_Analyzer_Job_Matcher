/**
 * ResumePulse AI - Main Application Controller
 */

const DEMO_RESUMES = {
  fullstack: `ALEX RIVERA
San Francisco, CA | alex.rivera@airesume.io | (555) 234-5678 | linkedin.com/in/alex-rivera-dev | github.com/alexrivera-tech

SUMMARY
Senior Full Stack Software Engineer with 6+ years of experience architecting high-throughput distributed systems, microservices, and modern responsive web applications. Proven track record of improving system uptime to 99.99% and accelerating developer deployment velocity by 45%.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, Go, SQL, HTML5, CSS3
Frameworks & Libraries: FastAPI, Django, React, Next.js, Node.js, Express, Tailwind CSS
Databases & Cache: PostgreSQL, MySQL, Redis, MongoDB, Elasticsearch
Cloud & DevOps: AWS (EC2, S3, RDS, Lambda), Docker, Kubernetes, GitHub Actions, Terraform, Nginx
Core Competencies: System Design, RESTful APIs, GraphQL, Microservices, CI/CD, Agile / Scrum

PROFESSIONAL EXPERIENCE
Senior Software Engineer | CloudScale Systems, San Francisco, CA | 2022 - Present
- Architected and deployed 18+ high-volume REST and GraphQL microservice APIs in FastAPI and Go, processing over 12 million requests per day with sub-50ms p99 latency.
- Spearheaded database migration from legacy monolithic MySQL to horizontally sharded PostgreSQL cluster, reducing query response times by 42%.
- Built and maintained real-time websocket synchronization engine in React and TypeScript for 85,000 active enterprise users.
- Automated end-to-end CI/CD testing pipelines with Docker and GitHub Actions, slashing release cycle duration from 4 hours to 12 minutes.

Full Stack Engineer | Apex Data Labs, Austin, TX | 2019 - 2022
- Developed scalable customer dashboard in React, Next.js, and Node.js, driving 35% growth in monthly user engagement.
- Implemented multi-tier Redis caching strategy that decreased AWS server compute infrastructure expenses by $4,500 monthly.
- Integrated Stripe billing and webhook processing system handling $2.5M in annual recurring subscription revenue with zero transaction failure.
- Mentored 4 junior engineers on clean code practices, unit testing coverage, and asynchronous Python architecture.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley | 2015 - 2019
Honors: Magna Cum Laude | GPA: 3.85`,

  data_science: `DR. MAYA LIN
Seattle, WA | maya.lin@ai-ml-expert.io | (555) 876-5432 | linkedin.com/in/maya-lin-ai | github.com/mayalin-ml

SUMMARY
Staff Machine Learning & NLP Engineer with 7+ years of expertise in Large Language Models (LLMs), RAG pipelines, Deep Learning, and production MLOps. Published researcher with 5 IEEE papers and experience scaling generative AI inference pipelines to 50M+ API requests.

TECHNICAL SKILLS
Machine Learning / AI: PyTorch, TensorFlow, Scikit-learn, Hugging Face Transformers, LangChain, LlamaIndex, vLLM, DeepSpeed
NLP & LLMs: RAG, Embeddings, Tokenization, BERT, GPT Fine-tuning, LoRA, Prompt Engineering, Semantic Search
Languages & Tools: Python, C++, SQL, Docker, Kubernetes, Ray, Triton Inference Server, MLflow, AWS SageMaker
Big Data & DBs: PostgreSQL, Pinecone, Qdrant, Milvus, Spark, Kafka

PROFESSIONAL EXPERIENCE
Lead AI / ML Research Engineer | Nexus AI Labs, Seattle, WA | 2021 - Present
- Designed and operationalized enterprise-grade Retrieval-Augmented Generation (RAG) platform using LangChain, Qdrant, and fine-tuned LLaMA-3 models, serving 50M+ queries monthly.
- Reduced LLM token inference latency by 68% through quantization (AWQ/GPTQ) and continuous batching on Triton Inference Server.
- Led team of 6 researchers fine-tuning domain-specific foundation models, beating benchmark accuracy by 14.5% over generic GPT-4.
- Implemented real-time hallucination evaluation framework that increased customer response trust score to 96.8%.

Machine Learning Engineer | DataCore Systems, Boston, MA | 2018 - 2021
- Developed predictive anomaly detection pipeline analyzing 2TB+ daily telemetric data streams with 99.4% precision.
- Built distributed training workflows on multi-node GPU clusters using PyTorch and Horovod, reducing model training time from 7 days to 18 hours.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence) | MIT | 2014 - 2018
M.S. in Applied Mathematics | Stanford University | 2012 - 2014`,

  junior: `JORDAN SMITH
Chicago, IL | jordan.smith@gmail.com | (555) 432-1098

OBJECTIVE
Passionate junior programmer seeking an entry level software role where I can contribute to projects and learn new skills.

SKILLS
HTML, CSS, JavaScript, basic Python, Git.

EXPERIENCE
Junior Web Intern | Local Digital Agency | 2023 - 2024
- Helped update company website pages.
- Worked on fixing simple CSS bugs and making buttons look better.
- Attended weekly standup meetings and learned about frontend development.

EDUCATION
Associate Degree in Information Technology | Community College | 2021 - 2023`
};

class AppController {
  constructor() {
    this.activeResume = null;
    this.activeJob = null;
    this.activeMatch = null;
    this.jobsList = [];
    this.currentJobFilter = "all";
    this.savedResumes = [];
  }

  async init() {
    this.bindEvents();
    await this.loadInitialData();
  }

  bindEvents() {
    // Nav Tab Switching
    document.querySelectorAll(".nav-item").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tab = btn.getAttribute("data-tab");
        this.switchTab(tab);
      });
    });

    // Subtab switching (Analyzer)
    document.querySelectorAll(".subtab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".subtab-btn").forEach((b) => b.classList.remove("active"));
        document.querySelectorAll(".subtab-pane").forEach((p) => p.classList.remove("active"));
        btn.classList.add("active");
        const target = btn.getAttribute("data-subtab");
        const targetPane = document.getElementById(`subtab-${target}`);
        if (targetPane) targetPane.classList.add("active");
      });
    });

    // File Drag & Drop
    const dropZone = document.getElementById("resumeDropZone");
    const fileInput = document.getElementById("resumeFileInput");

    if (dropZone && fileInput) {
      dropZone.addEventListener("click", (e) => {
        if (e.target !== fileInput) fileInput.click();
      });

      dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
      });

      dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
      });

      dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        if (e.dataTransfer.files.length) {
          this.handleFileUpload(e.dataTransfer.files[0]);
        }
      });

      fileInput.addEventListener("change", (e) => {
        if (e.target.files.length) {
          this.handleFileUpload(e.target.files[0]);
        }
      });
    }

    // Quick demo button
    const btnQuickDemo = document.getElementById("btnQuickDemo");
    if (btnQuickDemo) {
      btnQuickDemo.addEventListener("click", () => {
        this.loadSampleResume("fullstack");
      });
    }

    // Settings Modal
    const btnSettings = document.getElementById("btnSettingsModal");
    const settingsModal = document.getElementById("settingsModal");
    if (btnSettings && settingsModal) {
      btnSettings.addEventListener("click", () => settingsModal.showModal());
    }

    // AI Provider Selector Sync
    const provSelect = document.getElementById("providerSelector");
    if (provSelect) {
      provSelect.value = localStorage.getItem("resumepulse_ai_provider") || "auto";
      provSelect.addEventListener("change", (e) => {
        localStorage.setItem("resumepulse_ai_provider", e.target.value);
        this.showToast(`AI Engine set to: ${e.target.options[e.target.selectedIndex].text}`, "success");
      });
    }
  }

  getSelectedAIProvider() {
    return document.getElementById("providerSelector")?.value || "auto";
  }

  switchTab(tabId, subAction = null) {
    document.querySelectorAll(".nav-item").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });

    document.querySelectorAll(".tab-pane").forEach((pane) => {
      pane.classList.toggle("active", pane.id === `tab-${tabId}`);
    });

    window.scrollTo({ top: 0, behavior: "smooth" });

    // Handle sub-actions (e.g. switch copilot subtool)
    if (tabId === "copilot" && subAction) {
      const toolBtn = document.querySelector(`.copilot-tab[data-tool="${subAction}"]`);
      if (toolBtn) toolBtn.click();
    }

    if (tabId === "dashboard") this.loadDashboardSummary();
    if (tabId === "matcher") this.loadJobs();
    if (tabId === "tracker") this.loadApplications();
  }

  switchCopilotTool(toolName, btnElement) {
    document.querySelectorAll(".copilot-tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".copilot-tool-pane").forEach((p) => p.classList.remove("active"));

    if (btnElement) btnElement.classList.add("active");
    const pane = document.getElementById(`tool-${toolName}`);
    if (pane) pane.classList.add("active");
  }

  showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    let icon = "fa-circle-info";
    if (type === "success") icon = "fa-circle-check text-green";
    if (type === "error") icon = "fa-circle-exclamation text-red";

    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  async loadInitialData() {
    try {
      await Promise.all([
        this.loadDashboardSummary(),
        this.loadJobs(),
        this.loadSavedResumesList(),
        this.loadApplications()
      ]);
    } catch (e) {
      console.warn("Initial data load encountered a notice:", e);
    }
  }

  // ==================== DASHBOARD ====================
  async loadDashboardSummary() {
    try {
      const summary = await api.getDashboardSummary();
      
      document.getElementById("statTotalResumes").textContent = summary.total_resumes_analyzed || 0;
      document.getElementById("statAvgAts").textContent = `${summary.average_ats_score || 0}%`;
      document.getElementById("statTotalJobs").textContent = summary.total_active_jobs || 0;
      document.getElementById("statTotalMatches").textContent = summary.total_matches_generated || 0;

      // Pipeline counts
      const counts = summary.pipeline_counts || {};
      const maxCount = Math.max(1, (counts.WISHLIST || 0) + (counts.APPLIED || 0) + (counts.INTERVIEWING || 0) + (counts.OFFER || 0));

      document.getElementById("countWishlist").textContent = counts.WISHLIST || 0;
      document.getElementById("countApplied").textContent = counts.APPLIED || 0;
      document.getElementById("countInterview").textContent = counts.INTERVIEWING || 0;
      document.getElementById("countOffer").textContent = counts.OFFER || 0;

      document.getElementById("barWishlist").style.width = `${Math.min(100, ((counts.WISHLIST || 0) / maxCount) * 100)}%`;
      document.getElementById("barApplied").style.width = `${Math.min(100, ((counts.APPLIED || 0) / maxCount) * 100)}%`;
      document.getElementById("barInterview").style.width = `${Math.min(100, ((counts.INTERVIEWING || 0) / maxCount) * 100)}%`;
      document.getElementById("barOffer").style.width = `${Math.min(100, ((counts.OFFER || 0) / maxCount) * 100)}%`;

      // Skills cloud
      const skillsContainer = document.getElementById("dashboardSkillsCloud");
      if (skillsContainer && summary.top_skills_in_demand) {
        skillsContainer.innerHTML = summary.top_skills_in_demand
          .map((s) => `<span class="skill-tag">${s.skill} <span class="skill-tag-count">${s.count}</span></span>`)
          .join("");
      }
    } catch (err) {
      console.error("Dashboard load failed:", err);
    }
  }

  // ==================== ANALYZER ====================
  async handleFileUpload(file) {
    this.showToast(`Uploading and analyzing ${file.name}...`, "info");
    const provider = this.getSelectedAIProvider();

    try {
      const result = await api.uploadResume(file, provider);
      this.activeResume = result;
      this.renderResumeScorecard(result);
      await this.loadSavedResumesList();
      this.showToast(`Successfully analyzed ${file.name}! ATS Score: ${result.ats_score}`, "success");
      this.switchTab("analyzer");
    } catch (err) {
      this.showToast(`Upload failed: ${err.message}`, "error");
    }
  }

  async analyzeRawResumeText() {
    const text = document.getElementById("rawResumeText").value;
    const role = document.getElementById("rawTargetTitle").value;
    if (!text.trim()) {
      this.showToast("Please paste resume text content first.", "error");
      return;
    }

    const btn = document.getElementById("btnAnalyzeRawText");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing...`;

    try {
      const provider = this.getSelectedAIProvider();
      const result = await api.analyzeResumeText(text, role, provider);
      this.activeResume = result;
      this.renderResumeScorecard(result);
      await this.loadSavedResumesList();
      this.showToast(`Analysis complete! ATS Score: ${result.ats_score}`, "success");
    } catch (err) {
      this.showToast(`Analysis failed: ${err.message}`, "error");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-bolt"></i> Analyze Text`;
    }
  }

  loadSampleResume(type) {
    const sampleText = DEMO_RESUMES[type];
    if (!sampleText) return;

    // Set text in raw tab
    const txtArea = document.getElementById("rawResumeText");
    if (txtArea) txtArea.value = sampleText;

    // Switch subtab
    const rawBtn = document.querySelector(`.subtab-btn[data-subtab="raw-text"]`);
    if (rawBtn) rawBtn.click();

    // Auto analyze
    this.analyzeRawResumeText();
  }

  async loadSavedResumesList() {
    try {
      const list = await api.getAllResumes();
      this.savedResumes = list;
      const select = document.getElementById("savedResumesSelect");
      if (!select) return;

      select.innerHTML = `<option value="">-- Load Analyzed Resume (${list.length}) --</option>` +
        list.map((r) => `<option value="${r.id}">${r.candidate_name || "Candidate"} - ${r.filename || "Resume"} (${r.ats_score} ATS)</option>`).join("");

      if (this.activeResume) {
        select.value = this.activeResume.id;
      }
    } catch (e) {
      console.warn("Could not load resumes list:", e);
    }
  }

  async handleSavedResumeSelect(id) {
    if (!id) return;
    try {
      const resume = await api.getResume(id);
      this.activeResume = resume;
      this.renderResumeScorecard(resume);
      this.showToast(`Loaded scorecard for ${resume.candidate_name}`, "info");
    } catch (e) {
      this.showToast("Could not load selected resume", "error");
    }
  }

  renderResumeScorecard(r) {
    document.getElementById("analyzerEmptyState").style.display = "none";
    document.getElementById("analyzerResultsContainer").style.display = "block";
    document.getElementById("btnExportPdf").disabled = false;

    // Contact Card
    const profileCard = document.getElementById("candidateProfileCard");
    const metaGrid = document.getElementById("candidateMetaGrid");
    if (profileCard && metaGrid) {
      profileCard.style.display = "block";
      metaGrid.innerHTML = `
        <div class="candidate-meta-item"><strong>Name</strong><span>${r.candidate_name || "Candidate"}</span></div>
        <div class="candidate-meta-item"><strong>Email</strong><span>${r.candidate_email || "N/A"}</span></div>
        <div class="candidate-meta-item"><strong>Phone</strong><span>${r.candidate_phone || "N/A"}</span></div>
        <div class="candidate-meta-item"><strong>LinkedIn</strong><span>${r.candidate_linkedin || "N/A"}</span></div>
      `;
    }

    // Score Dial
    const scoreVal = Math.round(r.ats_score || 0);
    document.getElementById("atsScoreValue").textContent = scoreVal;

    const dial = document.getElementById("scoreDial");
    const badge = document.getElementById("atsScoreBadge");
    
    let color = "#10b981"; // green
    let tag = "Excellent ATS Match";
    let bgBadge = "rgba(16, 185, 129, 0.2)";

    if (scoreVal < 60) {
      color = "#ef4444"; // red
      tag = "Needs Significant Optimization";
      bgBadge = "rgba(239, 68, 68, 0.2)";
    } else if (scoreVal < 80) {
      color = "#f59e0b"; // amber
      tag = "Good / Moderate Pass Rate";
      bgBadge = "rgba(245, 158, 11, 0.2)";
    }

    const deg = Math.round((scoreVal / 100) * 360);
    dial.style.background = `conic-gradient(${color} ${deg}deg, rgba(255, 255, 255, 0.08) ${deg}deg)`;
    badge.textContent = tag;
    badge.style.background = bgBadge;
    badge.style.color = color;

    // Breakdown Meters
    const breakdown = r.score_breakdown || {};
    const kw = breakdown.keywords || 0;
    const imp = breakdown.impact_metrics || 0;
    const sec = breakdown.section_completeness || 0;
    const fmt = breakdown.formatting || 0;

    document.getElementById("scoreKeywords").textContent = `${kw}/100`;
    document.getElementById("meterKeywords").style.width = `${kw}%`;

    document.getElementById("scoreImpact").textContent = `${imp}/100`;
    document.getElementById("meterImpact").style.width = `${imp}%`;

    document.getElementById("scoreSections").textContent = `${sec}/100`;
    document.getElementById("meterSections").style.width = `${sec}%`;

    document.getElementById("scoreFormatting").textContent = `${fmt}/100`;
    document.getElementById("meterFormatting").style.width = `${fmt}%`;

    // Strengths & Weaknesses
    const strengthsList = document.getElementById("strengthsList");
    strengthsList.innerHTML = (r.strengths || ["Well-structured layout"]).map((s) => `<li>${s}</li>`).join("");

    const weaknessesList = document.getElementById("weaknessesList");
    weaknessesList.innerHTML = (r.weaknesses || ["Add more quantifiable impact metrics"]).map((w) => `<li>${w}</li>`).join("");

    // Skills
    const totalSkills = (r.extracted_skills || []).length;
    document.getElementById("totalSkillsCount").textContent = `${totalSkills} Skills Detected`;

    const hardCont = document.getElementById("extractedHardSkills");
    hardCont.innerHTML = (r.hard_skills || []).map((s) => `<span class="pill-skill">${s}</span>`).join("") || `<span class="text-muted">No hard skills extracted.</span>`;

    const softCont = document.getElementById("extractedSoftSkills");
    softCont.innerHTML = (r.soft_skills || []).map((s) => `<span class="pill-skill" style="border-color: rgba(6, 182, 212, 0.4); color: #67e8f9;">${s}</span>`).join("") || `<span class="text-muted">No soft skills extracted.</span>`;

    // Bullet Rewrites
    const bulletsCont = document.getElementById("bulletOptimizationsList");
    const bullets = r.bullet_improvements || [];
    if (bullets.length) {
      bulletsCont.innerHTML = bullets.map((b) => `
        <div class="bullet-card">
          <div class="bullet-before"><i class="fa-solid fa-xmark text-red"></i> ${b.original}</div>
          <div class="bullet-after"><i class="fa-solid fa-check text-green"></i> ${b.improved}</div>
          <div class="bullet-why"><strong>AI Rationale:</strong> ${b.explanation || "Enhanced with active verbs and quantifiable business impact."}</div>
        </div>
      `).join("");
    } else {
      bulletsCont.innerHTML = `<p class="text-muted">No bullet points analyzed.</p>`;
    }
  }

  exportCurrentResumePdf() {
    if (!this.activeResume || !this.activeResume.id) {
      this.showToast("No active resume to export.", "error");
      return;
    }
    const url = api.getResumePdfUrl(this.activeResume.id);
    window.open(url, "_blank");
  }

  // ==================== JOB MATCHER ====================
  async loadJobs() {
    try {
      const jobs = await api.getJobs();
      this.jobsList = jobs;
      this.renderJobsList(jobs);
    } catch (err) {
      console.error("Could not load jobs:", err);
    }
  }

  renderJobsList(jobs) {
    const container = document.getElementById("jobsListContainer");
    if (!container) return;

    if (!jobs || !jobs.length) {
      container.innerHTML = `<div class="empty-state-inner"><p>No matching jobs found in database.</p></div>`;
      return;
    }

    container.innerHTML = jobs.map((job) => `
      <div class="job-card ${this.activeJob && this.activeJob.id === job.id ? 'active' : ''}" onclick="app.selectJobForMatch(${job.id})">
        <div class="job-card-header">
          <div>
            <div class="job-card-title">${job.title}</div>
            <div class="job-card-company">${job.company} • ${job.location || 'Remote'}</div>
          </div>
          ${job.match_score ? `<span class="job-card-match-tag">${job.match_score}% Match</span>` : ''}
        </div>
        <div class="job-meta-pills">
          <span class="pill pill-green">${job.salary_range || '$120k - $160k'}</span>
          <span class="pill">${job.experience_level || 'Mid-Senior'}</span>
          <span class="pill">${job.workplace_type || 'Remote'}</span>
        </div>
      </div>
    `).join("");
  }

  filterJobsList() {
    const query = (document.getElementById("jobSearchInput")?.value || "").toLowerCase();
    const filter = this.currentJobFilter;

    const filtered = this.jobsList.filter((j) => {
      const matchesQuery = !query ||
        j.title.toLowerCase().includes(query) ||
        j.company.toLowerCase().includes(query) ||
        (j.required_skills || []).some((s) => s.toLowerCase().includes(query));

      const matchesFilter = filter === "all" ||
        (j.workplace_type && j.workplace_type.toLowerCase() === filter.toLowerCase()) ||
        (j.experience_level && j.experience_level.toLowerCase().includes(filter.toLowerCase())) ||
        (j.job_type && j.job_type.toLowerCase() === filter.toLowerCase());

      return matchesQuery && matchesFilter;
    });

    this.renderJobsList(filtered);
  }

  setJobFilter(filter, btn) {
    this.currentJobFilter = filter;
    document.querySelectorAll(".filter-chip").forEach((b) => b.classList.remove("active"));
    if (btn) btn.classList.add("active");
    this.filterJobsList();
  }

  async selectJobForMatch(jobId) {
    const job = this.jobsList.find((j) => j.id === jobId);
    if (!job) return;
    this.activeJob = job;
    this.renderJobsList(this.jobsList); // update active highlight

    if (!this.activeResume) {
      // Auto-load sample resume if user hasn't uploaded yet
      await this.loadSampleResume("fullstack");
    }

    try {
      this.showToast(`Calculating match against ${job.company}...`, "info");
      const matchResult = await api.matchSingle({
        resume_id: this.activeResume ? this.activeResume.id : null,
        resume_text: this.activeResume ? this.activeResume.raw_text : "",
        job_id: job.id,
        job_title: job.title,
        job_description: job.description
      });
      this.activeMatch = matchResult;
      this.renderMatchDetail(matchResult, job);
    } catch (err) {
      this.showToast(`Match calculation error: ${err.message}`, "error");
    }
  }

  async runBatchMatchForActiveResume() {
    if (!this.activeResume || !this.activeResume.id) {
      this.showToast("Please analyze or select a resume first.", "error");
      this.switchTab("analyzer");
      return;
    }

    this.showToast("Batch evaluating resume against all active job vacancies...", "info");
    try {
      const batchResp = await api.batchMatchAll(this.activeResume.id);
      
      // Update jobs list with scores
      if (batchResp.ranked_jobs && batchResp.ranked_jobs.length) {
        this.jobsList = batchResp.ranked_jobs.map((item) => ({
          ...item.job_details,
          match_score: item.match_score,
          full_match: item
        }));
        this.renderJobsList(this.jobsList);
        
        // Select top job
        const topMatch = batchResp.ranked_jobs[0];
        this.activeJob = topMatch.job_details;
        this.activeMatch = topMatch;
        this.renderMatchDetail(topMatch, topMatch.job_details);
        this.showToast(`Batch matching completed! Top match: ${topMatch.match_score}% at ${topMatch.job_details.company}`, "success");
      }
    } catch (err) {
      this.showToast(`Batch match failed: ${err.message}`, "error");
    }
  }

  renderMatchDetail(m, job) {
    document.getElementById("matchDetailEmptyState").style.display = "none";
    document.getElementById("matchDetailContainer").style.display = "block";

    // Hero Meta
    document.getElementById("matchJobTitle").textContent = job.title;
    document.getElementById("matchJobCompany").textContent = job.company;
    document.getElementById("matchJobLocation").textContent = job.location || "Remote";
    document.getElementById("matchJobSalary").textContent = job.salary_range || "$130k - $170k";

    // Scores
    const scoreVal = Math.round(m.match_score || 0);
    document.getElementById("matchScoreVal").textContent = scoreVal;
    document.getElementById("metricSkillsScore").textContent = `${Math.round(m.skills_match_score || 0)}%`;
    document.getElementById("metricExpScore").textContent = `${Math.round(m.experience_match_score || 0)}%`;
    document.getElementById("metricSemanticScore").textContent = `${Math.round(m.semantic_similarity_score || 0)}%`;

    // Skills Matrix
    const matchedCont = document.getElementById("matchedSkillsPills");
    matchedCont.innerHTML = (m.matched_skills || []).map((s) => `<span class="pill-skill match-hit"><i class="fa-solid fa-check"></i> ${s}</span>`).join("") || `<span class="text-muted">No direct skill matches found.</span>`;

    const missCritCont = document.getElementById("missingCriticalPills");
    missCritCont.innerHTML = (m.missing_critical_skills || []).map((s) => `<span class="pill-skill match-miss"><i class="fa-solid fa-xmark"></i> ${s}</span>`).join("") || `<span class="text-muted text-green"><i class="fa-solid fa-circle-check"></i> All critical job skills matched!</span>`;

    const missNiceCont = document.getElementById("missingNicePills");
    missNiceCont.innerHTML = (m.missing_nice_to_have || []).map((s) => `<span class="pill-skill match-nice">${s}</span>`).join("") || `<span class="text-muted">None</span>`;

    // Fit & Recs
    document.getElementById("matchFitSummary").textContent = m.fit_summary || "Candidate exhibits strong technical foundation for the core requirements of this role.";
    
    const recsList = document.getElementById("matchRecsList");
    recsList.innerHTML = (m.tailored_recommendations || ["Highlight distributed systems experience in the top third of resume."]).map((r) => `<li>${r}</li>`).join("");

    const pointsList = document.getElementById("matchInterviewPointsList");
    pointsList.innerHTML = (m.interview_focus_areas || ["Explain how you handled high throughput API scaling."]).map((p) => `<li>${p}</li>`).join("");
  }

  openNewJobModal() {
    document.getElementById("newJobModal").showModal();
  }

  async submitNewJob() {
    const title = document.getElementById("njTitle").value;
    const company = document.getElementById("njCompany").value;
    const location = document.getElementById("njLocation").value;
    const salary = document.getElementById("njSalary").value;
    const skillsRaw = document.getElementById("njSkills").value;
    const description = document.getElementById("njDescription").value;

    const skills = skillsRaw.split(",").map((s) => s.trim()).filter(Boolean);

    try {
      const created = await api.createJob({
        title,
        company,
        location,
        salary_range: salary,
        required_skills: skills,
        description
      });
      this.showToast(`Job opening created: ${created.title} at ${created.company}`, "success");
      document.getElementById("newJobModal").close();
      document.getElementById("newJobForm").reset();
      await this.loadJobs();
      this.selectJobForMatch(created.id);
    } catch (err) {
      this.showToast(`Failed to add job: ${err.message}`, "error");
    }
  }

  // ==================== AI COPILOT SUITE ====================
  async generateCoverLetter() {
    const jobTitle = document.getElementById("clJobTitle").value;
    const company = document.getElementById("clCompanyName").value;
    const tone = document.getElementById("clTone").value;
    const jobDesc = document.getElementById("clJobDesc").value;
    const notes = document.getElementById("clCustomNotes").value;

    const btn = document.getElementById("btnGenCoverLetter");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Crafting Tailored Letter...`;

    try {
      const provider = this.getSelectedAIProvider();
      const result = await api.generateCoverLetter({
        resume_id: this.activeResume ? this.activeResume.id : null,
        resume_text: this.activeResume ? this.activeResume.raw_text : "",
        job_title: jobTitle,
        company_name: company,
        tone: tone,
        job_description: jobDesc,
        custom_notes: notes,
        ai_provider: provider
      });

      document.getElementById("coverLetterOutput").textContent = result.cover_letter;
      
      const sellingPointsCont = document.getElementById("clSellingPointsWrap");
      const pointsList = document.getElementById("clSellingPointsList");
      if (result.key_selling_points && result.key_selling_points.length) {
        sellingPointsCont.style.display = "block";
        pointsList.innerHTML = result.key_selling_points.map((p) => `<li>${p}</li>`).join("");
      } else {
        sellingPointsCont.style.display = "none";
      }

      this.showToast("Cover letter generated successfully!", "success");
    } catch (err) {
      this.showToast(`Generation failed: ${err.message}`, "error");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-sparkles"></i> Generate Tailored Cover Letter`;
    }
  }

  copyCoverLetterText() {
    const text = document.getElementById("coverLetterOutput").textContent;
    if (!text || text.includes("Fill in the role details")) return;
    navigator.clipboard.writeText(text);
    this.showToast("Cover letter copied to clipboard!", "success");
  }

  downloadCoverLetter() {
    const text = document.getElementById("coverLetterOutput").textContent;
    if (!text || text.includes("Fill in the role details")) return;
    const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `Cover_Letter_${document.getElementById("clCompanyName")?.value || "Company"}.txt`;
    link.click();
  }

  generateCoverLetterForCurrentMatch() {
    if (!this.activeJob) return;
    document.getElementById("clJobTitle").value = this.activeJob.title;
    document.getElementById("clCompanyName").value = this.activeJob.company;
    document.getElementById("clJobDesc").value = this.activeJob.description || "";
    this.switchTab("copilot", "cover_letter");
    this.generateCoverLetter();
  }

  async optimizeBulletPoints() {
    const rawBullets = document.getElementById("boBulletsInput").value;
    const targetRole = document.getElementById("boTargetRole").value;
    const bulletsList = rawBullets.split("\n").map((b) => b.trim()).filter(Boolean);

    if (!bulletsList.length) {
      this.showToast("Please enter at least one bullet point.", "error");
      return;
    }

    const btn = document.getElementById("btnOptimizeBullets");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Rewriting Impact Bullets...`;

    try {
      const provider = this.getSelectedAIProvider();
      const res = await api.optimizeBullets(bulletsList, targetRole, provider);
      const resultsCont = document.getElementById("customBulletsResults");
      
      resultsCont.innerHTML = res.optimized_bullets.map((b) => `
        <div class="bullet-card">
          <div class="bullet-before"><i class="fa-solid fa-xmark text-red"></i> ${b.original}</div>
          <div class="bullet-after"><i class="fa-solid fa-check text-green"></i> ${b.improved}</div>
          <div class="bullet-why"><strong>Formula Analysis:</strong> ${b.explanation || "Transformed with active verbs and quantified results."}</div>
        </div>
      `).join("");

      this.showToast("Resume bullets optimized!", "success");
    } catch (err) {
      this.showToast(`Bullet optimizer failed: ${err.message}`, "error");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Transform with AI Engine`;
    }
  }

  async generateInterviewPrep() {
    const title = document.getElementById("ipJobTitle").value;
    const desc = document.getElementById("ipJobDesc").value;
    const count = parseInt(document.getElementById("ipQuestionCount").value, 10) || 5;

    const btn = document.getElementById("btnGenInterviewPrep");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Simulating Interview Questions...`;

    try {
      const provider = this.getSelectedAIProvider();
      const result = await api.generateInterviewPrep({
        resume_id: this.activeResume ? this.activeResume.id : null,
        resume_text: this.activeResume ? this.activeResume.raw_text : "",
        job_title: title,
        job_description: desc,
        question_count: count,
        ai_provider: provider
      });

      const container = document.getElementById("interviewQuestionsResults");
      container.innerHTML = (result.questions || []).map((q, idx) => `
        <div class="interview-card">
          <div class="interview-q-header">
            <span class="interview-category"><i class="fa-solid fa-tag"></i> ${q.category || "Behavioral & Technical"}</span>
            <span class="badge badge-subtle">Q${idx + 1}</span>
          </div>
          <div class="interview-question">${q.question}</div>
          <div class="interview-star-box">
            <strong><i class="fa-solid fa-star"></i> Recommended STAR Answer Strategy:</strong><br/>
            ${q.recommended_star_answer}
          </div>
          <div class="interview-talking-point">
            <strong><i class="fa-solid fa-lightbulb text-amber"></i> Resume Talking Point:</strong> ${q.resume_talking_point}
          </div>
        </div>
      `).join("");

      this.showToast("Interview strategy and predicted Q&As ready!", "success");
    } catch (err) {
      this.showToast(`Interview prep error: ${err.message}`, "error");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-brain"></i> Generate Interview Strategy & Q&A`;
    }
  }

  generateInterviewPrepForCurrentMatch() {
    if (!this.activeJob) return;
    document.getElementById("ipJobTitle").value = this.activeJob.title;
    document.getElementById("ipJobDesc").value = this.activeJob.description || "";
    this.switchTab("copilot", "interview_prep");
    this.generateInterviewPrep();
  }

  async generateCareerRoadmap() {
    const target = document.getElementById("roadmapTargetRole").value || "Principal Cloud Architect";
    const skills = this.activeResume ? (this.activeResume.extracted_skills || []) : [];

    try {
      const result = await api.generateCareerRoadmap(target, skills);
      const container = document.getElementById("roadmapTimelineContainer");
      
      container.innerHTML = (result.milestones || []).map((m) => `
        <div class="milestone-item">
          <div class="milestone-phase">${m.phase}</div>
          <h4 class="milestone-title">${m.title}</h4>
          
          <div style="margin-bottom: 10px;">
            <strong style="font-size: 0.8rem; color: var(--cyan-accent); display: block; margin-bottom: 4px;">Skills to Master:</strong>
            <div class="skills-pill-group">
              ${(m.skills_to_learn || []).map((s) => `<span class="pill-skill">${s}</span>`).join("")}
            </div>
          </div>

          <div style="margin-bottom: 8px;">
            <strong style="font-size: 0.8rem; color: var(--green-accent); display: block; margin-bottom: 4px;">Recommended Portfolio Projects:</strong>
            <ul class="recommendation-list">
              ${(m.recommended_projects || []).map((p) => `<li>${p}</li>`).join("")}
            </ul>
          </div>
        </div>
      `).join("");

      this.showToast(`Career roadmap generated for ${target}!`, "success");
    } catch (err) {
      this.showToast("Roadmap generation failed", "error");
    }
  }

  // ==================== KANBAN APPLICATION TRACKER ====================
  async loadApplications() {
    try {
      const apps = await api.getApplications();
      this.renderKanbanBoard(apps);
    } catch (err) {
      console.error("Failed to load applications:", err);
    }
  }

  renderKanbanBoard(apps) {
    const columns = {
      WISHLIST: document.getElementById("col-WISHLIST"),
      APPLIED: document.getElementById("col-APPLIED"),
      INTERVIEWING: document.getElementById("col-INTERVIEWING"),
      OFFER: document.getElementById("col-OFFER"),
      REJECTED: document.getElementById("col-REJECTED"),
    };

    // Reset columns
    Object.values(columns).forEach((c) => { if (c) c.innerHTML = ""; });
    const counts = { WISHLIST: 0, APPLIED: 0, INTERVIEWING: 0, OFFER: 0, REJECTED: 0 };

    apps.forEach((app) => {
      const status = app.status ? app.status.toUpperCase() : "WISHLIST";
      if (columns[status]) {
        counts[status] = (counts[status] || 0) + 1;
        const card = document.createElement("div");
        card.className = "kanban-card";
        card.innerHTML = `
          <div class="kanban-card-title">${app.job_title}</div>
          <div class="kanban-card-company">${app.company_name} • ${app.location || "Remote"}</div>
          <div class="kanban-card-meta">
            ${app.match_score ? `<span class="pill pill-green">${app.match_score}% Fit</span>` : '<span></span>'}
            <select class="status-changer-select" onchange="app.moveAppStatus(${app.id}, this.value)">
              <option value="WISHLIST" ${status === 'WISHLIST' ? 'selected' : ''}>Wishlist</option>
              <option value="APPLIED" ${status === 'APPLIED' ? 'selected' : ''}>Applied</option>
              <option value="INTERVIEWING" ${status === 'INTERVIEWING' ? 'selected' : ''}>Interview</option>
              <option value="OFFER" ${status === 'OFFER' ? 'selected' : ''}>Offer</option>
              <option value="REJECTED" ${status === 'REJECTED' ? 'selected' : ''}>Archived</option>
            </select>
          </div>
        `;
        columns[status].appendChild(card);
      }
    });

    // Update counts
    document.getElementById("countColWishlist").textContent = counts.WISHLIST;
    document.getElementById("countColApplied").textContent = counts.APPLIED;
    document.getElementById("countColInterviewing").textContent = counts.INTERVIEWING;
    document.getElementById("countColOffer").textContent = counts.OFFER;
    document.getElementById("countColRejected").textContent = counts.REJECTED;
  }

  async moveAppStatus(appId, newStatus) {
    try {
      await api.updateApplication(appId, { status: newStatus });
      this.showToast(`Moved application to ${newStatus}`, "info");
      await this.loadApplications();
    } catch (err) {
      this.showToast(`Failed to update application: ${err.message}`, "error");
    }
  }

  openNewAppModal() {
    document.getElementById("newAppModal").showModal();
  }

  async submitNewApplication() {
    const company = document.getElementById("naCompany").value;
    const jobTitle = document.getElementById("naJobTitle").value;
    const status = document.getElementById("naStatus").value;
    const salary = document.getElementById("naSalary").value;
    const notes = document.getElementById("naNotes").value;

    try {
      await api.createApplication({
        company_name: company,
        job_title: jobTitle,
        status: status,
        salary_target: salary,
        notes: notes,
        match_score: this.activeMatch ? this.activeMatch.match_score : 85
      });
      this.showToast(`Tracked application at ${company}!`, "success");
      document.getElementById("newAppModal").close();
      document.getElementById("newAppForm").reset();
      await this.loadApplications();
      this.switchTab("tracker");
    } catch (err) {
      this.showToast(`Error creating application: ${err.message}`, "error");
    }
  }

  async trackCurrentJobMatch() {
    if (!this.activeJob) return;
    try {
      await api.createApplication({
        company_name: this.activeJob.company,
        job_title: this.activeJob.title,
        location: this.activeJob.location || "Remote",
        status: "APPLIED",
        salary_target: this.activeJob.salary_range || "$140k",
        job_id: this.activeJob.id,
        resume_id: this.activeResume ? this.activeResume.id : null,
        match_score: this.activeMatch ? this.activeMatch.match_score : 90
      });
      this.showToast(`Added ${this.activeJob.title} at ${this.activeJob.company} to Tracker!`, "success");
      await this.loadApplications();
      this.switchTab("tracker");
    } catch (err) {
      this.showToast(`Track failed: ${err.message}`, "error");
    }
  }

  // ==================== SETTINGS ====================
  saveSettings() {
    const backendUrl = document.getElementById("backendUrlInput").value;
    api.setBaseUrl(backendUrl);
    this.showToast("Settings and API endpoint saved successfully!", "success");
    document.getElementById("settingsModal").close();
  }
}

// Global App Instance
const app = new AppController();
document.addEventListener("DOMContentLoaded", () => {
  app.init();
});
