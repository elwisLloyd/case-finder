# How we are using AI in Mercado Libre’s accessibility team

Источник: https://medium.com/mercadolibre-tech/how-we-are-using-ai-in-mercado-libres-accessibility-team-e960b83283a9

How we are using AI in Mercado Libre’s accessibility team
AI isn’t here to replace accessibility work — it’s here to make it stronger.
Today, our accessibility team faces a challenge: supporting hundreds of designers and developers with questions, reviews, and continuous improvements. To scale this impact, we’re exploring how artificial intelligence (AI) can help us automate tasks, provide immediate answers, and foster collective learning.
That’s why we’ve launched several initiatives to speed up work, increase independence, and strengthen execution capacity.
Note: In many of these initiatives, we rely on automatization tools available in our internal development ecosystem, Fury.
The A11Y assistant for everyday work
How does it work?
This assistant:
- Activates when mentioned in the support channel.
- Processes both messages and screen images.
- Consults internal documentation, training materials, historical queries, previously reported accessibility tickets, and our design system.
- Uses a large language model (LLM) with Retrieval-Augmented Generation (RAG) to deliver reliable answers.
The result: contextualized responses grounded in internal resources and standards. From the query initiation to gathering additional context, and finally to delivering a response backed by verified information, the entire pipeline is crucial. This approach helps avoid “hallucinations” (invented or incorrect answers) and ensures the A11Y assistant stays focused on trusted resources. Thus, it provides solutions and resources that are not only accurate but also directly applicable and aligned with Mercado Libre’s internal accessibility standards and tools.
Understanding problems better to deliver better solutions
One of our biggest learnings is that teams need information that’s clear and easy to understand — not just technical reports.
In manual accessibility audits, we provide technical details such as assistive technologies used, reproduction steps, and affected WCAG (Web Content Accessibility Guidelines) criteria. While useful, this level of detail can be overwhelming for those not deeply familiar with accessibility.
That’s where AI comes in. For each generated ticket, AI automatically adds a contextual note covering three key aspects:
- Technical impact explained in user terms: A short, clear description of the problem — not just “this is wrong,” but why it’s wrong from a user-experience perspective.
- Suggestions or recommendations: Concrete guidance, such as code examples or references, always framed within our knowledge base and design patterns.
- How to verify the fix: Accessibility, like any bug, must be tested. To flatten the learning curve, AI provides the tools and exact steps to validate the correction.
Real example: In a search ticket, the “Skip to results” link was missing. AI explained the impact on keyboard users, suggested the correct code based on our guidelines, and listed the steps needed to verify the change.
For automated tools like Axe, which detect accessibility errors via rules, we enrich the detected issues with AI-generated context. This adds practical details that help developers better understand the problem in the HTML where it appears.
Each additional piece of context we provide significantly scales understanding without requiring constant involvement from the accessibility team (though we’re always available when needed). At the same time, this empowers development teams to become more autonomous in solving accessibility issues.
The accessibility notes assistant for handoffs
To bring accessibility into the UI design phase, we created an assistant that helps UX teams identify and add accessibility specifications in their handoffs.
Get Martín Di Luzio’s stories in your inbox
Join Medium for free to get updates from this writer.
Starting from a screen image (desktop web or native mobile), the assistant analyzes the visual context and platform type. It then generates a descriptive visual map, detailing the elements on the screen and recommending annotations based on our accessibility notes for Figma.
The assistant’s prompt focuses on explaining, in simple and clear terms, how to annotate components like headers, links, buttons, groups, or dynamic areas. The emphasis is on semantic specifications rather than technical implementation.
This tool resolves common doubts and helps teams incorporate accessibility independently, ensuring more complete and inclusive design deliveries. For now, responses are text-only since they’re far more accurate than image-based annotations.
Assisted reviews of resolved issues
Our team conducts weekly reviews of resolved accessibility tickets to validate fixes and learn from applied solutions. To scale this process and reduce manual review time, we developed an automation that integrates Jira, GitHub, and an AI agent.
What does this flow do?
- Pulls all accessibility tickets resolved that day.
- Breaks down each ticket into key information.
- Instructs the AI agent to:
- Analyze ticket comments and solution evidence.
- Identify linked GitHub pull requests (PRs) and review their technical content.
- Assess the clarity, relevance, and documentation of the solution.
- Classifies the ticket with a traffic-light emoji (🟢 green, 🟡 yellow, 🔴 red) based on fix quality.
- Stores the results in a shared spreadsheet.
Why is this useful?
This workflow filters which tickets need additional manual review, allowing us to focus our team’s time. With an agent aware of both ticket context and code details, we can:
- Automatically flag tickets lacking sufficient technical evidence.
- Objectively classify fix reliability.
- Request targeted information from teams when needed.
- Centralize the analysis in a shared dashboard.
Next steps: shifting accessibility left
Our goal is to bring accessibility further left into the early stages of the product development lifecycle. This means preventing issues before they arise, integrating smoothly into design and development workflows, and leveraging emerging paradigms like Vibe Coding.
Here, Fury, our internal development platform, plays a key role in scaling, securing, and centralizing these AI agents.
Conclusion
These initiatives show that AI doesn’t replace accessibility experts — it multiplies them. By automating responses, enriching tickets, and supporting teams, we gain time to focus on the next strategic challenges.
As accessibility professionals, we must actively engage with AI initiatives by testing, experimenting, discovering, and encouraging its responsible use so it benefits everyone.
A special shout-out to Rocío Ruiz, Julieta Natali Navazo, Manuela Sánchez Marino, and Guilherme Zangarini, among others, who are leading the way in AI and accessibility explorations at Mercado Libre.
If you work in tech, we invite you to experiment with AI and accessibility in your processes. Share your learnings, and let’s build a more inclusive community together.
