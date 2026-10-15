# Candidate Generation Using a Two Tower Approach With Expedia Group Traveler Data

Источник: https://medium.com/expedia-group-tech/candidate-generation-using-a-two-tower-approach-with-expedia-group-traveler-data-ca6a0dcab83e

Candidate Generation Using a Two Tower Approach With Expedia Group Traveler Data
Modeling context and item features to improve traveler recommendations
At Expedia Group™ we make extensive use of machine learning for recommending a variety of products to travelers so that they can find the perfect trip. From search, price forecasting, to recommendations machine learning can be found in various parts of Expedia Group websites. In our search for improving our recommender systems, we have experimented with the Two Tower Neural Network for recommendations and it has shown promising results. In this post, we go over implementing one using an Expedia Group open-source dataset.
We assume you’re comfortable using neural network libraries and spark, as we will use TensorFlow for building the model and PySpark for processing the data.
Two stage recommenders
When building a recommendation system in industrial settings we must typically consider the constraints produced by large item corpora. One such strategy for dealing with a huge item corpus is the two-stage pattern. The two-stage pattern separates the recommendation into the following steps, a candidate retrieval stage, and a ranking stage. Wherein the candidate stage we are interested in reducing our recommended items to the N most relevant items for the given query so that it is more manageable for our ranking stage. For example, our item corpus might contain 10 million items, but obviously reranking 10 million items every time we present a recommendation is intractable. The ranking stage is exactly as it sounds, the candidates produced by the candidate stage will be ranked so that the most relevant items are at the start of the recommendations list.
The graph below taken from Eugene Yan’s blog [1] clearly outlines how these two stages might work in practice and for a more detailed explanation on this topic please visit their site.
To tackle the retrieval stage we will be implementing a “two tower” neural network that will allow us the flexibility of using a variety of data as input to represent the user and item, such as historical interactions in the user tower alongside other “static” features or “non-tabular” data sources such as text. This model pattern also has nice properties that allow for fast and memory-efficient negative sampling and indexing of candidates for efficient retrieval when in production.
Model architecture
The “two tower“ architecture has seen wide success in a variety of recommendation use cases across different domains. Its major advantages are in its scalability to huge industrial product corpora due to its ability to store the item representations for ANN search (more on this later), and the flexibility that neural network architectures provide. For example, being able to model different data representations such as the implementations of Pinterest [3] and eBay [2] for representing user historical interactions with sequence-based models or by modifying the loss for increasing the diversity of retrieved items [7].
In the simplest case the two tower architecture is composed of the following, a “query encoder“, and an “item encoder”. The output of each encoder is interacted through a dot product and then fed into an activation function such as the SoftMax or sigmoid. The query encoder learns a representation from features such as a search query, reference item, user historical interactions, or any other sort of context related to the user and their search query. While the item encoder takes as input the candidate item and usually represents it through content features e.g., in the case of Expedia lodging, the property location, popularity-based features, and property amenities.
A bare-bones encoder is usually composed of a stack of fully connected layers with some nonlinear transformation (a ReLU in most cases). Critically, the output of each encoder i.e., the query encoder and item encoder output vector must be the same size due to the final dot product interaction in the network (the figure shown above illustrates this).
To train this model the two most popular losses are binary cross-entropy and categorical cross-entropy loss. Since we are using tf-recommenders for this tutorial we will be utilizing categorical cross entropy but with an in-batch sampled SoftMax strategy as this is the most out-of-the-box solution. Using another strategy with a different loss function would require a bit more work but is still possible with tf-recommenders.
The in-batch sampled SoftMax strategy allows us to use the examples in our batch as negatives (i.e., examples that the user did not interact with for that given query) without having to use resources to sample through our entire dataset. It is fast and has been shown to do well in not only recommendation systems for e-commerce settings but also other domains such as in the Question Answering domain [9].
You might ask why one would want to use this strategy instead of just computing the full SoftMax? Although, the item corpus is not huge for our tutorial, in practice the cardinality of the candidate set can reach millions making learning the full SoftMax intractable. For example, say we have 20 million products in our candidate set, computing the full SoftMax with a one-hot representation would require us to have a vector of size 20 million which would lead to memory issues. Instead by using the other targets in the mini-batch as negatives, we are left with a much smaller label matrix (or target matrix). In the usual SoftMax case your label matrix is of size (minibatch size, nb_classes) but since our number of classes is reduced to the items in our minibatch we are left with (minibatch size, minibatch size), more details on how this matrix is generated during training is shown later in this post.
However, one issue to note with the sampled SoftMax is that negatives are drawn from the data of positive interactions which will lead to a bias toward popular items. One way to correct this is to perform the logQ correction, which can be computed by subtracting the log probability of that item occurring within the data from the logits. A more math-heavy explanation is out of scope for this tutorial; for a more detailed explanation on the logQ correction please refer to [5] and [6].
One example of the how not using the logQ correction can impact model performance can be seen in the work by Xinyang Yi et al [4] (Table 1 below from paper [4] shows their experimental results). They experimented with two tower models for retrieving Wikipedia pages . Although they were demonstrating a streaming algorithm for calculating the probabilities of items, it’s still a solid example of how not applying the logQ correction can have disastrous effects on the performance of the model.
Although one can apply the logQ correction to help mitigate the bias induced by in-batch sampled SoftMax, there are other techniques that address this selection bias such as Mixed Negative Sampling from the work of Ji Yang et al. [14]. In its most basic form, the idea is to sample uniformly from all of your possible candidates to address the problem that in-batch sampled SoftMax can never generate negatives from items that were never interacted with in the training data. These negatives can be passed through the “item tower” and then the dot product score can be computed as usual. To accommodate the increased size of the logits matrix due to adding the mixed sample negatives; zeros can be appended to the right of the label matrix. Since we are computing a SoftMax over the sampled items appending zeros is just including other classes in the SoftMax computation.
Implementation
From here on out we will be going over the processing of the dataset and a simple implementation of a two-tower model.
Data
First, let’s download a dataset to develop our model on. We will be using an Expedia Group dataset released for use in travel recommendations
You can download the dataset from this dropbox linked here.
This dataset spans from a period of 2021–06–01 to 2021–07–31 and has been anonymized to protect user and commercial interests. The data is composed of “search results impressions” with over a million hotels, vacation rentals, apartments, and other property types. We encourage you to explore the data and apply recommendation modeling ideas to understand how well they perform on real traveler behavior.
Once you have your data the first transformation to the data will be to extract the positive examples, i.e., clicks, since we are training this model using in-batch SoftMax.
def add_impression_interaction_features(main: DataFrame) -> DataFrame:
return (
main
.withColumn("clicked", F.when(F.col('impression_num_clicks') > 0, 1).otherwise(0))
)
main_processed_clicks_only = main_processed.filter(F.col("clicked") == 1)
So as to not delve too much into the data processing as this post is geared towards the model itself, the most important things to note about the PySpark code are the following functions.
save_candidate_sampling_prob shown below computes the probability of that item occurring within the dataset which will be useful later on for the logQ correction.
def save_candidate_sampling_prob(data: DataFrame, candidate_column: str, path: str):
total_count: int = data.count()
counts: DataFrame = data.groupBy(candidate_column).count()
prob: List[Dict[str, float]] = (
counts
.withColumn("sampling_prob", F.col("count") / F.lit(total_count))
.select(candidate_column, "sampling_prob")
.toPandas()
.to_dict(orient="records"))
prob: Dict[str, float] = {d[candidate_column]: d["sampling_prob"] for d in prob}
save_pickle(prob, path)
When saving the data for TensorFlow we make use of tf-records and by utilizing the spark-tensorflow-connector library.
train \
.write.format("tfrecords") \
.option("recordType", "SequenceExample") \
.option("codec", "org.apache.hadoop.io.compress.GzipCodec") \
.mode("overwrite") \
.save(tfrecords_path)
There are comments explaining what to look out for in the code so if you plan on running this project please look at the PySpark ETL here.
Model
The model implementation for this blog can be found here, we will be going over the important parts of the implementation and will not be including whole class implementations, as much of the code is boilerplate.
Now first off let's create the “towers”, we can do this by creating a class that the user and item tower can inherit from by utilizing the tf.keras.Model class as the parent class. By using the tf.keras.Model class we can make use of the same machinery that we are used to from tf.keras.Sequential while being able to customize inner methods and this will be important later when we tie this with the tf-recommenders tfrs.Model class.
If you’re not comfortable with the tf.keras.Model class approach to building TensorFlow models refer here to the official TensorFlow documentation.
The TowerModel class constructor (__init__) shown below takes in some hyper-parameters and lists of features so that it is aware of how each feature being passed in the input tensor dictionary needs to be processed. For example, the way the model will process text features will be different from just categorical features such as a date.
class TwoTowerModel(tfrs.Model):
def __init__(
self,
user_model: TowerModel,
item_model: TowerModel,
vocab,
candidate_id: str,
task: tfrs.tasks.Retrieval
):
super().__init__()
self.user_model = user_model
self.item_model = item_model
self.candidate_id = candidate_id
self.task = task
self.item_lookups = {}
self.embeddings = {}
self._user_shared_embedding_features = None
self._item_shared_embedding_features = None
"""
for the rest of the init function refer to the repo
"""
def _set_tower(self, layer_sizes: List[int]):
# Use the ReLU activation for all but the last layer.
for layer_size in layer_sizes[:-1]:
self.dense_layers.add(tf.keras.Sequential([
tf.keras.layers.Dense(layer_size, activation="relu")
]))
# No activation for the last layer.
for layer_size in layer_sizes[-1:]:
self.dense_layers.add(tf.keras.layers.Dense(layer_size))
if self.output_l2:
self.dense_layers.add(L2NormLayer())
The function _set_tower in the class shows how we construct a basic MLP for the tower encoder. It is composed of simple “dense” layers and RELU activations except for the last layer with an optional l2 normalization.
Refer to _set_model_layers for different feature types were processed in TensorFlow for this model.
Now we can just create the UserTower and ItemTower classes by inheriting from the TowerModel class. This is redundant but allows us to modify how the user and item class are handled if need be in the future.
class ItemModel(TowerModel):
def __init__(self, layer_sizes, vocab: Dict[str, Dict[str, np.ndarray]],
categorical_features: List[CategoricalFeature],
multivalent_categorical_features: List[CategoricalFeature]):
super().__init__(layer_sizes, vocab, categorical_features, multivalent_categorical_features)
def call(self, x: tf.Tensor, *args, **kwargs) -> Dict[str, tf.Tensor]:
return super().call(x, *args, **kwargs)
class UserModel(TowerModel):
def __init__(self, layer_sizes, vocab: Dict[str, Dict[str, np.ndarray]],
categorical_features: List[CategoricalFeature],
multivalent_categorical_features: List[CategoricalFeature]):
super().__init__(layer_sizes, vocab, categorical_features, multivalent_categorical_features)
def call(self, x: tf.Tensor, *args, **kwargs) -> Dict[str, tf.Tensor]:
return super().call(x, *args, **kwargs)
Lastly, let’s create a model class that ties the towers together by inheriting from tfrs.Model and then overriding some methods.
As you can see below the class inherits from tfrs.Model and it only requires that you are able to compute two representations using a dot product and that the the class property task is set using a tfrs.tasks.Retrieval class for computing the loss.
class TwoTowerModel(tfrs.Model):
def __init__(
self,
user_model: tf.keras.Model,
item_model: tf.keras.Model,
candidate_id: str,
task: tfrs.tasks.Retrieval):
super().__init__()
self.user_model = user_model
self.item_model = item_model
self.candidate_id = candidate_id
self.task = task
The snippet below is the call function for the TwoTowerModel class. You might notice we don’t explicitly dot the output representations in the call method, this is due to tf-recommenders handling that for us in the tfrs.tasks.Retrieval class.
def call(self, features: Dict[Text, tf.Tensor]) -> Tuple[tf.Tensor, tf.Tensor]:
user_embeddings = self.user_model(features)
item_embeddings = self.item_model(features)
return user_embeddings, item_embeddings
The code below is from the call method of the tfrs.tasks.Retrieval. The dot product is performed by performing a matrix multiplication of the query representations and the item representations. This is exactly taking the dot product between the user and item embedding described earlier but by using the matmul operation we can compute the scores for batch_size-1 negatives at once.
scores = tf.linalg.matmul(
query_embeddings, candidate_embeddings, transpose_b=True)
Next, two important parent methods we override are train_step and test_step. Our implementation of the method train_step has two important modifications to make use of the parameters candidate_id and candidate_sampling_probability in the tfrs.tasks.Retrieval class call method. As you saw previously our model class stores the candidate_id and tfrs.tasks.Retrieval class as instance variables. We can use these instance variables to optionally grab tensors in the dict passed to the model’s call method so it can then be then passed to the Retrieval class call function shown a bit later.
Get Eric Rincon’s stories in your inbox
Join Medium for free to get updates from this writer.
The variable candidate_sampling_probability is especially important because it allows us to make use of the built in logQ correction in the Retrieval class as shown below.
class SamplingProbablityCorrection(tf.keras.layers.Layer):
"""Sampling probability correction."""
def __call__(self, logits: tf.Tensor,
candidate_sampling_probability: tf.Tensor) -> tf.Tensor:
"""Corrects the input logits to account for candidate sampling probability."""
return logits - tf.math.log(
tf.clip_by_value(candidate_sampling_probability, 1e-6, 1.))
An important note is that in our internal experiments, there is a large difference in performance when not using the logQ correction so it is critical that in most cases it is utilized during training. This is not a novel finding and is common practice when making use of the in-batch sampled SoftMax approach.
The variable candidate_id will be used for passing ids for removing accidental hits i.e., removing instances where there exists two of the same ids in the batch which can lead to problems as all other ids in the batch are assumed to be negatives.
A thing to note is that within the call function, the authors of the code mention that using an input mask is more “principled”, we have not tried this but it might be worth looking into.
class RemoveAccidentalHits(tf.keras.layers.Layer):
"""Zeroes the logits of accidental negatives."""
def call(self, labels: tf.Tensor, logits: tf.Tensor,
candidate_ids: tf.Tensor) -> tf.Tensor:
"""Zeros selected logits.
For each row in the batch, zeros the logits of negative candidates that have
the same id as the positive candidate in that row.
Args:
labels: [batch_size, num_candidates] one-hot labels tensor.
logits: [batch_size, num_candidates] logits tensor.
candidate_ids: [num_candidates] candidate identifiers tensor
Returns:
logits: Modified logits.
"""
# A more principled way is to implement softmax_cross_entropy_with_logits
# with a input mask. Here we approximate so by letting accidental hits
# have extremely small logits (MIN_FLOAT) for ease-of-implementation.
candidate_ids = tf.expand_dims(candidate_ids, 1)
positive_indices = tf.math.argmax(labels, axis=1)
positive_candidate_ids = tf.gather(candidate_ids, positive_indices)
duplicate = tf.cast(
tf.equal(positive_candidate_ids, tf.transpose(candidate_ids)),
labels.dtype
)
duplicate = duplicate - labels
return logits + duplicate * MIN_FLOAT
Now onto the train_step and test_step methods.
The train_step definition and its first line show how we default candidate_ids and candidate_sampling_probability to None as these are the default values in the call method of the Retrieval class.
def train_step(self, features: Dict[Text, tf.Tensor]) -> Dict[Text, tf.Tensor]:
candidate_ids, candidate_sampling_probability = None, None
In the train_step method snippet below, we check whether removal_accidental_hits was set to true (defaults to False) and whether the candidate_id was set to a string value so that we can grab the candidate ids tensor from the features input parameter of the train_step method.
if self.candidate_id is not None and self.task._remove_accidental_hits:
# yes we are accessing "hidden" instance variable...
candidate_ids = features[self.candidate_id]
if "candidate_sampling_probability" in features:
candidate_sampling_probability = features["candidate_sampling_probability"]
As you can see below the task call function shown will now always take these values as either None (the default) or the values we assigned to them.
loss = self.task(
query_embeddings,
item_embeddings,
compute_metrics=False,
candidate_ids=candidate_ids,
candidate_sampling_probability=candidate_sampling_probability)
Next, let’s go over how the label matrix for the sampled SoftMax is generated.
The code snippet. below is from the official tf-recommendors github in the call function of the Retrieval class.
num_queries = tf.shape(scores)[0]
num_candidates = tf.shape(scores)[1]
labels = tf.eye(num_queries, num_candidates)
The labels are created by calling tf.eye which generates an identity matrix based on how many query and item candidate embeddings are passed to it.
In the case where the number of queries and items is equal to the mini-batch size each row i and column i entry will be set as one and all other elements in that row will be zero which is exactly treating the other examples as negatives in the SoftMax case. This can be seen in the image above where the red elements in the label matrix created from the minibatch are the “negatives” and the diagonal is the “positives”.
Lastly, to train the model let’s write a simple training loop instead of only using .fit so that we can evaluate our model at the end of every epoch (this could be done at the end of N steps) but first let’s define what SCANN is. SCANN is an ANN (Approximate Nearest Neighbor) search algorithm that allows us to index our item embeddings for quick retrieval using our query representation. We can use this to quickly measure how well our retrieval model performs. Note, you don’t have to use SCANN to perform ANN search as there are alternatives such as FAISS [10] which have been shown to perform well. We default to SCANN as it easily integrates into TensorFlow pipelines and is competitive with other ANN libraries [11].
The train_loop function defined below trains the model for an epoch sets up SCANN fits scan to the new item representations and records the recall@k values.
def train_loop(
model: TwoTowerModel,
scann_params: Dict[str, Any],
train_dataset: tf.data.TFRecordDataset,
valid_dataset: tf.data.TFRecordDataset,
candidates_dataset: tf.data.TFRecordDataset,
train_opts: TrainOpts,
data_paths: DataPaths
) -> Tuple[TwoTowerModel, pd.DataFrame]:
summary_writer = tf.summary.create_file_writer(data_paths.tensorboard_log_dir)
compute_write_recall = ComputeWriteRecall(train_opts, summary_writer)
for epoch in range(1, train_opts.nb_epochs + 1):
history = model.fit(
train_dataset,
epochs=1,
callbacks=[tf.keras.callbacks.TerminateOnNaN()]
)
history = {k: v[0] for k, v in history.history.items()}
write_metrics(summary_writer, epoch - 1, history)
scann = tfrs.layers.factorized_top_k.ScaNN(**scann_params)
scann.index_from_dataset(
tf.data.Dataset.zip(candidates_dataset.map(  lambda d: (d[model.candidate_id], model.item_model_call(d))))
)
model.task.factorized_metrics = tfrs.metrics.FactorizedTopK(candidates=scann)
optimizer_config = model.optimizer.get_config()
optimizer = tf.keras.optimizers.Adam.from_config(optimizer_config)
compute_write_recall(model, scann, valid_dataset)
model.compile()
results = model.evaluate(valid_dataset, return_dict=True, verbose=0)
update_metrics(compute_write_recall.training_metrics, results)
write_metrics(summary_writer, epoch - 1, results)
metric = tfrs.metrics.FactorizedTopK(
candidates=tf.data.Dataset.zip(
candidates_dataset.map(lambda d: (d[model.candidate_id], model.item_model_call(d)))))
model.task = tfrs.tasks.Retrieval(
metrics=metric,
remove_accidental_hits=train_opts.remove_accidental_hits)
model.compile(optimizer=optimizer)
training_metrics = pd.DataFrame(compute_write_recall.training_metrics)
training_metrics["epoch"] = list(range(1, train_opts.nb_epochs + 1))
return model, training_metrics
Evaluation
To evaluate our model we split our dataset on the date 2021–07–24 to keep the last week of data for testing. We mark all clicked properties in each
Since we are building a retrieval model the main metric we are interested in is recall@k. We want to maximize the number of relevant items within a reasonable number of retrieved items without worrying too much about the ordering since we will rerank the retrieved items later using another model.
 for batch in valid_dataset:
scores, ids = scann(model.user_model(batch), k=k)
approx_results.append(ids)
ground_truth.append(batch[train_opts.recall_true_key])
The chart below shows how different model choices affect recall@k performance. BN refers to using a batch normalization layer right after the numerical inputs in order to standardize them, log(q) refers to applying the log(q) correction to the logits, and l2_norm refers to a normalization of the output of each tower. Applying batch normalization to the raw inputs has been shown to work well in some models such as TabNet [12] but the idea of using raw features and applying transformations during training and not in a preprocessing stage can also be seen in models such as DASLAC [13].
The naming convention below is the following, the model with only BN in the name would a be model that only applies a batch normalization to the numerical inputs and does not include the log(q) correction and output normalization. While the BN+log(q) utilizes a batch normalization layer and log(q) correction.
We can see that for all recall@k values the BN+log(q)+l2_norm model outperforms the rest and the BN only model severely underperforms the other two. This is exactly as we expect and ties to our earlier point about the importance of applying the log(q) correction.
The graphs below show the recall@k values across epochs for all three models and indicate that training for more epochs might improve performance.
We would like to note that we did not perform experiments across different random seeds and did not conduct extensive hyperparameter tuning. The main takeaway here is that applying the logQ correction is essential and that a tower composed of dense layers and non-linearities does not have to be the defacto tower architecture. Choosing the correct encoding whether it be in the feature or architecture space is crucial and we encourage you to modify the provided network architecture.
Conclusion
We hope that this blog post has been helpful in introducing how a two-tower model for retrieval can be used as a step in improving recommendations and how there are extra steps that must be taken in order for these models to perform well. Mainly in the application of the logQ correction and negative sampling strategies when training two-tower models. We encourage you to explore the repo and the open-source dataset and explore how machine learning can be applied to the travel domain.
The git repo for this blog can be found here.
Edited by Anantharaman Janakiraman from the Expedia Group Tech Blog editorial team
