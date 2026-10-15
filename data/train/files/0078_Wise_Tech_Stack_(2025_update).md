# Wise Tech Stack (2025 update)

Источник: https://medium.com/wise-engineering/wise-tech-stack-2025-update-d0e63fe718c7

Wise Engineering
As of the financial year 2025, Wise supports 15.6 million active customers, moving approximately £36 billion across borders each quarter. Approximately 65% of our transfers arrive instantly, and our Wise Platform facilitates payments for banks, financial institutions and enterprises globally. This success is driven by our technology-first approach, robust architecture, and dedicated engineering teams.
How we work at Wise
Wise has more than 850 engineers working across key global locations, organised into independent squads and tribes. These teams are empowered to innovate and make decisions independently, fostering transparency, trust, and collaboration.
This article follows our Tech Stack 2022 to cover the most recent improvements in Wise’s tech stack that enable us to achieve our mission of money without borders — instant, convenient, transparent and eventually free.
Moving money with Wise
Our web and mobile applications
Our web applications are built using CRAB (a Wise-specific abstraction on top of the popular Next.js framework) and comprises of 40 distinct apps, each handling specific product functions making deployments safer and more manageable.
One of the biggest changes has been in our testing methodology. We’ve adopted Storybook for visualising individual React components during development. Storybook pairs really well with Chromatic which captures snapshots after each change and can highlight the visual differences in the component. These snapshots are very effective for catching visual regressions during code changes which helps us prevent bugs from reaching our customers.
Wise mobile app: faster, smarter, and more efficient
Our iOS engineers have upgraded our infrastructure by migrating 250+ Xcode modules from Xcodegen to Tuist and switching from Cocoapods to Swift Package Manager (SPM), unlocking improvements in caching for builds. The team also improved flexibility, reducing zero-change build times from 28s to 2s. Development is smoother than ever now with the advanced build caching.
Our Android engineers remain focused on developing apps at scale. Our primary Android repository contains over 300 Gradle modules and roughly 1 million lines of code, comprising 2 production apps, 6 sample apps, 17 JVM modules, 221 Android modules, and 65 multiplatform modules. Our efforts to improve Android development velocity focus on these key themes:
- Using more BFFs to share code logic between Android, iOS, and web teams.
- Development of code generation tools built on KSP.
- Exploring applications of Kotlin Multiplatform.
On the user interface side, we’ve completely moved to Compose — first for our design system, and now for entire screens and navigation. We stay current with technology, quickly adopting Kotlin 2.0 and 2.1 when they were released. For handling asynchronous tasks we use Coroutines and Flows, while our architecture adheres to the standard MVVM patterns and is supported by Google’s Jetpack libraries.
Backend services
Wise runs on over 1000 services in total. In the backend we are primarily using Java and Kotlin. Since our last update, we have focused on automation and efficiency by developing in-house tools that improve development velocity and provide standard libraries to use across different services.
Building great applications faster
Since our last update, we have been focusing on enabling engineering at scale with automated code updates and scalable dependency management solutions. For this, we have:
- Introduced an in-house microservice chassis framework, built on the principle of minimal configuration and shipped as an artifact, allowing us to build standard micro services faster. It configures common capabilities that services use with a recommended defaults: security, observability, database communication, working with Kafka, and more, allowing teams to focus on business logic.
- Improved standardisation of build pipelines through an in-house collection of Gradle plugins. A notable example is our plugin that standardises GitHub Actions workflows. This enables organisation-wide workflow changes through simple plugin version updates, making initiatives like SLSA rollout effortless across our 700+ Java repositories.
- Introduced a language-agnostic automation service that enables us to make complex changes to the codebase at scale and create pull requests for the owning team to review. Using this service, we took our centralised Java dependency management platform a step further by automating dependency upgrades for Java services.
Directly integrating with local payment schemes
We went live with InstaPay, the instant payments system in the Philippines and were granted access to join Zengin, Japan’s instant payments system. We also received access to PIX in Brazil.
At Wise we put substantial effort into creating the most consistent architecture possible, with networking centralised using AWS Transit Gateways. There is substantial variance between the details of the integrations with physical data centres required in the UK, Hungary and Australia. Our Australian data centres were one of the first deployments of AWS Outpost Servers, allowing us to maintain consistent AWS tooling across as much of our infrastructure as possible.
Allowing businesses to use our API
Our public API allows businesses to integrate Wise’s cross-border payment services directly, using secure REST APIs backed by OAuth authentication. This provides businesses with functionality for transfers, currency exchange, and account management, along with comprehensive documentation and developer tools to streamline the integration process.
Wise Platform supports over 40 currencies and multiple payment routes, delivering seamless, globally connected solutions. The platform includes built-in compliance features, allowing for seamless cross-border operations while tapping into Wise’s extensive global infrastructure.
Scaling Wise’s infrastructure platform
To accommodate rapid growth, we’ve focused on rebuilding our infrastructure to ensure efficiency and flexibility while reducing operational burdens on our teams.
Introducing our new Kubernetes-backed Compute Runtime Platform
The Compute Runtime Platform (CRP) is our new, scalable platform leveraging Kubernetes, allowing engineering teams to host applications effortlessly without managing complex infrastructure setups.
Evolving our Kubernetes stack
Since 2018, Wise has relied on Kubernetes built with Terraform, JSONNET, and ConcourseCI to support service-mesh controls (Envoy), PCI-DSS compliance, and frictionless deployments. While this model served us well, we needed a more scalable & standardised approach. This is why we introduced CRP:
- Terraform still provisions infrastructure, but we rewrote our codebase from scratch for flexibility and maintainability.
- RKE2 handles cluster bootstrapping, with Rancher managing overall cluster state.
- Helm replaces JSONNET for better maintainability and upstream compatibility.
- ArgoCD with custom plugins ensures fully automated provisioning & consistency.
- Our Envoy-powered service proxy now includes seamless integration & discovery between services, boosting flexibility, resilience, and oversight across our platform.
As a result, we’ve grown from 6 Kubernetes clusters to more than 20 while keeping maintenance manageable and efficient.
Smarter autoscaling & cost optimisation
Get Milon James’s stories in your inbox
Join Medium for free to get updates from this writer.
Alongside the ability to better provision and maintain our infrastructure, we have also introduced efficiency improvements with CRP:
- We’re building a flexible, opt-in autoscaling solution to reduce cloud costs & cognitive load for teams.
- Automated container CPU rightsizing (via Vertical Pod Autoscaler) is now live in non-production and rolling out to production for non-critical workloads.
- Fully managed sidecar containers (like Envoy proxy) now simplify deployments for product teams.
- Expanding horizontal scaling with KEDA, optimising workloads based on daily & weekly traffic patterns.
The focus on cost optimisation is helping Wise move closer to Mission Zero.
Building a scalable, reliable, and intelligent data infrastructure
A lot of what we do at Wise comes down to moving and making sense of data. Whether it’s transferring funds, updating real-time dashboards, or powering machine learning models behind the scenes, our systems are constantly processing and distributing huge volumes of information. As our global footprint grows, so does our need for faster, more secure, and more flexible ways of handling data. Below is a quick look at how we’re evolving our data tech stack to keep delivering reliable, convenient, and efficient experiences for our customers.
Powering Our Data Backbone
At Wise, our databases are one of the foundations of everything we do, so we’ve invested a lot in making them both robust and easy to manage. Behind the scenes, our database engineers are tackling fascinating technical challenges that push the boundaries of what’s possible in financial data management.
- We’ve worked hard to migrate most of our MariaDB and Postgres workloads off EC2 and into Amazon RDS. This shift has cut down on maintenance tasks, reduced operational overhead, and offered more robust security features.
- Likewise, we’re moving from self-hosted MongoDB to MongoDB Atlas, which frees us up to focus on building new features rather than wrestling with scaling.
- Redis continues to power our in-memory workloads.
- We’re also currently exploring distributed databases for greater relational scalability.
Smarter workflow orchestration & observability
- We have adopted a workflow engine called Temporal to automate critical tasks like switchovers and recovery tests. This helps us keep downtime to a minimum and stay compliant with strict regulations on resilience.
- Tools like RDS Performance Insights and Percona Monitoring and Management (PMM) give us a clear view of how our databases are doing, so we can tackle issues early.
- We’re also experimenting with using direct cloud SDKs to manage our infrastructure — moving away from Terraform Enterprise to simplify our provisioning processes.
Keeping Data in Motion
- Kafka underpins most of our real-time data movement — whether it’s asynchronous messaging between services, log collection, or streaming updates for analytics.
- Our Kafka clusters have grown significantly in capacity, and we’ve introduced features like rack-aware stand-by replicas to boost fault tolerance.
- Our in-house data movement service helps funnel information from Kafka or databases into destinations like Snowflake, S3 Parquet, Iceberg, or other targets.
- Automated checks in the configuration process reduce human error, and its growing usage shows teams are finding it simpler and faster to set up new pipelines.
- Another in-house service, Data Archives, now archives more than 100 billion records across multiple databases. This not only saves on costs but also makes our databases easier to back up and recover.
Turning Data into Insights
Teams across Wise use our Business Intelligence tools to make strategic, data-driven decisions that enhance the customer experience — from fraud detection to personalised marketing and predictive analytics.
- Although we still rely on Snowflake as a core component of our analytics, we’ve been laying the foundations of a Data Lake on Amazon S3 using Apache Iceberg. Thanks to its robust open table format, Apache Iceberg enables us to store huge amounts of data on S3 more efficiently. It lets us modify our table structures without needing to rewrite all the data, which helps our queries run faster and keeps storage costs in check. Plus, its active open source community continuously drives improvements that benefit our long-term scalability.
- Sitting between our data sources and business intelligence tools is Trino, which lets us query Iceberg tables, Snowflake, or even Kafka streams in one place.
- A new Trino gateway handles workload separation and fault-tolerant queries, while complex workflows continue to be managed by Airflow and dbt-core. For an in-depth look at this topic, watch our data engineers’ recent conference presentation.
- Reporting and dashboards are built with Looker or Superset — teams choose whichever toolset fits best.
Driving Intelligent Solutions
Our machine learning architecture is designed to support both exploration and production, seamlessly integrating ML features into products to improve customer onboarding and fraud prevention, and leveraging responsible AI tech.
- Our data scientists work in Amazon SageMaker Studio, choosing either JupyterLab or VSCode to build experiments and explore data.
- Large-scale processing happens on Spark in EMR, while Airflow orchestrates data collection, cleaning, model training, and periodic re-training to keep every step on schedule.
- We use SageMaker Feature Store to keep hundreds of features in sync for both training and inference, and MLflow tracks experiments, metrics, and model versions. This setup simplifies comparing model variants or rolling back if needed.
- When a model is ready for production, we deploy it through an in-house prediction service based on Ray Serve.
- Thanks to MLflow plugins, our data scientists can roll out models with minimal friction — speeding up inference times for fraud detection, KYC, or other use cases where every millisecond counts.
- Automated checks help catch data drift or feature inconsistencies before they turn into serious issues.
Unlocking New AI Capabilities
We’ve created a secure gateway that connects us to multiple large language model providers, including Anthropic (Claude), AWS (Bedrock), Google (Gemini), and OpenAI (gpt and o families). This approach lets us experiment with different models without juggling separate credentials or complex compliance checks. A Python library, inspired by LangChain, wraps these APIs to speed up prototyping.
For cases where we need to reference internal documents, knowledge bases, or user data, we offer a custom Retrieval-Augmented Generation (RAG) service. It pulls the latest information from various data stores before generating responses — a handy feature for summarising complex documents or automating parts of customer service workflows.
Smart Data Management
Our data architecture is both vast and complex, so we’ve built a comprehensive inventory system and a dedicated governance portal to show where data is stored and how it’s classified.
We have automated data discovery across our data estate to know what data is created; who has created it; and what is the category of the data. We are leveraging our inventory of data in data deletion, data compliance and data discovery initiatives. This setup not only supports compliance efforts for audits and regulations but also boosts developer productivity.
With more engineers joining the governance effort, we’re able to roll out stricter policies, enhanced privacy checks, and automated data lifecycle management across the board.
Developer Enablement — Evolving CI/CD at Wise
To strengthen our delivery pipeline and developer experience, we’re continuously evolving our CI/CD platform to empower developers to ship features to customers faster and more reliably than ever before.
CI Improvements: speed and security
The migration from CircleCI to Github Actions brought new possibilities for optimisation. By implementing detailed metrics tracking, we uncovered crucial insights into build performance. For example, by pre-populating caches for frequently used containers, we slashed build times by 15%. At our scale of 500K monthly builds, this translates to over 1,000 hours saved each month.
We’ve been methodically implementing the SLSA framework across our build processes, strengthening our supply-chain security one language at a time.
CD Transformation from Octopus to Spinnaker
Following up on our earlier post about the state of our CI/CD pipeline, our deployment strategy has shifted with the transition from Octopus, our in-house tool to Spinnaker. This wasn’t just a tool swap — it represented a paradigm shift from viewing deployments as simple transactions to seeing them as orchestrated sequences of events.
This transformation allowed us to reduce engineering time spent on deployment management, and to minimise the risk of defects reaching customers. This has increased developer velocity to deliver to our customers much faster, without sacrificing quality and stability.
Advanced canary testing
Spinnaker’s Automated Canary Analysis has become a cornerstone of our deployment pipeline. The process is elegant in its simplicity yet powerful in execution:
- Only 5% of traffic routes to new service versions during testing
- Comprehensive 30-minute analysis of technical and business metrics
- Automatic rollback triggers for significant anomalies
As a result, in 2024 alone this system automatically prevented hundreds of potentially incident-causing deployments and saved thousands of engineering hours.
With over half of Wise’s services now running on Spinnaker and full migration expected by mid-2025, we’re positioned to take the next step: implementing managed delivery to orchestrate the entire SDLC, including testing and data management.
LGTM stack for observability
We have improved our observability ecosystem to better monitor, understand, and optimise the Wise product. The reliability engineers are focused on building a more powerful, efficient, and insightful observability platform that addresses critical challenges in our rapidly scaling environment.
Dedicated observability infrastructure
We have implemented dedicated observability CRP clusters. This provides out-of-the-box observability for services running across different environments. As a result, we have simplified the monitoring setup and reduced manual configuration overhead.
Unified metrics and monitoring stack
To address scalability we have moved over from Thanos to Grafana Mimir. This means that we are now running fully on the LGTM stack: Loki for logs, Grafana for dashboards and visualisation, Tempo for traces and Mimir for metrics. As part of our continuous improvement in observability, we’re pilot testing Grafana Pyroscope for profiling select services, exploring new dimensions of performance insight and optimisation.
Our metrics stack is ingesting ~6 million metric samples per second and processing 150 million active series for our largest metric tenant.
By unifying our stack, we have:
- Standardised observability across our entire technology ecosystem.
- Enhanced correlation between logs, metrics, traces, and dashboards.
- Improved performance and scalability of our monitoring infrastructure.
Cost optimsation and efficiency in observability
Lastly we have continued to invest in optimising our observability stack. We have been able to reduce operational costs, improve resource utilisation and ultimately have a more sustainable long-term observability strategy. Check out our previous article that details some of the work that we did on these initiatives.
This strategic evolution empowers our engineering teams with deeper, more actionable insights while ensuring our observability infrastructure remains both powerful and cost-effective.
Conclusion
In wrapping up, our 2025 tech stack is a testament to how we’re steering the ship at Wise to provide the fastest, most reliable, and cost-effective way to move money for our 15.6 million active customers worldwide. A big focus on standardisation and integration means our systems are built to scale efficiently while ensuring robust risk and compliance management.
Our engineering teams continue to refine our infrastructure across all areas, from mobile and web applications to backend services and machine learning. These efforts simplify and accelerate how money moves across borders, ensuring we’re ready for both current demands and future growth.
We are committed to long-term investments in building the best infrastructure to move and manage the world’s money. With each technical enhancement and new direct connection to payment systems, we’re steadily progressing towards our vision of achieving Money Without Borders.
If you are curious in what we do, check our tech blog on Medium, and check out our open Engineering roles here if you wish to join our team!
I’d like to thank my colleagues who contributed to both the work described in this blog and the writing process itself. Special thanks to my team members and team lead Marta Lima, for the encouragement and for their editorial support; Sten Raudmets for the help with Frontend section; Forrest Pangborn and Dmitry Serov for mobile; Pavel Dionisev for his help on the Backend section; Ed Hargin for sharing details about the Platform Integrations; Adrian Lopez for the content and editorial support on the Data & AI/ML section; Ritesh Modi, Geno Racklin Asher and Telmo Oliveira for the help with the Data Governance & Analytics content; James Bach-Nutman for his content contribution on the Compute platform and Kubernetes; Ervin Lumberg and Doron Solomon for the updates on the CI/CD stack; Massimo Pacher for the overall encouragement and guidance; Zsofia Kiss for the assistance on employer branding and every other person who reviewed the draft and shared their feedback. Your insights and time made this blog post possible!
