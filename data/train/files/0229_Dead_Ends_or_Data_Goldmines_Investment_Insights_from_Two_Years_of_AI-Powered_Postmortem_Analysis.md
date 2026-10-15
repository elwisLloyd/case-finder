# Dead Ends or Data Goldmines? Investment Insights from Two Years of AI-Powered Postmortem Analysis

Источник: https://engineering.zalando.com/posts/2025/02/llm-migration-ui-component-libraries.html

At Zalando, we continuously seek ways to improve our processes and focus on finding efficient solutions to complex challenges by using suitable new technologies. The in-house UI library project is one practical example of how we tackled technical debt efficiently by leveraging LLMs.
Overview of migration project¶
At Zalando, I work in Partner Tech, where we focus on empowering our partners to offer their products for sale on our platform (or supply to Zalando as a retailer). As the main interface between Zalando and our partners, we develop a range of user interfaces to facilitate their day-to-day operations.
Over time, our department had developed two distinct in-house UI component libraries, each being used in different types of partner-facing applications. This fragmentation led to several challenges impacting our internal efficiency and partner experience:
- Inconsistent user experience across different partner facing applications
- Duplicated design and development efforts
- Design side complexity in maintaining two design languages
- Increased maintenance complexity for the engineering teams
- Higher onboarding time for new developers
To resolve the above challenges, we initiated a project to migrate our partner facing applications from one of the UI component libraries to the other one. The project's scope encompassed 15 sophisticated B2B applications, and due to significant differences between the source and target UI component libraries, this migration required substantial resources and time.
Given the scale and complexity of this migration, we explored various automation approaches to reduce the effort and time required. We investigated traditional approaches like javascript codemods and also wanted to explore AI technologies like Large Language Models (LLMs) given the recent advances in their capabilities.
Migration using LLMs: Getting Started¶
When we first considered using LLMs for our migration, we had several questions and concerns that needed to be resolved before committing to using a LLM for migration: Would the models understand our custom components? Could they carry out the migration with high accuracy? Is there a risk of subtle, hard-to-detect bugs being introduced? These concerns were not just theoretical – any inaccuracies in the process could have a direct impact on our partners' experience.
LLM Hackathon - Investigating Feasibility¶
To validate the feasibility of LLMs for our use case, we participated in an internal LLM hackathon organised by the Zalando research team and Tech Academy. In this hackathon developers from different teams explored various ways AI could solve engineering challenges.
Our team focused specifically on validating LLMs' potential for automated code migration and carried out multiple experiments.
Experiment Setup
To keep our experiments focused and measurable, we chose a set of sample UI components of varying complexity from simple buttons and to more complex Select components that should be migrated. We also used up a simple test application to test the accuracy of migration under realistic conditions. We adopted an iterative approach, with each experiment building on insights from previous ones.
Iterative Experiments¶
Iteration 1: Transform using Source code¶
We initially attempted direct migration by providing the source code of the components to the LLM.
## Source files
[Source files of the component in the source library]
[Source files of the component in the target library]
## Instructions
Using the source files, migrate the components  in the below file to the target library:
[...file content...]
Output: This produced inconsistent results with numerous errors.
Why it failed: Our assumption was that the migration failed possibly due to the presence of multiple complex intermediary steps. The LLM needed to understand the source code, define an interface, create a mapping between the libraries, and then migrate the test application. It struggled to handle all these steps reliably in a single pass.
Iteration 2: Transform using interface¶
We divided the process into two steps:
- Generated detailed component interfaces by providing the source code to the LLM
- Passed the component interface as context to the LLM for carrying out the migration
// Prompt 1 - interface generation
## Source files
[Source files of the component in the source library]
[Source files of the component in the target library]
## Instructions
Using the source files, generate a detailed interface of the components.
// Prompt 2 - transformation using interface
## Interface
Here's a detailed list of attributes for the Button component:
1. type: "filled" | "outlined" | "link" Default: "filled"
Defines the type of the button. "filled" is ...
2. size: "small" | "medium"
//... rest of the interface
## Transformation instructions
Migrate the usages of button components in the below file:
[...file content...]
Output: This approach still yielded low accuracy, with the LLM failing to transform several component attributes.
Why it failed: We noticed that even though the interface was detailed, it lacked essential information present in the original source code that was necessary for complete component transformation.
Iteration 3: Transform using interface and transformation instructions¶
Building on previous iterations, we combined interfaces generated above with explicit instructions on how to transform a component and all of its attributes from the source library to the target.
## Interface
[As above]
## Mapping
Instruction to migrate button
1. convert variant=primary or variant=default to type="filled"
 ...
2. convert size="small" to size= "small" and size="medium" to size="medium"
## Transformation instructions
[As above]
Output: The code was transformed with medium accuracy, but revealed flaws in the automated mapping instructions that were generated. For example, for the button component, LLM created direct size mappings (converting "medium" sized button to "medium"), when in reality, a "medium" button in the original library was visually equivalent to a "large" button in the new library.
Why it failed: There were few reasons:
- Source code cannot reveal all information, e.g. design intent or visual relationships
- The LLM couldn't visualize how components are rendered
- Different libraries implement similar concepts (like "medium" size) differently
Iteration 4: Manual verification of interface and transformation instructions¶
To handle the issues in the above iteration, we included manual verification of the prompts, for example, fixing the size mapping if they were not accurate:
## Interface
[As above]
## Mapping
Instruction to migrate button
1. convert variant=primary or variant=default to type="filled"
 ...
// Fixed after manual verification
2. convert size="small" to size= "medium" and size="medium" to size="large"
## Transformation instructions
[As above]
Output: This improved accuracy even further for transforming basic components, but for complex components requiring substantial code restructuring it still had issues.
What could be missing: While the LLM had the information needed for transformation, most of it was theoretical. We felt that providing transformation examples with explanations would help the LLM learn from these patterns and enhance accuracy.
Iteration 5: Passing examples to the LLM¶
Our final iteration supplemented the instructions in the previous iteration with examples of increasing complexity. The examples were generated by the LLM but verified manually.
## Interface
[As above]
## Mapping
[As above]
## Examples
example 1: Simple transformation
// Source
<button size="medium" />
// Target
<button size="large" />
Migration Notes:
1. size="medium" maps to size="large" due to visual equivalence
... other examples...
## Transformation instructions
[As above]
Output: The code was transformed with a high degree of accuracy for all the components.
Through this series of iterative experiments, we were able to finalize our approach.
Building Our Migration Toolkit¶
After establishing our methodology through iterative experiments, the next challenge was to scale our approach while maintaining accuracy across the UI components.
Crafting component prompts¶
As we did in our hackathon, we crafted the transformation prompts for migration by providing the source code of our components to the LLM. These initial instructions included component interfaces, transformation rules, and example migrations. We utilized continue.dev to streamline this process, making the workflow of attaching source codes and generating prompt context more efficient.
System Prompts¶
We discovered that using system prompts enhanced the accuracy of the transformations. By instructing the LLM to operate as an experienced developer and clearly defining the task objectives, we achieved more consistent results. The system prompts also specified detailed requirements for code style, best practices, and error handling conventions. This proved instrumental in generating accurate code transformations that adhered to the instructed output format.
## System prompt
You are an expert frontend software developer with deep knowledge of frontend development,
component libraries, and design systems.
You MUST follow the instructions provided exactly as they are given.
Your task is to help migrate UI components from one library to another
while maintaining visual and functional equivalence.
// .. other instructions
Creating the tool¶
We developed a Python based migration tool using the llm library's conversation API. The tool processed each file in the given source directories and applied LLM-powered migrations for the components present in the file. We chose Python for its extensive support for working with LLMs and its rich ecosystem of libraries. Based on our hackathon results and subsequent testing, we opted for GPT-4o, which consistently delivered the most accurate transformations. It's worth noting that this tool was developed in September 2024 and started being used shortly after that, so our findings reflect the model's capabilities during this specific timeframe.
While the core implementation was straightforward, we encountered several technical challenges that required specific solutions:
- Handling large files: When files exceeded the 4K token limit, the output would get truncated mid-transformation. We resolved this by utilizing the conversation API and passing "continue" as a prompt whenever the content was cut off. This allowed the LLM to pick up where it left off and complete the transformation. As per our tests, a simple "continue" prompt proved more reliable than more complex prompts to continue the transformation.
- Output consistency: Initially, we noticed varying outputs for the same input, making testing and validation challenging. Changing LLM settings, like setting the temperature parameter to 0 made the LLM's output to be more deterministic and reproducible.
- Fixing output format: The LLM would sometimes include explanatory text or markdown formatting along with the transformed code. We resolved this by giving context to the tool and incorporating specific output formatting instructions in the system prompt.
You MUST return just the transformed file inside the <updatedContent> tag like:
<updatedContent>transformed-file</updatedContent> without any additional data.
- Limiting input context: We observed as the input prompt size grew, the transformation accuracy declined. To maintain high quality, we organized components into logical groups (like 'form', 'core', etc.), keeping context tokens between 40-50K per group of components. This grouping strategy helped maintain the LLM's focus and improved transformation accuracy.
- Automated tests: During development, we discovered that small adjustments to transformation instructions could lead to substantial changes in results. This highlighted a need to have prompt validation tests in place and led us to implement automated testing using LLM-generated examples. These examples served as validation tools and regression tests, helping us catch unexpected changes during the migration process.
- Caching and prompt structure: LLM APIs offer the ability to cache identical prompts, potentially reducing API costs and improving response times by reusing previous results (e.g. Prompt caching - OpenAI API). To leverage this capability effectively, we set up a structured prompt format that maximized cache hits. The prompt was organized to have the static part like transformation examples at top and the dynamic part (the file content) and the end, ensuring caching can be leveraged while transforming different files.
// Example prompt structure
## Transformation prompt  (static)
{transformation_context}
{For each component in group}
* {interface_details}
* {mapping_instruction}
* {examples}
## Content to be transformed (dynamic)
<file>
 {file_content}
</file>
Experience with LLM-Powered migration¶
The results of our LLM-powered migration project exceeded our initial expectations and cemented LLMs as one of tools for similar complex migrations in the future. While utilising LLMs for our complex migration task, we gained valuable insights on their power and limitations. Here's what we learned when putting LLMs to work in a real-world engineering challenge.
Cost effectiveness¶
When evaluating LLMs for large-scale code migrations, cost could become a critical factor. While having exact cost is challenging due to variations across the codebases, we can provide a rough estimation based on average metrics:
- Average prompt size per component group: ~45K tokens
- Average output file size: ~2K tokens
- Total groups of component: ~10 (each containing on average 3 components)
- Average number of files transformed per component group: ~30
Based on the GPT-4o pricing, this would come to be less than $40 for each code repository. The actual costs could potentially be lower due to possibility of prompt caching being applied.
While precisely quantifying the saved development effort is complex, the LLM-based approach achieved an accuracy of about 90% migrating components across large volumes of files, as reflected in the above metrics. This should imply that the LLM-based approach delivered significant time and resource savings and the approach was highly cost-effective.
What worked well¶
- High Accuracy: We achieved an overall accuracy of more than 90% for the component migration, with even higher accuracy for components of low to medium complexity. This reduced the amount of manual fixes needed after the llm powered migration.
- Code comprehension: LLMs have a good understanding of the different elements of code and their relationships. This was very useful in handling different edge cases encountered during the migration. This is a powerful capability, compared to traditional alternatives like codemods, where we need to explicitly code every edge case.
import {Typography } from …
const Header = Typography.Headline
// LLM would be able to correlate Typography.Headline and Header are same and will replace as per instructions
<Header></Header>
- Contextual intelligence: LLMs demonstrated contextual awareness during the migration process and were able to fill in the gaps in instructions based on provided examples and context. For example the LLM tool was able to provide correct default values during transformation even when the explicit instructions were missing.
- Accelerated development: Through LLMs we were able to generate the migration prompts and develop the tool faster than using traditional alternatives like codemods, which typically require more extensive development time.
Challenges and Limitation¶
Despite the strengths of LLM, we encountered some limitations, both LLM-specific issues and project-specific, that restricted full automation.
Some of the LLM limitations that we encountered:
- Reliability issues: Even with carefully crafted prompts, LLMs occasionally deviated from the provided instructions or made unexpected changes. Similarly, LLMs sometimes generated plausible-looking but incorrect code e.g. adding a property to the component which does not even exist.
- “Moody” behaviour: We observed that the LLM tools occasionally produced inconsistent outputs. These issues appeared without any clear reason, sometimes simply by rerunning the same prompt on the same file at a different time.
- Time consumption: Processing times ranged between 30 and 200 seconds per file, making large-scale migrations time-intensive. While not a major issue as the tool could transform files in the background, it made conducting quick, small-scale experiments more challenging
- No visual understanding: LLMs are unable to verify visual implications of the changes when migrating between design systems with different fundamental units. In our case, the source and target libraries had differences like different spacing scales and grid systems (12 vs 24 columns). This limitation meant that while a page could be syntactically migrated correctly, the layout may appear broken upon deployment.
We also encountered several project-specific challenges in our migration. These included differences in design philosophies of the two UI component libraries, difficulties in migrating test suites due to inconsistent practices, gaps in feature availability between the libraries, and variations in codebases and styling practices across applications. These challenges often required significant manual work and refactoring, as LLMs could not handle such complex transformations accurately. While these obstacles highlight the challenges with automated migration, they also demonstrate the importance of proper planning and setting realistic expectations when undertaking similar projects.
Lessons learned¶
While our experience confirmed LLMs as valuable tools for complex migrations, we learned few lessons on how to use them effectively for such use cases:
- Embrace iterative approach: We found that there is no universal formula or fixed approach on how to increase the effectiveness of a LLM. Our approach required an iterative approach of continuous experimentation and refinement. We found our prompts after testing different prompt variations, analyzing results, and incorporating feedback.
- Provide code examples: Including specific code examples enhanced migration accuracy. When we supplemented transformation instructions with examples, the LLM's ability to handle similar patterns improved. This was particularly visible in complex component migrations where abstract instructions alone proved insufficient.
- Human oversight is crucial: While LLMs demonstrated impressive capabilities, human oversight and verification is crucial while dealing with LLMs at every stage. For example, code reviews and thorough visual testing would be needed for catching subtle issues that LLMs might introduce. For example, consider the below example where visual review is needed:
// Transform 24 to 12 grid
<Grid>
  <Column span={9} />  <Column span={15} />
</Grid>
// Two possible options
// Option 1 - rounded up - page breaks into two line
<Grid>
  <Column span={5} />  <Column span={8} />
</Grid>
// Option 2 - rounded down, extra whitespace
<Grid>
  <Column span={4} />  <Column span={7} />
</Grid>
- Tool evaluation: It is important to evaluate available LLM tools before embarking on similar migration projects. Our initial approach of manually copying and pasting source code into LLM prompts proved time-consuming and error-prone. The adoption of continue.dev improved our workflow by automating source code handling.
- Effective Prompt engineering: Our success relied on evaluating different prompt engineering strategies and modifying them for our use case. For example, breaking down complex transformations into discrete steps or practical examples with instructions increased migration accuracy and enhanced LLM's reasoning capabilities.
- Prompt best practices: Follow established prompt engineering best practices (e.g., Prompt engineering - OpenAI, Prompt engineering for Copilot Chat - GitHub Docs) to ensure consistent and accurate results such as prompts should be clear and concise. For instance, consider the following prompts:
## Example 1
// ❌ prompt  not clear on how to handle when no button components are present
// transformed unrelated components if no button was found in the file
Migrate button components in the file as per the below instruction
//...
// ✅ clear instructions on transforming only when button components are present
// worked as expected
Migrate button components, if it exists, in the file as per the below instruction
## Example 2
// ❌ no clear mapping between sizes
"Map the sizes(small, medium) to (small, medium, large) appropriately"
// ✅ clear mapping between sizes
"Map size variants as follows:
 - small -> size='small'
 - medium -> size='large' (for visual equivalence)
 Note: Handle undefined size with 'medium' default"
Looking Forward¶
The use of LLMs in this project wasn't just about solving our immediate migration needs, but also to evaluate the feasibility of LLMs for tackling large-scale code transformation challenges with high degree of accuracy. While LLMs have limitations they've proven to be powerful tools. As we wrap up this phase of our UI migration, we're already identifying other areas where this approach could provide value and this time we would have a better idea how to approach such challenges.
We're hiring! Do you like working in an ever evolving organization such as Zalando? Consider joining our teams as a Frontend Engineer!
