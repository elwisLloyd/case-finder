# Transforming wholesale with AI: the sequel (now with more agents)

Источник: https://craft.faire.com/transforming-wholesale-with-ai-the-sequel-now-with-more-agents-9542f257dd45

Featured
Transforming wholesale with AI: the sequel (now with more agents)
How we’re advancing search and discovery for our customers, and more
On September 9, 2025, we opened our doors at Faire Waterloo for a two-part evening during Waterloo Tech Week: a fireside chat with two of our senior engineering leaders, followed by a series of lightning tech talks from the teams building AI into our marketplace.
You can watch a recording, and here are the highlights!
AI north star: solving real customer challenges
Faire’s mission is to empower brands and retailers to strengthen the unique character of local communities. That mission comes alive when we solve real, tractable problems our customers face. AI is one tool in our toolkit. Some key ways it can help are:
- Helping retailers find unique products: Buyers want to discover differentiated brands that fit their shop’s vibe, without needing to guess the right keywords.
- Providing personalized recommendations: Retailers expect curated assortments and insights tailored to their business.
- Delivering more value to all of our customers: Wholesale often depends on manual workflows and multiple tools — there’s an opportunity to simplify and create a smoother experience.
These needs shape our roadmap and where we apply AI — both externally for our customers, and internally to improve our systems and processes that ultimately serve our customers.
Supercharging developer productivity with AI tooling
If you’ve read our Toronto Tech Week recap, you know we believe AI augments engineers. In Waterloo, our speakers dug into what that looks like in practice:
Agentic development
Luke Bjerring shared how background coding agents take on well-scoped tasks (creating pull requests, writing tests, refactoring), so engineers can focus on harder problems. We walked through how we invoke GitHub Copilot programmatically, tailor instructions and setup, and wire in MCP servers to internal systems.
Project Cyberpunk
George Jacob presented our in‑house agentic development stack, aka Project Cyberpunk: pre‑warmed workspaces, a lightweight orchestrator that breaks work into reliable prompts, and a library of focused sub‑agents (e.g., settings cleanup, test authoring). Early usage patterns show steady adoption and meaningful offload on repetitive work.
Practical tips for mobile and more
Megan Bosiljevac presented real cases, from an Android UI color accessibility fix to scaffolding an 800‑line Server‑Driven UI screen in hours instead of days, and a reminder that prompting is a skill, experimentation compounds, and humans remain owners of the code.
Transforming discovery for retailers
There are several ways we’re applying AI to transform discovery for retailers, including:
Get Dave Collie’s stories in your inbox
Join Medium for free to get updates from this writer.
Natural‑language search: Tom Ma explained that buyers should be able to ask for what they want on our platform, similar to how they would speak to a rep: “Find me dresses made in Paris, under $100, and not sold on Amazon.” Our system parses the phrase into structured filters under the hood and returns relevant products without the filter‑guessing game.
Image search: Inspiration often starts with a photo. Upload an image and see visually similar products on Faire, turning a vibe into a shoppable result, especially on mobile.
Together, these capabilities reduce the distance between intent and discovery for Retailers saving them time and helping them stock their stores.
Service architecture evolution to support AI agents
Luan Nico shared Project Burrito: a hybrid architecture that pairs Python‑powered AI agents with our Kotlin macroservice “wrapper” to plan multi‑step buying flows for account managers (and many other agentic AI flows to serve our brands and retailers in the future). Instead of a one‑off search, an agent composes a coherent, purchasable assortment that fits a retailer’s profile, then iterates.
Fireside chat with Marcelo Cortes and Yvonne Luo
Similar to our Toronto Tech Week event, we ended with a fireside chat. This time, Co‑Founder & Chief Architect Marcelo Cortes was joined by Head of Engineering, Discovery, Yvonne Luo. The conversation took the following shape:
- AI as a new abstraction layer: Like cloud and mobile before it, AI changes what it means to be a product or infra team: it’s about interfaces that reason, not just route requests.
- Humans‑in‑the‑loop by design: Guardrails, observability, and explicit failure modes matter, especially when agents touch customer‑facing systems.
- Audience Q&A: We took questions from the crowd about Faire’s security stance, growth strategy, and culture.
Thank you, Waterloo 💙
We loved hosting builders, students, and community partners at our Waterloo office. A huge thanks to everyone who helped make the evening happen, and to our guests for the thoughtful questions during Q&A. If you didn’t catch us this time, we hope to see you at a future event at our Waterloo, Toronto, or San Francisco office!
Want to build with us? Explore roles at faire.com/careers and follow along on The Craft.
