# From Prototype to Production: How Perk Built a Voice AI Agent That Makes 10,000 Calls a Week

Источник: https://www.producttalk.org/from-prototype-to-production-how-perk-built-a-voice-ai-agent-that-makes-10-000-calls-a-week/

Listen to this episode on: Spotify | Apple Podcasts
What happens when you combine a real customer problem, a no-code prototype, and a team willing to listen to every single call?
In this episode of Just Now Possible, Teresa Torres talks with Steven Payne (Product Manager), Gabriel Stock (Senior Engineering Manager), and Philipe Steiff (Senior Software Engineer) from Perk—a company that helps businesses eliminate "shadow work" like travel booking and expense management. They share how they built a voice AI agent that calls hotels to verify virtual credit card payments, preventing travelers from arriving to find their rooms unpaid.
What started as a hackathon experiment in Make.com became a production system handling over 10,000 calls per week across multiple languages. Along the way, the team learned hard lessons about prompt engineering for voice (numbers, pronunciation, and a very "Karen-like" first version), how to break a single monolithic prompt into structured conversation stages, and why listening to actual calls beats any amount of theorizing.
You'll hear how they:
- Built a working prototype without writing a single line of backend code
- Structured the call into discrete stages (IVR, booking confirmation, payment) to improve reliability
- Created two eval systems: one for call success classification, another for conversational behavior
- Scaled from five calls a day to tens of thousands per week while maintaining quality
This is a detailed look at building AI for real-time human interaction—where the stakes are high and the feedback is immediate.
Show Notes
Guests
- Steven Payne, Product Manager, Perk
- Gabriel Stock, Senior Engineering Manager, Perk
- Philipe Steiff, Senior Software Engineer, Perk
What we cover in this episode
- How Perk's team identified an AI use case by connecting prior experimentation with a real operational problem
- Why they chose Make.com for prototyping—and shipped to production without touching backend code
- The evolution from a single prompt to structured conversation stages (IVR handling, booking confirmation, payment request)
- How breaking up the agent's task dramatically improved reliability
- Building two eval systems: classification for success rates and LLM-as-judge for conversational behavior
- Why the team still listens to calls manually even with automated metrics
- The challenge of prompt engineering for voice: numbers, booking references, and text-to-speech markup
- Lessons learned from expanding to German (prompts in native language improve results)
- How this project uncovered other operational problems they didn't know existed
Resources & Links
- Perk
- Make.com – No-code automation platform used for the prototype
- Twilio – Voice/telephony provider
- Eleven Labs – Text-to-speech provider (used in early experiments)
Chapters
00:00 Introduction to the Team
01:54 Understanding PERK's Mission
02:59 Challenges in Travel Booking
07:27 AI Solutions for Customer Care
09:52 Prototyping with AI and Voice
17:00 Implementing AI in Production
25:51 Learning Through Trial and Error
26:40 Prompting Challenges and Solutions
27:58 Iterating on Prompts and Evaluations
30:08 Scaling and Production Challenges
32:43 Advanced Evaluation Techniques
35:32 Real-World Applications and Success
49:07 Future Directions and Expansion
53:53 Conclusion and Team Reflections
Full Transcript
Podcast transcripts are only available to paid subscribers.
