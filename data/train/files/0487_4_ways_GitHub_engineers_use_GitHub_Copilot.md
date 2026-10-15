# 4 ways GitHub engineers use GitHub Copilot

Источник: https://github.blog/2024-04-09-4-ways-github-engineers-use-github-copilot/

Just recently, I was coding a new feature for GitHub Copilot Chat. My task was to enable the chat to recognize a user’s project dependencies, allowing it to provide magical answers when the user poses a question. While I could have easily listed the project dependencies and considered the task complete, I knew that to extract top-notch responses from these large language models, I needed to be careful to not overload the prompt to avoid confusing the model by providing too much context. This meant pre-processing the dependency list and selecting the most relevant ones to include in the chat prompt.
Creating machine-processable formats for the most prominent frameworks across various programming languages would have consumed days. It was during this time that I experienced one of those “Copilot moments.”
I simply queried the chat in my IDE:
Look at the data structure I have selected and create at least 10 examples that conform to the data structure. The data should cover the most prominent frameworks for the Go programming language.
Voilà, there it was my initial batch of machine-processable dependencies. Just 30 minutes later, I had amassed a comprehensive collection of significant dependencies for nearly all supported languages, complete with parameterized unit tests. Completing a task that would likely have taken days without GitHub Copilot, in just 30 minutes, was truly remarkable.
This led me to ponder: what other “Copilot moments” might my colleagues here at GitHub have experienced? Thus, here are a few ways we use GitHub Copilot at GitHub.
Semi-automating repetitive tasks is a topic that resonates with a colleague of mine from another team. He mentions that they are tasked with developing and maintaining several live services, many of which utilize protocol buffers for data communication. During maintenance, they often encounter a situation where they need to increment ID numbers in the protobuf definitions, as illustrated in the code snippet below:
protobuf
google.protobuf.StringValue fetcher = 130
  [(opts.cts_opt)={src:"Properties" key:"fetcher"}];
google.protobuf.StringValue proxy_enabled = 131
  [(opts.cts_opt)={src:"Properties" key:"proxy_enabled"}];
google.protobuf.StringValue proxy_auth = 132
  [(opts.cts_opt)={src:"Properties" key:"proxy_auth"}];
He particularly appreciates having GitHub Copilot completions in the editor for these tasks. It serves as a significant time saver, eliminating the need to manually generate ID numbers. Instead, one can simply tab through the completion suggestions until the task is complete.
Here’s another intriguing use case I heard about from a colleague. He needed to devise a regular expression to capture a Markdown code block and extract the language identifier. Fully immersed in his work, he preferred not to interrupt his flow by switching to chat, even though it could have provided a solution. Instead, he employed a creative approach by formalizing his task in a code comment:
// The string above contains a code block with a language identifier.
// Create a regexp that matches the code block and captures the language 
identifier.
// Use tagged capture groups for the language and the code. 
This prompted GitHub Copilot to generate the regular expression as the subsequent statement in his editor:
const re = /```(?<lang>\w+)(?<code>[\s\S]+?)```/;
With the comment deleted, the task was swiftly accomplished!
During a pleasant coffee chat, one of our support engineers shared an incident she experienced with a colleague last week. It was a Friday afternoon, and they were attempting to troubleshoot an issue for a specific customer. Eventually, they pinpointed the solution by creating various notes in VSCode. At GitHub, we prioritize remote collaboration. Thus, merely resolving the task wasn’t sufficient; it was also essential to inform our colleagues about the process to ensure the best possible experience for future customer requests. Consequently, even after completing this exhaustive task, they needed to document how they arrived at the solution.
She initiated GitHub Copilot Chat and simply typed something along the lines of, “Organize my notes, structure them, and compile the data in the editor into Markdown tables.” Within seconds, the task was completed, allowing them to commence their well-deserved weekend.
Enhancing and acquiring new skills are integral aspects of every engineer’s journey. John Berryman, a colleague of mine, undertook the challenge of leveraging GitHub Copilot to tackle a non-trivial coding task in a completely unfamiliar programming language. His goal was to delve into Rust, so on a Sunday, he embarked on this endeavor with the assistance of GitHub Copilot Chat. The task he set out to accomplish was to develop a program capable of converting any numerical input into its written English equivalent. While initially seeming straightforward, this task presented various complexities such as handling teen numbers, naming conventions for tens, placement of “and” in the output, and more.
Twenty-three minutes and nine seconds later, he successfully produced a functional version written in Rust, despite having no prior experience with the language. Notably, he documented his entire process, recording himself throughout the endeavor.
I found it incredibly enlightening to discover how my fellow Hubbers utilize GitHub Copilot, and their innovative approaches inspired me to incorporate some of their ideas into my daily workflows. If you’re eager to explore GitHub Copilot firsthand, getting started is a breeze. Simply install it into your preferred editor and ask away.
Tags:
Written by
Related posts
Developers are owning more of the delivery system around code, not just code itself. Join us during GitHub Universe to meet other devs, learn something new, and explore what’s next.
