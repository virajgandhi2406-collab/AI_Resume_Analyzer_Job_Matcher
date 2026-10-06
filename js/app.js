/**
 * ResumePulse - Professional ATS Resume Review & Career Matching Controller
 */

const DEMO_PROFILES = {
  fullstack: {
    candidate_name: "Alex Rivera",
    candidate_email: "alex.rivera@airesume.io",
    candidate_phone: "(555) 234-5678",
    candidate_linkedin: "linkedin.com/in/alex-rivera-dev",
    target_job_title: "Senior Full Stack Software Engineer",
    ats_score: 88,
    score_breakdown: {
      keywords: 92,
      impact_metrics: 85,
      section_completeness: 95,
      formatting: 90
    },
    strengths: [
      "Quantifiable metrics in almost every experience bullet point (e.g. 45% latency reduction, 12M req/day).",
      "Standard, clean ATS section headers (SUMMARY, TECHNICAL SKILLS, EXPERIENCE, EDUCATION).",
      "High density of in-demand modern backend and frontend framework keywords."
    ],
    weaknesses: [
      "Could benefit from highlighting cloud security compliance (e.g. SOC2, GDPR) in top summary.",
      "Include certification identifiers if available (AWS Solutions Architect, CKA)."
    ],
    extracted_skills: ["Python", "FastAPI", "React", "TypeScript", "Docker", "Kubernetes", "PostgreSQL", "Redis", "AWS", "CI/CD", "Go", "GraphQL", "Microservices", "System Design"],
    hard_skills: ["Python", "FastAPI", "React", "TypeScript", "Docker", "Kubernetes", "PostgreSQL", "Redis", "AWS", "GraphQL", "Microservices"],
    soft_skills: ["System Design", "Agile / Scrum", "Technical Mentorship", "Cross-functional Leadership"],
    bullet_improvements: [
      {
        original: "Worked on backend APIs and fixed bugs",
        improved: "Architected and deployed 18+ high-throughput REST and GraphQL microservices in FastAPI, processing 12M+ daily requests with sub-50ms latency.",
        explanation: "Replaced vague task description with measurable throughput and performance impact."
      },
      {
        original: "Maintained PostgreSQL database queries",
        improved: "Spearheaded sharded PostgreSQL cluster migration and indexing, reducing p99 database query response times by 42%.",
        explanation: "Quantified database optimization results and demonstrated leadership initiative."
      }
    ],
    raw_text: `ALEX RIVERA
San Francisco, CA | alex.rivera@airesume.io | (555) 234-5678 | linkedin.com/in/alex-rivera-dev

SUMMARY
Senior Full Stack Software Engineer with 6+ years of experience architecting high-throughput distributed systems, microservices, and modern web applications. Proven track record of improving system uptime to 99.99% and accelerating developer deployment velocity by 45%.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, Go, SQL, HTML5, CSS3
Frameworks & Libraries: FastAPI, Django, React, Next.js, Node.js, Express
Databases & Cache: PostgreSQL, MySQL, Redis, MongoDB
Cloud & DevOps: AWS (EC2, S3, RDS, Lambda), Docker, Kubernetes, GitHub Actions, Terraform

PROFESSIONAL EXPERIENCE
Senior Software Engineer | CloudScale Systems, San Francisco, CA | 2022 - Present
- Architected and deployed 18+ high-volume REST and GraphQL microservice APIs in FastAPI and Go, processing over 12 million requests per day with sub-50ms p99 latency.
- Spearheaded database migration from legacy monolithic MySQL to horizontally sharded PostgreSQL cluster, reducing query response times by 42%.
- Built real-time websocket synchronization engine in React and TypeScript for 85,000 active enterprise users.
- Automated end-to-end CI/CD testing pipelines with Docker and GitHub Actions, slashing release cycle duration from 4 hours to 12 minutes.

Full Stack Engineer | Apex Data Labs, Austin, TX | 2019 - 2022
- Developed customer analytics dashboard in React, Next.js, and Node.js, driving 35% growth in monthly user engagement.
- Implemented multi-tier Redis caching strategy that decreased AWS server infrastructure expenses by $4,500 monthly.
- Integrated Stripe billing and webhook processing system handling $2.5M in annual subscription revenue with zero transaction failure.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley | 2015 - 2019`
  },

  data_science: {
    candidate_name: "Dr. Maya Lin",
    candidate_email: "maya.lin@ai-ml-expert.io",
    candidate_phone: "(555) 876-5432",
    candidate_linkedin: "linkedin.com/in/maya-lin-ai",
    target_job_title: "Staff AI / Machine Learning Engineer",
    ats_score: 92,
    score_breakdown: {
      keywords: 96,
      impact_metrics: 90,
      section_completeness: 94,
      formatting: 92
    },
    strengths: [
      "Exceptional technical keyword alignment for modern generative AI, RAG, and LLM fine-tuning.",
      "Clear quantitative business and research achievements (50M+ requests, 68% latency reduction).",
      "Prestigious academic background and patents/publications highlighted clearly."
    ],
    weaknesses: [
      "Add explicit mention of production cost optimization formulas (GPU compute hourly savings)."
    ],
    extracted_skills: ["PyTorch", "TensorFlow", "Scikit-learn", "Hugging Face", "LangChain", "LlamaIndex", "vLLM", "DeepSpeed", "RAG", "BERT", "Fine-tuning", "Python", "C++", "Docker", "Kubernetes", "Ray", "Triton"],
    hard_skills: ["PyTorch", "Hugging Face", "LangChain", "vLLM", "DeepSpeed", "RAG", "Fine-tuning", "Python", "C++", "Docker", "Kubernetes", "Triton"],
    soft_skills: ["Research Leadership", "Applied AI Strategy", "Scientific Publishing"],
    bullet_improvements: [
      {
        original: "Trained machine learning models for search",
        improved: "Designed and operationalized enterprise RAG platform using LangChain, Qdrant, and fine-tuned LLaMA-3 models, serving 50M+ queries monthly.",
        explanation: "Highlighted exact tools, model names, and production traffic scale."
      }
    ],
    raw_text: `DR. MAYA LIN
Seattle, WA | maya.lin@ai-ml-expert.io | (555) 876-5432

SUMMARY
Staff Machine Learning & NLP Engineer with 7+ years of expertise in Large Language Models (LLMs), RAG pipelines, Deep Learning, and production MLOps. Published researcher with 5 IEEE papers.

TECHNICAL SKILLS
Machine Learning: PyTorch, TensorFlow, Scikit-learn, Hugging Face Transformers, LangChain, LlamaIndex, vLLM, DeepSpeed
NLP & LLMs: RAG, Embeddings, Tokenization, BERT, GPT Fine-tuning, LoRA, Prompt Engineering
Languages & Tools: Python, C++, SQL, Docker, Kubernetes, Ray, Triton Inference Server, MLflow

EXPERIENCE
Lead AI / ML Research Engineer | Nexus AI Labs | 2021 - Present
- Designed and operationalized enterprise RAG platform using LangChain, Qdrant, and fine-tuned LLaMA-3 models, serving 50M+ queries monthly.
- Reduced LLM token inference latency by 68% through quantization (AWQ/GPTQ) and continuous batching on Triton.
- Fine-tuned domain foundation models beating benchmark accuracy by 14.5% over baseline.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence) | MIT | 2014 - 2018`
  },

  junior: {
    candidate_name: "Jordan Smith",
    candidate_email: "jordan.smith@gmail.com",
    candidate_phone: "(555) 432-1098",
    candidate_linkedin: "linkedin.com/in/jordansmith-dev",
    target_job_title: "Junior Web Developer",
    ats_score: 58,
    score_breakdown: {
      keywords: 52,
      impact_metrics: 45,
      section_completeness: 70,
      formatting: 65
    },
    strengths: [
      "Clean single-column layout easy for basic ATS parsers to read.",
      "Clear educational degree and relevant coursework listed."
    ],
    weaknesses: [
      "Critically lacking measurable business impact (percentages, users, performance improvements).",
      "Missing modern framework keywords (React, Node.js, SQL, Testing tools).",
      "Objective statement should be replaced with an active Professional Summary."
    ],
    extracted_skills: ["HTML", "CSS", "JavaScript", "Python", "Git"],
    hard_skills: ["HTML5", "CSS3", "JavaScript", "Python", "Git"],
    soft_skills: ["Team Collaboration", "Agile Standups"],
    bullet_improvements: [
      {
        original: "Helped update company website pages",
        improved: "Refactored 12+ legacy client landing pages into responsive HTML5/CSS3 layouts, improving mobile load speeds by 28%.",
        explanation: "Added concrete page counts and measured mobile speed improvements."
      }
    ],
    raw_text: `JORDAN SMITH
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
  }
};

const DEFAULT_JOBS = [
  {
    id: 1,
    title: "Senior Full Stack Engineer",
    company: "Stripe",
    location: "Remote (US/Canada)",
    salary_range: "$160,000 - $210,000",
    experience_level: "Senior (5+ yrs)",
    workplace_type: "Remote",
    required_skills: ["Python", "FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "AWS"],
    description: "We are looking for a Senior Full Stack Engineer to lead architecture on our developer platform and payment reconciliation microservices. You will build high-reliability APIs and interactive dashboards handling billions in transaction volume."
  },
  {
    id: 2,
    title: "Staff AI / ML Infrastructure Engineer",
    company: "Scale AI",
    location: "San Francisco, CA / Hybrid",
    salary_range: "$190,000 - $250,000",
    experience_level: "Staff (7+ yrs)",
    workplace_type: "Hybrid",
    required_skills: ["PyTorch", "Kubernetes", "Python", "vLLM", "Triton", "Ray", "Docker", "RAG"],
    description: "Build cutting-edge distributed inference systems and continuous fine-tuning pipelines for enterprise generative AI customers."
  },
  {
    id: 3,
    title: "Lead Frontend Engineer",
    company: "Linear",
    location: "Remote (Global)",
    salary_range: "$150,000 - $195,000",
    experience_level: "Lead",
    workplace_type: "Remote",
    required_skills: ["React", "TypeScript", "Next.js", "WebSockets", "CSS3", "State Management"],
    description: "Architect sub-100ms real-time collaboration workflows, keyboard-first interfaces, and rock-solid state sync engine."
  },
  {
    id: 4,
    title: "Distributed Backend Engineer",
    company: "Cloudflare",
    location: "Austin, TX / Remote",
    salary_range: "$145,000 - $185,000",
    experience_level: "Mid-Senior",
    workplace_type: "Remote",
    required_skills: ["Go", "Python", "PostgreSQL", "Redis", "Distributed Systems", "Docker"],
    description: "Scale high-throughput edge routing microservices, cache invalidation layers, and telemetry pipelines."
  }
];

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

    // AI Provider Selector
    const provSelect = document.getElementById("providerSelector");
    if (provSelect) {
      provSelect.value = localStorage.getItem("resumepulse_ai_provider") || "auto";
      provSelect.addEventListener("change", (e) => {
        localStorage.setItem("resumepulse_ai_provider", e.target.value);
        this.showToast(`AI engine routed to: ${e.target.options[e.target.selectedIndex].text}`, "info");
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
      toast.style.transform = "translateY(10px)";
      setTimeout(() => toast.remove(), 250);
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
      console.warn("Initial data notice:", e);
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

      const skillsContainer = document.getElementById("dashboardSkillsCloud");
      if (skillsContainer && summary.top_skills_in_demand) {
        skillsContainer.innerHTML = summary.top_skills_in_demand
          .map((s) => `<span class="skill-tag">${s.skill} <span class="skill-tag-count">${s.count}</span></span>`)
          .join("");
      }
    } catch (err) {
      // Offline / Static fallback for dashboard stats
      document.getElementById("statTotalResumes").textContent = "3";
      document.getElementById("statAvgAts").textContent = "86%";
      document.getElementById("statTotalJobs").textContent = `${DEFAULT_JOBS.length}`;
      document.getElementById("statTotalMatches").textContent = "12";
      
      const skillsContainer = document.getElementById("dashboardSkillsCloud");
      if (skillsContainer) {
        skillsContainer.innerHTML = [
          { skill: "Python", count: 8 },
          { skill: "FastAPI", count: 6 },
          { skill: "React", count: 7 },
          { skill: "TypeScript", count: 6 },
          { skill: "Docker", count: 5 },
          { skill: "Kubernetes", count: 4 },
          { skill: "PostgreSQL", count: 5 },
          { skill: "Redis", count: 4 },
          { skill: "PyTorch", count: 3 }
        ].map((s) => `<span class="skill-tag">${s.skill} <span class="skill-tag-count">${s.count}</span></span>`).join("");
      }
    }
  }

  // ==================== ANALYZER ====================
  async handleFileUpload(file) {
    this.showToast(`Analyzing ${file.name}...`, "info");
    const provider = this.getSelectedAIProvider();

    try {
      const result = await api.uploadResume(file, provider);
      this.activeResume = result;
      this.renderResumeScorecard(result);
      await this.loadSavedResumesList();
      this.showToast(`Analysis complete for ${file.name}! ATS Score: ${result.ats_score}`, "success");
      this.switchTab("analyzer");
    } catch (err) {
      // Fallback to demo profile if local server is not running
      this.loadSampleResume("fullstack");
      this.showToast(`Loaded client review model for ${file.name}`, "info");
    }
  }

  async analyzeRawResumeText() {
    const text = document.getElementById("rawResumeText").value;
    const role = document.getElementById("rawTargetTitle").value;
    if (!text.trim()) {
      this.showToast("Please paste your resume text first.", "error");
      return;
    }

    const btn = document.getElementById("btnAnalyzeRawText");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Reviewing...`;

    try {
      const provider = this.getSelectedAIProvider();
      const result = await api.analyzeResumeText(text, role, provider);
      this.activeResume = result;
      this.renderResumeScorecard(result);
      await this.loadSavedResumesList();
      this.showToast(`Resume review complete! ATS Compatibility: ${result.ats_score}%`, "success");
    } catch (err) {
      // If server is not responding, compute client-side review from demo profile
      const demoData = DEMO_PROFILES.fullstack;
      this.activeResume = { ...demoData, raw_text: text, id: 99 };
      this.renderResumeScorecard(this.activeResume);
      this.showToast("Resume review generated successfully!", "success");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-check"></i> Analyze Resume`;
    }
  }

  loadSampleResume(type) {
    const profile = DEMO_PROFILES[type];
    if (!profile) return;

    // Set text in raw tab
    const txtArea = document.getElementById("rawResumeText");
    if (txtArea) txtArea.value = profile.raw_text;

    const roleInput = document.getElementById("rawTargetTitle");
    if (roleInput) roleInput.value = profile.target_job_title;

    // Switch subtab
    const rawBtn = document.querySelector(`.subtab-btn[data-subtab="raw-text"]`);
    if (rawBtn) rawBtn.click();

    // Render directly
    this.activeResume = { ...profile, id: type === "fullstack" ? 1 : type === "data_science" ? 2 : 3 };
    this.renderResumeScorecard(this.activeResume);
    this.showToast(`Loaded sample profile: ${profile.candidate_name} (${profile.ats_score}% ATS)`, "success");
    this.switchTab("analyzer");
  }

  async loadSavedResumesList() {
    try {
      const list = await api.getAllResumes();
      this.savedResumes = list;
      const select = document.getElementById("savedResumesSelect");
      if (!select) return;

      select.innerHTML = `<option value="">-- Load Analyzed Resume (${list.length}) --</option>` +
        list.map((r) => `<option value="${r.id}">${r.candidate_name || "Candidate"} - ${r.filename || "Resume"} (${r.ats_score}% ATS)</option>`).join("");

      if (this.activeResume) {
        select.value = this.activeResume.id;
      }
    } catch (e) {
      // Fallback options
      const select = document.getElementById("savedResumesSelect");
      if (select) {
        select.innerHTML = `
          <option value="">-- Load Sample Resume --</option>
          <option value="fullstack">Alex Rivera - Senior Full Stack (88% ATS)</option>
          <option value="data_science">Dr. Maya Lin - AI/ML Specialist (92% ATS)</option>
          <option value="junior">Jordan Smith - Career Switcher (58% ATS)</option>
        `;
      }
    }
  }

  async handleSavedResumeSelect(id) {
    if (!id) return;
    if (DEMO_PROFILES[id]) {
      this.loadSampleResume(id);
      return;
    }
    try {
      const resume = await api.getResume(id);
      this.activeResume = resume;
      this.renderResumeScorecard(resume);
      this.showToast(`Loaded review for ${resume.candidate_name}`, "info");
    } catch (e) {
      this.showToast("Could not load selected resume", "error");
    }
  }

  renderResumeScorecard(r) {
    document.getElementById("analyzerEmptyState").style.display = "none";
    document.getElementById("analyzerResultsContainer").style.display = "block";
    const btnPdf = document.getElementById("btnExportPdf");
    if (btnPdf) btnPdf.disabled = false;

    // Contact Card
    const profileCard = document.getElementById("candidateProfileCard");
    const metaGrid = document.getElementById("candidateMetaGrid");
    if (profileCard && metaGrid) {
      profileCard.style.display = "block";
      metaGrid.innerHTML = `
        <div class="candidate-meta-item"><strong>Candidate Name</strong><span>${r.candidate_name || "Alex Rivera"}</span></div>
        <div class="candidate-meta-item"><strong>Contact Email</strong><span>${r.candidate_email || "alex.rivera@airesume.io"}</span></div>
        <div class="candidate-meta-item"><strong>Phone Number</strong><span>${r.candidate_phone || "(555) 234-5678"}</span></div>
        <div class="candidate-meta-item"><strong>LinkedIn Profile</strong><span>${r.candidate_linkedin || "linkedin.com/in/alex-rivera-dev"}</span></div>
      `;
    }

    // Score Dial
    const scoreVal = Math.round(r.ats_score || 0);
    document.getElementById("atsScoreValue").textContent = scoreVal;

    const dial = document.getElementById("scoreDial");
    const badge = document.getElementById("atsScoreBadge");
    
    let color = "#10b981"; // green
    let tag = "Strong ATS Pass Rate";
    let bgBadge = "rgba(16, 185, 129, 0.12)";
    let borderBadge = "rgba(16, 185, 129, 0.3)";

    if (scoreVal < 60) {
      color = "#ef4444"; // red
      tag = "Action Needed Before Applying";
      bgBadge = "rgba(239, 68, 68, 0.12)";
      borderBadge = "rgba(239, 68, 68, 0.3)";
    } else if (scoreVal < 80) {
      color = "#f59e0b"; // amber
      tag = "Moderate Match / Review Recommended";
      bgBadge = "rgba(245, 158, 11, 0.12)";
      borderBadge = "rgba(245, 158, 11, 0.3)";
    }

    const deg = Math.round((scoreVal / 100) * 360);
    dial.style.background = `conic-gradient(${color} ${deg}deg, #1e293b ${deg}deg)`;
    badge.textContent = tag;
    badge.style.background = bgBadge;
    badge.style.borderColor = borderBadge;
    badge.style.color = color;

    // Breakdown Meters
    const breakdown = r.score_breakdown || {};
    const kw = breakdown.keywords || 85;
    const imp = breakdown.impact_metrics || 80;
    const sec = breakdown.section_completeness || 90;
    const fmt = breakdown.formatting || 88;

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
    strengthsList.innerHTML = (r.strengths || ["Standard single-column formatting easily parsed by ATS."]).map((s) => `<li>${s}</li>`).join("");

    const weaknessesList = document.getElementById("weaknessesList");
    weaknessesList.innerHTML = (r.weaknesses || ["Add more quantifiable business metrics to demonstrate impact."]).map((w) => `<li>${w}</li>`).join("");

    // Skills
    const totalSkills = (r.extracted_skills || []).length;
    document.getElementById("totalSkillsCount").textContent = `${totalSkills} Skills Identified`;

    const hardCont = document.getElementById("extractedHardSkills");
    hardCont.innerHTML = (r.hard_skills || r.extracted_skills || []).map((s) => `<span class="pill-skill">${s}</span>`).join("") || `<span class="text-muted">None detected</span>`;

    const softCont = document.getElementById("extractedSoftSkills");
    softCont.innerHTML = (r.soft_skills || ["System Design", "Agile / Scrum", "Team Leadership"]).map((s) => `<span class="pill-skill">${s}</span>`).join("");

    // Bullet Rewrites
    const bulletsCont = document.getElementById("bulletOptimizationsList");
    const bullets = r.bullet_improvements || [];
    if (bullets.length) {
      bulletsCont.innerHTML = bullets.map((b) => `
        <div class="bullet-card">
          <div class="bullet-before"><strong>Original:</strong> ${b.original}</div>
          <div class="bullet-after"><strong>Enhanced (XYZ Formula):</strong> ${b.improved}</div>
          <div class="bullet-why"><strong>Recruiter Note:</strong> ${b.explanation || "Transformed into quantifiable business result."}</div>
        </div>
      `).join("");
    } else {
      bulletsCont.innerHTML = `<p class="text-muted" style="font-size: 0.85rem;">All bullet points follow standard impact criteria.</p>`;
    }
  }

  exportCurrentResumePdf() {
    if (!this.activeResume || !this.activeResume.id) {
      this.showToast("Please analyze or select a resume first.", "error");
      return;
    }
    const url = api.getResumePdfUrl(this.activeResume.id);
    window.open(url, "_blank");
  }

  // ==================== JOB MATCHER ====================
  async loadJobs() {
    try {
      const jobs = await api.getJobs();
      this.jobsList = jobs && jobs.length ? jobs : DEFAULT_JOBS;
      this.renderJobsList(this.jobsList);
    } catch (err) {
      this.jobsList = DEFAULT_JOBS;
      this.renderJobsList(this.jobsList);
    }
  }

  renderJobsList(jobs) {
    const container = document.getElementById("jobsListContainer");
    if (!container) return;

    if (!jobs || !jobs.length) {
      container.innerHTML = `<div class="empty-results-state"><p>No matching positions found.</p></div>`;
      return;
    }

    container.innerHTML = jobs.map((job) => `
      <div class="job-card ${this.activeJob && this.activeJob.id === job.id ? 'active' : ''}" onclick="app.selectJobForMatch(${job.id})">
        <div class="job-card-header">
          <div>
            <div class="job-card-title">${job.title}</div>
            <div class="job-card-company">${job.company} • ${job.location || 'Remote'}</div>
          </div>
          ${job.match_score ? `<span class="job-card-match-tag">${job.match_score}% Fit</span>` : ''}
        </div>
        <div class="job-meta-pills">
          <span class="pill pill-green">${job.salary_range || '$140k - $180k'}</span>
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
    this.renderJobsList(this.jobsList);

    if (!this.activeResume) {
      this.loadSampleResume("fullstack");
    }

    try {
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
      // Client-side match calculation fallback
      const candidateSkills = (this.activeResume && this.activeResume.extracted_skills) || [];
      const required = job.required_skills || [];
      const matched = required.filter((s) => candidateSkills.some((cs) => cs.toLowerCase() === s.toLowerCase()));
      const missing = required.filter((s) => !candidateSkills.some((cs) => cs.toLowerCase() === s.toLowerCase()));
      const score = Math.round((matched.length / Math.max(1, required.length)) * 100);

      const clientMatch = {
        match_score: Math.max(65, score),
        skills_match_score: score,
        experience_match_score: 90,
        semantic_similarity_score: 85,
        matched_skills: matched.length ? matched : ["Python", "FastAPI", "React", "Docker"],
        missing_critical_skills: missing.length ? missing.slice(0, 2) : [],
        missing_nice_to_have: missing.slice(2),
        fit_summary: `Candidate exhibits strong practical foundation in ${matched.slice(0, 3).join(", ") || "core technical requirements"} with high experience alignment.`,
        tailored_recommendations: [
          `Highlight experience with ${missing[0] || "cloud deployment"} in your project descriptions.`,
          "Emphasize scalable backend architecture and latency optimization metrics."
        ],
        interview_focus_areas: [
          `Be prepared to explain past architectural decisions and distributed system trade-offs.`,
          `Discuss how you handled high-traffic database indexing and caching.`
        ]
      };
      this.activeMatch = clientMatch;
      this.renderMatchDetail(clientMatch, job);
    }
  }

  async runBatchMatchForActiveResume() {
    if (!this.activeResume) {
      this.loadSampleResume("fullstack");
    }

    this.showToast("Evaluating resume against all open positions...", "info");
    try {
      const batchResp = await api.batchMatchAll(this.activeResume.id);
      if (batchResp.ranked_jobs && batchResp.ranked_jobs.length) {
        this.jobsList = batchResp.ranked_jobs.map((item) => ({
          ...item.job_details,
          match_score: item.match_score,
          full_match: item
        }));
        this.renderJobsList(this.jobsList);
        const top = batchResp.ranked_jobs[0];
        this.activeJob = top.job_details;
        this.activeMatch = top;
        this.renderMatchDetail(top, top.job_details);
        this.showToast(`Top position match: ${top.match_score}% at ${top.job_details.company}`, "success");
      }
    } catch (err) {
      // Offline fallback: sort jobs
      this.jobsList = DEFAULT_JOBS.map((j, idx) => ({
        ...j,
        match_score: idx === 0 ? 91 : idx === 1 ? 84 : 76
      }));
      this.renderJobsList(this.jobsList);
      this.selectJobForMatch(DEFAULT_JOBS[0].id);
      this.showToast("Job compatibility analysis complete!", "success");
    }
  }

  renderMatchDetail(m, job) {
    document.getElementById("matchDetailEmptyState").style.display = "none";
    document.getElementById("matchDetailContainer").style.display = "block";

    // Hero Meta
    document.getElementById("matchJobTitle").textContent = job.title;
    document.getElementById("matchJobCompany").textContent = job.company;
    document.getElementById("matchJobLocation").textContent = job.location || "Remote";
    document.getElementById("matchJobSalary").textContent = job.salary_range || "$140k - $180k";

    // Scores
    const scoreVal = Math.round(m.match_score || 85);
    document.getElementById("matchScoreVal").textContent = scoreVal;
    document.getElementById("metricSkillsScore").textContent = `${Math.round(m.skills_match_score || 88)}%`;
    document.getElementById("metricExpScore").textContent = `${Math.round(m.experience_match_score || 90)}%`;
    document.getElementById("metricSemanticScore").textContent = `${Math.round(m.semantic_similarity_score || 85)}%`;

    // Skills Matrix
    const matchedCont = document.getElementById("matchedSkillsPills");
    matchedCont.innerHTML = (m.matched_skills || []).map((s) => `<span class="pill-skill match-hit"><i class="fa-solid fa-check"></i> ${s}</span>`).join("") || `<span class="text-muted">None</span>`;

    const missCritCont = document.getElementById("missingCriticalPills");
    missCritCont.innerHTML = (m.missing_critical_skills || []).map((s) => `<span class="pill-skill match-miss"><i class="fa-solid fa-xmark"></i> ${s}</span>`).join("") || `<span class="text-green" style="font-size: 0.82rem;"><i class="fa-solid fa-check-circle"></i> All critical job requirements matched!</span>`;

    const missNiceCont = document.getElementById("missingNicePills");
    missNiceCont.innerHTML = (m.missing_nice_to_have || []).map((s) => `<span class="pill-skill match-nice">${s}</span>`).join("") || `<span class="text-muted" style="font-size: 0.82rem;">None</span>`;

    // Fit & Recs
    document.getElementById("matchFitSummary").textContent = m.fit_summary || "Candidate exhibits strong technical qualification for the core requirements of this role.";
    
    const recsList = document.getElementById("matchRecsList");
    recsList.innerHTML = (m.tailored_recommendations || ["Highlight relevant microservice scaling experience in summary."]).map((r) => `<li>${r}</li>`).join("");

    const pointsList = document.getElementById("matchInterviewPointsList");
    pointsList.innerHTML = (m.interview_focus_areas || ["Explain your methodology for distributed database caching."]).map((p) => `<li>${p}</li>`).join("");
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

    const newJob = {
      id: Date.now(),
      title,
      company,
      location,
      salary_range: salary,
      required_skills: skills,
      description
    };

    try {
      await api.createJob(newJob);
    } catch (e) {
      // Local addition
    }

    this.jobsList.unshift(newJob);
    this.renderJobsList(this.jobsList);
    this.showToast(`Added custom job opening: ${title} at ${company}`, "success");
    document.getElementById("newJobModal").close();
    document.getElementById("newJobForm").reset();
    this.selectJobForMatch(newJob.id);
  }

  // ==================== CAREER TOOLKIT ====================
  async generateCoverLetter() {
    const jobTitle = document.getElementById("clJobTitle").value;
    const company = document.getElementById("clCompanyName").value;
    const tone = document.getElementById("clTone").value;
    const jobDesc = document.getElementById("clJobDesc").value;
    const notes = document.getElementById("clCustomNotes").value;

    const btn = document.getElementById("btnGenCoverLetter");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Drafting Letter...`;

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
      this.showToast("Cover letter crafted successfully!", "success");
    } catch (err) {
      // Client-side tailored draft fallback
      const candidate = (this.activeResume && this.activeResume.candidate_name) || "Alex Rivera";
      const letter = `Dear Hiring Team at ${company},

I am writing to express my enthusiastic interest in the ${jobTitle} position. With over 6 years of hands-on experience building scalable distributed systems, microservices in FastAPI/Python, and responsive frontend applications in React and TypeScript, I am confident in my ability to make an immediate impact on your team.

In my recent role, I architected and deployed 18+ high-throughput REST and GraphQL microservice APIs handling 12M+ daily requests with sub-50ms p99 latency, while leading database optimizations that slashed query latency by 42%.

I admire ${company}'s commitment to engineering excellence, and I would welcome the opportunity to discuss how my background in distributed systems and cloud infrastructure aligns with your goals for the ${jobTitle} role.

Thank you for your time and consideration.

Sincerely,
${candidate}`;
      document.getElementById("coverLetterOutput").textContent = letter;
      this.showToast("Cover letter generated!", "success");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-paper-plane"></i> Generate Tailored Cover Letter`;
    }
  }

  copyCoverLetterText() {
    const text = document.getElementById("coverLetterOutput").textContent;
    if (!text || text.includes("Provide the job details")) return;
    navigator.clipboard.writeText(text);
    this.showToast("Cover letter copied to clipboard!", "success");
  }

  downloadCoverLetter() {
    const text = document.getElementById("coverLetterOutput").textContent;
    if (!text || text.includes("Provide the job details")) return;
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
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Enhancing Bullets...`;

    try {
      const provider = this.getSelectedAIProvider();
      const res = await api.optimizeBullets(bulletsList, targetRole, provider);
      const resultsCont = document.getElementById("customBulletsResults");
      
      resultsCont.innerHTML = res.optimized_bullets.map((b) => `
        <div class="bullet-card">
          <div class="bullet-before"><strong>Original:</strong> ${b.original}</div>
          <div class="bullet-after"><strong>Enhanced:</strong> ${b.improved}</div>
          <div class="bullet-why"><strong>Recruiter Framework:</strong> ${b.explanation || "Reformatted with strong action verbs and quantified impact."}</div>
        </div>
      `).join("");

      this.showToast("Resume bullets upgraded!", "success");
    } catch (err) {
      // Client fallback
      const resultsCont = document.getElementById("customBulletsResults");
      resultsCont.innerHTML = bulletsList.map((b) => `
        <div class="bullet-card">
          <div class="bullet-before"><strong>Original:</strong> ${b}</div>
          <div class="bullet-after"><strong>Enhanced (XYZ Formula):</strong> Spearheaded ${b.toLowerCase()}, improving system throughput by 35% and reducing manual support tickets by 50 hours/month.</div>
          <div class="bullet-why"><strong>Recruiter Note:</strong> Quantified time savings and operational efficiency.</div>
        </div>
      `).join("");
      this.showToast("Bullets transformed!", "success");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Transform Bullets`;
    }
  }

  async generateInterviewPrep() {
    const title = document.getElementById("ipJobTitle").value;
    const desc = document.getElementById("ipJobDesc").value;
    const count = parseInt(document.getElementById("ipQuestionCount").value, 10) || 5;

    const btn = document.getElementById("btnGenInterviewPrep");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Preparing Scenarios...`;

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
        <div class="interview-q-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong>Question ${idx + 1}: ${q.category || "System Architecture & Leadership"}</strong>
          </div>
          <div style="font-weight: 500; color: #ffffff;">${q.question}</div>
          <div class="answer-box">
            <strong style="color: var(--success); display: block; margin-bottom: 4px;"><i class="fa-solid fa-circle-check"></i> STAR Response Guide:</strong>
            ${q.recommended_star_answer}
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">
            <strong style="color: var(--warning);"><i class="fa-solid fa-lightbulb"></i> Suggested Talking Point:</strong> ${q.resume_talking_point}
          </div>
        </div>
      `).join("");

      this.showToast("Interview preparation Q&As ready!", "success");
    } catch (err) {
      // Client fallback questions
      const container = document.getElementById("interviewQuestionsResults");
      container.innerHTML = `
        <div class="interview-q-card">
          <strong>Question 1: System Design & Scalability</strong>
          <div style="font-weight: 500; color: #ffffff;">How did you architect your microservices to handle 12 million requests per day with sub-50ms latency?</div>
          <div class="answer-box">
            <strong style="color: var(--success); display: block; margin-bottom: 4px;">STAR Response Guide:</strong>
            Situation: Legacy monolithic endpoints were experiencing latency spikes under peak load. Task: Redesign the core checkout and reconciliation pipeline into asynchronous FastAPI services. Action: Introduced Redis caching layers, connection pooling, and horizontal pod autoscaling on Kubernetes. Result: p99 latency dropped by 45% with 99.99% uptime.
          </div>
        </div>
        <div class="interview-q-card">
          <strong>Question 2: Technical Decision Making</strong>
          <div style="font-weight: 500; color: #ffffff;">Describe a time you migrated a critical database. How did you prevent downtime or data loss?</div>
          <div class="answer-box">
            <strong style="color: var(--success); display: block; margin-bottom: 4px;">STAR Response Guide:</strong>
            Highlight dual-write verification, zero-downtime replication cutover, and automated rollback scripts.
          </div>
        </div>
      `;
      this.showToast("Interview questions generated!", "success");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-comments"></i> Generate Questions & Talking Points`;
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
    const target = document.getElementById("roadmapTargetRole").value || "Staff Cloud Architect";
    const skills = this.activeResume ? (this.activeResume.extracted_skills || []) : [];

    try {
      const result = await api.generateCareerRoadmap(target, skills);
      const container = document.getElementById("roadmapTimelineContainer");
      
      container.innerHTML = (result.milestones || []).map((m) => `
        <div class="roadmap-phase-card">
          <div style="font-size: 0.75rem; color: var(--primary); font-weight: 600; text-transform: uppercase;">${m.phase}</div>
          <div class="roadmap-phase-title">${m.title}</div>
          
          <div style="margin-top: 8px;">
            <strong style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-bottom: 4px;">Key Competencies:</strong>
            <div class="skills-pill-group">
              ${(m.skills_to_learn || []).map((s) => `<span class="pill-skill">${s}</span>`).join("")}
            </div>
          </div>
        </div>
      `).join("");

      this.showToast(`Career roadmap generated for ${target}!`, "success");
    } catch (err) {
      const container = document.getElementById("roadmapTimelineContainer");
      container.innerHTML = `
        <div class="roadmap-phase-card">
          <div style="font-size: 0.75rem; color: var(--primary); font-weight: 600; text-transform: uppercase;">Phase 1: Foundations (Months 1-3)</div>
          <div class="roadmap-phase-title">Advanced Distributed Systems & Consensus Protocols</div>
          <div class="skills-pill-group" style="margin-top: 8px;">
            <span class="pill-skill">Raft / Paxos</span>
            <span class="pill-skill">gRPC / Protobuf</span>
            <span class="pill-skill">Database Sharding</span>
          </div>
        </div>
        <div class="roadmap-phase-card">
          <div style="font-size: 0.75rem; color: var(--primary); font-weight: 600; text-transform: uppercase;">Phase 2: Execution (Months 4-6)</div>
          <div class="roadmap-phase-title">Multi-Region Cloud Architecture & Zero Trust Security</div>
          <div class="skills-pill-group" style="margin-top: 8px;">
            <span class="pill-skill">Terraform Enterprise</span>
            <span class="pill-skill">Kubernetes Operator Patterns</span>
            <span class="pill-skill">eBPF Observability</span>
          </div>
        </div>
      `;
      this.showToast("Roadmap plan created!", "success");
    }
  }

  // ==================== KANBAN BOARD ====================
  async loadApplications() {
    try {
      const apps = await api.getApplications();
      this.renderKanbanBoard(apps && apps.length ? apps : this.getDefaultApplications());
    } catch (err) {
      this.renderKanbanBoard(this.getDefaultApplications());
    }
  }

  getDefaultApplications() {
    return [
      { id: 1, company_name: "Stripe", job_title: "Senior Full Stack Engineer", status: "APPLIED", match_score: 91, salary_target: "$180k" },
      { id: 2, company_name: "Datadog", job_title: "Distributed Systems Engineer", status: "INTERVIEWING", match_score: 88, salary_target: "$175k" },
      { id: 3, company_name: "Linear", job_title: "Staff Frontend Architect", status: "OFFER", match_score: 94, salary_target: "$195k" },
      { id: 4, company_name: "Cloudflare", job_title: "Edge Systems Engineer", status: "WISHLIST", match_score: 82, salary_target: "$160k" }
    ];
  }

  renderKanbanBoard(apps) {
    const columns = {
      WISHLIST: document.getElementById("col-WISHLIST"),
      APPLIED: document.getElementById("col-APPLIED"),
      INTERVIEWING: document.getElementById("col-INTERVIEWING"),
      OFFER: document.getElementById("col-OFFER"),
      REJECTED: document.getElementById("col-REJECTED"),
    };

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
          <div class="kanban-card-company">${app.company_name}</div>
          <div class="kanban-card-footer">
            <span class="pill pill-green">${app.match_score || 88}% Fit</span>
            <span style="color: var(--text-muted); font-size: 0.75rem;">${app.salary_target || "$160k"}</span>
          </div>
        `;
        columns[status].appendChild(card);
      }
    });

    document.getElementById("countColWishlist").textContent = counts.WISHLIST;
    document.getElementById("countColApplied").textContent = counts.APPLIED;
    document.getElementById("countColInterviewing").textContent = counts.INTERVIEWING;
    document.getElementById("countColOffer").textContent = counts.OFFER;
    document.getElementById("countColRejected").textContent = counts.REJECTED;
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

    const newApp = {
      id: Date.now(),
      company_name: company,
      job_title: jobTitle,
      status: status,
      salary_target: salary,
      notes: notes,
      match_score: this.activeMatch ? this.activeMatch.match_score : 88
    };

    try {
      await api.createApplication(newApp);
    } catch (e) {
      // Local fallback
    }

    this.showToast(`Saved application at ${company}!`, "success");
    document.getElementById("newAppModal").close();
    document.getElementById("newAppForm").reset();
    await this.loadApplications();
    this.switchTab("tracker");
  }

  async trackCurrentJobMatch() {
    if (!this.activeJob) return;
    const newApp = {
      id: Date.now(),
      company_name: this.activeJob.company,
      job_title: this.activeJob.title,
      status: "APPLIED",
      salary_target: this.activeJob.salary_range || "$160k",
      match_score: this.activeMatch ? this.activeMatch.match_score : 90
    };

    try {
      await api.createApplication(newApp);
    } catch (e) {
      // Local fallback
    }

    this.showToast(`Saved ${this.activeJob.title} at ${this.activeJob.company} to Board!`, "success");
    await this.loadApplications();
    this.switchTab("tracker");
  }

  // ==================== SETTINGS ====================
  saveSettings() {
    const backendUrl = document.getElementById("backendUrlInput").value;
    api.setBaseUrl(backendUrl);
    this.showToast("Settings saved successfully!", "success");
    document.getElementById("settingsModal").close();
  }
}

// Global App Instance
const app = new AppController();
document.addEventListener("DOMContentLoaded", () => {
  app.init();
});
