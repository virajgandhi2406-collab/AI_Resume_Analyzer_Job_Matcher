"""
Comprehensive Skill Taxonomy and Keyword Dictionaries for Resume Analysis & Job Matching
"""

SKILL_TAXONOMY = {
    # Programming Languages
    "languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "golang", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "sql", "html", "css", "bash", "shell", "powershell"
    ],
    
    # Frontend Technologies
    "frontend": [
        "react", "react.js", "reactjs", "vue", "vue.js", "angular", "next.js", "nextjs", "nuxt.js", "svelte",
        "tailwind css", "tailwindcss", "bootstrap", "sass", "scss", "redux", "zustand", "graphql", "webpack", "vite"
    ],
    
    # Backend Frameworks & APIs
    "backend": [
        "fastapi", "flask", "django", "express", "express.js", "nestjs", "node.js", "nodejs",
        "spring boot", "springboot", "asp.net", "ruby on rails", "laravel", "gin", "grpc", "rest api", "restful api", "microservices"
    ],
    
    # Databases & Caching
    "databases": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
        "cassandra", "dynamodb", "neo4j", "supabase", "firebase", "mariadb", "snowflake", "oracle"
    ],
    
    # Cloud & DevOps & Infra
    "cloud_devops": [
        "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes", "k8s",
        "terraform", "ansible", "jenkins", "github actions", "gitlab ci", "ci/cd", "helm", "linux", "nginx", "prometheus", "grafana"
    ],
    
    # AI / Machine Learning / Data Science
    "ai_ml_data": [
        "machine learning", "deep learning", "nlp", "natural language processing", "llm", "large language models",
        "generative ai", "genai", "pytorch", "tensorflow", "scikit-learn", "keras", "hugging face", "huggingface",
        "langchain", "llamaindex", "openai", "transformers", "pandas", "numpy", "matplotlib", "seaborn", "opencv",
        "vector database", "rag", "fine-tuning", "bert", "prompt engineering", "spark", "pyspark", "hadoop", "airflow"
    ],
    
    # System Design & Architecture
    "architecture": [
        "system design", "microservices architecture", "event-driven architecture", "distributed systems",
        "scalability", "load balancing", "caching strategies", "design patterns", "clean architecture", "domain-driven design"
    ],
    
    # Soft Skills & Professional Attributes
    "soft_skills": [
        "leadership", "communication", "teamwork", "problem solving", "critical thinking", "adaptability",
        "time management", "mentoring", "cross-functional collaboration", "agile", "scrum", "project management",
        "stakeholder management", "analytical skills", "conflict resolution", "creativity"
    ]
}

# Strong action verbs favored by ATS scanners and recruiters (XYZ formula)
ACTION_VERBS = {
    "achievement": ["accomplished", "achieved", "delivered", "exceeded", "generated", "maximized", "outperformed", "surpassed"],
    "leadership": ["led", "managed", "spearheaded", "directed", "orchestrated", "mentored", "supervised", "pioneered"],
    "technical": ["architected", "engineered", "developed", "built", "implemented", "deployed", "refactored", "optimized", "integrated"],
    "problem_solving": ["resolved", "diagnosed", "troubleshot", "overhauled", "streamlined", "automated", "modernized"],
    "collaboration": ["collaborated", "partnered", "coordinated", "facilitated", "negotiated"]
}

# Skill Alias Normalization Map
SKILL_ALIASES = {
    "react.js": "React",
    "reactjs": "React",
    "react": "React",
    "vue.js": "Vue",
    "vuejs": "Vue",
    "vue": "Vue",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "golang": "Go",
    "go": "Go",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "docker": "Docker",
    "fastapi": "FastAPI",
    "tailwind css": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "natural language processing": "NLP",
    "nlp": "NLP",
    "llm": "LLMs",
    "large language models": "LLMs",
    "generative ai": "Generative AI",
    "genai": "Generative AI",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "ci/cd": "CI/CD",
    "rest api": "REST APIs",
    "restful api": "REST APIs",
    "microservices": "Microservices"
}

def normalize_skill(skill_raw: str) -> str:
    """Normalize raw skill term to canonical formatted string"""
    cleaned = skill_raw.strip().lower()
    if cleaned in SKILL_ALIASES:
        return SKILL_ALIASES[cleaned]
    return skill_raw.strip().title()

def get_all_hard_skills() -> list:
    """Retrieve flattened list of all technical/hard skills"""
    hard_skills = []
    for category in ["languages", "frontend", "backend", "databases", "cloud_devops", "ai_ml_data", "architecture"]:
        hard_skills.extend(SKILL_TAXONOMY[category])
    return hard_skills

def get_all_soft_skills() -> list:
    """Retrieve all soft skills"""
    return SKILL_TAXONOMY["soft_skills"]
