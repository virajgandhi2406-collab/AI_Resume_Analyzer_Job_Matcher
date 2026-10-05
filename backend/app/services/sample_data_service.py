from sqlalchemy.orm import Session
from app.models.job import Job

SAMPLE_JOBS = [
    {
        "title": "Senior AI / Machine Learning Engineer",
        "company": "Anthropic AI Labs",
        "logo_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&auto=format&fit=crop&q=80",
        "location": "San Francisco, CA (Remote)",
        "job_type": "Full-time",
        "workplace_type": "Remote",
        "experience_level": "Senior",
        "min_experience_years": 4,
        "salary_range": "$160,000 - $215,000",
        "description": "We are seeking a Senior AI/ML Engineer to build LLM pipelines, RAG architectures, and fine-tuning infrastructure. You will work on productionizing generative AI models with high throughput and low latency.",
        "responsibilities": [
            "Architect and optimize high-concurrency LLM inference microservices using FastAPI and PyTorch.",
            "Design vector search retrieval pipelines with LangChain, LlamaIndex, and Qdrant/Pinecone.",
            "Implement automated evaluation benchmarks and guardrail telemetry for model outputs.",
            "Collaborate with frontend engineers to build dynamic AI streaming experiences."
        ],
        "requirements": [
            "4+ years experience in Python, PyTorch, Transformers, and LLM development.",
            "Proven track record deploying machine learning models into production environments.",
            "Deep understanding of embeddings, semantic search, and RAG architectures."
        ],
        "required_skills": ["Python", "PyTorch", "LLMs", "FastAPI", "NLP", "Docker", "PostgreSQL", "LangChain"],
        "preferred_skills": ["Kubernetes", "Vector Database", "AWS", "Redis", "TypeScript"],
        "industry": "Artificial Intelligence",
        "source": "Featured"
    },
    {
        "title": "Full Stack Software Engineer (React & FastAPI/Node)",
        "company": "Stripe Tech Ventures",
        "logo_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=120&auto=format&fit=crop&q=80",
        "location": "New York, NY (Hybrid)",
        "job_type": "Full-time",
        "workplace_type": "Hybrid",
        "experience_level": "Mid-Level",
        "min_experience_years": 3,
        "salary_range": "$135,000 - $175,000",
        "description": "Join our core product team building high-performance fintech applications. You will own features end-to-end from responsive React interfaces to scalable Python/FastAPI microservices and PostgreSQL databases.",
        "responsibilities": [
            "Build intuitive, accessible UI dashboards using React, Vite, and Tailwind CSS.",
            "Develop clean RESTful and GraphQL APIs with FastAPI, SQLAlchemy, and PostgreSQL.",
            "Ensure 99.9% uptime with robust automated tests, CI/CD pipelines, and observability."
        ],
        "requirements": [
            "3+ years experience with React, TypeScript/JavaScript, and modern state management.",
            "Strong backend development in Python (FastAPI/Django) or Node.js.",
            "Hands-on database modeling and query optimization with PostgreSQL."
        ],
        "required_skills": ["React", "JavaScript", "TypeScript", "Python", "FastAPI", "PostgreSQL", "Tailwind CSS", "REST APIs"],
        "preferred_skills": ["Docker", "Redis", "Next.js", "CI/CD", "AWS"],
        "industry": "Fintech & SaaS",
        "source": "Featured"
    },
    {
        "title": "Backend Systems & Cloud Engineer",
        "company": "Databricks Cloud Platform",
        "logo_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=120&auto=format&fit=crop&q=80",
        "location": "Seattle, WA (Remote)",
        "job_type": "Full-time",
        "workplace_type": "Remote",
        "experience_level": "Senior",
        "min_experience_years": 5,
        "salary_range": "$170,000 - $225,000",
        "description": "Architect mission-critical distributed data pipelines and cloud microservices. Focus on low-latency caching, database sharding, and container orchestration across multi-cloud environments.",
        "responsibilities": [
            "Lead architecture for distributed ingestion engines processing millions of events per second.",
            "Deploy and manage infrastructure as code with Terraform, Docker, and Kubernetes.",
            "Optimize PostgreSQL connection pooling, indexes, and caching strategies with Redis."
        ],
        "requirements": [
            "5+ years backend engineering in Python, Go, or Java.",
            "Deep expertise with PostgreSQL, Redis, and distributed systems architecture.",
            "Strong DevOps experience with Docker, Kubernetes, and AWS/GCP."
        ],
        "required_skills": ["Python", "PostgreSQL", "Docker", "Kubernetes", "AWS", "Redis", "Microservices", "CI/CD"],
        "preferred_skills": ["Go", "Terraform", "Kafka", "Elasticsearch", "System Design"],
        "industry": "Cloud Infrastructure",
        "source": "Featured"
    },
    {
        "title": "Lead Frontend React Architect",
        "company": "Vercel Ecosystems",
        "logo_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=120&auto=format&fit=crop&q=80",
        "location": "Austin, TX (Remote)",
        "job_type": "Full-time",
        "workplace_type": "Remote",
        "experience_level": "Lead",
        "min_experience_years": 6,
        "salary_range": "$175,000 - $230,000",
        "description": "Looking for a Frontend Architect to pioneer state-of-the-art developer experiences, component design systems, and lightning-fast web applications.",
        "responsibilities": [
            "Architect reusable component design systems used across hundreds of thousands of users.",
            "Champion web performance optimization (Core Web Vitals, SSR, streaming rendering).",
            "Mentor engineering teams on modern React patterns, state management, and testing."
        ],
        "requirements": [
            "6+ years frontend engineering with React, Next.js, and TypeScript.",
            "Expert understanding of browser rendering engines, modern CSS, and web performance.",
            "Proven leadership and mentoring track record."
        ],
        "required_skills": ["React", "TypeScript", "Next.js", "JavaScript", "Tailwind CSS", "GraphQL", "Vite"],
        "preferred_skills": ["Node.js", "Jest", "Framer Motion", "Docker"],
        "industry": "Developer Tools",
        "source": "Featured"
    },
    {
        "title": "Data Scientist & Predictive Analytics Lead",
        "company": "BioHealth Analytics",
        "logo_url": "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?w=120&auto=format&fit=crop&q=80",
        "location": "Boston, MA (Hybrid)",
        "job_type": "Full-time",
        "workplace_type": "Hybrid",
        "experience_level": "Mid-Senior",
        "min_experience_years": 3,
        "salary_range": "$140,000 - $185,000",
        "description": "Build predictive machine learning models, statistical analysis pipelines, and clinical data insights utilizing Python, Scikit-learn, and Pandas.",
        "responsibilities": [
            "Develop, validate, and deploy predictive classification and regression models.",
            "Perform statistical exploratory data analysis on multi-terabyte datasets.",
            "Communicate insights and model performance to clinical and executive stakeholders."
        ],
        "requirements": [
            "3+ years experience with Python, Scikit-Learn, Pandas, and SQL.",
            "Solid foundation in statistics, probability, and machine learning principles.",
            "Experience with data visualization (Matplotlib, Seaborn, Tableau)."
        ],
        "required_skills": ["Python", "Machine Learning", "Scikit-Learn", "Pandas", "NumPy", "SQL", "PostgreSQL"],
        "preferred_skills": ["PyTorch", "Airflow", "Docker", "AWS"],
        "industry": "Healthcare & Biotech",
        "source": "Featured"
    }
]

def seed_sample_jobs(db: Session):
    """Seed sample jobs if table is empty"""
    count = db.query(Job).count()
    if count == 0:
        for job_data in SAMPLE_JOBS:
            job = Job(**job_data)
            db.add(job)
        db.commit()
