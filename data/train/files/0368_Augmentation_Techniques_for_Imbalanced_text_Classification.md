# Augmentation Techniques for Imbalanced text Classification

Источник: https://medium.com/walmartglobaltech/augmentation-techniques-for-imbalanced-text-classification-f0d29c0f8ce1

Authors: Uruj Fatima, Deepak Singla, Subhadip Paul
Walmart Global Technology Center
Introduction
Data imbalance challenge often occurs in classification problems when some classes are more represented than others. Because of fewer data points, it is difficult for any machine learning model to learn characteristics of the minority class. This problem is predominant in scenarios where anomaly detection is crucial like fraudulent transactions in banks, identification of rare diseases, manufacturing defect detection, invoice reviews etc.
There are different techniques [1] to handle imbalance in data and can be broadly categorized into two groups:
- Algorithmic-level-approaches: These approaches focus on algorithm by modifying the classifiers to make them more robust to imbalance in distributions.
- Data-level-approaches: These approaches are more oriented towards the modification of the underlying dataset to make it more balanced either by under sampling or oversampling.
What is our approach?
Our approach, which tries to solve the problem of reviewing legal invoices for inconsistencies using machine learning, is more focused on the latter. It is more data-centric and compares different kinds of data augmentation methodologies, recommending the one that is best suited for the supplied dataset. It is agnostic to the kind of classifier used, thereby allowing more flexibility in comparison to algorithm-level approaches. Some of the data augmentation techniques that have been incorporated in our approach are as follows:
- Character: Two kinds of character-based augmentation methods have been implemented from NLPAug [2]
- Keyboard: This augmenter simulates typing error by using one keyboard distance to replace character by possible keyboard error e.g., we replace K with L and create augmented data since K is close to L on the keyboard.
- OCR: This augmenter simulates OCR error by using a pre-defined mapping to replace character by possible OCR error e.g., 0 (digit) is replaced with O (alphabet) since they look similar.
- Word: Two kinds of word-based augmentation methods have been implemented from NLPAug
- Contextual: This augmenter applies word level operations to text input by using contextual word embeddings.
- Back Translation: This augmenter applies word level operations to text input by leveraging two translation models for augmentation. Given an input text in some source language e.g., English, this text is then translated to a temporary destination language e.g., German, and then back to the source language.
- Sentence: The following type of sentence-based augmentation method has been incorporated
- Contextual: This augmenter applies sentence level operations to text input by using contextual word embeddings from two different models from XLNet and GPT2.
- Keywords to Sentence: This is a novel technique that has been introduced in the augmentation module. The idea is to first generate keywords from the textual sentences and then use these keywords to generate augmented sentences. YAKE [3] has been used for Keyword Extraction and GPT Neo for sentence generation.
Once the data is provided specifying the target and feature set, the module automates the following:
- Target Encoding: The target variable is one-hot encoded.
- Imbalance Data Check: Before proceeding with augmentation, it becomes important to check upfront whether the data even represents a case of imbalance thereby avoiding the need for unnecessary overhead of augmentation for a dataset that is already balanced.
- Train-Test Split: If data is indeed imbalanced, then it is split into train and test sets so that augmentation only takes place on the train set, avoiding any possibilities of leakage into the test set.
- Data Augmentation: Once the prior steps are performed, train dataset is passed through the different data augmentation techniques specified previously.
- Classifier: The module has an inbuilt bert-based classifier that fine-tunes the model with respect to the train data. This fine-tuning is carried out for each data augmentation technique to compare the performance against a baseline without any data augmentation.
- Evaluation Metrics and Comparison: Finally, predictions are made on the test set, and these are then passed through the different metrics like Precision, Recall, Weighted Balanced Accuracy and F-Beta Score to evaluate and compare the performance.
How does our approach perform?
Get Uruj Fatima’s stories in your inbox
Join Medium for free to get updates from this writer.
On over 100,000 line items from invoices, we tried different augmentation techniques for which results can be seen in the following tables. As can be seen in Table 1, we start with a baseline model that is unable to capture any of the minority class observations. Amongst word augmentation-based approaches, contextual word embedding does a good job of capturing 27% of the minority class observations with a precision of 50%, retaining the overall accuracy of 95%.
Table 2 captures the performance of the character and sentence-based augmentation techniques. While KeyboardAug is unable to capture any minority class observations, OCRAug does slightly better. Sentence based augmentation techniques fare poorly overall.
The new technique that we introduced in this augmentation module of Keyword to Sentence based augmentation does better than its sentence and character-based counterparts. Based on the results, we can conclude that the augmentation technique with contextual word embedding is giving best result where we see F1 score getting improved to 0.35 for minority class compared to 0 in baseline model. The next best F1 score for minority class is of 0.19 using the novel technique where we extract keywords using YAKE and use those keywords to generate sentence using GPT-Neo model, having 125mn parameters.
Conclusion
Our approach, by being agnostic to the type of classifier, provides a more flexible solution in comparison to algorithmic-level approaches. It incorporates the flexibility of different evaluation metrics for the user to choose from to decide on the best augmentation technique most suited for the business problem at hand. For our use case, contextual word embedding based approach performs the best followed by Keyword to Sentence based augmentation.
However, the scope of this blog is limited to analyzing this problem from the lens of text features. This study can be expanded to also incorporate a mix of text, numerical and categorical features in future, thereby widening the usability irrespective of the type of data at hand.
References
- López, V., Fernández, A., García, S., Palade, V., & Herrera, F. (2013). An insight into classification with imbalanced data: Empirical results and current trends on using data intrinsic characteristics. Information sciences, 250, 113–141. [1]
- Edward Ma. (2019). NLP Augmentation https://github.com/makcedward/nlpaug. [2]
- Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences Journal. Elsevier, Vol 509, pp 257–289. [3]
