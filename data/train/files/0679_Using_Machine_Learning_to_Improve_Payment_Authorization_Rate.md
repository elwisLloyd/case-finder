# Using Machine Learning to Improve Payment Authorization Rate

Источник: https://medium.com/paypal-tech/using-machine-learning-to-improve-payment-authorization-rates-bc3b2cbf4999

When our customers make purchases with credit or debit cards in their PayPal wallet, we send the payment details through card networks to card issuing banks for payment authorization. During this process, payments can be declined by the issuing banks for various reasons, such as the card: exceeding its credit limit, not having enough balance, being reported as stolen, or outdated information(see here for more information regarding issuer declines causes).
Apart from these reasons, issuers also consider many other factors when deciding to approve or decline a payment request, such as: what type of card is being used for the payment? What merchandise is being purchased? What time is the payment request submitted? What is the card’s approval and decline history from issuers?
Improving authorization rate (or auth rate) — the percentage of issuer approved payment requests out of all payment requests made by customers to PayPal — is essential for us and our customers. Auth rate improvement through accurate issuer decline prediction can translate into millions of dollars of revenue increase for online merchants, and give customers a smooth shopping experience. It is especially critical for PayPal considering our scale as a global payment provider.
Recently, we built and deployed machine learning models to handle many of the dynamics in issuer decline prediction and successfully helped our payment product improve transaction auth rate and user experience.
Applying Machine Learning
Feature Engineering
In order to create relevant features for the auth rate optimization model, we aggregate raw transaction and issuer response data at a card-level in different ways. For example, we use:
- Issuer decline ratio for each card in the past N days.
- Issuers’ decline and approval pattern for different card bins and seller industries.
- Time and day when the transaction happens. Certain days of the week and days of the month have a higher success rate than other days.
Choosing the Best Model
Card issuers’ decision process to accept or reject a transaction is typically like a decision tree (see example below).
Naturally, it makes sense to choose a tree-based algorithm for the auth rate optimization problem as well. After experimenting with tree-based algorithms like Random Forest and Gradient Boosting Machine (GBM), and more complex models such as neural networks, we decided to use GBM for the production model as it had the best performance.
Gradient Boosting Machine is a forward learning ensemble method that builds many shallow and weak decision trees with each tree fitting to the residuals from the previous one and improving the model performance. A loss function is used to detect the residuals (for example, mean squared error for regression problems and log loss for classification problems).
Each tree is added to the existing sequence of trees using gradient descent to minimize the loss of the model. Once the maximum number of trees are added or the loss does not reduce any more, the training process is terminated.
During the model training process, we used Grid Search to fine-tune the optimal hyperparameters for the models, such as the learning rate, number of trees and depth of trees.
Evaluating Model Performance
Popular methods to evaluate model performance include ROC curve and ROC AUC. But in auth rate optimization, we frequently deal with highly imbalanced classification data. Our data is usually dominated by negative (approved) class and only contains < 5% positive (declined) class. Using ROC AUC might give us an excessively optimistic performance assessment of our model.
Get Lei Mu’s stories in your inbox
Join Medium for free to get updates from this writer.
To illustrate why the ROC AUC may be biased, consider the following experiment: two dummy datasets A and B are created. Dataset A is more balanced with 40% positive vs. 60% negative class distribution, while Dataset B is highly imbalanced with 5% positive class.
Then, we train decision tree models with the same parameters on both datasets and look at their ROC AUC.
We also plot the two models’ precision-recall curve:
Precision-Recall curve shows that Model B is not performing well, but the ROC curve tells a different story.
From the above experiment, we see that the ROC curve gives us an over-optimistic result for the model trained on imbalanced data. The reason is that the ROC curve considers both False Positive Rate and True Positive Rate, which cover both classes. In imbalanced datasets, as long as the model performs well on the majority class, the overall ROC AUC score can still be high.
True Positive % = True Positive / (True Positive + False Negative)False Positive % = False Positive / (False Positive + True Negative)
Precision and recall focus on each class individually. This makes it an effective tool for evaluating imbalanced models.
Precision = True Positive / (True Positive + False Positive)Recall = True Positive / (True Positive + False Negative)
Results
With the machine learning models trained following the above process, we were able to provide the following enhanced capabilities to PayPal’s payment product to improve transaction auth rate.
- More specific issuer response prediction to target different types of declines (Nonsufficient funds, Do Not Honor, Hard declines, etc.)
- Doubled the accuracy on issuer response prediction compared to rule-based solutions
- Scaled the model execution frequency to increase the number of scored cards
- Regular refresh with the latest data to keep the models up to date
In our live use cases, machine learning models predict if a card will be declined for a transaction and prevent the purchase from being completed. If a decline is predicted, we can create a custom experience that will ensure a valid purchase goes through, which has resulted in significant improvement of auth rates. For example, we can surface a different payment method in the user’s PayPal wallet that has been successful in the past, or request second-factor authentication and Card Verification Value (CVV number) to make sure the user is the real card owner.
Machine learning models also help us identify good cards so that we can approve their transactions when merchants face technical issues such as system outages that interrupt transaction processing. We can also go one step further by approving loyal customers even when their cards are declined by issuers. Both scenarios minimize losses for merchants and give consumers confidence that their payment will go through when using PayPal.
Finally, to learn more about how we use machine learning to improve our payment product, please see this article.
