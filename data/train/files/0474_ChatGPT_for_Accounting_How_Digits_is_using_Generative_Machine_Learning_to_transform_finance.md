# ChatGPT for Accounting: How Digits is using Generative Machine Learning to transform finance

Источник: https://digits.com/developer/posts/assisting-accountants-with-generative-machine-learning/

ChatGPT for Accounting: How Digits is using Generative Machine Learning to transform finance
ChatGPT, one of the largest and most sophisticated language models ever created, has recently become a household topic of conversation. If you've been wondering how this incredible technology can be applied to the accounting and finance space, this is the article for you :)
Welcome to chapter two of our three-part series on machine learning! We kicked off with an introduction to similarity-based machine learning, and how we apply it to accounting use cases at Digits. Today, let's explore generative machine learning and what it can bring to the accounting world.
Generative machine learning has received significant attention because it opens up a completely new field of "AI". It is getting closer to fulfilling the human dream of teaching machines some form of "creativity." Model architectures like ChatGPT, DALL-E, and T5 have provided solutions to various problems including writing text, generating photo-realistic images, and summarizing complex topics. In this blog post, we are excited to explore machine learning for natural language generation and how we are using these concepts today at Digits.
What is Generative Machine Learning?
Traditionally, machine learning has been applied to classification problems, where you take some text and distill it into different buckets or categories. You can think of the text as being "encoded" into those categories. For years, the dream has been to push beyond that, and train a machine learning model that can actually generate text, rather that just classify it. How might that work?
Researchers began building on this approach by experimenting with model architectures that first reduce information through a model encoder and then "decompress" the information back into human-readable text through a decoder. They made a significant breakthrough in 2017 when they presented an encoder-decoder model architecture called Transformer.
The model architecture shown above shows the encoder (left side) – decoder (right side) structure. Over the last few years, researchers further refined this architecture by increasing the number of model weights, which allows capturing more "knowledge" into the model, and by fine-tuning the decoder side to respond to decoder "instructions." The fact that models can now use "instructions" as model inputs unlocked meta-learning, where a model can generate text for untrained scenarios. For example, we can train a model on translating English-German and English-French, and through "instructions," the model can then be prompted to translate between German and French.
To generate text for a given input text, the decoder model uses the reduced information as an embedding it obtains from the encoder and the initial instruction to generate the first-word token for the generated text. Then it uses the newly generated token together with the instructions and the embedding to generate the second-word token for the text. This generation loop continues until the decoder has reached its maximum sequence lengths (usually 512 or 1024 tokens) or the decoder produces a stop-token instructing the decoder that any text generated following is considered padding. The generated text will then reflect the model's response to the input text and the given instruction. Here is an example:
Text:"Digits helps accountants save valuable time."
Instruction: "Translate from English to German"
Output:"Digits spart Buchalter/-innen kostbare Zeit."
Next, we will dive into how we use such generative models at Digits.
Why do we use Generative Machine Learning at Digits?
Digits' mission is to bring joy to small-business finance and help accountants WOW their clients, and we strive to save our users both time and tedium. Generative models play a critical role in this mission. Through generative models, we can assist accountants when they want to raise questions about a transaction with a client. In this case, we use generative machine learning to provide accountants with suggested questions they could ask about each transaction. The accountants can either confirm the question and send it to their client with just a click, or they can edit the question, but they won't have to type it all from scratch every time. This saves them valuable seconds on each and every client interaction!
What are the concerns about Generative Machine Learning?
The underlying models for generative tasks are almost exclusively trained by machine learning teams at large corporations like Microsoft, Google, or Facebook. OpenAI shared that training their 2020 GPT-3 3B model took 50 petaflop/s-days of computing power. Such pre-trained models are often open-sourced and made available for other companies, like Digits, to fine-tune for their domain-specific applications. While we have full control over the data we use for our fine-tuning training (more details on how we train generative models at Digits below in this post), we don't have insights into the training data used by the large model providers. This carries the risk of an implicit model bias originating from the training data.
Another concern around generative models is that they can hallucinate. This can happen because the decoder of the generative model generates text token by token (you can think of it as word by word). As explained earlier, the already-produced tokens of the generated text influence the next generated token. Therefore, generative models hold the risk of going off on a tangent (sometimes described as hallucinating) if a token was chosen during the unrolling, which might be more probable, but in this specific context, less relevant.
Here is an example of hallucination (which our quality checks caught):
Text: "transaction: CHICK-FIL-A #000001
Instruction: "Generate a professional sounding question"
Output: "What is this charge from chick-fil-a-fil-a-fil-a-fil-a-fil-a-fil-a-fil-a-fil-a-fil-a-fil-a"
In this example, the decoder failed to generate a stop token and got stuck generating "fil-a" over and over.
Despite these potential downsides, generative machine learning models unlock vast new capabilities to save accountants and small business owners time and tedium. In the following section, we'll dive into how we counterbalance the concerns around generative models to maximize the wins.
How do we make sure Generative Machine Learning is safe?
When we use generative models, we go the extra mile to make sure that we do so safely.
When our models generate suggested questions that will be seen by business owners, each output goes through at least three individual checks. First of all, we automatically screen every generated message for toxicity, insults, and obscenity. If the slightest indication is detected, we discard the text before it is ever displayed, and we automatically alert our Machine Learning team to investigate the incident.
Secondly, we validate generated suggestions against common patterns of hallucinations and automatically discard matches. Often, the hallucinations aren't toxic or insulting but rather completely out of context or confusing and therefore would diminish the product experience.
And last but not least, a human accountant will always review and confirm the model's suggested question before it is sent to a client.
Another critical aspect we care about is user privacy. We fine-tune machine learning models in-house and never share customer data without consent.
How do we train Generative Machine Learning Models at Digits?
For our generative models currently in production, we use a model of the T5 family as our base model. The base model has been pre-trained by the Google Brain team, and we fine-tune it for our domain-specific application. In the following three sections, let's dive into the generation of training sets, the actual model training, and how we evaluate generative models at Digits.
Take, for example, the question generation model below. For transactions that an accountant may need more context around, this model generates questions based on the description and features of the transaction. The accountants can then send the question off to their clients, or use it as inspiration and edit it as they see fit before submitting it to their clients.
Training Sets and Data Preprocessing
For this particular use case, we are fine-tuning a generative model to write questions based on two inputs:
- Transaction description
- Persona
We train our models to represent multiple personas: for example, to generate concise, professional questions or more casual and wordy questions. That way, the accountants can choose the tone of voice they prefer for each client. As accountants have varied relationships with each of their clients, preserving the authenticity of that relationship, even in generative text, is critical.
Here is an example of our training data structure:
Transaction: UNITED AIR 6786632 11/22 NY
Question: Can you tell me more about this travel expense?
Transaction: SQ* COFFEESHOP ST JOHNS PORTLAND
Question: Can you tell me what this coffee shop expense was for? 
After mapping the transaction descriptions with the respective persona, we preprocess the training data into the data structures expected from the underlying T5 model. All the data preprocessing happens with TensorFlow Transform, which allows us to scale our preprocessing jobs via Google Cloud Dataflow. We can export the preprocessing graph later, which simplifies the model deployment tremendously.
def preprocessing_fn(inputs: tf.Tensor) -> Dict[Text, Any]:
    """tf.transform's callback function for preprocessing inputs.
    Args:
      inputs: map from feature keys to raw not-yet-transformed features.
    Returns:
      Map from string feature key to transformed feature operations.
    """
    outputs = {}
    tmp = {}
    PAD_ID = tf.constant(0, dtype=tf.int32)
    input_ids = tokenizer.tokenize(inputs["text"])
    input_ids_dense = input_ids.to_tensor(default_value=PAD_ID)
    input_ids_dense = input_ids_dense[:, : configs.ENCODER_MAX_LEN]
    padding = configs.ENCODER_MAX_LEN - tf.shape(input_ids_dense)[1]
    input_ids_dense = tf.pad(input_ids_dense, [[0, 0], [0, padding]], constant_values=PAD_ID)
    input_ids_dense = tf.cast(tf.reshape(input_ids_dense, (-1, configs.ENCODER_MAX_LEN)), tf.int64)
    input_mask = tf.cast(input_ids_dense > 0, tf.int64)
    output_feature_ids = tokenizer.tokenize(inputs["question"])
    output_feature_ids_dense = output_feature_ids.to_tensor(default_value=PAD_ID)
    output_feature_ids_dense = output_feature_ids_dense[:, : configs.DECODER_MAX_LEN]
    padding = configs.DECODER_MAX_LEN - tf.shape(output_feature_ids_dense)[1]
    output_feature_ids_dense = tf.pad(output_feature_ids_dense, [[0, 0], [0, padding]], constant_values=PAD_ID)
    output_feature_ids_dense = tf.cast(tf.reshape(output_feature_ids_dense, (-1, configs.DECODER_MAX_LEN)), tf.int64)
    output_feature_mask = tf.cast(output_feature_ids_dense > 0, tf.int64)
    # Stitch together output dict
    outputs["input_ids"] = input_ids_dense
    outputs["attention_mask"] = input_mask
    outputs["labels"] = output_feature_ids_dense
    outputs["decoder_attention_mask"] = output_feature_mask
    return outputs
For the text tokenization, we use the FastSentencePieceTokenizer from TensorFlow Text. TensorFlow Text allows us to export the tokenization as part of the model (as shown below), and therefore the model can then accept raw text inputs as inputs to the model.
This removes the requirement to keep the tokenization in the data pipelines and the models in sync; it simplifies the model deployment process and avoids a common training-serving skew.
Model Training
We train our machine learning model through TensorFlow Extended (TFX) running on Google Cloud's Vertex AI platform. This setup allows us to scale our model training while keeping all training artifacts (raw data, preprocessed training data, trained model, evaluation results, etc.) in our company-wide metadata store.
Preprocessing the training data ahead of time makes the fine-tuning of the model straightforward.
metrics = [tf.keras.metrics.SparseTopKCategoricalAccuracy(name="accuracy")]
model = DigitsHuggingfaceT5.from_pretrained(configs.BASE_HUGGINGFACE_MODEL_NAME)
model.compile(metrics=metrics)
...
def _get_serve_features_signature(model, tf_transform_output):
    """Returns a function that parses a raw inputs and applies TFT."""
    model.tft_layer_inference = tf_transform_output.transform_features_layer()
    @tf.function(
        input_signature=(tf.TensorSpec((None,), tf.string, name="text"))
    )
    def serving(text, context):
        text = tf.reshape(text, shape=[-1, 1])
        transformed_features = model.tft_layer_inference({"text": text})
        outputs = model.generate(
            input_ids=transformed_features["input_ids"],
            attention_mask=transformed_features["attention_mask"],
            max_new_tokens=configs.DECODER_MAX_LEN,
            return_dict_in_generate=True,
        )
        sentences = model.tokenizer.detokenize(outputs["sequences"])
        return sentences
    return serving
_ = model.fit(train_dataset,
                epochs=constants.EPOCHS,
                validation_data=eval_dataset,
                verbose=2
)
model.save(
    fn_args.serving_model_dir,
    save_format="tf",
    signatures={
        "serving_default": _get_serve_features_signature(model, tf_transform_output)
    }
)
While we import a T5 model from HuggingFace as the base model, we convert all model ops to TensorFlow. This allows us later to deploy the model on TensorFlow Serving without needing a Python layer as part of the deployment. In the code above, you can see the reusability of the TensorFlow Transform layers from our data preprocessing step. That way, we can avoid the training-serving skew between the model training and the model deployment.
Model Evaluation
We evaluate every model version as part of our TFX training pipelines. Therefore, we developed a custom TFX component that checks our model version for five different metrics, compares the model version against the last released version, and then decides whether to recommend deploying the new model version. This allows us a consistent model comparison, and it removes humans from the decision-making process.
For the evaluation, we developed a data set with human-curated questions for each transaction. During our model evaluation, we compare the generated questions with the questions expected by the human curators.
Over time, we adopted several metrics to evaluate our generative models, including
- Levenshtein distance between expected and generated questions
- Semantic similarity between expected and generated questions
- Recall-Oriented Understudy for Gisting Evaluation (Rouge) metric
- Score of must-have and optional tokens
We want to tune our models to achieve a high language diversity. Therefore, we strive for a high Levenshtein distance (meaning that the generated question is expressed vastly different from the human-curated question) while we keep the semantic similarity between the expected and generated question high. We also evaluate our models through the "Recall-Oriented Understudy for Gisting Evaluation" (Rouge) metric, which is a standard metric for text generation models.
Here is an example:
Human curated: "Could you please share details about this meal expense?" 
Generated:  "Can you tell me more about this Starbucks charge?"
Levenshtein distance: 34.0 
Semantic similarity:  0.343 
Rouge-L f-score:  0.333
(An exact match would result in a 0.0 Levenshtein distance, 1.0 similarity score, and 1.0 Rouge-L f-score.)
Finally, we check our models for must-have and optional tokens. For example, our generative model can learn that a United Airlines transaction is related to a travel expense and therefore generate:
Transaction: UNITED AIR 6786632 11/22 NY
Question: Can you tell me more about this travel expense?
In this case above, we give the model "bonus points" for paraphrasing the question in the context of "travel."
Final Thoughts
Generative models can simplify accountants' interactions with clients and save them valuable time and tedium. In this blog post, we've highlighted the steps we have taken to adopt large generative models and fine-tune them for domain-specific use cases while keeping our intellectual property in-house and, most impotantly, our customer data private.
We introduced how we trained and evaluated generative models and, furthermore, we explained how we exported our fine-tuned generative model using the TensorFlow ecosystem.
All of this work is live in production, and you can experience it as part of the Digits product today!
Further Reading
Check out these great resources for even more details on generative models and how to perform Natural Language Preprocessing with TensorFlow Text:
Stay up to date with Digits
Unsubscribe anytime.
