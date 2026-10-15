# Spotify Track Neural Recommender System

Источник: https://medium.com/stanford-cs224w/spotify-track-neural-recommender-system-51d266e31e16

By Eva Batelaan, Thomas Brink, and Benjamin Wittenbrink
Do you find yourself listening to the same songs over and over again, wishing you had a better way to discover new music? We certainly do. But what if we told you there was a way to automatically generate a playlist that’s tailored to your specific music preferences? A playlist that not only includes your favorite songs but also introduces you to new tracks that perfectly complement your taste.
With graph neural networks, we can do just that. As music enthusiasts and machine learning students, we’ve been fascinated by the power of GNNs to revolutionize the music recommendation space. In this post, we’ll show you how we can use the latest advancements in deep learning to build a cutting-edge playlist-track recommender system that’s personalized to you.
According to the Digital Music Alliance’s 2018 Annual Music Report, playlists are becoming increasingly popular among music consumers. In fact, 54% of consumers reported that they now listen to playlists more often than albums [1]. Consequently, the demand for seamless, high-quality playlists is also increasing. Indeed, Spotify — one of the most popular music streaming services — has seen over 4 billion playlists created and shared by users to date. However, creating cohesive playlists can be challenging and time-consuming. Personally, we know this all too well: at least one of us just shuffles through their “liked songs” section!
Automated playlist continuation offers a solution to this problem, harnessing the power of computers and machine learning algorithms to provide song recommendations that continue the theme, style, and/or mood of an existing playlist, thereby making playlist creation easier and helping users find more of the music they love. The algorithm might make use of musical features of the songs in the original playlist, such as the genre, tempo, or key, a user’s listening history, what similar users enjoy, or what similar playlists contain.
In this blog post, we focus on the last point: using neural graph methods to learn playlist and track similarities, which will enable us to automatically continue a playlist by sourcing recommendations for songs that are contained on similar playlists. But before delving deeper into our methods, let’s first talk about the data and feel free to follow along on our Colab!
Data
(follow along in the Loading and processing data and the Constructing a graph dataset sections of our Colab)
The Spotify Million Playlist Dataset has been a valuable resource for researchers and data enthusiasts alike. Initially released by Spotify Research solely for the RecSys Challenge 2018 [2], the dataset was later made publicly available on AIcrowd in October 2020 [1]. If you’re interested in exploring the dataset, you can easily access it for free (although registration is required) through this link.
The dataset consists of a staggering one million Spotify playlists, created between January 2010 and October 2017, complete with track information, artist details, and album data. In total, the dataset boasts over 2 million unique songs from nearly 300,000 artists, making it “the largest public dataset of music playlists in the world”, according to AIcrowd.
To give you an idea of what the data looks like, we’ve provided an example JSON playlist below.
You might think that a million playlists, each with all of their own songs and metadata, take up a lot of space. And you’d be right! The full dataset folder is roughly 34 gigabytes, made up of 1,000 JSON files containing 1,000 playlists each. For our demonstration purposes in this post, we definitely don’t need to use all of the data. Instead, we will focus on a subsample using just the first 50 files. Once you feel comfortable with this data and our models, we encourage you to try your hand at larger samples!
As discussed above, our data consists of playlists with their corresponding tracks, artists, and albums. We can conceptualize this data as a graph, where each node represents a playlist, track, artist, or album, and edges link playlists with the tracks, artists, and albums they contain. Additionally, edges link tracks to their respective artist(s) and album, and artists to their albums. Being concerned with song recommendations for playlists, our goal is to learn to predict the playlist-track edges well.
We want to note that the initial set-up (with 4 node types) would lend itself well to a very interesting heterogeneous graph analysis, so if you enjoyed this post and want to learn more, this would be a great place to start to explore further! For the purposes of this post, however, we will exclude the artist and album nodes. This leaves us with a bipartite graph between playlists and tracks, where an edge indicates that a track is contained in a playlist. We illustrate this processing in the image below.
The resulting graph still has 512 thousand nodes and over 3.3 million edges. Unfortunately, given our computational resources on Colab (25 GB system RAM, 15 GB GPU RAM), this graph is too large to train our models on. As a result, we will need to identify a subgraph to continue our analysis. To do so, we use the graph theory concept of a “K-core”, which is defined as the maximally connected subgraph in which all nodes have degree of at least K. This means that any node that is not in the K-core must have a degree strictly less than K. Practically, taking the K-core of our graph allows us to identify a central, highly-connected subgraph of the original graph, where each playlist contains at least K tracks, and each such track is a member of at least K-1 other playlists. We have included a K-core visualization below.
In this post, we set K = 30, though you’re welcome to experiment with other values. Our settings yields a subgraph of 35 thousand nodes, with around 1.6 million edges. Thus, the subgraph reduces the size of our node-space by a factor of 15 and halves the number of edges. Moreover, this subgraph is significantly denser: the average node degree in the subgraph is approximately 90, almost seven times larger than in the original graph (approximately 13). This should significantly aid the learning process, allowing our methods to better capture and propagate information through the graph structure, resulting in better node embeddings, which are essential for accurate predictions.
Specifically, our final subgraph contains 34,810 nodes (22,563 playlists and 12,247 tracks) with 1,578,286 edges. We briefly recap the steps for obtaining this subgraph below:
- Load the first 50 JSON files, containing 50,000 playlists.
- Drop artist and album information to create a bipartite graph between playlists and tracks.
- Compute the 30-core of this graph.
Below we visualize a small subgraph of this graph on 1,875 nodes and 5,057 edges.
Before we dive into the models, there is one critical step we must take: splitting our data into train, validation, and test samples. While this is a standard practice in supervised learning, graph data presents unique challenges. Unlike tabular data, where splitting is a straightforward process, randomly splitting nodes or edges in a graph would disrupt the neighborhood structures we aim to learn from.
To tackle this issue, we will use a “transductive link prediction” split. Here’s how it works: we keep the true graph structure visible at all times but mask certain edges for prediction at each split. We call the visible edges “message passing” edges and the hidden ones we aim to predict “supervision” edges.
This split results in the following behavior:
- During training, we use the train message passing edges to predict the train supervision edges.
- During validation, we use all train edges to predict the validation supervision edges.
- During testing, we use all train and validation edges to predict the test supervision edges.
This means the number of edges used to exchange messages increases as we move from train to validation to test. We follow a 70–15–15 percent split.
An example of this splitting is shown in the image below.
Approach
(follow along in the Designing our model and the Defining training, test functions sections of our Colab)
With our subgraph in place, we can now turn our attention to the next step: building models. Our goal is to leverage the subgraph to learn node-level similarity and, ultimately, output track recommendations.
Why use graph neural networks?
Looking at the original RecSys challenge, none of the best teams used any graph-based methods. In fact, the word “graph” doesn’t even appear in the paper “An Analysis of Approaches Taken in the ACM RecSys Challenge 2018 for Automatic Music Playlist Continuation” once [3]! Given the growing popularity and success of graph neural networks (GNNs) on other recommender system problems and in other, more general, areas, we thought this would be a perfect opportunity to explore the potential of GNNs.
The primary motivation behind the development of GNNs is that most machine learning methods are focused on data ordered as a sequence (e.g., text) or a grid (e.g., image), and struggle to handle the complex, structural nature of graph data. For example, one naive approach might be to model a graph as its adjacency matrix — from which longer paths could be recovered by taking powers of this matrix — and use this as an input for a deep neural network. However, this idea has many issues, among others that it is sensitive to node ordering and graph size. Similarly, if we wanted to apply a convolutional neural network (CNN), we would immediately encounter problems, as there is no notion of a fixed sliding window on a graph.
In contrast, GNNs are designed to leverage the graph structure of data and can capture higher-order dependencies between nodes and edges as well as node- and edge-level features to learn embeddings or representations of nodes, edges, or (sub)graphs. This makes them an ideal choice for recommendation systems that operate on large, interconnected datasets such as music playlists. But how do they work?
In short, the main insight is that we can initialize each node to carry a message and then propagate these messages along the edges of the graph, aggregating and updating many times. Specifically, each node sends its message to all of its neighboring nodes and receives messages from all of its neighbors. Each node then aggregates all of its received messages using a permutation invariant function (a function not dependent on the ordering of the messages). Next, each node updates its new message as a function of its previous message and the result of the aggregation step. We can then stack these layers to increase the receptive field of a node to neighbors multiple hops away (as with CNNs). Through the multiple graph convolution layers, the model aggregates information from nodes that are further apart in the graph, thus capturing the global structure of the data.
Building our models
One prominent approach for recommender systems is collaborative filtering (CF). CF methods can be broadly classified into three categories: matrix factorization, neighborhood-based, and rule-based [4]. Matrix factorization methods factorize the user-item interaction matrix into lower-dimensional embeddings that capture the latent features of users and items. Neighborhood-based methods rely on the similarity between users or items to form clusters from which they make recommendations, while rule-based methods use explicit rules to generate recommendations. Hybrid methods that combine multiple techniques are also common. While these methods have been successful in many applications, they may not be as effective at capturing more complex patterns and dependencies in the data as neural methods such as graph neural networks.
Among the various graph-based models, we decided to explore the convolutional layers of LightGCN (LGConv), Graph Attention Network (GATConv), and GraphSAGE (SAGEConv) for their unique features and strengths. LGConv, for instance, has a lightweight architecture that makes it highly scalable for large datasets commonly found in recommendation systems. Its simplicity and focus on embeddings allow it to efficiently learn representations of nodes in the graph, making it a strong contender for our problem. On the other hand, GATConv offers an attention mechanism that can dynamically focus on relevant parts of the graph, leading to more accurate recommendations. This mechanism allows GATConv to weigh the importance of neighboring nodes, helping the model to emphasize the most relevant connections between playlists and tracks. Lastly, the SAGEConv adds complexity and richness to the message representation relative to LGConv but is still scalable.
One implementation note before diving in: for all of our graph neural network models, we use the PyTorch Geometric (PyG) library. This is a library that is built upon PyTorch and integrates seamlessly into a standard deep learning coding environment. Most code we provide in this article and the associated Colab assume that you have a working and up-to-date version of both PyG and PyTorch. See the documentation here.
Get Benjamin Wittenbrink’s stories in your inbox
Join Medium for free to get updates from this writer.
We start off with LightGCN, which is widely considered to be one of the state-of-the-art neural collaborative filtering algorithms [5]. As discussed, this model is very lightweight, as it eliminates all learnable weight matrices and activation functions such that the only trainable model parameters are the embeddings at the initial layer. This simplification also reduces the risk of over-smoothing, which occurs when node embeddings become indistinguishable after multiple layers of aggregation.
We provide a straightforward implementation of this using the PyG library below. We do so exclusively for demonstration purposes to showcase the functionality of PyG and the MessagePassing layers. We hope this gives some intuition for how the graph neural networks are actually operating under the hood. In our Colab, we use the official version implemented at torch_geometric.nn.conv.LGConv as it is better optimized and more robust.
class LGConv(MessagePassing):
def __init__(self, **kwargs):  
super(LGConv, self).__init__(**kwargs)
def forward(self, x, edge_index, size = None):
# calculate normalization term (in the above: 1 / sqrt(...))
src, dst = edge_index
node_degree = torch_geometric.utils.degree(dst)
node_degree_inv_sqrt = node_degree.pow(-0.5)
norm = node_degree_inv_sqrt[src] * node_degree_inv_sqrt[dst]
# pass to propagate (returns the term on the RHS in above)
out = self.propagate(edge_index, x = x, norm = norm, size = size)
return out
def message(self, x_j, norm):
# calculating normalized message (term in the sum above)
return x_j * norm.view(-1, 1)
# Note: could also just pass aggr = 'add' to __init__()
def aggregate(self, inputs, index, dim_size = None):
# aggregation (the sum above)
out = torch_scatter.scatter(inputs, index, dim=self.node_dim, reduce='sum')
return out
To obtain the final embedding, the embeddings at each layer are aggregated. This is useful as it allows the model to retain information from each stage. For this aggregation, we consider two approaches; assigning equal weight to all layers, or treating the layer-specific weights as learnable parameters. The first approach is commonly used as an easy-to-go method, whereas the latter allows us to put more focus on a specific neighborhood hop scale.
In addition to using LightGCN, we explore two alternative approaches that leverage the same overall architecture but replace the LGConv calls with more complex convolutional layers. We are specifically interested in testing the model’s ability to capture complex structural relationships. The first variant replaces LGConv with GATConv, the convolutional layer present in the Graph Attention Network (GAT), as shown below [7]. We define multiple attention heads and also define a linear layer to map the concatenated outputs back to the original embedding dimension. The second variant uses SAGEConv (from GraphSAGE) as the replacement convolutional layer, also shown below [8].
Clearly, both of these convolutional layers are significantly more complex than LGConv, and provide enhanced local information aggregation. This has the potential to improve our performance by providing the capability of learning more complex graphical structure. We will see whether this holds in practice shortly!
For the implementation of these convolutional layers (GATConv and SAGEConv), please refer to the PyG documentation at this link. For the implementation of the overall GNN architecture, we maintain the same as with LightGCN, simply exchanging its convolutional layer. We provide an example for this below.
class GCN(torch.nn.Module):
def __init__(
self,
...
conv_layer = "LGC",
...
):
...
# initialize convolutional layers 
self.conv_layer = conv_layer
if conv_layer == "LGC":  
self.convs = ModuleList([LGConv(**kwargs) for _ in range(num_layers)])
elif conv_layer == "GAT": # initialize GAT layer with multiple heads
n_heads = 5
self.convs = ModuleList([
GATConv(embedding_dim, embedding_dim, heads = n_heads, 
dropout = 0.5, **kwargs) for _ in range(num_layers)
])
self.linears = ModuleList([Linear(n_heads * embedding_dim, 
embedding_dim) for _ in range(num_layers)])
elif conv_layer == "SAGE": #  initialize GraphSAGE conv
self.convs = ModuleList([ 
SAGEConv(embedding_dim, embedding_dim, **kwargs) 
for _ in range(num_layers)
])
Obtaining a similarity metric
In the last section, we discussed how our models obtain embeddings for the nodes. But: how do we actually use these embeddings to output track-playlist combinations? Or, more specifically: how do we go about converting our embeddings into notions of similarity and ultimately recommendations?
The simplest approach — and the approach we will take — is to take the dot product between two embeddings, which is an often-used metric for similarity. This effectively is calculating how much the two vectors overlap in the high-dimensional embedding space, both in terms of magnitude and direction.
Thus, if we have a matrix of playlist embeddings P and a matrix of track embeddings T, we can compute the matrix multiplication between P and T transposed to obtain a matrix of scores where each cell i, j represents the similarity of track j to playlist i. We can then just select the top K tracks for each playlist as our recommendations.
Defining our loss
Now we know how to calculate recommendations, how do we know if these are any good? To answer this, we introduce our main evaluation criterion: Recall@K. This criterion is defined as the fraction of the relevant tracks (in our case, tracks that are contained in the playlist) that are predicted in the top K. We provide an illustration below.
Looking at this criterion, we see an obvious problem: this metric is not differentiable, so how do we optimize it? To solve this problem, we will have to find a differentiable objective that is well-aligned with our Recall@K metric. Our candidate loss function is the Bayesian Personalized Ranking (BPR) loss, which provides a “personalized” (i.e., playlist-specific) quantity as to what good and bad recommendations are. In order to calculate this loss function, we need scores for pairs of positive and negative edges. In this case, a negative edge is just an edge that doesn’t exist in the graph, while a positive edge is an existing track-playlist combination that we want to predict — more on how we pick these later. For now, assume that, for every positive edge (i, j_+), we have access to a negative edge (i, j_-). Then we can define the loss function for a user i as:
We can implement this in Python as follows.
class BPRLoss(_Loss):
def __init__(self, lambda_reg: float = 0, **kwargs):
super().__init__(None, None, "sum", **kwargs)
self.lambda_reg = lambda_reg
def forward(self, positives: Tensor, negatives: Tensor,
parameters: Tensor = None) -> Tensor:
n_pairs = positives(0)
log_prob = F.logsigmoid(positives - negatives).sum()
regularization = 0
if self.lambda_reg != 0:
regularization = self.lambda_reg * parameters.norm(p=2).pow(2)
return (-log_prob + regularization) / n_pairs Now, let’s get back to the negative edges for a bit. As mentioned above, a positive edge (i, j_+) is just a supervision edge (an existing edge that we wish to predict) in the graph and a negative edge is one that does not exist, say (i, k). For our purposes, the negative edge will always be defined as a pair to a positive edge, in particular coming out of the same playlist node as the positive edge. The idea behind this is that we want to encode the following to the model: “Playlist i is like track j but not like track k”. Without any negative edges, you can convince yourself that you might just end up with everything having the same exact embedding! This is obviously not desirable. So, the negative edge forces the model to learn different representations for different clusters.
As you’ve probably guessed, there are way more negative edges in our graph than positive ones. So how do we sample them? Honestly, this is a lot easier than you probably think. We just randomly pick a track and assume that it is a negative edge. Yes, there’s a risk that we are inadvertently picking a positive edge, but the odds are very low. The median playlist has 84 tracks, which means the median playlist has a 0.6 percent chance of picking a positive edge. We call this approach “random negative sampling”.
def sample_negative_edges_nocheck(data, num_playlists, num_tracks, device = None):
# this function is called _nocheck, as it does not check for positive edges 
# before generating the negative edges
playlists = data.edge_label_index[0, :]
# generate random index of track to select
tracks = torch.randint(num_playlists, num_playlists + num_tracks - 1, size = data.edge_label_index[1, :].size())
tracks = tracks.to(device)
# stack together to get  dim = (2, len(playlists))
neg_edge_index = torch.stack((playlists, tracks), dim = 0)
# negative edges so assign label of zero 
neg_edge_label = torch.zeros(neg_edge_index.shape[1])
neg_edge_label = neg_edge_label.to(device)
return neg_edge_index, neg_edge_label
If you are still concerned about the presence of positive edges in our sampling function, do not worry! In our Colab, we also define a function sample_negative_edges that first defines a mask to filter out all of the positive edges and then randomly samples. However, we think this code is significantly less clear to follow and it did not offer any meaningful performance improvement. Thus, we prefer to present the simple random negative edge sampling technique above.
We also take a somewhat more interesting approach to negative sampling, termed “hard negative sampling.” The idea is that, as the model gets progressively better, we begin sampling progressively harder edges. The intuition is that as the model starts out, you want to provide “easier” negatives so that the model can learn global neighborhoods. Then, as the model starts to learn these, you want to provide edges that refine these neighborhoods to learn more local information. In order to obtain hard edges, we calculate the matrix of playlist-track scores, as discussed above, and sample from a subsample of the top tracks. So, halfway through training, we might sample from the top 50 percent of edges, and so on. Below, we provide our Python implementation of hard negative sampling. As you can probably tell, this is significantly more computationally expensive than the previous approach.
def sample_hard_negative_edges(data, model, num_playlists, num_tracks, device=None, batch_size=500, frac_sample = 1):
# get embeddings 
with torch.no_grad():
embeddings = model.get_embedding(data.edge_index)
playlists_embeddings = embeddings[:num_playlists].to(device)
tracks_embeddings = embeddings[num_playlists:].to(device)
positive_playlists, positive_tracks = data.edge_label_index
num_edges = positive_playlists.size(0)
# Create a boolean mask for all the positive edges
positive_mask = torch.zeros(num_playlists, num_tracks, device=device, dtype=torch.bool)
positive_mask[positive_playlists, positive_tracks - num_playlists] = True
neg_edges_list = []
neg_edge_label_list = []
# need to loop in batch, as matmul will overflow otherwise
for batch_start in range(0, num_edges, batch_size):
batch_end = min(batch_start + batch_size, num_edges)
# calculate scores
batch_scores = torch.matmul(
playlists_embeddings[positive_playlists[batch_start:batch_end]], tracks_embeddings.t()
)
# Set the scores of the positive edges to negative infinity
batch_scores[positive_mask[positive_playlists[batch_start:batch_end]]] = -float("inf")
# Select the top k highest scoring negative edges for each playlist in the current batch
# positive edges will be at the very end
_, top_indices = torch.topk(batch_scores, int(frac_sample * num_tracks), dim=1)
selected_indices = torch.randint(0, int(frac_sample * num_tracks), size = (batch_end - batch_start, ))
top_indices_selected = top_indices[torch.arange(batch_end - batch_start), selected_indices] + n_playlists
# Create the negative edges tensor for the current batch
neg_edges_batch = torch.stack(
(positive_playlists[batch_start:batch_end], top_indices_selected), dim=0
)
neg_edge_label_batch = torch.zeros(neg_edges_batch.shape[1], device=device)
neg_edges_list.append(neg_edges_batch)
neg_edge_label_list.append(neg_edge_label_batch)
# Concatenate the batch tensors
neg_edges = torch.cat(neg_edges_list, dim=1)
neg_edge_label = torch.cat(neg_edge_label_list)
return neg_edges, neg_edge_label
Results
(follow along in the Training our models and the Visualizing our results sections of our Colab)
We’re now ready to train the model! To perform neural network updates, we use an Adam optimizer with a learning rate of 0.01. We learn 64-dimensional embeddings, while we include 3 convolutional layers when using GATConv and SAGEConv and 4 layers when using LGConv. After checking convergence dynamics of the models, we decide to train for 300 epochs. We run all models using both our random and our hard negative sampling, where we consider both fixed and learnable layer weights.
As discussed, we use the Recall@K metric for our main evaluation measure. For this post, we choose a value of K = 300, which we think is a reasonable choice given that we have approximately 12,250 tracks. This value of K means that we pick roughly the top 2.5 percent of recommended tracks. We felt that a one percent threshold might be too narrow a filter, whereas five percent might just be too large in absolute values (roughly 600 tracks) to be super meaningful. Thus, we felt K = 300 was a happy compromise.
Below we plot the validation BPR loss of all of our models over the 300 epochs. On the left, we only plot the models with random negative sampling. On the right, we introduce the models with hard negative sampling as well. We omit training loss from the plots for clarity, but in all scenarios it is below the validation loss, as we expect.
Looking at the plot on the left, the more complex convolutions — GATConv and SAGEConv — are able to attain significantly lower validation losses compared with LGConv. There is a lot of instability in the initial 50 epochs for GATConv and SAGEConv likely due to the complexity of the model, but this is ultimately resolved. Nonetheless, it clearly takes more epochs for GATConv to converge than the others. Overall, SAGEConv appears to perform best overall in terms of performance, stability, and convergence speed. Now turning our attention to the hard negative sampling on the right, one immediate impression is that the loss is actually increasing after a certain amount of epochs. This is incredibly interesting, and illustrates the increasing difficulty of the hard negative edge sampling. As train losses are still decreasing, it is likely that the models may be overfitting to a certain extent to the more difficult samples in the training data, which then leads to worse overall validation performance.
Nonetheless, our validation Recall@300 metric, which we evaluated every 10 epochs, tells a different story. Indeed, as we can see in the plot below, even as the validation losses are increasing, the Recall@300 score is still increasing. One important difference between these two quantities is that input to the loss function are the raw scores while the input to the recall metric are only the top rankings. Thus, this might reflect that the models learn a bias toward distinguishing the harder negatives, which makes generalizing to the broader class of negatives more difficult.
Comparing the models with one another, once again, the SAGEConv performs the best, followed by GATConv, and LGConv. Another interesting note is that the random and hard negative sampling methods seem to lead to similar performances for LightGCN for the first 200 epochs. Thereafter, the random sampling appears to have converged while the hard sampling begins to increase. This behavior is in line with the idea of our hard negative sampling; we first have our model get a “general” idea of what good and bad predictions are (near random negative sampling), while, as we gradually increase difficulty of the negative samples, we then allow our model to learn about separating good and bad predictions in a more specific embedding space. This leads to improved performance even after many epochs.
The above figures were obtained by setting the layer weights alpha vector equal across all layers. We also ran experiments with alpha as a learnable parameter. However, these results are omitted for brevity, as the results are quite similar for all methods. In addition, we have functionality to use a standard binary cross entropy loss instead and log the ROC area und the curve (ROC-AUC). Feel free to explore this in our Colab!
Visualizations
(follow along in the Visualizations section of our Colab)
After creating the models, we decided to visualize some of the embeddings produced by one of the best performing models. We chose to explore the 30-core SAGEConv model that was trained on 50 data files.
Since our embeddings are in 64 dimensions, we used uniform manifold approximation and projection to reduce the embeddings to three dimensions. We graphed the reduced embeddings across epochs. We created a graph for the model that used random negative sampling (left) and one for the the model that used hard negative sampling (right). We found that as our model trained, the embedding in both cases started to form a tight cluster that would morph and move in a group from epoch to epoch. A small subset of playlists, typically around 630 nodes, formed a small, cluster that would often be separate from the larger cluster. However, with further analysis, it did not appear that the nodes within this smaller cluster was consistent across epochs. Therefore, we had difficultly extracting significance from these visualizations. It is also possible that a lot of the distinguishing and/or relevant information is lost when compressing the embeddings into the low-dimensional space.
After exploring the general distribution of all playlist embeddings, we chose to investigate the embeddings of playlist that feature particular artists. Specifically, we investigated playlists that featured Glass Animals (artist id: 4yvcSjfu4PC0CYQyLy4wSq) and Gryffin (artist id: 2ZRQcIgzPCVaT9XKhXZIzh), as these artists occurred sufficiently frequently to have the potential for meaningful clusters but were not too common to dominate the playlist embeddings. We identified all the playlists that feature Glass Animals but not Gryffin (yellow), playlists that feature both (gray), and playlists that feature Gryffin but not Glass Animals (blue). We found that the graph of playlists featuring just these artists resembled that of all playlists, suggesting that a single artist in a playlist has little impact on the embeddings.
Conclusion
In conclusion, our exploration of graph neural networks has shown their potential to transform music recommendation systems. Our work showcases that even without explicit supervision, graph neural networks can effectively distinguish between different genres and make personalized recommendations. The practical implications of our findings are evident with the emergence of features like Spotify’s Enhance and Apple’s Autoplay, which leverage advanced recommendation algorithms to provide seamless and enjoyable listening experiences. Together, we can ensure that the joy of music discovery and the seamless continuation of playlists remain an integral part of our shared experiences, enhancing our lives one song at a time.
We encourage those interested in advancing their understanding of graph neural networks and learning more about state-of-the-art methods in graph-based recommendation systems to explore the course materials and resources available through Stanford’s CS 224W!
References
[1] Spotify Research. (2020). Spotify Million Playlist Dataset Challenge. AIcrowd.com.
[2] C. W. Chen, P. Lemere, M. Schedl, and H. Zamani. (2018). Recsys challenge 2018: Automatic music playlist continuation. Proceedings of the 12th ACM Conference on Recommender Systems.
[3] H. Zamani, M. Schedl, P. Lamere, and C.W. Chen. (2019). An Analysis of Approaches Taken in the ACM RecSys Challenge 2018 for Automatic Music Playlist Continuation. ACM Transactions on Intelligent Systems and Technology.
[4] X. Su, and T. Khoshgoftaar. (2009). A Survey of Collaborative Filtering Techniques. Advances in Artificial Intelligence.
[5] X. He, K. Deng, X. Wang, Y. Li and Y. Zhang & M. Wang. (2020). LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation. Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval.
[6] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò, and Y. Bengio (2017). Graph Attention Networks. arXiv preprint arXiv:1710.10903.
[7] W. Hamilton, R. Ying, and J. Leskovec. (2018). Inductive Representation Learning on Large Graphs. Advances in neural information processing systems, 30.
