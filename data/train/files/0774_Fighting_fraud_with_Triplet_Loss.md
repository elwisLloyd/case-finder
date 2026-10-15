# Fighting fraud with Triplet Loss

Источник: https://tech.olx.com/fighting-fraud-with-triplet-loss-86e5f79c7a3e

One of the common problems of the online advertising industry is fraud. Even though it varies across markets, fraud methods have a lot of similarities worldwide.
In this post, we’ll meet:
- Fraudsters, who change images
- Embeddings, which help find distances so we can distinguish images from each other faster
- Siamese Network with Triplet Loss explained in simple language
- Tricks and Hacks — so we can train network better
Possible attacks
One of the known methods of fraud is stealing pictures of the goods from the original seller. Fraudsters pass these pictures off for their own, selling the fake goods, or renting out fake apartments.
Often, in order to bypass security systems, they not only copy the ad but also make changes both in the text and attached images. Sometimes the text is rewritten completely and the only way to determine the duplicate is an image.
Of course, there are systems that help determine such duplicates. But as the number of images increases, it becomes longer and more difficult to compare them directly with each other.
So here comes an embedding to help us.
What is embedding?
An embedding is a relatively low-dimensional space into which you can translate high-dimensional vectors — in our case, images.
That means that we can transform an image of any size to a not very long vector and then compare not the images themselves but their embeddings, which is much faster. The speed is important here, as we have a large dataset. We can make it more efficient by converting the embeddings to hashes. For example, we can use locality-sensitive hashing for that.
Embeddings and distances
So, how does the process of determining a duplicate looks like?
- When a new image is uploaded to the database, distances between the embedding of the uploaded image and embeddings of the images, already stored in the database, are calculated.
- If the distance is less than the “Undoubtedly duplicate” threshold, we can immediately mark the listing as a fraud.
- If this distance is greater than the threshold “Undoubtedly original”, we can pass the image on to the site.
- If this distance is between these two thresholds, then moderators come to the rescue — they can determine whether the image is a duplicate or not.
Thus, there is another requirement for any system to search for duplicates — it must not only correctly mark the duplicate, but also find the most similar image to it.
Meet Siamese Network with Triplet Loss
Now we need to understand how we can get these embeddings. There are a lot of methods, both machine learning and not, but in this article, we will look at one interesting architecture — a Siamese network with triplet loss. In simple language, it is a network that trains to get embedding so that the distance between similar images is much smaller than the distance between completely different ones.
That means that through the same neural network, which we will call the base network, we run the first image, then a similar image (for example, augmentation, as in our case!) and a different image. Let’s check what we do next with the formula below (don’t worry we’ll explain it soon!):
Here we find the distance between the original and the similar image (‖A − P‖), and the distance between the original and the dissimilar image (‖A − N‖) so that one distance is much smaller than the other.
What is alpha?
Now let’s try to go one level deeper — where does the alpha come from and why is it needed? It’s simple: since the task of backpropagation is to minimize the loss, the most effective way to train this neural network with loss without alpha would be to zero all weights. Then the distances would be equal to 0 and the distance between the distances — also 0! The neural network is happy with zero loss, but we, on the contrary, are not happy, because no matter what we do run through, the output is always zeros.
Get Artemii Frolov’s stories in your inbox
Join Medium for free to get updates from this writer.
So that this situation does not happen, there is an alpha — the margin between the positive (original minus similar) and negative (original minus different) distance. This margin will make zeroing not the most effective step, and the neural network will have to train a more effective way of making loss closer to zero.
Triplet generation
Previously we defined the original image, the positive example, and the negative example. Together, they form a triplet that is used for training. One of the interesting features of a neural network with triplet loss, in our case, that we don’t need a large dataset.
Indeed, having one image, with the help of augmentations it is possible to generate several positive examples and select several negative examples. These examples can be any different images, but there are also some techniques on how to choose a proper negative example, which will be discussed later. It turns out that one image transforms into several (or even many!) triplets, and many triplets mean a better-trained network.
Easy, semi-hard, and hard triplets
Another important detail of neural networks with triplet loss is a selection of negative examples. As practice shows, even without special techniques the network trains successfully, but with extra work, it does it both faster and more effectively. The selection is as follows — we enter the following groups of triplets:
- easy triplets: ‖A − P‖ + α < ‖A −N‖
- semi-hard triplets: ‖A − P‖ < ‖A − N‖ < ‖A − P‖ + α
- hard triplets: ‖A − N‖ < ‖A−P‖
As usual, A is for the original image, P is for a similar image (positive), N is for dissimilar image (negative).
Of course, it’s most beneficial to train the network on hard examples (because network works the worst with them), with mixing semi-hard and easy so that the network does not forget its correct state — and one of the easiest ways to do this is the next:
1. Evaluate several random batches
2. Choose a few triplets with the highest loss
3. Mix random triplets with these ones and get, thus, a batch for training
Last, but not least — Transfer Learning
The last tool in training will be using a network with pre-trained weights as a basic network. They can be either fully trained or frozen with only the tail of the network trained, but the result of such a transfer learning will only improve the network as a whole.
Using the network
The network is trained, all that remains is to get embedding. To do this, one just needs to run the image through the base network (without using any triplets!), and the output will be the final vector. As it was written before, now it is possible to do anything with it — immediately use it as an image mapping, or convert it to a hash — it depends only on the task. The main thing is that this technology can help to quickly and effectively identify the fraudsters trying to change the image in the ad.
Conclusion
Today we learned:
- Fraudsters can cheat by stealing and changing the image of other users to create a fake listing;
- We need a fast way to find similar images, so we can find distances between corresponding embeddings;
- We can compute embeddings using Siamese Network with Triplet Loss;
- We can generate many positive and select the best negative example to generate triplets;
- This way, we can quickly and effectively identify the fraudsters trying to use someone else’s image in their ad.
