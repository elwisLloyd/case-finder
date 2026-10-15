# Reinventing Risk at Revolut

Источник: https://medium.com/revolut/reinventing-risk-at-revolut-77e63c552503

Reinventing Risk at Revolut
Revolut is known for its innovation in delivering “super-app” financial services to its customers. The success is evident not only through the rocketing user growth, but also via the ripple effects caused across the banking industry — traditional finance has to reinvent and evolve, or remain part of history, just like the internet search replaced the paper phonebook.
Behind this success stands a complex and impressive machinery, which is still piloted by the same founders, who also engineered the very first components and set the Revolut rocketship in motion.
This machine is mostly known for its software excellence, however, with any financial services comes the responsibility of navigating a complex net of regulations and risks. True to the company values, the Risk function at Revolut also innovates, leveraging the decades of banking experience of its leadership and adding the challenger way of thinking with the latest technology.
What is Risk?
One can find many definitions of risk, ranging from explanations suitable for children, “The possibility of something bad happening”, to advanced statistical definitions used in finance:
Uncertainty of the return on investment, characterised by standard deviation, asymmetry and tails of the return distribution
and the generic ISO 31000 definition:
“The effect of uncertainty on objectives”
In addition, both graduate textbooks and banking regulations define two general types of risk:
- Financial: related to financial positions, such as: user deposits, lending, and investments in market instruments.
- Operational: related to failure of operations, such as: system outage, fraud and natural disasters.
Some of you might already sense the inevitable challenges in distinguishing the above definitions and risks. Events seldom happen in isolation and independently: a natural disaster can lead to system outages and market crashes, similarly fraudsters might use fake accounts to withdraw loans which would never be repaid. Finally, sometimes adverse events just happen simultaneously even without having a common cause.
Problem statement
Financial institutions estimate and manage risk in large, segregated departments specialising in their own risk type. For example, the operational risk department has teams specialising in fraud and technology failures. The market risk department has teams focusing on risks stemming from investments in bonds or derivatives. To make it even more complicated, model risk teams oversee the possibility of all of the other teams using inappropriate techniques in estimating their risks — leading to the risk of risk, or something like risk squared.
The above approach leads to methodological silos of how risk is defined, monitored, and estimated. Although the underlying probability theory is the same, the financial and operational risk departments might have broadly inconsistent approaches and even diverge in their views of the same risk event or double count some of the risks. This prevents accurate view and management of risk on enterprise level.
Note that this legacy banking set-up is not the result of some careful consideration of all possible risk types and the optimal way to oversee them consistently. It is simply the result of old banking, tree-like structures which kept appending new teams and systems for tackling the risks from new products and regulatory requirements.
Solution requirements
If we imagine a new type of Enterprise Risk Management Framework (ERMF), what features should it posses in order to solve the above problems?
- Scientific: Use scientific principles as universal and reusable building blocks that can define any risk, but also be shared across multiple risks.
- Measurable & Comparable: Enable calculation of a standardised set of metrics for each risk that can be compared and combined across risks.
- Hypothetical: Allow for risk to be defined as a hypothesis of something that could happen, even when no observed data is available.
- Data Driven: Link the risks to live data sources in order to enable monitoring against data of observed business events, with the ability to monitor for any events that are missing in the currently defined risks.
- Learning: Update the hypothesis (requirement 3) based on the difference between expected and observed data.
- Explainable: Be able to explain and decompose any result of calculated metrics (requirement 2) to all components that lead to its derivation, including data inputs and logical rules. The generated audit trail will be extremely valuable during regulatory, audit, and validation exercises.
- AI assisted: Enable interaction via natural language with the defined risks and the audit trail of the calculated metrics, we can call this functionality Risk to Text. Equally important is the ability to generate risks, from natural language descriptions such as regulations or expert reports, we can call this functionality Text to Risk.
Reinventing Risk
How NOT to do it
Legacy risk frameworks often start from high-level, top-down definitions such as risk types, controls, materiality, risk appetite, and so on, without clarifying their relations or defining first the common ground concepts that they share.
Thus, you end up with a framework in which you have a lot of high-level concepts which seem to be expert knowledge, however, when you drill down you find most of them overlapping or even contradicting each other. The culmination of this approach is usually a tree structure called Risk Taxonomy of different risk types and subtypes, here is what the Open Risk Manual says about issues with this approach:
“Risk types in practice may exhibit significant overlap either due to poor definition or due to the fact that a complex Risk Event intrinsically maps to multiple risk types”
How to GET IT DONE
A general principle is to define as little as possible concepts unless they are based on our scientific building blocks, or if I may quote a famous electric car enthusiast “The best part is no part”.
We will start from the bottom-up and if a more specific concept cannot be derived from the building block, then either our foundation is not good or the concept is not needed at all.
Building blocks = events
Our choice of building block is the event, with the following arguments:
- The natural way that risk is usually thought of and described by humans typically involves events: “The risk that in the event of …”. This increases the ability to satisfy requirement 7, and the translation of risk to and from natural language.
- Risk estimation is heavily reliant on probability theory for things like frequency and severity distributions, both of these are always in terms of specific events such as risk incidents that lead to losses. This is consistent with requirement 1 for using scientific building blocks.
- Modern IT systems are to a large extent event-driven, in order to deliver live information on things like news and stock prices. By making our risk framework event-based, we are opening the door to seamless integration with the data sources and live monitoring of our risks, based on specific business events. This is consistent with requirement 4.
The way we will think about an event is quite general, in terms of the event leading to a transition between two states over a period of time:
The main benefit of this is that we can stack any number of events and states into a network/graph of things that may or may not happen, sounds a bit similar to risk, right?
The other benefit is on the scientific side, from having the ability to perform standardised calculations over such structure. This is essentially a state space (Markov chain) representation, which is widely used in statistics. This satisfies requirements 1,2, and 3.
Risk = chain of events
Jumping straight into a specific example, one of the risks that Revolut faces is related to a user’s balance becoming negative (money owed to Revolut) and subsequently becoming a financial loss if not repaid within a given timeframe. This risk is interesting from two aspects:
- The base risk population has the broad scope of all users with positive balance.
- The loss of negative balances represents pure credit risk, however, some of these losses can arise due to fraud which is operational risk, hence we could have composite risk with both financial and operational risk events. For simplicity, we will include only the credit risk in the example, however the extension with additional events and states is analogous.
The main states included in the risk are: positive balance (+Balance), negative balance (-Balance), and (Lost). Where each state is defined in terms of the characteristics of the user instances. Stacking the states and the transitioning events, we obtain the following chain of events:
Transitions from a state to itself are also possible, like a +Balance staying such, but also some states can be completely absorbing like a Lost balance always remaining such. Finally, above in red, we introduce the notion of loss rate which indicates what proportion of money can be lost in a given state. For simplicity, we assume 100% loss rate only in the lost state, however, in reality there could also be losses associated with the -Balance state, for example, due to collection costs from the negative balances.
Now that we have a solid and scientific building block, let’s start making structures with it. The above chain of events is our first example of a specific risk and generalising the definition, we end up with the following single sentence:
Risk: The potential of financial loss, as a result of a chain of events, over a given time horizon
Note that apart from defining risk as a chain of events, we also require it to be linked to a tangible financial loss and have a strict time dimension. This will help satisfy requirement 2, by being able to calculate risk metrics. The financial loss need not necessarily be in absolute terms, and it could be in relative terms as opportunity cost relative to an objective, which is consistent with the ISO 31000 definition of risk.
Metrics
A main advantage of formal risk definition is that it enables the calculation of a standardised set of metrics for every risk. Back to the negative balance risk example, let’s set values for the main parameters of the risk, which can be considered ex-ante expert estimates:
- Amount of +Balances: 100£
- Probabilities of events: 
- P(stay +): 90%
- P(become -): 10%
- P(become +): 20%
- P(become lost): 80%
- P(stay lost): 100%
Maximum loss
The first and most trivial metric is worst case scenario loss, knowing that all probabilities above are just ex-ante expectations one can ask: what is the most I could lose in the worst case scenario? In our simplified example, this will happen if all £100 of positive balances become negative and then lost, leading to a loss of £100 * 100% = £100.
Expected loss
Now let’s try a more sophisticated metric in the form of Expected Losses (EL or ECL). For this, we will need to define a time horizon, e.g. whether we form our expectation over 1 or 10 periods, and we will need to iterate over our ex-ante expectations. To keep the example simple let’s consider 2 period horizon, and starting from the +Balance state, we have the following paths at 2 period distance, where the cumulative probability along a path is obtained by multiplying the individual probabilities:
- [+Balance → -Balance → Lost]: P = 10% * 80% = 8%
- [+Balance → -Balance → +Balance]: P = 10% * 20% = 2%
- [+Balance → +Balance → -Balance]: P = 90% * 10% = 9%
- [+Balance → +Balance → +Balance]: P = 90% * 90% = 81%
In this simplified example, we can calculate EL only by considering the paths which end state have a loss rate, since all others will be multiplied by 0. This is the path ending with Lost state, with 8% probability and 100% loss rate, leading to EL = £100 * 8% * 100% = £8. Note the big difference between the maximum(£100) and the expected loss (£8) due to the probability weighting of the events in the risk.
Generalising further, the risk definition essentially gives us a generator of discrete loss distributions for any time horizon at which we want to form our expectations. These distributions are the backbone of risk theory and estimation, used even in bank regulations for calculating capital requirements. The maximum, expected, and unexpected losses are just one of the many generic metrics that can be calculated from such distributions which satisfy requirement 2.
Fellow nerds, might have recognised the embedded Markov chain in our Risk definition. This automatically unlocks the utilisation of tonnes of scientific knowledge, from things like efficiently computing n-period transitions via matrix multiplication, to advanced topics like: Bayesian inference, time inhomogeneous probabilities and probabilistic graphical models.
Observed loss
In addition to enabling the calculation of standardised ex-ante expectations about what could happen, our risk definition also enables the monitoring of actual live events and calculation of ex-post observed metrics. This means that we can form subjective expectations before we even launch a given product. However, once data is available, we can calculate losses and use this to update our initial expectations. This satisfies learning requirement 5 and is dependent on having an implementation that links our abstract states to data sources (requirement 4). We will talk about this in the next section.
Sounds nice, but how would you actually do it?
The implementation requirements are becoming non-trivial, taking into account the needs of: defining high-level abstractions, linking them to data, performing efficiently recursive calculations over a large graph of rules, while preserving explainability and audit trail of the derived facts.
Reasoning
Semantic reasoning is the “inference of logical consequences from a set of asserted facts” (Semantic Reasoner). It became initially popular with the idea of Semantic Web in the early 2000s, representing the evolution of the internet from linked pages (Web 1.0), to linked apps (Web 2.0), and linked data (Web 3.0). Reasoners enjoy a new surge of popularity together with the AI hype, due to their interaction with language models in terms of adding explainability and reducing hallucination.
For our demo, we used Prometheux, an explainable AI platform for big data and distributed processing, which we used as our reasoning layer. Prometheux’s research-backed platform abstracts away our various data sources, letting us iterate quickly on a virtual knowledge graph of our data and business rules, instead of writing complex database queries or migrating data.
Get Konstantin Vasilev’s stories in your inbox
Join Medium for free to get updates from this writer.
While other knowledge graph technologies require representing relationships as triplets consisting of Subject, Predicate, Object, (e.g. is_son(Child,Father)), Prometheux is capable of representing more complex rules based on n-tuples.
Methodology implementation
Using Prometheux, we start by implementing our new risk methodology, first specifying data models of our main concepts: State, Event, Risk. The code below defines:
- State: something having ID and loss rate.
- Event: something consisting of start and end State and a probability.
- Risk: collection of Events.
@model("state","['State(ID):string', 'LossRate:double']").
@model("event","['Event(ID):string', 'StartState:state', 'EndState:state', 'Probability:double']").
@model("risk","['Risk(ID):string', 'Events:[event]']").
Next, we proceed by adding the first logical rules, for a given set of parameters: [Risk, StartState, NumPeriods], we want to calculate all paths of NumPeriods distance from the StartState and their cumulative probability. The first rule initialises the path at the StartState, with 0 periods and a probability of 1, with the parameters being provided in curly brackets {}:
risk_path_probability(Risk, StartState, StartState, NumPeriods, Events, Probability) :-
risk(Risk, Events),
NumPeriods = 0,
StartState = ${start_state},
Probability=1.0.
The second rule defines a recursion that traverses events within the specified Risk, until the NumPeriods distance is reached, accumulating the probability of every new event along the path:
risk_path_probability(Risk, StartState, EndStateNew, NumPeriodsNew, Events, ProbabilityNew) :-
risk_path_probability(Risk, StartState, EndStateOld, NumPeriodsOld, Events, ProbabilityOld),
event(Event, EndStateOld, EndStateNew, ProbabilityEvent), 
NumPeriodsNew = NumPeriodsOld + 1,
ProbabilityNew = ProbabilityOld * ProbabilityEvent,
IsEventOfRiskInstance = collections:contains(Events, Event), IsEventOfRiskInstance=#T,
NumPeriodsNew <= ${num_periods}.
Finally, we define predicates that store the end probability at NumPeriods distance and one that aggregates all paths that end in the same state, to get end-state probabilities:
risk_path_probability_end(Risk, StartState, NumPeriods, EndState, Probability) :-
risk_path_probability(Risk, StartState, EndState, NumPeriods, Events, Probability),
NumPeriods = ${num_periods}.
risk_state_probability_end(Risk, StartState, NumPeriods, EndState, ProbabilityState) :-
risk_path_probability_end(Risk, StartState, NumPeriods, EndState, ProbabilityPath),
ProbabilityState = msum(ProbabilityPath).
Risk register
Now that we have data models and some logic, let’s define our negative balances risk with it. In the negative balances risk, the main abstraction is the user with their Balance property. Note that the object instances used in the risk have to comply with the earlier defined data models. One of the main advantages of using a reasoner, is that upon compilation it verifies the logical consistency amongst rules and data without allowing any contradictions.
state(“Positive balance”, 0.0).
state(“Negative balance”, 0.0).
state(“Lost”, 1.0).
event("Become negative", "Positive balance", "Negative balance", 0.1).
event("Stay positive", "Positive balance", "Positive balance", 0.9).
event("Recovery", "Negative balance", "Positive balance", 0.2).
event("Loss", "Negative balance", "Lost", 0.8).
event("Stay lost", "Lost", "Lost", 1.0).
risk(
"Negative Balances Risk",
["Become negative", "Stay positive", "Recovery", "Loss", "Stay lost"]
).
Data driven
Requirement 4 is for our methodology to be data driven. The above ex-ante definitions are already enough to calculate metrics like expected losses, however, without an easy way to link to data sources we can’t calculate ex-post observed metrics and update our initial beliefs, which is part of the learning requirement 5.
Fortunately, our reasoner allows us to directly bind predicates to data sources, such as: CSV, DB table/query, API. This is as simple as a single line pointing the predicate “user” to the data source, and of course, the data source is required to match the data model of the predicate:
@input("user").
@bind("user","csv useHeaders=true","disk/negative balances/data","users.csv").
In our case, the user abstraction is something with ID, Revolut entity ID, Balance, and Date. And we can imagine it being linked to a daily data source with all Revolut users and their balances. In this case, we’ve created an artificial dataset of user balance time series. Based on user data, we can derive our Risk specific states, depending on whether the balance is positive, negative, or if there has been a loss event:
user_state(State, User, Balance, Date) :-
user(User, EntityId, Balance, Date),
not loss_event(User, EntityId, Balance, Date),
Balance >= 0,
State = “Positive balance”.
user_state(State, User, Balance, Date) :-
user(User, EntityId, Balance, Date),
not loss_event(User, EntityId, Balance, Date),
Balance < 0,
State = "Negative balance".
user_state(State, User, Balance, Date) :-
user(User, EntityId, Balance, Date),
loss_event(User, EntityId, Balance, EventDate),
Date >= EventDate,
State = "Lost".
Risk calculation
Before we trigger the calculation, let’s see how the reasoner querying works. This is as simple as requesting which predicate to be outputted, then all dependencies are evaluated including fetching from the data sources.
First we initiate the parameters which in our case is the starting state, date, and number of periods. Then we output the predicates. In this case let’s explore the artificial data, and see the user states at the start date and the end date at 11 days distance.
@param("start_state", "Positive balance").
@param("start_date", "2024-12-01").
@param("num_periods", 11).
@output("risk_state_start").
@output("risk_state_end").
Now let’s output a predicate which defines how ex-ante expected loss is calculated — this will immediately trigger the materialisation=calculation of all dependencies. In this case, we can calculate expectations purely out of the risk definition and ex-ante probabilities, before we even have any actual data.
First, let’s output the end state probabilities at 11 periods distance from the starting state. Then we output the expected loss, which in this simplified case is dependent only on the Lost end state and its probability = 0.538 (all other end states have 0 loss rate), hence the expected loss of each user is proportional to their current balance ExpectedLoss = Balance*0.538
@output("risk_state_probability_end").
@output("risk_expected_loss").
Finally, using the end-state data we can calculate the observed losses, which closes the feedback loop and enables requirement 5 for learning based on expected vs actual observations:
Generalisations
Note that so far we’ve kept the example simple on purpose, however, the implemented methodology is general enough to accommodate more complicated cases:
- Apply calculations for a given Risk on a population with multiple states, e.g. if we want to calculate expected losses for the entire population of users including both those currently in negative and positive balance states.
- Calculate metrics for different time horizons — parameterised by the number of periods.
- Calculate multiple Risks for a given abstraction, e.g. a user can have both negative balances risk and credit risk if it possesses a credit product.
Explainable audit trail
So far, there is nothing that effectively differs from an alternative Python implementation and which satisfies requirement 6 for explainability.
However, our implementation choice via reasoner keeps track of logic rules and their materialised results called facts inside a knowledge graph, which can provide explanation and audit trail (proof tree) of every derived fact. Let’s take, for example, one particular calculated fact and ask for its explanation:
explain(fact="risk_expected_loss(B,8.07)")
The above fact is based on the predicate risk_expected_loss with the arguments: user B in our population and calculated expected loss value of 8.07, but how was this derived?
By default, the reasoner provides a proof tree of all predicates that were used to derive the fact selected for explanation. The proof tree is described in code but can also be visualised as a graph:
In the proof above, we can clearly see that the fact risk_expected_loss(B,8.07) was derived by the fact risk_expected_loss_rate(0.538) and the start state of the user, with the latter being further derived from a positive balance state of a user of Revolut Ltd.
The explain functionality of the reasoner satisfies requirement 6 which is extremely valuable in the financial sector where audit trail and logical transparency is of very high priority. In the risk domain, there are further benefits from explainability in delivering clear and objective methodology when assessing and controlling the risks of the business teams.
What if we want to deliver this explainability to the non-technical user and avoid code and predicates in the proof tree? Fortunately, the structured explanations are easily translated to natural language (NL) by a large language model (LLM).
Risk xAI
As I’ve previously discussed, LLMs perform pattern matching and prediction of the most likely sequence of words without having any semantic understanding of the concepts behind them. This often leads to “hallucination” which can be fun in artistic domains but unacceptable in scientific ones.
Fortunately, our use of semantic reasoner enables an architecture that solves exactly this problem. The benefit of the reasoner is that it ensures 100% consistency and audit trail, with the drawback of the latter being in the form of machine code which is not human friendly, especially at scale. In combination, the Reasoner and LLM prove to be a surprisingly good tandem.
The Reasoner can handle:
- Data models and Rules of our Risk risk domain compiled in a fully consistent Ontology (onto-logos from Greek meaning the study of existence, in our case the existence of Risk).
- Binding of Data sources which can be used as required Inputs in order to derive requested Outputs following our Ontology. This process is called reasoning and is used to derive new Facts.
- Explanation of any Fact via Proof tree.
Similar to the popular use of RAG (Retrieval-Augmented-Generation) for providing additional information to the LLM, we can store our domain Ontology and any Proof tree in a Vector DB and make this information available to the LLM.
The LLM can handle:
- Show NL (natural language) description of the individual Rules, e.g. “How is expected loss calculated?”.
- Show NL description of the entire Ontology, including shared concepts between rules, e.g. “What is Risk and how it is defined?”.
- Explain any fact by translating the Proof tree, e.g. “How was the expected loss of x£ derived?”.
- Have a NL chat around all of the above: facts, rules, explanations.
The architecture above satisfies requirement 7, as we can harness the power of the reasoner and access it via human friendly NL. Now let’s see how it works in practice.
Natural language explanation
Using the LLM, we can generate a NL description of the fact risk_expected_loss(B,8.07)which proof tree and diagram we saw previously:
User B has a positive balance of 15 with Revolut Ltd as of 2024-12-01.
The expected loss for user B is 8.07, with a loss rate of 0.538
Note that the association with Revolut Ltd, is not something directly available in the fact on which the explanation was requested, this was correctly inferred by the LLM through the knowledge of the proof tree and the complete ontology from which the association with Revolut Ltd is visible.
Some might say “I can give the LLM python code and function results and it can also generate explanation” — yes, you can, but here the reasoner has the responsibility of providing 100% accurate explanation while the LLM has the task of “prettifying” this explanation to NL. The resulting combination is much more robust than any standalone LLM explanation.
Risk to Text
Proof tree explanation is just one of the surprisingly good interactions between reasoner and LLM. Even before any facts and explanations are generated, we can easily generate NL descriptions of the logic that we have implemented and the risk instances that we have added to it. Let’s look at the NL description of the predicate risk_path_probability:
The probability of encountering risk when transitioning from a start state
to a new end state over a given number of periods is calculated
by multiplying the probability of encountering risk
in the previous period by the probability of the event causing the state transition,
provided the event is a risk instance and the total number
of periods does not exceed a specified limit.
Just think of the current development and documentation process of such rules, in which risk managers have to provide business specifications and developers have to implement, while also writing an elaborate documentation. Here, essentially we have logic which can be self-describing and documenting.
Auto doc and policy
Let’s see the LLM generated NL description of our entire ontology. You can imagine a use case of this functionality in automatically generating and updating documentations and internal policies and procedures. All of our examples are with minimal promt engineering meaning that there is room for a lot of customisation and improvement:
The ontology defines a framework for assessing risk and loss in financial states through various predicates and rules. The key predicates and their roles are:
1. **state**: Represents financial states with an associated loss rate. Used to define states like “Positive balance”, “Negative balance”, and “Lost” with specific loss rates.
2. **event**: Describes transitions between states with associated probabilities. Events like “Become negative”, “Stay positive”, “Recovery”, “Loss”, and “Stay lost” define how states change over time.
3. **risk**: Represents a collection of events that define a specific risk, such as “Negative Balances Risk”, which includes events affecting balance states.
4. **user_state**: Indicates the state of a user’s balance at a given date. It determines if a user is in a “Positive balance”, “Negative balance”, or “Lost” state based on their balance and loss events.
5. **risk_state_start**: Marks the beginning of a risk state for a group with a specific amount and date. It is derived from the user state at the start date.
6. **risk_state_end**: Marks the end of a risk state for a group with a specific amount and date. It is derived from the user state at the end date.
7. **risk_path_probability**: Represents the probability of encountering a risk when transitioning between states over a number of periods, considering the occurrence of events.
8. **risk_path_probability_end**: Represents the probability of transitioning from a start state to an end state over a specified number of periods, summarizing the risk path probabilities.
9. **risk_state_probability_end**: Represents the probability of a risk transitioning from a start state to an end state over a number of periods. It aggregates the probabilities from risk path probabilities.
10. **risk_state_expected_loss_rate**: Represents the expected loss rate for an end state. It is calculated by multiplying the loss rate of the state by the probability of reaching that state.
11. **risk_expected_loss_rate**: Represents the overall anticipated loss rate associated with a specific risk. It sums the expected loss rates of all states.
12. **risk_expected_loss**: Represents the expected loss for a group, calculated by multiplying the expected loss rate by the amount at the start.
13. **count_state_start**: Represents the count of a state at the start. It is derived from the number of groups starting in that state.
14. **count_state_end**: Represents the count of a state at the end. It is derived from the number of groups ending in that state.
15. **risk_observed_state_probability**: Represents the observed probability of a risk ending in a specific state. It is calculated by dividing the count of the state at the end by the count at the start.
16. **risk_observed_loss**: Represents the observed loss for a group at the end state. It is calculated by multiplying the end amount by the loss rate of the end state.
The predicates link through rules to form a cohesive risk assessment model. Events define state transitions, which are grouped into risks. User states determine initial and final risk states, which are used to calculate probabilities and loss rates. The model aggregates these calculations to determine expected and observed losses and probabilities, providing a comprehensive understanding of financial risks and their impacts.
AI assistant
Combining the ontology together with all of the reasoner — LLM interactions above, we can unleash the full potential by creating our own AI assistant with which we can chat about the different rules, how they work, but also how specific results were derived:
chat("What are the risks associated with users?")
Generates the following response:
The risks associated with users include transitioning from
a "Positive balance" to a "Negative balance" with a probability of 0.1,
transitioning from a "Negative balance" to a "Lost" state with a probability of 0.8,
and remaining in a "Lost" state with a probability of 1.0.
The "Lost" state has a level of loss of 1.0, indicating a complete loss.
Additionally, users may experience "Recovery" from a "Negative balance"
to a "Positive balance" with a probability of 0.2,
and "Stay positive" where the "Positive balance" remains unchanged with a probability of 0.9.
The expected loss for a user is calculated based on these transitions and their associated probabilities.
Text to Risk and challenges ahead
So far we implemented flexible and scientifically grounded methodology and with the help of LLM, delivered a user-friendly interaction without sacrificing accuracy and objectivity.
However, if we are to fully automate the process, we ought to improve the initial step of manually coding our specific risk instances. One way to do this is by using the LLM as software developer which has to follow both correct syntax but also the codified risk instances have to be compatible with the generic risk ontology. In that case, we can think of the ontology as a schema which provides a template for the LLM for what constitutes a valid risk. The success of the LLM can then be tested via compiling the existing ontology and the newly generated risk by the reasoner.
Our concept workflow is the following:
- Risk manager: describes new risk and references data sources where its events can be observed.
- LLM: generates code for the new risk instance including the chain of events and possible states, as well as bindings to the data sources.
- Reasoner: adds the new risk to the existing ontology and compiles it. If compilation is successful, the risk is sent to the risk manager for review. If not, it is sent back to the LLM for correction.
The above is a separate project by itself and is similar to the emerging topic of AI agents for code generation and iterative testing. Nevertheless, this is just another highlight of the vast potential for future development that is made possible by our scientific approach to Risk.
