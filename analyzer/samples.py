"""
Sample resumes and matching job descriptions for instant testing.
"""

SAMPLES = {
    "fullstack": {
        "id": "fullstack",
        "title": "Senior Full Stack Engineer",
        "role_category": "Software Engineering",
        "short_desc": "TypeScript, React, Node.js, Next.js, PostgreSQL, AWS Cloud Architecture",
        "resume": """ALEX CHEN
San Francisco, CA • alex.chen@example.com • (555) 349-2041 • linkedin.com/in/alexchen-dev • github.com/alexchen

PROFESSIONAL SUMMARY
Senior Full Stack Engineer with 6+ years of experience architecting resilient cloud-native web applications, distributed microservices, and high-conversion client interfaces. Proven track record reducing API latency by 45% and leading cross-functional teams of 8 engineers. Specializes in TypeScript, React, Next.js, Node.js, and AWS.

CORE TECHNICAL SKILLS
• Languages: TypeScript, JavaScript (ES6+), Python, SQL, HTML5, CSS3
• Frontend: React, Next.js, Redux Toolkit, Tailwind CSS, Webpack, Responsive Design, Web Vitals
• Backend: Node.js, Express, NestJS, RESTful APIs, GraphQL, Microservices
• Databases & Caching: PostgreSQL, MongoDB, Redis, Prisma ORM
• Cloud & DevOps: AWS (ECS, S3, CloudFront, Lambda), Docker, GitHub Actions CI/CD, Terraform
• Testing & Quality: Jest, React Testing Library, Cypress, Vitest, TDD
• Methodologies: Agile/Scrum, System Design, Code Reviews, Cross-functional Mentorship

PROFESSIONAL EXPERIENCE

Senior Full Stack Software Engineer | Horizon Fintech Solutions
San Francisco, CA | 2022 – Present
• Architected a real-time portfolio management dashboard serving 250,000+ active users using Next.js 14, React, and TypeScript.
• Redesigned distributed backend transaction microservices using Node.js and PostgreSQL, decreasing p99 response times from 340ms to 85ms.
• Implemented automated CI/CD deployment pipelines using GitHub Actions and AWS ECS, boosting release frequency by 3x and eliminating downtime.
• Integrated Stripe payment gateways and Plaid financial APIs, processing over $40M in annual automated recurring billing.
• Mentored 5 mid-level and junior software engineers through structured 1-on-1s and code review standards.

Full Stack Engineer | CloudScale Systems
San Jose, CA | 2019 – 2022
• Developed reusable React UI component library used across 6 internal enterprise products, cutting frontend feature development time by 30%.
• Built high-throughput REST APIs and asynchronous background task queues with Node.js, Redis, and BullMQ.
• Migrated legacy monolithic MySQL database schema to optimized PostgreSQL with zero data loss or customer disruption.
• Maintained 92% automated test coverage across core billing engines using Jest and Cypress end-to-end testing suites.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley (2015 – 2019)
Dean's Honor List • GPA 3.82 / 4.0

CERTIFICATIONS
• AWS Certified Solutions Architect – Associate (2023)
""",
        "job_description": """Position: Senior Full Stack Engineer (Cloud & Web Platforms)
Company: Apex Innovations
Location: San Francisco, CA / Remote

About the Role:
We are looking for a passionate Senior Full Stack Engineer to build and scale our next-generation enterprise SaaS collaboration platform. You will design mission-critical customer-facing web applications and distributed backend microservices that handle millions of daily events.

Key Responsibilities:
• Build modern, high-performance web applications using React, TypeScript, and Next.js.
• Design robust, secure RESTful and GraphQL APIs using Node.js and modern database systems (PostgreSQL, Redis).
• Deploy, monitor, and scale cloud infrastructure on AWS (Docker, ECS, CloudFront, Terraform).
• Drive end-to-end architectural decisions, code reviews, and automated CI/CD testing pipelines.
• Collaborate closely with product managers, UX designers, and security engineers to deliver high-impact features on tight iterations.
• Mentor junior engineers and advocate for software engineering best practices.

Requirements & Qualifications:
• 5+ years of full-stack software development experience building production SaaS applications.
• Deep proficiency in TypeScript, React, and modern state management.
• Strong hands-on backend expertise with Node.js, Express/NestJS, and SQL relational databases (PostgreSQL preferred).
• Solid understanding of cloud infrastructure (AWS), containerization (Docker), and automated CI/CD pipelines.
• Experience with unit and integration testing (Jest, Cypress, or Vitest).
• Excellent communication skills, empathetic team leadership, and product mindset.
• Experience with Kafka or message brokers is a strong plus.
"""
    },
    "product_manager": {
        "id": "product_manager",
        "title": "Technical Product Manager",
        "role_category": "Product Management",
        "short_desc": "Product Roadmap, A/B Testing, User Research, Agile, SaaS Metrics (ARR, Retention)",
        "resume": """SARAH JENNINGS
New York, NY • sarah.jennings@example.com • (555) 812-9430 • linkedin.com/in/sarahjennings-pm

EXECUTIVE SUMMARY
Strategic and data-driven Technical Product Manager with 5+ years of experience leading cross-functional teams to build enterprise B2B SaaS products. Demonstrated success scaling products from 0 to $12M ARR, increasing user retention by 28%, and driving customer-led innovation through rigorous user discovery and quantitative experimentation.

AREAS OF EXPERTISE
• Product Strategy & Roadmapping: OKRs, PRDs, Opportunity Solution Trees, Go-to-Market (GTM)
• Data & Analytics: SQL, Amplitude, Mixpanel, Tableau, Google Analytics, A/B Testing
• Agile Execution: Scrum Master, Jira, Linear, Sprint Planning, Backlog Grooming, Release Management
• User Research & Design: User Interviews, Wireframing, Figma, Usability Testing, Customer Journey Mapping
• Technical Acumen: REST APIs, System Architecture basics, Webhooks, Data Pipelines, AI/ML Product workflows

PROFESSIONAL EXPERIENCE

Senior Product Manager | DataFlow Technologies
New York, NY | 2022 – Present
• Spearheaded product vision and roadmap for DataFlow's core automated workflow engine, driving $8.5M in net-new ARR in FY2023.
• Partnered with engineering leads to prioritize technical debt vs feature requests, delivering 14 major quarterly releases with 98% on-time milestone delivery.
• Designed and launched multi-channel notification service, improving enterprise user 30-day retention from 61% to 78%.
• Conducted 80+ customer discovery interviews with VP-level stakeholders to identify friction points and validate high-impact roadmap bets.

Product Manager | Omnia SaaS Solutions
Boston, MA | 2019 – 2022
• Managed end-to-end lifecycle of self-serve onboarding flow, increasing trial-to-paid conversion rate by 34% through rapid A/B testing cycles.
• Authored comprehensive PRDs and user stories in Jira for a squad of 10 engineers and 2 UX designers.
• Built executive-facing dashboards in Tableau and Amplitude tracking DAU/MAU, CAC, LTV, and feature adoption funnels.

EDUCATION
Bachelor of Science in Business Administration & Information Systems | Boston University (2015 – 2019)
Magna Cum Laude

CERTIFICATIONS
• Pragmatic Institute Certified (PMC-III)
• Certified Scrum Product Owner (CSPO)
""",
        "job_description": """Role: Lead Technical Product Manager - Enterprise AI Platforms
Company: Nexus Enterprise Software
Location: New York, NY / Hybrid

Overview:
Nexus is seeking an experienced Lead Technical Product Manager to oversee our AI-assisted automation suite. You will bridge the gap between enterprise customers, engineering teams, and machine learning researchers to deliver generative workflow tools.

What You Will Do:
• Define product vision, 12-month strategy, and quarterly roadmap for enterprise automation capabilities.
• Work hand-in-hand with engineering squads, data scientists, and designers to translate complex customer needs into clear PRDs.
• Establish product telemetry, North Star metrics, and experiment frameworks using Amplitude or Mixpanel.
• Lead enterprise customer advisory councils and synthesize qualitative user feedback into actionable backlog priorities.
• Partner with Sales and Product Marketing on pricing, packaging, and Go-to-Market launch execution.

What We Are Looking For:
• 4+ years of product management experience in B2B SaaS or technical software platforms.
• Strong analytical foundation: proficiency in SQL, cohort analysis, and statistical A/B testing methodologies.
• Demonstrated ability to communicate complex technical concepts with engineers, data teams, and C-level executive stakeholders.
• Hands-on experience with Agile/Scrum methodologies, PRD documentation, and roadmapping tools (Jira, Linear).
• Prior experience with AI, Machine Learning integrations, or developer-facing APIs is highly preferred.
"""
    },
    "data_science": {
        "id": "data_science",
        "title": "Junior Data Analyst → Machine Learning Role",
        "role_category": "Data & AI Transition",
        "short_desc": "Demonstrates clear skill gap analysis (Excel/SQL → PyTorch, MLOps, Deep Learning)",
        "resume": """DAVID PATEL
Chicago, IL • david.patel@example.com • (555) 438-9921 • linkedin.com/in/davidpatel-data

OBJECTIVE
Motivated Data Analyst with 2 years of experience analyzing business metrics, building BI dashboards, and writing SQL queries. Seeking to transition into Machine Learning and Predictive Analytics to leverage data modeling skills.

SKILLS
• Languages: Python (Pandas, NumPy, Matplotlib), SQL (PostgreSQL, MySQL), Excel (VLOOKUP, Pivot Tables)
• BI Tools: Power BI, Tableau
• Statistics: Descriptive Statistics, Linear Regression, Hypothesis Testing
• Version Control: Git, GitHub

WORK EXPERIENCE

Data Analyst | Midwest Retail Analytics
Chicago, IL | 2022 – Present
• Created automated weekly sales reports in Tableau, saving 6 hours of manual spreadsheet compiling per week.
• Queried enterprise PostgreSQL databases to extract transactional data across 120 retail store locations.
• Conducted cohort retention analysis and churn rate calculations for customer loyalty programs.
• Built basic exploratory data analysis (EDA) scripts in Python to spot seasonal inventory discrepancies.

Junior Reporting Specialist | Apex Logistics
Chicago, IL | 2021 – 2022
• Maintained inventory spreadsheets and verified shipment log accuracy for 500+ monthly shipments.
• Created executive presentations and chart visualizations in PowerPoint and Excel.

EDUCATION
Bachelor of Science in Statistics | University of Illinois at Chicago (2017 – 2021)
""",
        "job_description": """Position: Machine Learning Engineer (Predictive Systems)
Company: Cortex Intelligence Labs
Location: Chicago, IL / Remote

About the Team:
Cortex Intelligence Labs builds real-time machine learning inference systems for high-frequency financial and demand-forecasting applications.

Responsibilities:
• Architect, train, and deploy production machine learning models using PyTorch, Scikit-Learn, and XGBoost.
• Build scalable data feature pipelines and batch inference workflows using Apache Spark, Docker, and Kubernetes.
• Implement MLOps best practices: automated experiment tracking (MLflow, Weights & Biases), model drift monitoring, and CI/CD for ML.
• Optimize model latency and throughput on GPU clusters for real-time streaming data.
• Collaborate with backend engineers to integrate ML models into microservice APIs.

Requirements:
• 3+ years of professional experience building and deploying machine learning pipelines in production.
• Strong programming skills in Python, PyTorch or TensorFlow, and C++ (preferred).
• Proven track record with distributed data processing (Spark, Kafka) and cloud containerization (Docker, Kubernetes, AWS/GCP).
• Solid understanding of deep learning architectures, time-series forecasting, and model evaluation metrics (AUC, F1, RMSE).
• Experience with MLOps frameworks like MLflow or Kubeflow.
"""
    }
}
