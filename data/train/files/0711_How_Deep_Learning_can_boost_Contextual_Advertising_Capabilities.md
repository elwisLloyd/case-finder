# How Deep Learning can boost Contextual Advertising Capabilities

Источник: https://medium.com/dailymotion/how-deep-learning-can-boost-contextual-advertising-capabilities-c9ca7c8fc4e9

How Deep Learning can boost Contextual Advertising Capabilities
Dailymotion’s advertising solution uses video frame signals and computer vision techniques to target categories from the IAB taxonomy while respecting user privacy
In a world where the end of web cookies is fast approaching — bringing uncertainty for advertisers and marketers — and where technical and legal constraints are constantly increasing, the need for user privacy and personalized ads has never been so important. One of the biggest challenges for contextualization is the categorization of content at scale. Here is how we enhanced our in-house contextual advertising solution at Dailymotion, using state-of-the-art computer vision techniques for video categorization.
Well-categorized content provides a superior user experience through better recommendations and contextual ads, using video categorization to place ads adjacent to relevant content. Additionally, it provides more capabilities and better performance to our advertisers. Hence, the idea to classify our videos was born.
Currently, our Partners can select an “upload category” while uploading their content to Dailymotion. Since it is very high-level information (for instance: news, sports, lifestyle, etc.), we wanted to go a step further to obtain a more granular definition of our content. For example, for the upload category “sports” we would like to say whether it is soccer, basketball, or rugby.
Video Classification Problem
From a machine learning standpoint, the problem that we are trying to solve is called a multi-label classification problem, which is a generalization of multiclass classification. In the multi-label problem, there are no restrictions on how many of the classes the instance can be assigned to.
The IAB content taxonomy
Now that we have the idea to classify our content we need to define which categories to use and what granularity level we want. We opted to use the IAB content taxonomy as it has become the new standard in the ad industry. This taxonomy is supposed to describe every possible content and it enables us to describe each video of our catalog more accurately and consistently.
We selected a subset of 196 IAB categories that suited our catalog variety. This allowed us to slightly simplify the classification task.
The Dataset
Since we wanted to tackle this problem with a supervised training model using the IAB categories as labels, we need a properly labeled dataset. There are many different signals we can use to define the examples in our dataset:
- video metadata: video owner, upload category, language, the upload date, etc.
- textual signals: video title and video description
- visual signals: video frames
- audio signals: audio track
Through the use of textual signals, we have already developed several solutions that tackle the content classification problem and currently have two textual models in production.
One dedicated to French and English text:
And one dedicated to multiple other languages:
Although these textual models work well and are already in production at Dailymotion. But sometimes the title and description do not allow us to predict an IAB category either because they are very short, too vague, or in a language that we do not handle yet. That’s why we thought having another model based only on visual signals would allow us to improve our predictions in some scenarios:
- It would improve our overall coverage, predicting categories for the videos in a language that we do not handle yet
- As the problem is multi-label, it would increase the number of correct IAB categories per video, for the videos already classified by the textual models
In this example, a first model based on textual signal only has predicted “Interior Decorating” and from the video frames, our visual model has predicted “Food Movements”. Both predictions seem to be accurate given their respective signal. This is the complementarity we hope to get for the already categorized videos.
Getting the IAB labels to train our model
To train our classifier we will use the predictions given by the textual models as labels for the visual model. Here we introduce some uncertainty by using labels that come from the predictions of another model but we are confident in these predictions and we carefully selected a scope where they perform well to constitute our dataset. That is why we think that on average the textual model predictions would be good ground truth for the visual model.
We don’t want the models (textual and visual) to be identical, ie. to predict the same categories for the same video. Since they use a very different signal as input we hope to get a good complementarity both in terms of coverage and number of categories per video between them.
Visual Scope
One particularity of the visual model is the fact that we only use the frames to classify a video and it implies two strong hypotheses:
- It is better if the video is short (between 1 & 10 minutes). Usually, it makes less sense to try to predict a category like “Automotive”, “Cooking” or “Pets” on a one-hour long documentary, for instance.
- The categories that we try to predict must be visual. It is very difficult to predict “News”, “Politics”, or “Jazz” just by looking at the frames of a video, even for a human.
This is why we had to reduce the number of categories the model can predict to the visual ones only. Here is an example of what could be non-visual and visual according to us:
Video Classification State of the Art
Now that we have defined our problem, we know that it corresponds to a video classification problem where we want to train our model end-to-end with our own data and labels. Therefore, we looked at the video classification literature and in particular two workshops from CVPR 17' [1] and ECCV 18' [2].
The NeXtVLAD [5] is one of the best performing non-ensemble architectures for the video understanding competition (YT8M). We were particularly interested in non-ensemble solutions for simplicity's sake and running costs. The NeXtVLAD is an improvement of the NetVLAD network [3][4] that proved to be effective for spatial and temporal aggregation of visual and audio features [6].
Get Brice De La Briere’s stories in your inbox
Join Medium for free to get updates from this writer.
It uses video frame features (image descriptors) from another model inceptionv3 [8] learned on the Imagenet dataset as inputs. Then these described frames are temporally aggregated at the video level by the NeXtVLAD layer. The video aggregation is then enhanced by a SE Context Gating module, aiming to model the interdependency among labels [6][7]. This video aggregation is finally used to predict some video categories.
End-to-end Training & In-house Tuning
The NeXtVLAD has performed very well on video classification challenge yt8m, but our goal is slightly different and we needed to retrain the network from end-to-end for three main reasons:
- We have defined our own labels, a subset of visual IAB categories that suits the advertising needs. Initially, we tried to map the yt8m challenge labels to our own IAB categories to avoid retraining end-to-end but the results we obtained were not satisfying enough. This was most likely because the mapping that we created ourselves was not perfect and introduced errors, and also because our video distribution might be different from the one in the training dataset from the yt8m challenge.
- We want the model to be fully trained on the distribution of our own labels to get the best performance on our videos
- We made some light modifications to the original network architecture
To fit our needs and get the best possible performance for our task, we modified the original architecture with two main changes:
- Addition of in-house metadata in the model architecture to improve the classification. Our metadata is encoded and concatenated to the video level aggregated vector (NeXtVLAD layer output)
- For engineering simplicity's sake, we ignored the audio input feature at least initially
Here is the modified architecture we currently use:
The only part of the pipeline that we do not re-train and use as it is, is the InceptionV3 [8] network used to describe the frames and given as input to the NeXtVLAD.
Performance Measurement & Results
Performance metrics
The way we evaluate our model must be aligned with our product needs and we need to make sure we optimize for the right metric. In our case, the product need is defined as follows: for any given category we want to maximize the number of videos correctly labeled with it. This would be useful for both recommendation and advertising purposes but to do so, we need to split it into two objectives:
- Coverage: we want to have as many videos labeled with a relevant IAB category as possible.
- The number of IAB categories per video: we want to have as many relevant IAB categories per video as possible.
To measure our performance on the test set, we will plot the precision-coverage curves and in particular, we will look at the coverage value we obtain for the given precision of 80%.
Training Loss
The loss we use to train the network must be tractable and differentiable, we used the sigmoid cross-entropy: which measures the probability error in discrete classification tasks in which each class is independent and not mutually exclusive.
Results
Below is an evaluation example with two different trainings runs, one with the base NeXtVLAD architecture (dashed) and the other with some architecture improvement like adding in-house metadata (plain).
Let’s have a look at the precision-coverage curves:
For our product requirement of 80% precision, we obtain the following results:
- Not retrained model, mapping initial yt8m labels to ours: we had around 30% coverage, giving an f1 score of ~0.44
- Base architecture: we have obtained around 46% coverage, f1 score~0.58
- Improved architecture: we have obtained around 64% coverage, f1 score~0.71
By adding our in-house metadata within the network and retraining it end-to-end, we managed to significantly increase the coverage.
Production Pipeline Overview
To put such a model in production is a challenge since many different parts need to work at scale: video download, frame extraction, preprocessing with InceptionV3, and finally the NeXtVLAD network inference. We need to put all of these parts together in a pipeline to answer our two use cases:
- Run our model on every new video uploaded. An important scaling is required.
- Backfill our video catalog, ie. run the model for all our videos uploaded in the past. Huge scaling is needed here since there are dozens of millions of videos available in our catalog.
To fit these two use cases with the scale they require we designed the following pipeline:
This pipeline uses the framework Klio developed by Spotify, initially designed for large-scale audio pipelines but it also suits our video pipeline needs.
Merging Visual & Textual results
We have two kinds of models that classify our content based on different inputs: textual and visual. We can think about how to use and merge the different predictions we get when a video is scored by two different models. Since one of our product needs is to increase the number of IAB categories per video we decided to begin with a simple union of the predictions.
With this simple approach, for the video already classified by a textual model, we managed to increase our number of IAB categories by 44% on French and English videos and by 50% for our multilingual model.
Future Work & Improvements
Enhancing our targeting possibilities with computer vision has been very challenging both in terms of machine learning and data engineering and we are happy we have managed to improve the base performance we initially achieved. Still, we have many ideas to continue to improve our pipeline:
- As mentioned earlier, we initially excluded the audio input, and obviously re-adding it would be a good improvement possibility.
- The union of the different predictions is a simple but naive approach that we can improve.
- We also think that with better visual descriptions of the frames we would attain better performance. We currently use the output from InceptionV3 but some more recent architectures have better performance on ImageNet. Also, we have seen at Neurips this year that robustness leads to improved feature representation [9], so using a robustly trained ImageNet model could be an idea as well.
Video categorization has already allowed us to improve Dailymotion’s user experience and contextual advertising capabilities while respecting user privacy. Advanced Machine Learning models can now interpret what a video is about, the feeling it’s evoking, and at which exact video frame a specific product category is shown, opening infinite new opportunities for hyper contextual targeting.
The quest to find more sustainable methods and “healthy data” is only just beginning, so stay tuned to hear more about our technical solutions to leverage video signals.
