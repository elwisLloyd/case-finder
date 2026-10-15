# Exploring an Entity Resolution Framework Across Various Use Cases

Источник: https://medium.com/walmartglobaltech/exploring-an-entity-resolution-framework-across-various-use-cases-cb172632e4ae

Agenda
- Introduction
- Challenges
- Rule-Base Entity Resolution
- ML Algorithm based Entity Resolution
- Case Study
- Summary
- Reference
Introduction
I want to take a moment to explain what entity resolution is in the way that we think about it. There are a lot of definitions for it. Such as:
1. Provides powerful insights about who is who, and who is related to whom
2. the process that resolves entities and detects relationships
Yes, it is. The idea is to identify that two records pertain to the same individual even when described differently. It is important to look for various parts, such as differences in names and addresses. Fuzzy matching techniques (which we often use in the search engine) are often needed to link their records and establish connections between them. This involves keeping track of possible matches and managing relationships between records, which could involve a disclosed relationship, like twins.
Also, Data Quality and Data elements also play a huge role in deciding which Entity Resolution process to follow.
We propose two approaches — Rule-based Entity Resolution and ML Algorithm-based Entity Resolution process based on Data quality and elements.
Challenges
Entity resolution is a complex task that involves identifying and linking records across multiple datasets. However, several challenges arise during the process, including:
- Inconsistent data
- Long text fields
- Need for contextual understanding
- Lot of Pre-processing needed to standardize the data
- Imbalanced data
Rule-Based Entity Resolution
Rule-Based is pre-defined. This approach involves creating a set of pre-established rules that must be met for two records to be identified as related to the same entity.
When we have standard identifiers like SSN, phone numbers, NPI, DEA, etc., We would need to use a rule-based approach for Entity Resolution based on the business use case and priorities.
Advantages:
- Accuracy of results, if we have good data, allows for creating customized rules that can be tailored to specific use cases.
- Increases transparency as the rules used to match are easily understood and analyzed (Transparency is super useful when there are strict regulations on data handling and privacy, such as in healthcare and finance.)
- Faster deployment processing time since it doesn’t require large amounts of training data and allows quick deployment.
Limitations:
- Time-consuming because the rule needs to be built by us, and we need to develop and maintain the rules.
- If we don’t have good-quality data, the accuracy will be lower.
ML Algorithm based Entity Resolution
Unlike rule-based ER, which relies on predefined rules. ML-based involves using algorithms to identify patterns and relationships in the data automatically. Dealing with text-based fields and having inconsistent data would require ML Algorithm based Entity Resolution.
Advantages:
- Reduce manual effort.
- Continuous learning and improvement (feedback loop).
- Useful when dealing with text-based fields.
- Works well with Inconsistent data.
- Provides a contextual understanding of data.
Limitations:
- While achieving interpretability in machine learning models can be challenging, there are several techniques that can be used to improve interpretability, such as LIME, SHAP, or MUSE.
- Labeling training data can be expensive regarding time, resources, and labor.
- It is important to carefully validate the training data and algorithm to address bias.
Case Study
Case Study 1: Rule Base
Suppose a company has a large customer database that contains records with three unique identity ids: PID, SID, and TID.
Get Jiazhen Zhu’s stories in your inbox
Join Medium for free to get updates from this writer.
After consulting with business stakeholders, it is determined that PID is the primary id, while SID and TID are secondary identity ids. This means that records with the same PID should be considered the same entity, even if they have different SID or TID values. But when PID is missing, we need to use SID and TID to link the records.
Our rule base logic is shown in Figure 1:
- The first rule states that if a PID (primary identity id) is found, it should be used as the unique id for the entity. This means that all records with the same PID value will be considered the same entity, regardless of any other identity is present.
- The second rule states that if a PID is missing or more than one PID is found, and a SID (secondary identity id) is present for a record that matches a PID value in the dataset, and the PID value should be used to create the profile for the entity. This means that if two records have different SID values but the same PID value, they should be considered the same entity.
- The third rule in this approach is similar to the second rule.
- The fourth rule is to generate new identity ids for unmatched records.
Case Study 2: ML Base
Suppose we have two datasets containing information about companies. One dataset contains company names, addresses, and other details, while the other contains similar information but slight variations in the company names and addresses. We aim to match the records across the two datasets to identify which ones refer to the same company entity.
Figure 2 illustrates the entire process flow of the discussed entity resolution approach.
Pre-processing
- Removing stop words and lemmatization.
- Feature Engineering by generating megaphones of name columns.
- Address Standardization using Google Geocoding API.
Exact match base
- Address(geocode match) exact match.
- Name exact match.
- Address matching by calculating the haversine distance between geo-locations.
Name match based on Ditto Model
- Novel entity matching system based on pre-trained Transformer-based language models such as BERT.
- Serializes each data entry into a text sequence and casts Entity Matching as a sequence-pair classification problem.
- To classify as match or not, token embeddings and Transformer layers from a pre-trained language model (BERT) and task-specific layers (linear followed by softmax).
Indexing using Blocking
- Without Blocking Candidate pairs would be (A1, B1), (A1, B2), (A2, B1), (A2, B2)
- With Blocking on first_name: (A1, B1 ), (A2, B2)
Example Module of Indexing using Blocking
- Indexing through Blocking of feature engineered variable (metaphone of First name, metaphone of last name) and date of birth matches completely.
- Comparison links are compared at the given threshold using ‘jarowinkler’ comparison:
compare.string(‘first_name’, ‘first_name’, threshold=0.70)
compare.string(‘last_name’, ‘last_name’, threshold=0.65)
- The comparison result is processed through a classifier that generates each comparison link's probability.
- Comparison link with probability >90 % will be identified as a Match.
Classification:
- Supervised Algorithms — Logistic Regression Classifier, Naive Bayes Classifier, etc.
- Unsupervised Algorithms — Expectation/Conditional Maximization classifier, KMeans classifier, etc.
Summary
Rule-based Entity Resolution works well with standard identifiers with non-text-based data elements. Coordinating with business partners to decide on the rules is the key factor.
ML Algorithm based Entity Resolution works well when dealing with text-based data fields, inconsistent data, and entity matching requires contextual understanding.
Future Direction: Building an automated Entity Resolution framework, which takes as input the datasets directly and generates an automated match/non-match classification using different ML algorithms.
