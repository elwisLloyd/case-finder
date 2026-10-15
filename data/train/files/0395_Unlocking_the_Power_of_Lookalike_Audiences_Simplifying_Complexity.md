# Unlocking the Power of Lookalike Audiences: Simplifying Complexity

Источник: https://medium.com/mercadolibre-tech/unlocking-the-power-of-lookalike-audiences-simplifying-complexity-74275f537e20

Unlocking the Power of Lookalike Audiences: Simplifying Complexity
At Mercado Libre, we constantly encourage our users to make the most of our ecosystem, experiencing a WOW! in both the financial world (Mercado Pago) and online shopping (Mercado Libre). However, this poses a significant challenge: “delivering the right value proposition to the right user while minimizing spam for others”.
Every day, our Marketing and Business teams send millions of communications with the goal of acquiring new customers, preventing churn, and generating cross-selling proposals to enhance our users’ 360-degree experience. These actions are carried out through various channels, including email, real estate, and push notifications.
To ensure precise execution of these actions and develop impactful contact strategies, it is crucial to have a deep understanding of our users’ profile. This provides us with a competitive advantage in improving campaign conversion rates.
Let’s explore the different types of user profiles:
- Persuadable: These customers convert when stimulated and pay attention to promotional campaigns; they play a vital role in the incremental success of our campaigns and represent the quadrant with the greatest growth opportunity.
- Loyal: These customers actively engage with our products. They are loyal and frequent consumers.
- Unpersuadable: These customers show no interest in our value proposition and are unresponsive to marketing efforts or stimuli.
- Beware: These customers are not swayed by promotions and, if they find them boring, we can discourage their purchase.
Taking into account these four user profiles will help us generate different data products to maximize our ROI by focusing on the customers in the upper quadrants (Persuadables and Sure Things) and disregarding those who are not interested or not at the right moment in their User Journey.
To design a precise strategy, it is essential to predict future actions or identify the stimuli that can change the user’s opinion. Machine Learning and Artificial Intelligence models provide us with a solution.
Current marketing teams have access to a wide variety of Machine Learning and Data Science tools and techniques, which can be grouped into 3 types: descriptive, predictive, and prescriptive.
- Descriptive: it summarizes what we know, e,g,: “The conversion rate has increased by 10%.”
- Predictive: it makes predictions about what we don’t know, e.g.: “John is 70% likely to churn next month.”
- Prescriptive: it makes recommendations about what we should do, e.g.: “Send a push notification to John to increase his chance of buying by 20%.”
Undoubtedly, with the advent of new technologies, Machine Learning and AI techniques have become great allies in discovering valuable insights about each user segment and applying them to various business decisions. Achieving a perfect balance between communication and conversion is essential, maximizing the potential to attract new users without being intrusive or completely losing their attention (also known as OPT-OUT).
This article explores a range of techniques with different uses and purposes, that allow us to create propensity models and, above all, Lookalike models.
Lookalike Models
A lookalike model, also known as a “similar audience” is a technique used in marketing and advertising to identify and reach new potential customers who share similar characteristics with a specific group of existing customers, particularly successful ones. In other words, it involves analyzing the behaviors and attributes of customers who have taken a specific action such as purchasing a product or service, and then seeking potential customers with a similar profile.
This approach is based on the premise that if a group of people has already shown interest or commitment to a particular service, brand, or product, individuals with similar characteristics are likely to do the same. Facebook introduced this technique to its platform in 2013, and since then, several Ad-tech platforms have also started offering their own version.
Lookalike models are a powerful tool for reaching new customers who share similar characteristics with existing ones, exploring new customer segments, and improving return on investment (ROI) in advertising, discounts, and acquisition.
To create a lookalike model, you should follow these steps:
- Seed Group: Start by selecting a group of current customers who are representative of your most valuable customers. This can be based on their purchase history, website interactions, subscriptions, and other relevant factors. The more specific and relevant this base group is, the better the lookalike model will perform.
- Relevant Data: Collect data about your customers that allows you to identify important aspects and describe usage and consumption patterns of your products. This can include demographic information such as age, gender, location, as well as behavioral data like purchase history, purchase frequency, and products acquired. Gather any other relevant details specific to your business.
- Train Model: Choose the ML model that best suits the business you want to model, whether it is a classification model, clustering model or a hybrid approach.
- Backtesting: Before impacting users in production, it is important to carry out a simulation of how your model would have performed. Backtesting is the most suitable approach for this. It involves taking a completed marketing campaign and using the model to evaluate your users and see how the predictions are ranked. Accompany the results with a Decile analysis for the perfect combination to fine-tune your model.
- Deploy to Production: Deploy your data pipeline and trained model in your preferred MLOps environment. This enables continuous monitoring and ensures the correct lifecycle management of your model.
The path to follow sounds excellent and challenging but still, some questions arise:
- Do I have to go through this whole flow for each campaign?
- What team do I need to develop and maintain these data products?
- Does the user also need to be an ML expert to use it?
- How can I scale this solution in a “self-service” way for a company like Mercado Libre?
There is no doubt that Machine Learning (ML) is a powerful tool that can be used to solve a variety of problems. However, developing and implementing an ML model can be a complex task, especially for users without solid experience or programming knowledge.
Next, we will describe how we’ve designed and developed a tool to create and implement ML models using a non-code platform, specially designed for users without coding knowledge.
Machine learning (ML) has become an indispensable tool in various industries. Yet, its adoption has traditionally been limited to individuals with specialized programming and data science skills. However, with the advent of “no-code” or “Auto ML platforms,” democratizing the application of ML and making it accessible to non-experts has become a reality.
No-code platforms are specifically designed to be user-friendly, even for those without a solid programming background. This accessibility makes them an excellent choice for companies and individuals who want to leverage complex techniques to solve problems but lack the time or resources to learn how to develop and implement a model from scratch.
Democratizing ML Tools
There are several benefits to democratizing access to machine learning tools, including:
- Increased productivity: ML tools can help employees automate tasks, freeing up time for more creative and strategic work.
- Improved decision-making: ML tools can empower employees to make better decisions by providing them with valuable insights and information they may find it hard to find on their own.
- Reduced costs: ML tools can help businesses cut costs by automating tasks.
- Enhanced innovation: ML tools foster innovation within companies by offering alternative approaches to problem-solving and to creating new products and services.
In the same way, there are some benefits of using “No-Code or AutoML” platforms:
- Reduced development time: These platforms can help reduce the development time of ML products and services by providing a drag-and-drop visual interface that simplifies the creation and configuration of ML models.
- Increased accessibility: These platforms can help increase the accessibility of ML products and services by enabling non-technical or non-expert users to easily create and deploy ML models.
- Improved collaboration: These platforms can improve collaboration by providing a central platform where users can share and collaborate on machine learning models.
Overall, providing access to machine learning tools to more people within the company can help improve productivity, decision-making, costs, customer service, and innovation. This, in turn, can generate a range of benefits for the company, such as revenue growth, expense reduction, and increased customer satisfaction.
Technological solution applied
The main objective from a technological perspective is to provide a user-friendly tool for individuals without programming knowledge. For this reason, Dataiku was chosen, primarily for its ability to generate Machine Learning applications that are easily accessible and intuitive. The user does not require deep technical knowledge and can focus on solving the business problem.
In the case of lookalike audiences, the focus is on defining the key features that will determine the search for “lookalikes” or define the predictive model.
The Lookalike application is structured in a “wizard” format with 4 main sections:
- User Selection
- Feature Selection
- Model Training
- Prediction
Below are some technical details regarding the use of each of these sections and how they contribute to the overall functionality of the solution.
User Selection
The selection of initial data for the application’s training involves several decisions by the user:
- Selecting the Seed Group Table where the model is located: The user needs to choose the table where the Seed Group, with targets 1 and 0, is located. This table should be hosted in BigQuery. This step is crucial and requires significant user intervention, as it relies on the user’s business knowledge to define “who is an interesting user” and who is not. By doing so, the user defines the contrast and sensitivity of the model.
- Choosing “Books Features” and “Features Timeframe” to be included in the training of the model: The user can select from three main Books, each containing hundreds of features associated with the use of our products and behavior/consumption patterns: Fintech, Commerce, and Cross. These features are calculated at runtime, allowing the user to configure the associated time frame in the “Feature Time Frame” option. For instance, if the user wants to consider or learn from recent patterns, they can include time frames of “15” and “30” days. On the other hand, if they want to analyze continuous patterns or trends, time frames of “90”, “60”, and “30” days can be included.
It is important to consider that this information comes from a library in the MELI technology stack called “ds-meli-abt”, so all the details and catalogs regarding the created features can be referred to in this project. [1]. With the help of this library, used by the application, we have the capability of “computing once, running anywhere and anytime”. This means that calculations are done once and can be executed anywhere and at any time.
Feature Selection
In this step, the “feature engineering” stage is carried out, which involves a semi-automatic process. This process is named so because, supported by the application’s suggestions and the user’s knowledge regarding the business problem being solved, it gives the user the ability to select the features that will determine the predictive model. This process is fundamental and directly affects the results.
As mentioned earlier, the application suggests a set of features based on cleaning criteria. Basically, it discards features that do not provide relevant information and potential features that may lead to overfitting, which is when the model performs well on the training data but poorly on new data (reference). The algorithm for feature selection is detailed below.
Suggested Feature Selection
When executed, this tool identifies the most relevant set of features and eliminates those that could potentially cause overfitting of the model. To prevent this, the following algorithm is used.
Get Alexis Peña y Javier Bianco’s stories in your inbox
Join Medium for free to get updates from this writer.
Algorithm (K Features)
- Let i be a feature.
- Train a binary classification tree K using the Weight of Evidence (WOE) transformation.
- Perform a test on the feature:
- Exclude all features with an Information Value (IV) less than 0.1 (irrelevance).
- Exclude all features that suggest a perfect classification observed in the confusion matrix (above a threshold).
4. Repeat step 1 until all features are completed.
5. Train a classifier model using XGBoost with all the variables that passed tests 1–3 and select the 50 most important ones.
Custom Feature Selection
This feature enables the selection of the most relevant features by utilizing an XG BOOST classifier as an initial suggestion. The process involves iteratively removing features manually. Optionally, this process can start from the suggested model or from the previous step of data loading, allowing for the skipping of the previous step if desired.
Training the model
Once the relevant features have been selected and irrelevant or noisy data has been cleaned up, the final model is trained and selected using a set of techniques known as the “Champion Challenge”. These techniques include Random Forest, Light GBM, XG Boost, and KNN.
To ensure reliability of the selected model, users should validate it using various model quality metrics such as accuracy, recall, ROC AUC, and confusion matrix. These metrics are readily available and are shown in the following image.
Based on this report, it is necessary to determine whether the trained model meets the predictive capacity and therefore generates value to effectively increase the audience.
Backtesting
Once the model has been trained and validated technically, it is advisable to conduct a test or simulation using real data or previous campaigns before proceeding with the scoring process (explained in the next section). This involves comparing the disparities and similarities between “what our model would have predicted” and “what actually happened”. This experiment is commonly referred to as backtesting.
To perform this task, we require a fully executed marketing campaign as a basis for the simulation. Here is the step-by-step process we follow:
- We identify all users who actively engaged in the marketing campaign and assign two binary flags: communication open and campaign conversion.
- Using the trained model, we assign a score to all users.
- We conduct a decile analysis to analyze conversions across various segments or buckets.
The decile analysis allows us to identify earnings by ranges, which helps define the calibration and strategic cutoff points along with the corresponding ROI functions for each business. This validation is crucial and mandatory for conducting subsequent tests in direct customer contact campaigns.
Prediction
During this phase, individual scores are generated to determine whether each individual is a “lookalike” or the likelihood of them being one, based on the trained model. Additionally, the intensity level of the score enables the definition of different actions. To simplify the interpretation and use of these scores, they are categorized into buckets or deciles defined in the previous step.
The outcome of this step is automatically saved in a BigQuery table that includes the scores and all the attributes utilized by the model. This provides users with the flexibility to perform any required analysis.
Finally, the score or simplified score in deciles, along with the model specifications, allows us to profile the audience and define the next actions.
User Onboarding
A fundamental element for the success of this tool is a proper user onboarding process, which provides them with support and assistance throughout the development of their first project, from start to finish. It is also necessary to measure their satisfaction with user experience (UX) as well as the impact generated on the business.
To meet these three pillars, we have created a Beta-Users group, where each participant brings their project to develop and receives support in different stages of the lifecycle:
- Use case definition: Using a design canvas, the user defines the main guidelines of the project and the functional details of the initial group (seed group).
- Weekly support meetings: With the defined seed group and their table in BigQuery, we guide them in developing their first model. The objective is to explore all the options of the tool and train their first Lookalike model.
- Backtesting: Before going into production, it is necessary to validate the performance and calibrate the use of the model. For this purpose, we use a similar campaign that has already been completed to see the ranking of the trained model. We obtain an expanded decile report to calibrate the model and make strategic decisions regarding the use of scores.
- Marketing Test: This involves designing an experiment where we send two well-defined campaigns that will compete against each other: BAU vs Lookalike. Let’s take the following example as a classic experiment design:
- Root Audience: Formed by all users who meet the basic conditions to acquire Product X.
- BAU Audience: Formed by 50% of users randomly chosen from the Root Audience, which are filtered again by the rules that currently define the BAU audiences.
- Lookalike Audience: Formed by the remaining 50% of users randomly chosen from the Root Audience, which are filtered based on the decile calibration generated in the previous step.
Both audiences are sent on the same day and time, and different performance metrics are measured, such as open rate, conversion rate, lift, and cost per acquisition.
5. Deploy to production: Finally, if the Lookalike campaign outperforms the BAU campaign, the model is sent to our production environment called Fury Data Apps (FDA). An automatic execution job is generated to make the audiences with scores available in BigQuery for the entire company’s use.
Feedback and Continuous Improvement
As stated in our MELI DNA, we remain in Continuous Beta mode throughout the entire lifecycle. In addition to providing support, we actively gather feedback on bugs and feature requests to plan for the next version of the tool. During our interactions, we have identified two key areas where there is a lack of understanding:
- Accurate definition of the business universe to be modeled.
- Appropriate design of the initial group (seed group).
We are currently discussing new features that will enhance the user experience (UX) by addressing the interpretation of model performance and analysis of deciles in future versions.
Currently, we have 18 beta users with 16 projects, of which:
- 3 projects have already been automated in FDA, our ML model development and deployment platform.
- 90% of users have successfully trained their first model.
- 75% of users have conducted marketing campaign tests.
- Remittances in Mexico: Increase Conversion Rate by 1,66X from 0.03% to 0.05% and decrease the Contact per Acquisition by -38%
- Portability in Brazil: Increase Conversion Rate by 2X from 0.14% to 0.28%.
- Point in Mexico: Increase Conversion Rate by 2,66X from 0.03% to 0.08% and decrease the Contact per Acquisition by -62%.
After completing this initial stress testing phase of the tool and gathering key improvement points from users, our goal is to open access to all Meli teams so that each one can independently manage the setup of their own campaigns. This approach ensures the democratization of access to decision-making using advanced techniques in a simple manner.
As we have demonstrated, unlocking the power of Lookalike Audiences is simple once you understand how to do it. This technique allows you to identify and reach new potential customers who share similar characteristics to your existing successful customers. By applying Lookalike models, you can enhance your marketing strategies, increase campaign effectiveness, and maximize return on investment. Do not underestimate the power of connecting with the right audience and offering them a personalized experience! There’s no denying the importance of continuously exploring and leveraging Machine Learning techniques to drive the growth and success of a business.
