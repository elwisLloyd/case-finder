# Under the Hood of the Grammarly Editor, Part Two: How Suggestions Work

Источник: https://www.grammarly.com/blog/engineering/how-suggestions-work-grammarly-editor/

This article was co-written by Front-End Software Engineers Anton Pets and Oleksii Levzhynskyi.
Have you ever wondered about the architecture and algorithms behind how Grammarly suggestions are applied to a piece of text? In this blog post, we’ll discuss how the most simple and complex Grammarly suggestions are represented in code and the lifecycle of how suggestions are managed in the Grammarly Editor. We’ll explain how we ensure suggestions are always applied to the right place in the user’s text. And we’ll finish up by walking through some interesting nuances around applying multiple suggestions to the text at once.
This is the second part of a series by Grammarly’s Front-End team where we explain the core pieces of code that power our cloud text editor. For some background on the concepts in this article, we recommend first reading Part One: Real-Time Collaborative Text Editing.
Grammarly suggestions demystified
As discussed in Part One, we use an operational transformation (OT) protocol to represent text changes via the simple yet expressive Delta format. We use Deltas to represent the text itself and the changes made to the text by the user. In other words, Deltas represent how the text in the Grammarly Editor changes from one state to another.
To illustrate this, let’s get back to the example of a hypothetical user, Harper, an economics student writing her essay in the Grammarly Editor.
Before Harper has written anything, the Delta representation for the empty Grammarly Editor is as follows:
    {insert: "n"}
Because of technical constraints, any document (even an empty one) must end with a new line symbol: n
Imagine that Harper then starts typing, but she makes a typo, entering the phrase “A supply schock” rather than “shock.”
This change will be represented as follows:
    {insert: "A supply schock"}
We then update the Delta for the text in the Grammarly Editor by “rebasing” it onto Harper’s changes. Now the text Delta is this:
[
    {insert: "A supply schock"},
    {insert: "n"}
]
This text change is then communicated to our back-end, which scans for mistakes and sends suggestions to the client. When a suggestion is received from the back-end, a suggestion card appears in the Grammarly Editor UI:
An important trait of our OT protocol is extensibility. To express Grammarly suggestions, we were able to simply extend the protocol to include a new transform field. This field contains a Delta that represents the suggested text change. In other words, we’re able to represent any Grammarly suggestion in the same way that we represent ordinary text changes coming from the user:
{
    category: "correctness",
    transform: [
      { retain: 9 },
      { "insert": "shock" },
      { "delete": 6 }
              ]
}
A simplified representation of a Grammarly suggestion
Within the Delta, retain is used to specify where the suggestion should be applied (in this case, position 9). In practice, we also include some syntactic sugar and additional metainformation about the suggestions that our backends produce. But in essence, Grammarly suggestions, user text, and text edits made by a user are all represented via a simple yet expressive Delta format. 
But if Harper accepts the suggestion, how do we apply Grammarly’s correction to her text? We employ Delta’s special compose() function, which lets you compose any Delta with another Delta. The result will be equivalent to applying both Deltas sequentially. For example, composing
[{insert: "A shockn"}]
(representing the string “A shock” in the Grammarly Editor UI) with
[{retain :1}, {insert: " supply"}]
(adding a word at the second position) would result in
[{insert: "A supply shockn"}].
Composing Deltas works in exactly the same way for suggestions. To apply a suggestion to the text, we just compose the text Delta with the Delta representing Grammarly’s suggestion. Voilà: The typo is fixed.
Extending our protocol to support more complex suggestions
Being able to introduce new commands to our client-server communication protocol is a powerful feature, allowing us to express new types of suggestions of any complexity. However, each new command must comply with an important requirement of our OT protocol: It should be possible to adapt (“rebase”) the command according to the user’s ongoing text edits without waiting for updates from the back-end. Otherwise, we would end up with a slow application and a poor user experience.
At the time of introducing this protocol, Grammarly was mainly focused on suggestions that replaced a single word or short phrase, like correcting spelling mistakes. But our product has evolved, and now, a single suggestion can rewrite a sentence to make it easier to follow, restructure a paragraph to highlight the key takeaways, or even make changes across the whole document to improve consistency.
Despite adding these features, we’ve never had to change our protocol, because it’s been flexible enough to handle any new suggestions. But as we’ve added more complex features, including the ability to accept multiple suggestions at once, there’s a lot of orchestration to manage on the client. Next, we’ll discuss how we update and apply suggestions in the Grammarly Editor while maintaining a fast and fluid user experience.
Suggestion management and rebase
There are two critical requirements for any Grammarly suggestion: One, it should always be correct, and two, it should always be relevant. At Grammarly we spend a lot of time improving the quality of our suggestions, but relevance is just as important. For example, imagine that Harper fixed her typo in the word “shock” on her own. We’d want to hide our spelling correction card ASAP, as it’s no longer relevant.
For the simplest cases, such as spelling correction, we just have to keep track of what word the suggestion is for. If a user changes that word, we know we should hide the suggestion. But when suggestions span more text, like a sentence or paragraph, the logic can become quite complex.
An example of a suggestion for rephrasing a sentence.
Suggestions that span more text only need to be hidden if a user makes changes to the phrases highlighted in the suggestion card. In the example above, if Harper changed a non-highlighted part of the sentence—replacing the word “sudden” with the word “drastic,” for instance—we would want to retain the suggestion rather than hide it.
In addition to these requirements, we need to make sure that cards don’t flicker in the UI and that suggestions can always be applied instantly—which means doing a complex update of the suggestion Delta on the client side. The architecture of the Grammarly Editor has been carefully designed to perform these updates while keeping the UX fast and responsive.
Architecture for managing suggestions
A simplified Grammarly Editor architecture
All the suggestions received from the back-end are stored in the Suggestions Repository. If the user fixes a mistake in the text, or our back-end decides that the suggestion is no longer relevant, we remove it from the Repository and notify other pieces of the system. First, we need to notify our Delta Manager, which is used to keep our suggestion Deltas relevant and correct and to render suggestion cards. We also notify our Highlights Manager, whose job is to correctly highlight mistakes in the text. At a high level, every time something changes in the text, we need to repeat a “cycle”: notifying our Highlights and Delta Managers, re-rendering affected highlights and cards, probably updating the Suggestion Repository, and sending and receiving updates from the server.
Having many interconnected entities that may perform nontrivial computations in the browser is one reason why our engineers need to know and use proper algorithms and data structures. In such a setup, if slightly suboptimal algorithms are used in multiple places, it could lead to a slow or unresponsive application.
The rebase procedure
Within our architecture for managing suggestions, the Delta Manager has an important job: It rebases suggestion Deltas according to new changes coming in. Here’s an example to help illustrate how this works:
Imagine that after entering the initial phrase “A supply schock”, Harper decides to change it to “The supply schock”. At this point, the suggestion Delta that is stored in Delta Manager is not up to date anymore: Its target, “schock”, has shifted two positions to the right. Therefore, the Delta Manager performs a procedure called rebase, which updates the suggestion Delta according to the changes made by the edit Delta. 
So what exactly happens during the rebase procedure? Any Delta consists of one or more Delta operations. As we have already described in the previous article, each operation may be one of three types: “insert”, “delete”, “retain”. In our case, we need to rebase the suggestion Delta ([{retain: 9},{"insert": "shock"}, {"delete": 6}]) onto the edit Delta [{delete: 1},{insert: "The"}]). To do so, we iterate over both Deltas’ operation lists and merge them into a new operation list, resulting in a rebased Delta. (As this merging procedure is based on Quill’s rebase algorithm, we won’t get into the low-level details here.) 
When all’s said and done, the Delta Manager will have the following suggestion Delta, pointing to the right target in the text:
[{retain: 11}, {insert: 'shock'}, {delete: 6}]
You might notice that the retain operation from the original suggestion Delta, which had a value of 9, has been increased by 2, which is the length of text affected by the edit Delta.
Accepting many suggestions at once
For many Grammarly Editor users, including the authors of this blog post, the writing workflow starts with composing text from beginning to end, without paying attention to mistakes and style issues. Then, users turn their attention to the list of suggestion cards and start applying or ignoring them one by one. Many mistakes, like simple typos, are quite straightforward, and one of Grammarly’s top-requested features was the ability to accept such suggestions all at once. Last year, we implemented a special card to do just that. Here, we’ll focus on the technical aspects of how we apply many suggestions at once to the text (and some interesting challenges that came up along the way).
Every time a user accepts a suggestion, we change its state in our Suggestion Repository from registered, which means it is relevant and correct, to applied, which means it should be removed from the system. We also let other parts of the system know that the suggestion is now applied, so they can react accordingly. The Suggestion Feed is updated, and highlights in the text are removed. But most importantly, we need to save the text changes. To do so, you may recall that we take the suggestion Delta and compose it with the text Delta to generate a new text Delta with the user’s mistake fixed. We then update our editor’s text content.
To apply multiple suggestions at once, we naturally need to repeat this process for every suggestion in the group, each with its own Delta:
delta1= [{retain: 11},{insert: 'shock'},{delete: 6}]
delta2= [{retain: 259},{insert: 'being'},{delete: 5}]
delta3= [{retain: 278},{insert: 'Examples'},{delete: 8}]
…
deltaN= …
From our system’s point of view, this is the same as if the user quickly accepted all the individual suggestions one after the other. Such a solution would theoretically work in production. But it would create a serious UX issue: If a large group of suggestions was accepted at once, the user might notice that the Grammarly Editor would freeze for a few seconds. While the process of applying a single suggestion appears instantaneous, repeating it many times, even very quickly, results in noticeable delays of UI updates in the web browser. This occurs because browsers can only do one task at a time, and for each suggestion we need to repeat a “cycle” of updating all the related parts of our architecture, as described earlier in this article.
While building this feature, our investigations revealed that the most time-consuming task in this process was updating the Delta that represents the text in the editor, a task that was repeated for each suggestion in the group. Luckily, we can easily join multiple Deltas into one simply by composing them. By “glueing” the suggestion Deltas together and later composing the result with the text editor Delta, we turned a repeated process into a single step:
const bulk = [delta2, ..., deltaN]
let composedDelta = delta1
for (const delta of bulk) {
composedDelta = composedDelta.compose (delta)
}
// here we can use composedDelta to apply
// all changes at once This trick eliminated the problem of the UI hanging. But it introduced a new puzzle. After applying multiple suggestions, the text would look broken—as if the characters were all mixed up:
It took us some time to figure out why this was happening. To explain, let’s imagine a situation when a user applies an individual suggestion. This action changes the text, and all other suggestions cannot be applied as-is anymore, because they should be updated accordingly.
Speaking a bit more technically, the suggestion Delta is composed with the text Delta, effectively modifying the text Delta. At this point, the Suggestion Repository may still contain other registered suggestions. But because they were created for the previous state of the text editor Delta, we cannot use them anymore. That’s why every time something changes in our text Delta, the Delta Manager needs to rebase all the registered suggestions according to the latest changes in the text. And this is the reason why our composed Delta for accepting multiple suggestions breaks the text. Every time we join a new suggestion Delta onto the composed Delta, we need to rebase this suggestion as if all the previous suggestions in the composed Delta had already been applied to our text. The resulting code looks like this:
let composedDelta = delta1
const bulk = [delta2, ..., deltaN]
for (const delta in bulk) {
// Adapt the current suggestion delta
// as if the previous suggestions were already applied
const rebasedDelta = delta.rebase (composedDelta)
composedDelta = composedDelta.compose (rebasedDelta)
}
The result is a feature that applies multiple suggestions at once, correctly and instantly:
Wrapping up
Let’s summarize what we’ve discussed:
- We use Deltas to represent text changes produced by Grammarly suggestions. Deltas are also used to represent the user’s edits and the text itself.
- Our OT protocol is highly extensible, so we’ve been able to add new types of suggestions—even those that affect multiple paragraphs—all using the same simple format.
- To manage suggestions so that they’re always correct and relevant, we have architecture that maintains a repository of suggestions and continuously updates suggestion Deltas via the rebase procedure.
- Suggestions are applied by simply composing the text Delta with the suggestion Delta. However, applying multiple suggestions at once is a little trickier because we have to make sure we’re correctly rebasing the suggestions first.
We hope you’ve learned something helpful from this article! If you’re interested in working with our protocol to implement new Grammarly suggestions and many other user-facing features that impact 30 million people and 30,000 professional teams every day, come join our team!
