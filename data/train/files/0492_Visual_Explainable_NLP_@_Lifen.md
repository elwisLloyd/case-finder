# Visual Explainable NLP @ Lifen

Источник: https://medium.com/lifen-engineering/visual-explainable-nlp-lifen-4d4dd5007205

Today at Lifen, our machine learning models (mostly NLP) serve more than 1M daily predictions to our users. This volume inevitably generates support requests when our AI is wrong or makes a counterintuitive prediction.
Our objective was to develop a tool that:
- streamline the support process by making our explainable AI tools easily accessible to authorized users
- is easily maintainable and always up-to-date with our AI
- provides some insight into how the ML model made its prediction
The end result
The result is a web app lifen-ai-explainer accessible internally to Data Scientists and Customer Support. Given a document id (provided by the client requesting support), this web app will display the anonymized document and predictions our AI made. (Predictions are also anonymised but made on the original document, otherwise, changes on the doc by anonymization process could produce different results)
We built lifen-ai-explainer and the pseudonymisation algorithm internally for this purpose and it’s been fully integrated into our daily processes since mid-2020.
Explaining classification
In addition to anonymizing and displaying the predictions, we try to explain them. For example, we want to understand how our machine learning text classifiers (eg: document type, patient gender) made their predictions by highlighting which words impacted the prediction the most.
Here is a demo of what this looks like on the patient gender classification algorithm (whose goal is to detect the gender of the patient mentioned in the document — without relying on the name — to. increase identitovigilance)
This feature proved useful in real-world situations to understand how for example a misread/misplaced word or simply a typo leads to a wrong prediction.
Explaining NER
We also use this tool to debug our NERs models. On the document view we show the raw softmax output (score for each class for each token), on the left side we show the final post-processed prediction.
How does it work?
Our classifiers are made with an Embedding + LSTM architecture (long documents, resources, and time constraints mean no Transformers). However, this architecture is not out-of-the-box well suited for explainability purposes.
Get Jean-Charles Louis’s stories in your inbox
Join Medium for free to get updates from this writer.
Let’s go into detail to understand why. Here we use the last hidden state that we pass to a dense layer and softmax to produce our prediction:
The problem is simply that we have no idea which word impacted the final prediction. (There is also a problem of vanishing gradient and bottleneck where if the important words are at the beginning of a very long sequence, the LSTM has to learn to remember it for many time steps) But we can fix that with a simple inexpensive tweak in the model.
Global attention layer
Our solution is to add a global attention layer (or attentive pooling layer) [1] that compute an attention score for each token with a dense + softmax layer which is then used to compute a weighted sum of all the hidden state at each time step (which roughly correspond to information contained in the current word).
This weighted sum is therefore a whole document embedding (similar to the last hidden state that we used in the previous architecture) that we can use for classification, but we also have in bonus those attention scores per word which we can interpret as “importances scores” for each word. Those scores proved empirically very interpretable.
The layer code
This layer is a simple Keras layer made from well-known building blocks. In practice, we use more than one attention head which can make the interpretation more tricky but improve performance.
def MultiGlobalAttention(timesteps: tf.Tensor, n_heads: int = 1) -> tf.Tensor:
"""Global Attention layer. Computes a weighted sum of all the timesteps.
Input: N timesteps of dim D
Output: 1 of dim D
Zhou et al https://www.aclweb.org/anthology/P16-2034  §3.3"""
attention = Dense(n_heads, use_bias=False, activation="linear")(timesteps)
attention = Activation(softmax_axis(1), name="attention")(attention)
weighted_sum = dot([attention, timesteps], axes=1)
return Flatten()(weighted_sum)
How to get those attention scores? We extract an attention sub-model that is not run in typical inference scenarios, but only for support in lifen-ai-explainer.
def attention_model(model: Model) -> Model:
"""make attention_model from model"""
return Model(inputs=model.input, outputs=model.get_layer("attention").output)
Architecture of lifen-ai-explainer (+ lifen-ai)
The web app is a React Single-page application written in TypeScript that communicates with a REST python backend based on FastAPI (the backend also serves the static files for the frontend).
The frontend tooling is based on Vite which handles all the complexity of a modern frontend app (we rather do data science than tinker with babel/webpack config files).
The web app needs to make the same predictions as lifen-ai. We therefore decided to build the backend as a python app that can import the existing lifen-ai as a library.
Python lacks explicit access modifiers, which can make it difficult to maintain good encapsulation and ensure the maintainability of a large interconnected codebase. We use import-linter to enforce encapsulation rules and allow lifen-ai-explainer to import lifen-ai but not the other way around.
How to keep our ai-explainer in sync with new features?
Our AI is rapidly evolving and we need lifen-ai-explainer to stay in sync at all times. We never want to be in a position where there is a new feature that we cannot debug with lifen-ai-explainer.
Mono repo & mypy & front-back client generation
We decided to put both apps in the same mono repo. This allows atomic changes: when making a Pull Request to add a prediction to lifen-ai, you can simultaneously add the implementation to lifen-ai-explainer. This is enforced by design: because 100% of our codebase is type annotated with mypy, a breaking change in lifen-ai will break CI for lifen-ai-explainer, so you are required to keep it up to date. Our unit & integration tests do the rest.
The frontend client is autogenerated by Orval using the OpenAPI spec which is also autogenerated by FastAPI. As a result, any changes made to the output of a model will cause the CI to fail and direct you to the exact location in the frontend code where updates are required 🎉.
We use poetry to manage python dependencies which don’t support mono-repo but allow us to split dependencies into groups. This way, lifen-ai-explainer includes all the dependencies of lifen-ai but not the other way around.
lifen-ai-explainer has been fully integrated into our daily processes since mid-2020 and we have since expended its features with a dataset labellisation interface, and a post-training errors review tool.
