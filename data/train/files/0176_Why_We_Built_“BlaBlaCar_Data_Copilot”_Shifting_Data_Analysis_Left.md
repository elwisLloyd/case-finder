# Why We Built “BlaBlaCar Data Copilot”: Shifting Data Analysis Left

Источник: https://medium.com/blablacar/why-we-built-blablacar-data-copilot-shifting-data-analysis-left-b4cc246faf52

Why We Built “BlaBlaCar Data Copilot”: Shifting Data Analysis Left
At BlaBlaCar, we have always believed in the power of shared journeys. Usually, that refers to a driver and a passenger sharing a ride to Paris or Brest. But recently, we noticed another journey that was far less efficient: the one between our Software Engineers (SWE) and our Data Analysts (DA).For years, a continuous white line stood between these two groups, a strict boundary that neither side felt safe crossing.
- The SWE holds the keys to the production code and has deep domain context (“I know exactly when this booking_request event is fired”). But they often treat the Data Warehouse as a black box, blocked by complex SQL dialects, DBT syntax and Airflow operators.
- The DA holds the keys to the insights. But they are often buried under a mountain of “quick questions”. To keep up, they are forced to constantly rebuild business logic into ad-hoc, easy-to-query structures just to get an answer out the door. This results in a sprawl of unmaintainable spaghetti SQL scattered across connected sheets and notebooks.
This disconnect is ironic. Most Software Engineers possess mathematical backgrounds and analytical training, often exceeding the technical requirements of a typical business query. They shouldn’t be afraid of running analysis. The barrier isn’t a lack of skill; it is the friction of unfamiliar tooling, the fear of “doing it wrong” without a safety net, and the organizational silos that make it difficult to cross the line between engineering and data teams.
We realized that to scale our data culture, we didn’t need more dashboards. We needed to Shift Left. We needed to give Software Engineers the tools to answer their own team questions, safely, accurately, and with the rigorous standards of code.
The Philosophy: Why Shift Data Left?
“Shifting Left” is a concept borrowed from the world of DevOps. In software delivery, it means moving critical tasks (like testing and security) earlier in the process, closer to the person writing the code.
In the context of data, the logic is identical.
- The Old Way (Right): Data Analysts discover data quality issues or business logic errors after the feature is in production and the data has landed in the warehouse. Fixing these errors downstream is expensive, slow, and reactive.
- The New Way (Left): Software Engineers validate data and answer questions while they are releasing the feature.
For the Data Analyst, shifting left is releasing them from the never ending Run tasks. Instead of acting as human search engines for basic questions, they evolve into data mentors and architects, reviewing complex pull requests and critical analysis, designing the key performance indicator, running challenging cohort and A/B tests analysis, reviewing complex pull requests, and focusing on high-leverage modeling.
By enabling this shift, we are not just improving velocity; we are operationalizing the Data Mesh. We are empowering domain teams to truly own their data products, treating data quality as an upstream engineering constraint rather than a downstream analytics problem.
The Ecotone: Thriving at the Interface
In ecology, an ecotone is the transition zone between two biological communities (like an estuary where the river meets the sea, or the marshlands at the edge of a forest). While these areas can be chaotic, they are often the most diverse and productive ecosystems on the planet.
We found that the same principle applies to our engineering culture.
The greatest value doesn’t always come from being the absolute best Java developer or the most advanced statistician. Often, the most impactful innovations happen at the interface: the messy, complex boundary between Software Engineering and Data Analysis.
Historically, thriving in this “data ecotone” was difficult. It required an individual to be in the top 20% of both fields. But Large Language Models (LLMs) have changed the equation.
LLMs excel at translation and synthesis. They allow us to inhabit this interface without needing to master every nuance of the opposing discipline. By positioning our Data Copilot exactly at this edge, we are generating great value with remarkably simple, existing tools. We aren’t building a complex new platform; we are simply using AI to bridge the gap, allowing our teams to thrive in the interface between code and data.
The Junior Analyst in Your IDE
Most Text-to-SQL tools on the market today are designed for business users, replacing the analyst with a chat bot. We took a different approach. We built a tool designed explicitly for Engineers, living where they live: In the IDE.
BlaBlaCar Data Copilot is an AI-powered extension that tunnels securely into our BigQuery environment, removing the need for the dreaded BigQuery Console. It acts less like a vending machine for answers and more like a Junior Analyst riding shotgun while the engineer drives.
1. Context Over Syntax
Generic AI assistants know SQL syntax, but they don’t know our business. They don’t know that a “search intent” is defined differently in 2024 than it was in 2022.
Our Copilot has access to a set of curated queries, those used in our production DBT models and verified reporting, as well as a preview of each table the users have permissions on. When an engineer asks, “Show me the driver churn rate,” the Copilot doesn’t hallucinate a definition. It retrieves the logic used by our Data Team from the curated example queries and table, bridging the gap between raw data and business reality.
2. The Data Health Card: Linter for Logic
In software, we have linters to catch syntax errors. In data, a query can be syntactically perfect but analytically disastrous. Our Copilot solves this by generating a Data Health Card alongside every analysis. It runs heuristic checks providing a Soft Warning system. This allows engineers to move fast while passively learning to spot bad data patterns without being blocked.
3. Insights as transparent Artifacts
Unlike standard BI tools that hide logic behind drag-and-drop interfaces, Our Data Copilot treats analysis as artifacts generated by a unique composition of Code and LLM.
Get Thomas Pocreau’s stories in your inbox
Join Medium for free to get updates from this writer.
The AI doesn’t just deliver a static chart; it generates the raw SQL and Python code required to build it. This yields exceptional results for our power users, allowing them to open the hood, interact with the logic, and modify the SQL or Python parameters at any time. The analysis remains fluid and transparent.
4. Insights as Pull Requests
Perhaps the biggest shift is cultural. In the old world, an analysis was a screenshot of a chart pasted into Slack. It was ephemeral, unverified, and hard to reproduce.
With Data Copilot, every analysis is generated as a Python script with auto-generated Unit Tests (assertions).
- The Engineer commits the script.
- The Data Analyst reviews the Pull Request.
- The DA doesn’t just see a chart; they see the code and the passing tests.
This transforms the DA from a Query Factory into a Reviewer and Guide. They spend less time writing SELECT * and more time guiding engineers toward rigorous analytical standards.
5. Repository as Memory
One of the greatest frustrations in data analysis is the amnesiac workflow: an analysis is done, shared, and then lost in Slack history, only to be redone from scratch six months later.
Because Data Copilot treats analysis as code, every insight is committed to a central repository. This creates a powerful positive feedback loop. The Copilot indexes every merged Pull Request, meaning the repository effectively becomes its long-term memory.
- Never Start from Zero: If an engineer asks a question similar to one answered last quarter, the Copilot can surface the original script as a starting point.
- One-Prompt Refreshes: Old analyses aren’t dead artifacts; they can be pulled, re-run against live data, and updated in minutes.
- Composable Knowledge: A complex segmentation logic built by a Senior DA for one project becomes a reusable module for an SWE’s future query.
The Architecture
Why This Works: The “Zero-Infrastructure” RAG
The beauty of BlaBlaCar Data Copilot lies in its simplicity. We bypass complex infrastructure like vector databases or separate ‘Model Context Protocol’ (MCP) servers. Instead, we leverage the native capabilities of the engineer’s existing environment.
A lightweight Python script bridges BigQuery and the IDE. It exports key context, schema definitions, Golden queries, and table samples, into standard text files (Markdown, SQL, JSON) directly within the project’s repository. Because these are simply files in the workspace, they are automatically indexed by VS Code, making them instantaneously available to GitHub Copilot.
The real magic happens in the interaction. When an engineer asks, ‘How do I calculate monthly active users?’, Copilot activates VS Code’s built-in toolset to retrieve the answer:
- It triggers #codebase to perform a semantic search across the workspace, identifying the intent behind the query.
- It utilizes #textSearch to scan for literal string matches within the generated documentation.
- It surfaces files like tables/kpis_mau/usage.sql or tables/carpool_members/ddl.sql and injects their content directly into the chat context.
By placing the right knowledge directly in the IDE’s line of sight, we effectively transform a standard code completion tool into an expert data analyst — without writing a single line of custom AI code.
The Impact: Velocity & Trust
Since launching BlaBlaCar Data Copilot, we’ve seen two major shifts:
- Engineers are Autonomous: Questions that used to sit in a Jira backlog for 3 weeks are now answered in 10 minutes inside VS Code. Engineers are using data to validate feature ideas before they build them.
- Analysts are Scalable: Freed from the support queue, our DAs are focusing on deep-dive modeling and improving the core data platform.
We believe the future of data isn’t just about democratizing access. By giving Software Engineers the safety net they need to explore data, we aren’t just building better charts, we’re building a stronger engineering culture.
Try It Yourself
We believe this problem isn’t unique to BlaBlaCar. That is why we have built an Open Source version of our Data Copilot that everyone can use. All you need is a Github Copilot licence with access to premium models.
This lightweight version allows you to connect to BigQuery sample datasets or to your own Data Warehouse and start asking questions.
We invite you to fork it, break it, and help us build the bridge across the ecotone.
