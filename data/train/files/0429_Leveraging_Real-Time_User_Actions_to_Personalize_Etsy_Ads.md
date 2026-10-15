# Leveraging Real-Time User Actions to Personalize Etsy Ads

Источник: https://arxiv.org/pdf/2302.01255.pdf

adSformers: Personalization from Short-Term Sequences and
                 Diversity of Representations in Etsy Ads

                                         Alaa Awad, Denisa Roberts∗
          Eden Dolev, Andrea Heyman, Zahra Ebrahimzadeh, Zoe Weil, Marcin Mejran, Vaibhav Malpani,
                                             Mahir Yavuz
                                                                 Etsy
                                                          Brooklyn, NY, USA
                                           {aawad,denisaroberts,edolev,aheyman}@etsy.com

      ABSTRACT
           In this article, we present a general approach to personalizing ads
          through encoding and learning from variable-length sequences of2023    recent user actions and diverse representations. To this end we
           introduce a three-component module called the adSformer diversi-
             fiable personalization module (ADPM) that learns a dynamic userJun    representation. We illustrate the module’s effectiveness and flexibil-                                                                                                                                                  (a) non-personalized ranking
9     ity by personalizing the Click-Through Rate (CTR) and Post-Click
          Conversion Rate (PCCVR) models used in sponsored search. The
              first component of the ADPM, the adSformer encoder, includes
          a novel adSformer block which learns the most salient sequence
            signals. ADPM’s second component enriches the learned signal
          through visual, multimodal, and other pretrained representations.
            Lastly, the third ADPM "learned on the fly" component further[cs.LG]     diversifies the signal encoded in the dynamic user representation.                               (b) with ADPM-personalized ranking
         The ADPM-personalized CTR and PCCVR models, henceforth re-     Figure 1: Ad results from the query jacket for a user who
           ferred to as adSformer CTR and adSformer PCCVR, outperform      recently interacted with mens leather jackets.
           the CTR and PCCVR production baselines by +2.66% and +2.42%,
            respectively, in offline Area Under the Receiver Operating Char-
             acteristic Curve (ROC-AUC). Following the robust online gains in
                                                                                  personalize industrial applications, for better user satisfaction and
         A/B tests, Etsy Ads deployed the ADPM-personalized sponsored
                                                                               business outcomes [11, 34, 49, 63].
           search system to 100% of traffic as of February 2023.
                                                                                   In this article we introduce a general approach to personaliza-
      CCS CONCEPTS                                                   tion in industrial large-scale applications via a methodology called
                                                                             the adSformer diversifiable personalization module (ADPM). We
              • Information systems →Personalization; Sponsored Search                                                                                                illustrate how this methodology is deployed to personalize Etsy Ads
          Advertising; • Machine Learning Approaches →Neural Net-                                                                            ranking and bidding systems in order to demonstrate the method’s
         works.                                                                                       effectiveness. The ADPM-personalized sponsored search system
                                                                         has been deployed to 100% of user traffic and delivering robust
      KEYWORDS                                                                                online results since February 2023 in Etsy Ads.
           Personalization, Sponsored Search, Online Advertising, Neural      We make the following contributions:arXiv:2302.01255v2
          Networks, Transformers, Representation Learning, Multimodality,
                                                                         • We introduce the adSformer diversifiable personalization
           Ranking, Bidding, Ads Computer Vision
                                                                          module (ADPM henceforth), a highly configurable module
        1  INTRODUCTION                                            used to encode sequences of recent user actions and de-
                                                                                                 rive a short-term dynamic user representation. The module
          Online advertising is a multi-billion dollar industry (>$300 billion
                                                                                can handle sequences of variable lengths. ADPM’s architec-
            in the fiscal year 2022) [1] and sponsored search is one of its largest
                                                                                            ture includes three components which learn diverse signals
             sub-fields. In the "pay-per-click" model, advertisers are charged for
                                                                                            symbiotically: 1. the adSformer encoder component; 2. the
              clicks. Thus, sponsored search systems have an incentive to engage
                                                                                        pretrained representations component; 3. the learned "on-
           users via accurate real-time predictions of clicks and purchases.
                                                                                                 the-fly" component. We detail ADPM’s architecture and
         Deep learning methods have been employed in recent years to
                                                                                        explain its implementation for impact and scalability.
          improve the performance of these systems in online advertising [55,                                                                         • The first component of the ADPM, the adSformer encoder,
            56, 58, 63]. More generally, powerful deep learning architectures
                                                                                     introduces a novel variation on the classic transformer
          have been employed to leverage signals from user behaviors and
                                                                                           block, where a global max pooling layer is added at the
              ∗Denisa Roberts is the corresponding author.                                                   last stage, borrowing from the computer vision literature.

Awad, Roberts, Dolev, and Heyman, et al.


     We explain the architecture design choice and learning
        behavior.
    • We demonstrate the module’s effectiveness in practice by
        describing how the ADPM is employed to personalize spon-
       sored search (ad) ranking. We include offline and online
       experimental results and deployment considerations. We
       share reproducibility details including optimal hyperpa-
        rameters, model design choices, pretrained representations
       workflows, and training approaches.

1.1  Related Work
1.1.1   Personalization from user sequences. A useful survey of deep
learning methods employed in sponsored search is [58]. A few
other works include sequences of user actions to more generally
improve click-through rate prediction models in [3, 11, 18, 21, 34–     Figure 2: The adSformer diversifiable personalization module
36, 49, 52, 62, 63], which is an essential task in online advertising.    (ADPM) derives a dynamic user representation from variable-
Recent developments in personalization emerged to separate se-     length sequences of user actions. The adSformer Encoder
quences into long-term and recent or short-term. Pinterest describes     component includes the adSformer block displayed on the
an end-to-end ranking application in [49], with a brief reference to      right.
recent user actions encoded via a multi-headed self-attention layer
and fed to downstream ranking tasks such as search, recommenda-
tions, and ads. In personalized eCommerce search, [3] at Ebay had       pairs are 𝑒= 𝑙𝑖𝑠𝑡𝑖𝑛𝑔𝐼𝐷and 𝑎= 𝑣𝑖𝑒𝑤𝑒𝑑. The sequence length 𝑦
employed the representations of the most recent five clicked items        is a random variable taking values in {0, ..., 𝑀}, where 𝑀is the
to personalize search rankers.                             maximum sequence length dictated by the engineering system.
                                                                       Realized values of𝑦are dictated by the time delta threshold, which is
1.1.2  Transformers in personalization. Transformer encoders have       set to one hour in most of our experiments. All ADPM-encoded user
been used in personalized product search, both at retrieval and re-      actions would have happened within this time delta, and actions
ranking phases. The transformer architecture captures the context      outside the decided upon time delta are masked. The ADPM outputs
of users’ intents by encoding the sequential nature of user behav-      a short-term dynamic user representation which captures complex
ior sequences as seen in previous works from Alibaba, Pinterest,      relationships within and between different source sequences due
and others [11, 21, 34, 44]. Particularly relevant to our work is the       to its three components. The ADPM can be used within the context
behavioral sequence transformer in [11] which encodes a sequence      of any model that can benefit from real time personalization in
of last 20 actions to personalize downstream click-through rate       industrial large-scale applications.
models. Focusing on the retrieval phase, TEM, a transformer based
model, can tune the amount of personalization applied based on     2.2  Diversity of Signals from ADPM’s
the query characteristics [7], illustrating the versatility of the trans-       Components
former architecture. In addition to employing attention mechanisms
                                                       The three-component ADPM design is motivated by its intendedand transformer architecture, authors in [57] employ graph neural
                                                                  use in personalization. Diversity of information helps to capture thenetworks to build a session-aware recommender, where a session
                                                             nuanced patterns of individual users. The three ADPM componentsrepresents a short-term user sequence. In a similar vein, sequence
                                                                     learn different signals from the sequences of user actions. Thisand graph modelling came together as a heterogeneous user graph
                                                                          diversity of signals goal is typical when designing neural networktransformer in [42] to improve personalized recommendations.
                                                                       architectures and the ADPM architecture achieves this goal for  The rest of the article is organized as follows. We introduce the
                                                                    user sequence modelling. The signals learned by each componentthree-component ADPM in Section 2. Component two of the ADPM
                                                         complement each other which fosters symbiotic learning. In de-employs pretrained representations therefore we detail Etsy Ads’
                                                               ployed applications, this symbiotic diversity of signals improvesrepresentation learning workflows in Section 3. To demonstrate
                                                                  robustness to input distribution shifts. The diversity of learnedADPM’s effectiveness and generality, we describe how this module
                                                                         signals also leads to more relevant personalized results through acan be configured and deployed to personalize sponsored search
                                                                          better derived user representation. We evaluate the quality of thisranking models in Section 4. We present offline ablation studies and
                                                                       representation in experiments discussed in Section 5.1.1. Lastly, theonline experiment results in Section 5, after which we conclude.
                                                                     diverse signals learned by the three components help the ADPM
                                                                           better adapt to diverse downstream tasks such as ranking, retrieval,
2 ADPM METHODOLOGY                                                           and recommendations.
2.1  Variable Length Sequences
The ADPM, as seen in left-hand side of Figure 2, encodes sequences     2.3  Component One: adSformer Encoders
of recent user actions 𝑆𝑖= (𝑎𝑖,𝑒𝑖) of variable lengths 𝑦𝑖, variable     The adSformer encoder component uses one or more custom adS-
entity types 𝑒𝑖and variable action types 𝑎𝑖. Examples of (𝑒,𝑎)      former blocks as seen in Figure 2, right panel. This component

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads


learns a deep, expressive representation of the input sequence. The      Formally, for a given sequence of listing IDs’ embedding vectors
adSformer block modifies the standard transformer block in [46]     𝑒𝑖∈R𝑑2 with 𝑑2 = 256, we compute
by adding a final global max pooling layer. This layer downsamples
the block’s outputs by extracting the most salient signals from the                 𝑜2 = 𝐺𝑙𝑜𝑏𝑎𝑙𝐴𝑣𝑒𝑟𝑎𝑔𝑒𝑃𝑜𝑜𝑙𝑖𝑛𝑔([𝑒1,𝑒2, ...,𝑒𝑦])           (9)
sequence representation.                                        where𝑦is the sequence length. Then the output of ADPM’s com-
  The adSformer block starts with an embedding layer which en-                                                             ponent two 𝑜2 is a sequence representation vector of size 𝑑2. The
codes listing IDs into dense vectors of size 𝑑1 = 32. We pad the       individual listing ID’s pretrained representations are kept frozen in
variable length sequence to a common length of 𝑀and mask the                                                            downstream tasks, not requiring an expensive gradient calculation,
padding token. We concatenate the target listing representation                                                                 while adding multimodal signal.
at position zero as in [11]. We then add a fully learnable position
embedding of same dimension 𝑑1 to learn the sequence order for     2.5  Component Three: Representations Learned
the concatenated (𝑡𝑎𝑟𝑔𝑒𝑡,𝑠𝑒𝑞𝑢𝑒𝑛𝑐𝑒) as in [15]. A multi-head self                                              "On the Fly"
attention layer with scaled dot-product attention [46] follows. First
                                                       The third component of the ADPM introduces representationswe get
                                                                    learned for each sequence from scratch in its own vector space as
                          QK𝑇                            part of the downstream models. This component learns light weight
              A(Q, K, V) = softmax √   V,                 (1)      representations for many different (𝑒,𝑎) sequences for which we                                    𝑑
                                                         do not have pretrained representations. For example we encode
where Q, K and V are query, keys and values respectively, and 𝐴is                                                                 sequences of entities 𝑒of type {listingID, taxonomyID, shopID} for
the attention. Then the multi-head self attention is                                                                   user actions 𝑎of type {cart add, favorited, purchased}. Formally,
     MHSA(𝐸𝑃) = Concat(ℎ𝑒𝑎𝑑1,ℎ𝑒𝑎𝑑2, · · · ,ℎ𝑒𝑎𝑑ℎ)W𝐻,     (2)       for 𝑆𝑖= (𝑎𝑖,𝑒𝑖) of variable lengths 𝑦𝑖, variable entity types 𝑒𝑖and
                                                                          variable action types 𝑎𝑖, we embed each entity 𝑒𝑖in the action spacewith ℎ𝑒𝑎𝑑𝑖= A(EW𝑄, EW𝐾, EW𝑉). The projection matrices are
                                                             𝑎𝑖to get a vector representation 𝐸𝑎𝑒𝑖∈R𝑑𝑎𝑒of dimensions 𝑑𝑎𝑒,W𝑄, W𝐾, W𝑉∈R𝑑×𝑑, and 𝐸𝑃represents listing embedding added
to position embedding 𝐸𝑃= 𝐸+ 𝑃. Then the block adds point-wise
feed-forward networks 𝐹𝐹𝑁, 𝐿𝑒𝑎𝑘𝑦𝑅𝑒𝑙𝑢non-linearity as in [11],             𝐸𝑆𝑖= 𝐺𝑙𝑜𝑏𝑎𝑙𝐴𝑣𝑒𝑟𝑎𝑔𝑒𝑃𝑜𝑜𝑙𝑖𝑛𝑔([𝑒1,𝑒2, ...,𝑒𝑦𝑖])        (10)
and residual connections, dropout and layer normalization in the                 𝑜3 = 𝐶𝑜𝑛𝑐𝑎𝑡([𝐸𝑆1, 𝐸𝑆2, ..., 𝐸𝑆𝑧])                     (11)
usual sequence. To simplify notation, 𝑥is the output of the previous
                                                              with 𝑖∈{1, ...,𝑧} and 𝑧is the number of sequences encoded bylayer in the block and 𝑔(𝑥) represents the next layer:
                                                          component three.

             𝑔(𝑥) = 𝑥+ 𝐷𝑟𝑜𝑝𝑜𝑢𝑡(𝑀𝐻𝑆𝐴(𝑥))                    (3)     2.6  Dynamic User Representation
          𝑥= 𝐿𝑎𝑦𝑒𝑟𝑁𝑜𝑟𝑚(𝑥+ 𝑔(𝑥))                       (4)     Given an input set of 𝑝user action sequences 𝑆𝑖= (𝑎𝑖,𝑒𝑖), 𝑖∈
             𝑔(𝑥) = 𝐷𝑟𝑜𝑝𝑜𝑢𝑡(𝐹𝐹𝑁(𝐿𝑒𝑎𝑘𝑦𝑅𝑒𝑙𝑢(𝑥))             (5)       {1, ..., 𝑝}, of variable lengths 𝑦𝑖, the ADPM layer concatenates the
                                                                    three components’ outputs to derive a short term dynamic user          𝑥= 𝐿𝑎𝑦𝑒𝑟𝑁𝑜𝑟𝑚(𝑥+ 𝑔(𝑥)).                      (6)
                                                                      representation of size 𝑑1 + 𝑑2 + Í𝑑𝑎𝑒.
                                                                         (7)
  We add the global max pooling layer at the last stage              𝑢= 𝐴𝐷𝑃𝑀(𝑆1,𝑆2, ...,𝑆𝑝) = 𝐶𝑜𝑛𝑐𝑎𝑡([𝑜1,𝑜2,𝑜3]).      (12)
                                              We concatenate this user representation 𝑢to the input layer in
                 𝑜1 = 𝐺𝑙𝑜𝑏𝑎𝑙𝑀𝑎𝑥𝑃𝑜𝑜𝑙𝑖𝑛𝑔(𝑥).                   (8)     downstream personalization tasks.
  The global pooling layer downsamples the output of the trans-
                                                         2.7 ADPM Implementationformer block to a representation vector of size 𝑑1 instead of out-
putting the concatenated transformer block features for the entire    We designed the ADPM as a general plug-and-play module and
sequence. We thus retain the most salient signal, in a parameter     implement it as a TensorFlow [2] Keras layer which can be reused
efficient manner. We experiment with replacing the global max      across personalization use-cases with a simple import statement.
pooling layer with global average pooling layer and present offline     The ADPM layer is configurable, allowing arguments for customiz-
ablation results in Section 5.                                        ing the ADPM’s three components. Since sequences of streamed
                                                                   user actions are made available by the Feature System team to all
2.4  Component Two: Pretrained                      downstream Etsy applications, ADPM-based personalization can be
     Representations                                             easily scaled to multiple downstream personalization tasks while
                                                                           at the same time introducing a per-model customization to avoid
Component two encodes sequences using listing ID pretrained rep-
                                                                             sacrificing performance.
resentations together with average pooling. Depending on down-
stream performance and availability, we choose from multimodal       2.7.1  Vocabularies. ADPM’s sequence representations are imple-
(AIR) representations detailed in Section 3.2, visual representations     mented as lookup tables. However, when vocabularies are large,
detailed in Section 3.1, or interaction-based representations detailed      the corresponding weight matrices can take up too much memory
in 3.3. Thus component two encodes rich image, text, and multi-     and disk space, a significant challenge in deployments. To over-
modal signals from all the listings in the variable length sequence.     come this challenge and reduce memory consumption, we limit

Awad, Roberts, Dolev, and Heyman, et al.





Figure 3: Etsy Ads personalizes sponsored search’s CTR and PCCVR models by concatenating the short-term dynamic user
representation from ADPM to the input representation layer. Both models share a similar architecture with slight differences
in numbers of layers and hidden units.


the vocabulary size for each sequence to the top 𝐾most frequent     ADPM’s component two’s optimum pretrained representation de-
entities, tuning 𝐾as a hyperparameter in downstream CTR and     pends on the specifics of the downstream tasks, as illustrated in
PCCVR models. For example, the CTR’s vocabulary corresponding       ablation studies from Section 5. Figure 4 shows that the top k near-
to sequences of listing IDs was capped to top 𝐾= 750, 000 listings,       est neighbors for a listing are different when using visual versus
down from 100 million in total. The top 𝐾listings carry the largest     AIR representations. AIR representations better encode price, cate-
impact, after which increasing vocabulary size led to only marginal       gory, and text while the visual representations better encode color,
improvements in model performance. Hence vocabulary size impact      shape, and background image.
on model performance follows a power distribution [41]. We built
the vocabularies dynamically, from the corpus of variable-length
sequences present in the downstream models’ training datasets,
further maximizing impact. The time delta is a hyperparameter that                                                 (b) AIR representation
we can easily tune through ADPM’s flexible implementation.

2.7.2  Software implementation of the pretrained representations
component. Pretrained representations are useful for feature encod-
                                                                                                       (a) Target listing                    (c) Visual representation
ing, scalability and modularity and we describe learning pretrained     Figure 4: Given a target listing of an emerald ring shown
representations for every active listing in Section 3. Running this                                                               in (a), we visualize the top 6 nearest neighbors based on the
process offline allows for deeper architectures without latency con-                                                                            listing’s pretrained AIR representation (b) and listing’s visual
cerns. The pretrained representation vectors are read by ADPM’s                                                              representation (c).
component two through the use of lookup tables and a mapping
between vocabulary and index positions. To make pretrained rep-
resentations easily accessible to downstream models, we wrap the
                                                         3.1  Visual Representationslookup table in a TensorFlow SavedModel which includes average
pooling layers and handling of default padding values. By saving      Pinterest authors lament the scarcity of visual representations
the lookup table with the downstream model, we assure that the      across large-scale industrial applications [6]. In Etsy Ads, we em-
representations used at training time are the same ones used at      ploy image signals across a variety of tasks, such as visually similar
serving time.                                                      candidate generation, search by image, learning other pretrained
                                                                        representations, and the ADPM’s second component.
3  PRETRAINED REPRESENTATION                                                                                   3.1.1  Model design. We train image representations using a mul-
  LEARNING                                                       titask classification architecture [54], an improvement over the
Component two of the ADPM employs pretrained representations       "classic" classification as a proxy to metric learning [53]. By using
to encode variable-length sequences of user actions. For this reason      multiple classification heads, such as taxonomy, color, and material,
we give an overview of Etsy Ads’ pretrained representation learn-     our representations are able to capture more diverse information
ing workflows. Several flavors of representations are trained and      about the image. An EfficientNetB0 architecture [45] with weights
used to encode listing IDs: visual, multimodal (AIR), and skip-gram.      pretrained on ImageNet [14] served as the backbone, and the final

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads


layer was replaced with a 256-dimensional convolutional block, the
desired output representation size. Image random rotation, trans-
lation, zoom, and a color contrast transformation to augment the
dataset were applied during training.

3.1.2  Multitask learning of visual representations. Rather than us-
ing a single dataset of listing images with multiple label columns,
heterogeneous dataset sources containing product images with
different selected attributes as the labels were included. Listing
attributes such as color and material are optionally input by sellers,
so they can be sparse. To mitigate this concern we implemented
a dataset sampler, pictured in Figure 5, which takes in the sepa-
rate datasets, each with its own unique label type. The sampler
evenly distributes examples from each dataset to construct bal-
anced training batches and ascertain that only loss coming from
the respective task’s classification head is considered during back-
propagation. One additional benefit of this approach is that we can
mix in datasets of images from different visual domains to support
more use cases, such as user-uploaded review photos. The multitask
visual representations are integrated into the visually similar ad
recommendations as well as the Search by Image application built
by Etsy Ads, with more details included in [17] and Etsy’s blog post
[16].                                                          Figure 6: Learning AIR: pseudo-two-tower architecture with
                                                          shared weights.


                                                                          of listing’s title, tags and taxonomy path average pooled from light-
                                                                weight fastText pretrained representations [8], and a series of other
                                                               normalized features. We train the AIR model with a softmax loss
                                                                       [54] and a classification objective. During training, we inference
                                                                    source and candidate 256-dimensional representations for each pair
                                                                         in the batch. We then compute a matrix of cosine similarity scores
                                                             between each example’s source and candidate representations [32].
                                                                                Finally, we compute the classification loss using these scores.
Figure 5: Multitask and multi-dataset visual representations
training architecture. The data sampler combines examples     3.3  Skip-Gram Listing Representations
from an arbitrary number of datasets corresponding to re-
                                                                    Visual and AIR pretrained listing representations do not capture
spective classification heads.
                                                                           signals from the sequential browsing behavior of users within a web
                                                                            session. Therefore we learn a listing representation from sequences
                                                                        of listings in a browsing session by employing the skip-gram [29]
3.2  Multimodal Representations: Learning AIR      model, similarly to [18, 60]. We learn a vector representation of
3.2.1  Model design. We design Ads Information Retrieval (AIR)      dimension 𝑑= 64 for each unique listing in the training set. We use
pretrained listing representations with the explicit goal of driving      a hierarchical softmax loss function ([31] and [30]), which showed
ad clicks. The AIR model is a neural network with a pseudo-two-     much better results than classic negative sampling. We found that
tower architecture pictured in Figure 6. The source and candidate       fastText library 1 worked well for training, as long as we disabled
towers share all trainable weights, for which reason we add the       functionality to consider subwords.
prefix "pseudo" to the canonical two-tower architecture [50, 51].
                                               4 ADPM - PERSONALIZED SPONSORED
3.2.2  Learning. We compile a dataset of listing pairs that have been
                                      SEARCH RANKINGclicked together on various pages and we consider one listing as the
"source" and the other listing as the "candidate" within the same ex-     4.1  Background
ample. The training dataset includes source-candidate pairs, where                                                         To demonstrate ADPM’s effectiveness and generality, we describe
for each source we consider its corresponding candidate pair as the                                                   how Etsy Ads employes it to personalize ranking and bidding mod-
positive label, while a sample of the other examples in the same                                                                               els in sponsored search. First, we’ll give an overview of the spon-
batch are the negative labels. For each of the source and candidate                                                                  sored search system. As many online advertising services, sellers
listings, we preprocess and concatenate into an input layer a set of                                                               sponsor their listings (ads) through a second-price cost-per-click
multimodal features. For example, we concatenate the multitask
visual representations described in Section 3.1, text representations         1https://fasttext.cc/

Awad, Roberts, Dolev, and Heyman, et al.

auction campaign. In order to decide which ads to show to a user,     Table 1: The different CTR and PCCVR ADPM configurations
Etsy Ads employs Learning to Rank (LTR) [9, 25] framework in         Config                                     CTR        PCCVR
Figure 7. The system is divided according to the classic two-stage          Pretrained Representation Type                        AIR       skip&visual
dichotomy: ads candidate retrieval and then ads ranking. First, the      Num adSformer Blocks                                     1                1
                                                                                  adSformer Block Dropout                                  0                0
candidate retrieval step winnows the full inventory from over 100         adSformer Num Heads                                     3                2
million listings (items) to under 1000 candidates, after which re-        Learned Listing Representation Dimension                  32               32
sults are reranked based on a combined value score obtained from         Learned Shop Representation Dimension                    16               16
                                                                                  Learned Taxonomy Representation Dimension                8                8
the ranking and bidding models predictions, the CTR and PCCVR             (e, a) (Learned Component)                                    (all e, all a)           (all e, all a)
models respectively.                                                                                          (e, a)((Pretrained Component)                            (listing, all a)        (listing, all a)
   In the CTR case, 𝑝(x) denotes the predicted probability 𝑝(𝑦𝐶𝑇𝑅=             (e,(listing,a) (adSformerviewed) VocabularyEncoder)   Size                     (listing, viewed)750K    (listing, viewed)650K
1) that the candidate listing will be clicked. For PCCVR 𝑝(x) denotes      Num OOV Tokens                                         1                1
the predicted conditional probability 𝑝(𝑦𝑃𝐶𝐶𝑉𝑅= 1|𝑦𝐶𝑇𝑅= 1) that
the listing will be purchased, having been clicked [4].
   Before including the ADPM, baseline production models’ archi-       [11]. The optimum ADPM configuration for the three components
tectures in Etsy Ads were standard stacked deep and cross neural       differs between the CTR and the PCCVR models as Table 1 details,
networks (DCN) [48]. We used these as baselines in all our of-     and this flexibility is one of ADPM’s strengths. Each configuration
fline and online comparisons. The CTR’s DCN has four cross and      choice is similar to a hyperparameter that we tune.
four deep layers with sizes 5000, 2500, 250, 500 and PCCVR’s DCN         After employing ADPM personalization we call the new mod-
employs two cross and two deep layers of sizes 240, and 120 respec-       els the adSformer CTR and PCCVR. Figure 3 depicts the model
tively.                                                                   architecture corresponding to the adSformer CTR and PCCVR after
                                          ADPM inclusion.
4.2  ADPM-Personalized CTR and PCCVR                                                                                    4.2.1  The adSformer CTR. For the adSformer CTR model, the adS-
The goal is to personalize CTR and PCCVR using the ADPM for im-     former encoder component includes one adSformer block with
proved user outcomes. We employ the ADPM to encode sequences      three attention heads. The adSformer encoder encodes user and
of recent user actions anywhere on Etsy for both logged-in and      browser sequences of recently viewed listings since these (𝑒,𝑎)
logged-out users. Instead of considering the last M user actions as      have the highest session frequency. Within the pretrained represen-
typically seen in [11, 34, 49], we consider a sliding one hour window       tations component, the multimodal pretrained representation (AIR)
of user actions, in reverse chronological order of timestamps, to      described in Section 3.2 works best for the CTR task to encode all
encode only recent behavior. More formally, let 𝑆= (𝑎,𝑒,𝑡), be a      sequences of listing IDs. ADPM’s third, "on the fly", component
one-hour sequence of user actions, where 𝑎is the action type one      encodes all one-hour sequences of recent user actions.
of {view, favorite, cart add, purchase, search}, and 𝑒represents one         After concatenating the ADPM’s output to the input represen-
of the entities {listingID, shopID, categoryID, text query} associ-      tation layer, it is critical to have a cross network (DCN) in the
ated with action 𝑎performed at timestamp 𝑡. Due to semantics and      personalized adSformer CTR architecture [47]. As recognized in
infrastructure constraints we further cap the maximum sequence      recent work [23, 24, 40, 43, 48, 56, 56], learning higher order feature
length at 𝑀= 50 actions. Each sequence 𝐼is truncated to within       interactions effectively from the input layer helps performance in
one hour of the most recent action, so 𝑡0 −𝑡𝑙𝑎𝑠𝑡≤1ℎ𝑟. The result-      large scale CTR prediction. For the adSformer CTR, the interac-
ing sequences have variable length which the ADPM can handle      tion module (DCN) is necessary to fully leverage the wide input
through padding and masking.                                       representation which includes the ADPM. The cross layer exclu-
  We concatenate ADPM’s output, the dynamic user representa-      sion leads to a 1.17% drop in ROC AUC. The large capacity of the
tion, to the rest of the wide input feature vector [12] similarly to      adSformer CTR model aids learning and generalization by provid-
                                                                    ing a smoother loss landscape and more stable and faster learning
                                                               dynamics. The adSformer CTR only needs one epoch of training,
                                                                           for a total of 11 hours (one A100 GPU) using Adam [22] optimizer.
                                                           Throughout model training we decay the learning rate using co-
                                                                       sine annealing [26]. We select the largest batch size that can fit in
                                                     memory (8192) and tune the learning rate to an optimum 𝑙𝑟= 0.002.

                                                                                  4.2.2  The adSformer PCCVR. To obtain the ADPM-personalized
                                                                adSformer PCCVR model, we configure the ADPM and concatenate
                                                                                           its output user representation to the baseline PCCVR model input
                                                                                layer, similarly to the CTR. Table 1 gives the ADPM configuration
                                                                            for the adSformer PCCVR model. The major differences to the CTR’s
                                                                      case is a smaller optimum adSformer encoder component with only
                                                          two heads. The PCCVR trains on smaller datasets. We parameterize
                                                                     the ADPM’s pretrained representations component with pretrained
Figure 7: In our Learning to Rank system, ads are ranked by                                                                 skip-gram and visual listing representations. While we trained the
a value score.                                                 PCCVR baseline production model on only two weeks of historical

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads


click logs (135 million examples), the adSformer PCCVR has more       article) at an embedding size of 32 and for the same batch size
parameters after the ADPM addition and thrives with three weeks     employed in all experiments, so we downsize to five and three
of data (200mln examples).                                            heads.
                                                       One of ADPM’s strength is the ability to derive maximum signal
4.2.3  Learning. Both the CTR and PCCVR before and after ADPM-
                                                               with constraints on training and serving resources. We also proxy
based personalization are formulated as binary classification prob-                                                                   Ebay’s [3] encoding of last 𝑘= 5 user actions as an alternative base-
lems, and we use a binary cross entropy loss function
                                                                               line for ADPM. In the original article BST is run on a fixed sequence
   𝐿= −1  ∑︁  (𝑦𝑙𝑜𝑔𝑝(x) + (1 −𝑦) 𝑙𝑜𝑔(1 −𝑝(x))) ,     (13)      length of 20, so we apply both the BST and the ADPM with three
       𝑁                                                  components on a sequence of most recent 20 actions as well. To sum-
             (x,𝑦)∈𝐷
                                                               marize the results in Tables 2 and 3, the three-component ADPM
where 𝐷represent all samples in the training dataset, 𝑦∈{0, 1}      outperforms all the other component combinations as well as the
is the label, 𝑝(𝑥) is the predicted probability, and 𝑥is the input     BST and other baselines, although the BST is a strong alternative.
vector containing (listing, query, and context) attributes as well as
the ADPM’s user representation output.                          Table 2: Ablation studies showing offline lift in metrics
                                                           within the CTR downstream task. Each variant is compared
5  EXPERIMENTAL RESULTS                          against the baseline, non-personalized, CTR model. Each
We evaluate ADPM’s effectiveness through offline and online ex-     variant represents either a configuration of the three compo-
periments by comparing the adSformer CTR and adSformer PCCVR     nent ADPM or another personalization method we compare
models to their non-personalized baselines described in Section 4.     the ADPM against. We vary the ADPM’s three components:
We also perform ablation studies where we compare the ADPM     Comp1=adSformerEncoder; Comp2=Pretrained; Comp3=On-
with other user sequence modeling approaches. Finally, we com-      the-fly. Personalization baselines are: BST=Alibaba’s Behav-
pare the effectiveness of permutations of ADPM configurations in      ioral Sequence Transformer; Ebay’s last k=5.
offline experiments.                                                                                  CTR                                                                                                    Configuration           ROC-AUC  PR-AUC
                                                                  𝐴𝐷𝑃𝑀−3[𝑀𝑎𝑥𝑃𝑜𝑜𝑙]        +2.71%    +8.88%
5.1  Offline Experiments                                         𝐴𝐷𝑃𝑀−3[𝐴𝑣𝑔𝑃𝑜𝑜𝑙]          +2.67%    +8.36%
                                                                           [𝐶𝑜𝑚𝑝1,𝐶𝑜𝑚𝑝2]              +2.42%    +7.19%We evaluate offline performance using PR-AUC and ROC-AUC                                                                           [𝐶𝑜𝑚𝑝1,𝐶𝑜𝑚𝑝3]              +2.04%    +6.36%
metrics and present lifts as compared to baselines in all the ablation                [𝐶𝑜𝑚𝑝2,𝐶𝑜𝑚𝑝3]              +2.43%    +7.65%
studies.                                                                      [𝐶𝑜𝑚𝑝1]                     +1.71%    +5.46%
                                                                             [𝐶𝑜𝑚𝑝2]                     +2.09%    +6.31%
                                                                             [𝐶𝑜𝑚𝑝3]                     +1.75%    +5.74%5.1.1  Evaluating The Effectiveness of ADPM’s Components and Their                                                         [𝐴𝐷𝑃𝑀−𝑘= 20]             +2.66%     +8.5%
Symbiotic Learning Behavior. We aim to better understand the sym-             [𝐵𝑆𝑇−𝑘= 20 −8ℎ𝑒𝑎𝑑𝑠]      +1.77%    +5.55%
biotic learning behavior from the combination of the three compo-              [𝐵𝑆𝑇−1 −ℎ𝑟−5ℎ𝑒𝑎𝑑𝑠]      +1.82%    +3.99%
                                                                  [𝐵𝑆𝑇−1 −ℎ𝑟−3ℎ𝑒𝑎𝑑𝑠]      +1.78%    +4.31%
nents of the ADPM. Our hypothesis is that each component learns                                                                [𝐸𝑏𝑎𝑦−𝑘= 5]                +1.65%    +4.58%
different signals and together through this diversity lead to better            [𝐴𝐷𝑃𝑀−𝑘= 5]              +2.43%     +7.4%
outcomes in downstream tasks. For a comparison, we permute the              [𝐵𝑆𝑇−𝑘= 5]                 +1.45%    +4.77%
configuration of the ADPM holding constant all other modelling
choices and provide lifts in the CTR and PCCVR AUC metrics.
   Furthermore we compare the three-component ADPM to a base-     Table 3: Ablation studies comparing downstream perfor-
line encoder of user sequences, such as the BST employed by [11],    mance for permutations of ADPM’s components within the
which uses an eight head transformer encoder with one block to    PCCVR downstream task.
encode a sequence of 20 user actions and their timestamp. Other                                        PCCVR
                                                                                                     Configuration         ROC-AUC   PR-AUC
alternatives exist, such as the attention mechanisms in [63] or [49]
                                                                   𝐴𝐷𝑃𝑀−3[𝑀𝑎𝑥𝑃𝑜𝑜𝑙]      +2.42%   +28.47%but the BST model in [11] outperforms most of these approaches                                                                      𝐴𝐷𝑃𝑀−3[𝐴𝑣𝑔𝑃𝑜𝑜𝑙]       +2.37%    +26.76%
according to [11]. We also compare against a simple average em-                 [𝐶𝑜𝑚𝑝1,𝐶𝑜𝑚𝑝2]           +1.09%    +13.15%
bedding aggregation of the last five actions, similarly to Ebay’s [3].                 [𝐶𝑜𝑚𝑝1,𝐶𝑜𝑚𝑝3]           +1.87%    +18.14%
                                                                            [𝐶𝑜𝑚𝑝2,𝐶𝑜𝑚𝑝3]           +2.12%    +24.38%
The goal is to understand if the ADPM is more effective through                  [𝐶𝑜𝑚𝑝1]                   +0.36%    +3.47%
its design choices then these baselines when used to personalize a                  [𝐶𝑜𝑚𝑝2]                   +0.84%    +10.76%
                                                                              [𝐶𝑜𝑚𝑝3]                   +1.55%    +15.48%downstream task, such as the CTR model.
  We strive to make comparisons as relevant as possible by using
the same underlying sequence lengths and datasets, training bud-     We have additionally experimented with a an average pooling
gets, as well as hyperparameters from the original papers, however       layer replacing the final global max pooling layer in the adSformer
some differences remain dictated by the implementation pipelines.      block within ADPM’s component one. Results are similar for the
For example, we do learn the position embedding for the BST sim-      two, which makes intuitive sense since the average is influenced
ilarly to the ADPM instead of using timestamp deltas but do not     by extreme values in a sample such as the max. The global max
foresee major differences as noted in [46]. When employed to per-     pooling is still more effective in deriving a different signal from
sonalize the CTR model in ADPM’s place, the BST runs out of      the sequence which complements the signals derived by the other
memory for a one hour sequence and eight heads (as in the BST     two components. Interestingly, ADPM also outperformes when

Awad, Roberts, Dolev, and Heyman, et al.

encoding the last five or the last 20 instead of a one-hour, variable-     Table 5: Hyperparameters for training the adSformer CTR
length, sequence.                                         and its baseline, the non-personalized CTR prediction model
                                                     which is a neural network with four fully connected layers.
5.1.2  Evaluating the Impact of Different Choices of Pretrained Rep-                            Config                           adSformer CTR        baseline NN CTR
resentations in ADPM’s Component Two. In Table 4 we can see how                   Num Epochs                                  1                     3
different configurations of the pretrained representation compo-                           LearningLearning RateRate Scheduler                     cosine0.002                 0.00061cosine
nent two of ADPM lead to different test ROC AUC and PR AUC. We                            Optimizer                         Adam           LazyAdam
                                                                                                    Adam 𝛽1                                           0.9                        0.9
notice that combining all three flavors of pretrained representations                     Adam 𝛽2                                      0.999                    0.999
                                                                                                    Adam 𝜖                                     1e-08                   1e-08
in CTR’s ADPM configuration leads to the highest test ROC AUC.                          Dropout Hidden Layers                         0                     0
However only AIR was included in the deployed adSformer CTR,                           BatchCross ModuleNorm Hidden(DCN)Layer                     yesyes                    yesno
since both ROC AUC and PR AUC are top ranking and memory re-                           BatchBatch SizeSize (train)(validation)                       8192500                  8192500
quirements are lower. In PCCVR’s ADPM configuration skip-gram                          MachineMachine TypeType (training)(evaluation)                 A100A100                 P100T4
and visual representations performed best together in terms of PR                            Loss                         BinaryCrossEntropy    BinaryCrossEntropy
                                                                                           Num Parameters (trainable)              708,504,031              233,709,623
AUC, however the ADPM configuration with only the adSformer                   Num Parameters (total)                  897,499,741              243,726,397
encoder component and the learned component performed well.
One hypothesis is that the adSformer encoder learns a signal similar                                                             Table 6: Train and validation datasets characteristics for adS-
to the signal from the pretrained skip-gram since they both encode                                                       former CTR and PCCVR
the sequential nature of sequences of listing IDs.
                                                                           Model                   Config                  Training           Validation
Table 4: Ablation studies showing offline lift in metrics       CTR         Num Examples                 300mln             8.5mln
against the baseline, non-personalized, models for various       CTR    Num Consecutive Days                      30                 1
                                                               CTR             Sampling Type   50-50 negative sampling   random sampling
configurations of the ADPM’s pretrained representation com-      PCCVR       Num Examples                 200mln             8.5mln
ponent.                                                        PCCVR  Num Consecutive Days                      21                 1
                              CTR             PCCVR            PCCVR          Sampling Type                click filtered   random sampling
  Pretrained Selection         ROC-AUC  PR-AUC  ROC-AUC   PR-AUC

  Skipgram                         +1.99%    +5.88%      +1.35%    +9.93%
  Visual                           +1.90%    +5.37%      +1.33%    +10.21%
 AIR                              +2.14%    +6.44%      +1.23%    +8.19%
  Skipgram/Visual                  +2.10%    +5.71%      +1.32%   +10.38%
  AIR/Skipgram                    +2.20%    +6.44%      +1.25%    +7.51%
  AIR/Visual                       +2.16%    +6.22%      +1.17%    +8.54%
  AIR/Skipgram/Visual             +2.26%    +6.17%      +1.14%    +7.56%
 No Pretrained Representations      +1.60%    +4.89%     +1.37%    +10.24%


  The adSformer CTR and PCCVR differ in ADPM’s pretrained
component optimal configuration. We are not surprised, given that
a user may have different intents during their browsing journey.                                                            Figure 8: Daily offline AUC evaluation of adSformer per-
For example, a buyer shown an ad impression is likely to be earlier                                                               sonalized PCCVR model against the baseline PCCVR model
in the purchase funnel and the click intent (CTR prediction) may be                                                    from 2023-01-11 to 2023-01-21.
around shopping for inspiration or price comparisons, so the AIR
embedding works better. Post-click the purchase intent (PCCVR
prediction) may be more narrowly focused on stylistic variations     5.2  Online A/B Experiments
and shipping profiles of a candidate listing, so the visual signal from
                                                                  Before deploying to 100% traffic we evaluated the adSformer CTR
the image embedding is more important.
                                                          and adSformer PCCVR in online A/B tests with results in Table 7.
  For reproducibility, Table 9 gives hyperparameters and other
                                                       Compared to the previous production model, the adSformer PC-
machine learning choices for the adSformer CTR as well as for its
                                              CVR demonstrated an increase in Return on Ad Spend (ROAS),
baseline, the non-personalized standard CTR prediction model. The
                                                      PCCVR, and Gross Merchandised Sale (GMS). For Etsy Ads sellers
adSformer PCCVR has similar settings.
                                                                             this translates to an increase in orders with larger sale values at a
   Table 10 gives the dataset choices for the winning adSformer
                                                               lower cost. The CTR model shows improved engagement metrics
CTR and PCCVR. For the CTR we sample 50 percent of non-clicked
                                                          and the adSformer CTR and PCCVR models deployed in tandem
impressions in the training dataset but perform a random sampling
                                                                            for A/B test demonstrated even larger increases in ROAS and GMS
for the validation set, so that validation and test sets are repre-
                                                    when comparing to individual model contributions.
sentative of the production data seen in the wild. The PCCVR is
trained on clicked impressions but evaluated on a representative
                                                         5.3  Additional Considerations in the Deployedtest sample, similarly to the adSformer CTR.
   In Etsy Ads production, models are trained daily and evaluated        ADPM-Personalized Ads System
on next-day test datasets. In Figure 8 we can see the PR AUC and     Sampling biases, such as position bias [20], can reduce ad rank-
ROC AUC lift for the ADPM-personalized adSformer PCCVR as      ing improvements from ADPM. A correlation can be observed
compared to the non-personalized PCCVR production baseline     between the positional rank of a shown ad and the probability of
across a period of ten days.                                         being clicked, which can lead to a feedback loop where the model

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads

Table 7: Statistically significant online A/B experiment re-    6  CONCLUSION
sults (p-value < 0.001).
                                                                     In this article we introduced a scalable general approach to ads
     Metric     ADPM-CTR  ADPM-PCCVR  Tandem           personalization from variable-lengthsequences of recent user ac-
    Ads CTR          +2.55%           -0.02%   +2.42%             tions, the adSformer diversifiable personalization module (ADPM).
    Ads PCCVR       +0.29%          +1.26%   +0.90%          Following the success of deploying the ADPM-personalized spon-
    Ads ROAS        +1.02%          +3.51%   +5.34%          sored search, Etsy Ads is currently experimenting with ADPM-
    Ads GMS         +3.02%          +2.24%   +4.17%           personalized recommendation ads. Future work includes further
                                                               experimenting with the ADPM’s three components by creating
                                                                  other adSformer encoder architectures, adding pretrained graph
                                                                      representations to component two, and updating image, text, and
                                                              multimodal representations. To this end, Etsy Ads continues im-
inadvertently prioritizes certain candidates due to their previous      proving their pretrained representations through strengthening the
high ranking and not due to model improvement. To address this      ads computer vision capabilities. Finally, Etsy Ads plans to extend
challenge, an auxiliary debiasing model [61] was included in the        artificial intelligence driven personalization efforts to the seller
adSformer CTR.                                                    toolbox via generative image, multimodal, and video technologies.
   Predicted CTR and PCCVR scores must reflect true probabilities
in order to assign monetary value and forecast budget depletion,
                                               7 ACKNOWLEDGMENTStherefore a calibration layer is also introduced for each of the CTR
and PCCVR models. Calibration is achieved through the parametric    We thank engineers in Etsy Ads for their work leading to developing
approach of Platt Scaling [19, 37].                               and deploying the adSformers. In alphabetical order: Julie Chien,
  Numerous real world machine learning applications across natu-      Eric Herrmann, Julia Hoffman, Rezwana Karim, Mason Kirchner,
ral language processing [38], computer vision [6], trajectory pre-      Melissa Louie, Alec Malstrom, Seoyoon Park, Maharshi Thakker,
diction [39], personalized ads, search and recommendations [5, 61],      Justin Tse, Gerardo Veltri. We also thank the Rivulet streaming
and computational advertising [27, 28] employ multitask learning       features team, Information Retrieval Platform, and the ML Platform
[10]. A technique many decades old, multitask learning commonly     team for their support.
improves accuracy of tasks as well as efficiency of machine learning
pipelines. However, the case for multitask learning in mature ma-
                                      REFERENCES
chine learning systems that have been deployed as separate models
                                                                                                  [1]  2023. Forecast 2023: Ad Spending Will Slow Down Next Year But Will Continue To
for many years, is complex in practice. For example, models such            Grow. https://www.forbes.com/sites/bradadgate/2022/12/08/forecast-2023-ad-
as the adSformer CTR and the adSformer PCCVR have been tuned             spending-will-slow-down-next-year-but-will-continue-to-grow/
separately with different choices in terms of training datasets, neu-         [2]  Martín Abadi, Paul Barham, Jianmin Chen, Zhifeng Chen, Andy Davis, Jeffrey
                                                                                     Dean, Matthieu Devin, Sanjay Ghemawat, Geoffrey Irving, Michael Isard, et al.
ral network capacities, and optimum ADPM configurations. Etsy              2016. TensorFlow: A system for large-scale machine learning. In 12th USENIX
Ads is in the process of experimenting with the multitask learning            symposium on operating systems design and implementation (OSDI 16). 265–283.
                                                                                                  [3]  Grigor Aslanyan, Aritra Mandal, Prathyusha Senthil Kumar, Amit Jaiswal, and
paradigm in personalized sponsored search.                                 Manojkumar Rangasamy Kannadasan. 2020. Personalized ranking in eCommerce
                                                                                                   search. In Companion Proceedings of the Web Conference 2020. 96–97.
                                                                                                  [4]  Alaa Awad, Congzhe Su, and Erica Greene. 2022. How We Built A Context-Specific
5.4  Infrastructure Considerations in Deployed               Bidding System for Etsy Ads. https://www.etsy.com/codeascraft/how-we-built-
    ADPM-Personalized Ads System                               [5]  a-context-specific-bidding-system-for-etsy-adsPaul Baltescu, Haoyu Chen, Nikil Pancha, Andrew Zhai, Jure Leskovec, and
Introducing most recent / real time sequences into a production             Charles Rosenberg. 2022. ItemSage: Learning product embeddings for shopping
                                                                                   recommendations at Pinterest. arXiv preprint arXiv:2205.11728 (2022).
training and serving path includes infrastructure challenges, and a          [6]  Josh Beal, Hao-Yu Wu, Dong Huk Park, Andrew Zhai, and Dmitry Kislyuk.
heavy investment in streaming architecture. Thankfully, much of              2022. Billion-scale pretraining with vision transformers for multi-task visual
this infrastructure has already been standardized across Etsy. Etsy’s              representations. In Proceedings of the IEEE/CVF Winter Conference on Applications
                                                                                                          of Computer Vision. 564–573.
Feature System team uses a low latency streaming system powered          [7]  Keping Bi, Qingyao Ai, and W Bruce Croft. 2020. A transformer-based embedding
by Kafka PubSub for writing interaction event logs to a low latency           model for personalized product search. In Proceedings of the 43rd International
feature store. The logged-in and logged-out user features are made        ACM SIGIR Conference on Research and Development in Information Retrieval.
                                                                                          1521–1524.
available through a scalable micro service. The fetched in-session          [8]  Piotr Bojanowski, Edouard Grave, Armand Joulin, and Tomas Mikolov. 2017.
features are captured and preserved in training logs as close as             Enriching word vectors with subword information. Transactions of the association
                                                                                                            for computational linguistics 5 (2017), 135–146.
possible to model serving, which minimizes skew between training          [9] Zhe Cao, Tao Qin, Tie-Yan Liu, Ming-Feng Tsai, and Hang Li. 2007. Learning
and serving feature set. Our model serving system uses memcache              to rank: from pairwise approach to listwise approach. In Proceedings of the 24th
to cache model scores thereby reducing latency and volume to               international conference on Machine learning. 129–136.
                                                                                            [10]  Rich Caruana. 1997. Multitask learning. Machine learning 28, 1 (1997), 41–75.
downstream feature fetching and model inference services. The key        [11] Qiwei Chen, Huan Zhao, Wei Li, Pipei Huang, and Wenwu Ou. 2019. Behavior
used to write and read requests must be updated to include user             sequence transformer for e-commerce recommendation in Alibaba. In Proceedings
and browser ID (for logged-out users). The real-time nature of the               of the 1st International Workshop on Deep Learning Practice for High-Dimensional
                                                                                               Sparse Data. 1–4.
user action sequences demands that either the cache is removed        [12] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra,
or that the expiration TTL is lowered dramatically. At scale, in our             Hrishi Aradhye, Glen Anderson, Greg Corrado, Wei Chai, Mustafa Ispir, et al.
                                                                                                 2016. Wide & deep learning for recommender systems. In Proceedings of the 1st
production systems, we pay close attention to latency and cloud            workshop on deep learning for recommender systems. 7–10.
cost surges due to increased volume to downstream services.               [13] Comet.com. 2021. Comet.com home page. https://www.comet.com/

Awad, Roberts, Dolev, and Heyman, et al.



[14]  Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. 2009. Im-               10, 3 (1999), 61–74.
     agenet: A large-scale hierarchical image database. In 2009 IEEE conference on        [38]  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya
     computer vision and pattern recognition. Ieee, 248–255.                                      Sutskever, et al. 2019. Language models are unsupervised multitask learners.
[15]  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert:           OpenAI blog 1, 8 (2019), 9.
      Pre-training of deep bidirectional transformers for language understanding.        [39]  Denisa Roberts. 2019. Neural networks for Lorenz map prediction: A trip through
     arXiv preprint arXiv:1810.04805 (2018).                                                       time. arXiv preprint arXiv:1903.07768 (2019).
[16] Eden Dolev and Alaa Awad. 2023. From Image Classification to Multitask Modeling:        [40]  Denisa AO Roberts and Lucas R Roberts. 2020. QR and LQ Decomposition Matrix
      Building Etsy’s Search by Image Feature. https://www.etsy.com/codeascraft/from-            Backpropagation Algorithms for Square, Wide, and Deep–Real or Complex–
     image-classification-to-multitask-modeling-building-etsys-search-by-image-             Matrices and Their Software Implementation. arXiv preprint arXiv:2009.10071
      feature                                                                                           (2020).
[17] Eden Dolev, Alaa Awad, Denisa Roberts, Zahra Ebrahimzadeh, Marcin Mejran,        [41]  Lucas Roberts and Denisa Roberts. 2017.  An expectation maximization
     Vaibhav Malpani, and Mahir Yavuz. 2023. Efficient Large-Scale Vision Represen-           framework for Yule-Simon preferential attachment models.  arXiv preprint
      tation Learning. arXiv preprint arXiv:2305.13399 (2023).                                     arXiv:1710.08511 (2017).
[18]  Mihajlo Grbovic and Haibin Cheng. 2018. Real-time personalization using em-        [42] Zeren Shui, Ge Liu, Anoop Deoras, and George Karypis. 2022. Sequence-graph
     beddings for search ranking at Airbnb. In Proceedings of the 24th ACM SIGKDD               duality: Unifying user modeling with self-attention for sequential recommenda-
      International Conference on Knowledge Discovery & Data Mining. 311–320.                     tion. (2022).
[19] Chuan Guo, GeoffPleiss, Yu Sun, and Kilian Q Weinberger. 2017. On calibration        [43] Weiping Song, Chence Shi, Zhiping Xiao, Zhijian Duan, Yewen Xu, Ming Zhang,
      of modern neural networks. In International conference on machine learning.           and Jian Tang. 2019. Autoint: Automatic feature interaction learning via self-
    PMLR, 1321–1330.                                                                              attentive neural networks. In Proceedings of the 28th ACM International Conference
[20]  Jianqiang Huang, Ke Hu, Qingtao Tang, Mingjian Chen, Yi Qi, Jia Cheng, and            on Information and Knowledge Management. 1161–1170.
     Jun Lei. 2021. Deep position-wise interaction network for CTR Prediction. In        [44]  Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, and Peng Jiang.
      Proceedings of the 44th International ACM SIGIR Conference on Research and              2019. BERT4Rec: Sequential recommendation with bidirectional encoder rep-
     Development in Information Retrieval. 1885–1889.                                          resentations from transformer. In Proceedings of the 28th ACM international
[21] Wang-Cheng Kang and Julian McAuley. 2018. Self-attentive sequential recom-              conference on information and knowledge management. 1441–1450.
     mendation. In 2018 IEEE international conference on data mining (ICDM). IEEE,        [45] Mingxing Tan and Quoc V. Le. 2019. EfficientNet: rethinking model scaling for
     197–206.                                                                               convolutional neural networks. CoRR abs/1905.11946 (2019). arXiv:1905.11946
[22]  Diederik P Kingma and Jimmy Ba. 2014. Adam: A method for stochastic opti-              http://arxiv.org/abs/1905.11946
      mization. arXiv preprint arXiv:1412.6980 (2014).                                        [46] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
[23] Lang Lang, Zhenlong Zhu, Xuanye Liu, Jianxin Zhao, Jixing Xu, and Minghui           Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017.  Attention is all
     Shan. 2021. Architecture and operation adaptive network for online recom-           you need. Advances in neural information processing systems 30 (2017).
     mendations. In Proceedings of the 27th ACM SIGKDD Conference on Knowledge        [47]  Ruoxi Wang, Bin Fu, Gang Fu, and Mingliang Wang. 2017. Deep & cross network
     Discovery & Data Mining. 3139–3149.                                                          for ad click predictions. In Proceedings of the ADKDD’17. 1–7.
[24] Zeyu Li, Wei Cheng, Yang Chen, Haifeng Chen, and Wei Wang. 2020. Inter-        [48]  Ruoxi Wang, Rakesh Shivanna, Derek Cheng, Sagar Jain, Dong Lin, Lichan Hong,
      pretable click-through rate prediction through hierarchical attention. In Pro-            and Ed Chi. 2021. DCN v2: Improved deep & cross network and practical lessons
      ceedings of the 13th International Conference on Web Search and Data Mining.              for web-scale learning to rank systems. In Proceedings of the Web Conference
     313–321.                                                                                      2021. 1785–1797.
[25]  Tie-Yan Liu. 2011. Learning to rank for information retrieval. Springer Science &        [49]  Jiajing Xu, Andrew Zhai, and Charles Rosenberg. 2022. Rethinking personalized
     Business Media.                                                                   ranking at Pinterest: An end-to-end approach. In Proceedings of the 16th ACM
[26]  Ilya Loshchilov and Frank Hutter. 2016. Sgdr: Stochastic gradient descent with             Conference on Recommender Systems. 502–505.
    warm restarts. arXiv preprint arXiv:1608.03983 (2016).                                  [50]  Ji Yang, Xinyang Yi, Derek Zhiyuan Cheng, Lichan Hong, Yang Li, Simon Xiaom-
[27]  Jiaqi Ma, Zhe Zhao, Xinyang Yi, Jilin Chen, Lichan Hong, and Ed H Chi. 2018.             ing Wang, Taibai Xu, and Ed H Chi. 2020. Mixed negative sampling for learning
     Modeling task relationships in multi-task learning with multi-gate mixture-of-            two-tower neural networks in recommendations. In Companion Proceedings of
      experts. In Proceedings of the 24th ACM SIGKDD international conference on              the Web Conference 2020. 441–447.
     knowledge discovery & data mining. 1930–1939.                                        [51] Xinyang Yi, Ji Yang, Lichan Hong, Derek Zhiyuan Cheng, Lukasz Heldt, Aditee
[28]  Xiao Ma, Liqin Zhao, Guan Huang, Zhi Wang, Zelin Hu, Xiaoqiang Zhu, and Kun            Kumthekar, Zhe Zhao, Li Wei, and Ed Chi. 2019. Sampling-bias-corrected neural
      Gai. 2018. Entire space multi-task model: An effective approach for estimating            modeling for large corpus item recommendations. In Proceedings of the 13th ACM
      post-click conversion rate. In The 41st International ACM SIGIR Conference on             Conference on Recommender Systems. 269–277.
     Research & Development in Information Retrieval. 1137–1140.                           [52]  Lucia Yu, Ethan Benjamin, Congzhe Su, Yinlin Fu, Jon Eskreis-Winkler, Xiaoting
[29] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013.  Efficient            Zhao, and Diane Hu. 2021. Personalization in e-commerce product search by
      estimation of word representations in vector space. arXiv preprint arXiv:1301.3781              user-centric ranking. KMECommerce Workshop Held at WWW ’21 (2021).
      (2013).                                                                                [53] Andrew Zhai and Hao-Yu Wu. 2018. Making classification competitive for
[30] Andriy Mnih and Geoffrey E Hinton. 2008. A scalable hierarchical distributed            deep metric learning. CoRR abs/1811.12649 (2018).  arXiv:1811.12649  http:
     language model. Advances in neural information processing systems 21 (2008).                //arxiv.org/abs/1811.12649
[31]  Frederic Morin and Yoshua Bengio. 2005.  Hierarchical probabilistic neural        [54] Andrew Zhai, Hao-Yu Wu, Eric Tzeng, Dong Huk Park, and Charles Rosen-
     network language model. In International workshop on artificial intelligence and              berg. 2019. Learning a unified embedding for visual search at Pinterest. CoRR
       statistics. PMLR, 246–252.                                                               abs/1908.01707 (2019). arXiv:1908.01707 http://arxiv.org/abs/1908.01707
[32]  Priyanka Nigam, Yiwei Song, Vijai Mohan, Vihan Lakshman, Weitian Ding, Ankit        [55]  Shuangfei Zhai, Keng-hao Chang, Ruofei Zhang, and Zhongfei Mark Zhang. 2016.
      Shingavi, Choon Hui Teo, Hao Gu, and Bing Yin. 2019. Semantic product search.             Deepintent: Learning attentions for online advertising with recurrent neural
      In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge             networks. In Proceedings of the 22nd ACM SIGKDD international conference on
     Discovery & Data Mining. 2876–2885.                                                 knowledge discovery and data mining. 1295–1304.
[33]  Priyanka Nigam, Yiwei Song, Vijai Mohan, Vihan Lakshman, Weitian Ding, Ankit        [56] Buyun Zhang, Liang Luo, Xi Liu, Jay Li, Zeliang Chen, Weilin Zhang, Xiaohan
      Shingavi, Choon Hui Teo, Hao Gu, and Bing Yin. 2019. Semantic product search.            Wei, Yuchen Hao, Michael Tsang, Wenjun Wang, et al. 2022. DHEN: A deep
      In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge            and hierarchical ensemble network for large-scale click-through rate prediction.
     Discovery & Data Mining. 2876–2885.                                                   arXiv preprint arXiv:2203.11014 (2022).
[34]  Nikil Pancha, Andrew Zhai, Jure Leskovec, and Charles Rosenberg. 2022. Pinner-        [57] Mengqi Zhang, Shu Wu, Meng Gao, Xin Jiang, Ke Xu, and Liang Wang. 2020.
     Former: Sequence modeling for user representation at Pinterest. arXiv preprint              Personalized graph neural networks with attention mechanism for session-aware
      arXiv:2205.04507 (2022).                                                            recommendation. IEEE Transactions on Knowledge and Data Engineering (2020).
[35] Qi Pi, Weijie Bian, Guorui Zhou, Xiaoqiang Zhu, and Kun Gai. 2019. Practice        [58] Weinan Zhang, Jiarui Qin, Wei Guo, Ruiming Tang, and Xiuqiang He. 2021.
    on long sequential user behavior modeling for click-through rate prediction.           Deep learning for click-through rate estimation. arXiv preprint arXiv:2104.10584
      In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge               (2021).
     Discovery & Data Mining. 2671–2679.                                                  [59] Yang Zhang, Dong Wang, Qiang Li, Yue Shen, Ziqi Liu, Xiaodong Zeng, Zhiqiang
[36] Qi Pi, Guorui Zhou, Yujing Zhang, Zhe Wang, Lejian Ren, Ying Fan, Xiaoqiang            Zhang, Jinjie Gu, and Derek F Wong. 2021. User retention: A causal approach
     Zhu, and Kun Gai. 2020. Search-based user interest modeling with lifelong            with triple task modeling.. In IJCAI. 3399–3405.
      sequential behavior data for click-through rate prediction. In Proceedings of the        [60]  Xiaoting Zhao, Raphael Louca, Diane Hu, and Liangjie Hong. 2018.  Learn-
     29th ACM International Conference on Information & Knowledge Management.             ing item-interaction embeddings for user recommendations.  arXiv preprint
     2685–2692.                                                                                arXiv:1812.04407 (2018).
[37]  John Platt et al. 1999. Probabilistic outputs for support vector machines and com-        [61] Zhe Zhao, Lichan Hong, Li Wei, Jilin Chen, Aniruddh Nath, Shawn Andrews,
      parisons to regularized likelihood methods. Advances in large margin classifiers             Aditee Kumthekar, Maheswaran Sathiamoorthy, Xinyang Yi, and Ed Chi. 2019.

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads


    Recommending what video to watch next: a multitask ranking system. In Pro-   A  ADDITIONAL INFORMATION FOR
                                                                43–51.      ceedings                of the                    13th               ACM                             Conference                                    on                                     Recommender                                                          Systems.
[62]     Guorui Zhou,              Na                  Mou,                         Ying                                 Fan, Qi                                                   Pi,                                            Weijie Bian,                                             Chang Zhou,                                                                Xiaoqiang      REPRODUCIBILITY
     Zhu,         and Kun                    Gai. 2019. Deep                                       interest                                           evolution                                              network                                                                  for                                                                 click-through                                                                                    rate
      prediction.                                                                                   Vol.                                                                                         33.    A.1  Candidate Generation for Personalized Ad                 In Proceedings                                  of the                           AAAI conference                                              on                                                                     artificial                                                                           intelligence,
     5941–5948.                                           Ranking: Ads Retrieval
[63]  Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui
     Yan, Junqi Jin, Han Li, and Kun Gai. 2018. Deep interest network for click-through      Since performing real-time inference for adSformer CTR and PC-
      rate prediction. In Proceedings of the 24th ACM SIGKDD international conference    CVR models for the full set of ad listings would be prohibitively
     on knowledge discovery & data mining. 1059–1068.
                                                                     expensive, we briefly describe the candidate retrieval system that
                                                             produce up to 600 candidate listings to re-rank. We employ a hy-
                                                                       brid lexical and pretrained representation-based retrieval system,
                                                                designed to produce maximally relevant results for all types of
                                                                   user queries. Lexical retrieval. In this first retrieval pass, we use
                                                                                 "static" CTR and PCCVR models that are batch inferenced offline
                                                                                   daily. The predicted scores, along with every listing’s title and tags,
                                                                    as well as the ad budget remaining for each listing’s campaign,
                                                                    are indexed in a sharded inverted index search database running
                                                          Apache Solr2. At query time, we fetch up to 1000 listings from each
                                                                shard based on title and tag matching and that have ad budget
                                                                  remaining, and we calculate a ranking score which is similar to
                                                                   the value function. We also boost listings by a taxonomy match-
                                                                    ing prediction score, obtained from a separately trained and batch
                                                                   inferenced BERT [15] model, as well as additional business logic.
                                                              Pretrained representation-based retrieval. We currently lever-
                                                              age representations from a two-tower(query and listing towers,
                                                                           textual inputs only) model built for organic search retrieval at Etsy,
                                                                          similarly to Amazon’s [33]. We have plans to test multimodal AIR
                                                                      representations next. Given the trained two-tower model, we host
                                                                   the query tower online for live inference and batch inference the
                                                                     representations from the listing tower, which are indexed into an
                                                             Approximate Nearest Neighbor (ANN) database. A large challenge
                                                  we faced adopting off-the-shelf ANN solutions for an ads use case
                                                                                        is that the index quickly becomes stale as sellers’ budgets deplete
                                                               throughout the day, ANN options on the market do not allow for
                                                                               filtering on attributes that change with such high frequency. We
                                                                       are experimenting with promising new in-house infrastructure that
                                                                     incorporates integrated filtering directly into the ANN.

                                                A.2  Training the adSformer CTR and PCCVR:
                                                       Additional Details
                                              We run extensive offline experiments and ablation studies and omit
                                                   many of the results for brevity. For example, we study the vocabu-
                                                                          lary size effect when encoding the ADPM representations of listing
                                                          ID sequences and give results in 8. All three components of the
                                                             ADPM-learned, pretrained and adSformer encoded representations-
                                                                  use the same vocabulary. We gain minimally by increasing vocabu-
                                                                         lary size after a certain point.
                                                               Note that throughout this article the offline comparison numbers
                                                 may vary for the same model variant due to variability inherent
                                                                       in sampled datasets. For reproducibility, Table 9 gives all hyper-
                                                               parameters and other machine learning choices for the winning
                                                              adSformer CTR.
                                                                    Table 10 gives the dataset choices for the winning adSformer
                                                 CTR and PCCVR. For the CTR we sample 50 percent of non-clicked
                                                                    impressions in the training dataset but perform a random sampling


                                                                                                2https://solr.apache.org/

Awad, Roberts, Dolev, and Heyman, et al.


Table 8: Performance metrics for two selected adSformer CTR models with vocabulary sizes of 600K and 750K vs baseline NN,
corresponding to training dynamics in Figures 9 and 10 from Comet

           Model                      PR AUC (lift range)     ROC AUC (lift range)   Train time (machine)

            adSformer CTR 750 (fuchsia)  0.0425 (+6.15% to +6.65)  0.73954 (+1.94 to +2.36%)         11 hrs (A100)
            adSformer CTR 600 (purple)   0.0423 (+5.00% to +5.75%)     0.7391 (+1.83% to +1.9%)         10 hrs (A100)
              baseline NN CTR (orange)                       0.0400                      0.7258          16 hrs (P100)


  Table 9: adSformer CTR: 600K vs 750K vocabulary size         Table 8 we see the final metric lifts and training times achieved on
      Config                            adSformer750          adSformer600             baseline NN          the same train and validation datasets (described in Table 10). Fig-
    Num           Epochs                                                    1                                                                          1                                                                                                 3          ure 10 helps visually understand the lift achieved by the adSformer       Learning               Rate                                 0.002                                                                               0.001                                                                                                   0.00061
       Learning               Rate Scheduler                     cosine                                                                           cosine                                                                                                    cosine       CTR variants in validation AUC metrics.
       Optimizer                                     Adam                                                      Adam           LazyAdam
     Adam 𝛽1                                           0.9                        0.9                        0.9
     Adam 𝛽2                                      0.999                    0.999                    0.999
     Adam 𝜖                                     1e-08                   1e-08                   1e-08
      Dropout Hidden Layers                         0                     0                     0
      Batch Norm Hidden Layer                     yes                    yes                    yes
      Cross Module (DCN)                          yes                    yes                  no
      Batch Size (train)                            8192                  8192                  8192
      Batch Size (validation)                        500                   500                   500
      Machine Type (training)                   A100                A100                 P100
      Machine Type (evaluation)                 A100                 P100                  T4
       Loss                         BinaryCrossEntropy    BinaryCrossEntropy    BinaryCrossEntropy
    Num Parameters (trainable)              708,504,031              690,842,559              233,709,623
    Num Parameters (total)                  897,499,741              844,564,093              243,726,397


Table 10: Train and validation datasets characteristics for
adSformer CTR and PCCVR                                                            Figure 9: adSformer CTR model selection: train and valida-
  Model                   Config                  Training           Validation     tion loss curves. Lower is better. Source: Comet.
 CTR         Num Examples                 300mln             8.5mln
 CTR    Num Consecutive Days                      30                 1
 CTR             Sampling Type   50-50 negative sampling   random sampling
 PCCVR       Num Examples                 200mln             8.5mln
 PCCVR  Num Consecutive Days                      21                 1
 PCCVR          Sampling Type                click filtered   random sampling


for the validation set, so that validation and test sets are repre-
sentative of the production data seen in the wild. The PCCVR is
trained on clicked impressions but evaluated on a representative
test sample, similarly to the adSformer CTR.
   Furthermore, Table 11 illustrates gains in PCCVR performance
from increased training dataset size after including the ADPM.        Figure 10: adSformer CTR selected models vs baseline: ROC
                                         AUC and PR AUC curves. Higher is better. Source: Comet.
Table 11: Increased performance metrics for adSformer PC-
CVR model vs the baseline NN production model on the same
validation dataset for different training window sizes

  Training Window   ROC-AUC Lift  PR-AUC Lift   Train Duration

  2 weeks Baseline              0.0%          0.0%            6 hrs
  3 weeks Baseline           +0.01%        +0.11%            8 hrs
  2 weeks adSformer         +1.28%        +9.61%           11 hrs
  3 weeks adSformer         +1.58%       +12.07%           16 hrs


  To determine optimal hyperparameters, we combine random
search, deep learning expert manual selection, and Bayesian hy-
                                                            Figure 11: adSformer PCCVR eval metrics during training:
perparameter search, depending on the hyperparameter of interest.
                                        ROC AUC and PR AUC per step. Higher is better. Source:
We visualize training dynamics curves in Comet [13] to guide our
                                                      Comet.
model choices. For example, in Figures 9 we see that both adSformer
CTR model flavors (with listing ID vocabularies of 750K and 600K
respectively) trained for one epoch achieve slightly lower training         In additional ablation studies we vary multiple hyperparameters,
losses and significantly lower validation losses when compared to       for example the number of heads in the adSformer encoder and
the baseline neural network trained for three epochs. Table 9 gives      the listing representation size in ADPM’s learned component. In
the complete configuration for these three compared models. In      Table 12 we see that removing the average pooled learned listing

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads

Table 12: Additional ablations studies. Offline metric lift in    A.3  Additional Sampling Biases Discussion
comparison to the baseline for the adSformer CTR.
                                                                     In addition to position debiasing, we are actively considering the
  Config                                       Test ROC AUC Lift   Test PR AUC Lift    practical implications of other selection biases, such as the condi-
  All Listing Pretrained + Listing Learned                +2.26%            +6.17%    tionality of our PCCVR prediction target on the CTR target. The
  All Listing Pretrained + No Listing Learned              +2.18%           +6.20%
                                                                   personalized PCCVR model predicts 𝑃(𝑦𝑃𝐶𝐶𝑉𝑅= 1|𝑦𝐶𝑇𝑅= 1,𝑥)
  adSformer Encoder 2 Heads                           +2.13%            +6.42%    effectively ignoring the sample space of non-clicked purchased
  adSformer Encoder 3 Heads                          +2.14%           +6.44%
                                                                    items in the personalized search ads space, the case of 𝑃(𝑦𝑃𝐶𝐶𝑉𝑅=
  Learned           Listing                  Size                    16                                                     +2.10%                                                                       +6.50%
  Learned           Listing                  Size                    32                                                     +2.14%                                                                       +6.44%  1|𝑦𝐶𝑇𝑅= 0,𝑥). In preliminary evaluations of potential explicit
  Learned Listing Size 64                               +2.04%            +6.14%   treatment for this selection bias, for example by using an inverse
  adSformer Encoder 0 Dropout                        +2.14%           +6.44%   propensity weighting in a multitask CTR-PCCVR formulation simi-
  adSformer Encoder 0.1 Dropout                      +2.10%           +6.34%    larly to [59], or the approach in [28], we determined that the metric
                                                           improvements do not sufficiently reward an increase in machine
                                                                     learning system complexity. We plan to revisit sampling biases in
Table 13: adSformer PCCVR hyperparameters and other al-      the future, possibly as part of a multitask learning paradigm.
gorithmic choices
    Config                       adSformer PCCVR            baseline NN       A.4  Additional Calibration Information
   Num Epochs                                 2                    2
    Learning Rate                              0.0001                 0.0001         After the uncalibrated model is trained, we use the raw logits as a
    Learning Rate Scheduler                    cosine                 cosine          feature to the calibration layer, which is a simple logistic regression
    Optimizer                        Adam          LazyAdam
   Adam 𝛽1                                           0.9                       0.9        model trained on the validation set reflecting the production data.
   Adam 𝛽2                                     0.999                   0.999        The calibration layer learns a single parameter 𝐴and bias term 𝐵,
   Adam 𝜖                                    1e-08                 1e-08                                                            and outputs 𝑃(𝑦= 1|𝑥) =          1                 . The calibration map-    Dropout Hidden Layers                        0.02                    0                                  1+exp(−(𝐴𝑓(𝑥)+𝐵))
    Batch Norm Hidden Layer                    yes                   yes         ping function is isotonic (monotonically increasing), preserving the
    Cross Module (DCN)                         yes                   yes           relative ordering of predictions. As a sanity-check, the evaluation
    Batch Size (train)                           500                  500
    Batch Size (validation)                       500                  500          metric, AUC, should be identical between the calibrated and un-
    Machine Type (training)                   P100                P100          calibrated models. We evaluate miscalibration by monitoring the
    Machine Type (evaluation)                 P100                T4         Expected Calibration Error (ECE) and Normalized Cross Entropy
    Loss                        BinaryCrossEntropy   BinaryCrossEntropy
   Num Parameters (trainable)            549,005,007            322,975,106         (NCE). ECE aims to measure the difference in expectation between
   Num Parameters (total)                 704,469,589            332,978,320         confidence and accuracy. We approximate the ECE by partitioning
    Training Dataset Size                  200M              135M                                                                      predictions into 𝑀equally-spaced bins and taking the weighted
                                                                 average of the bins’ 𝑎𝑐𝑐𝑢𝑟𝑎𝑐𝑦/𝑐𝑜𝑛𝑓𝑖𝑑𝑒𝑛𝑐𝑒difference.

Table 14: Performance metrics for the selected adSformer
CTR and PCCVR models vs NN baselines. Results extracted    A.5  Visual Representations Additional
from the daily training and evaluation jobs.                     Information
    Model             PR AUC  ROC AUC       Train time            A.5.1  Multitask Learning of Visual Representations. We saw best re-
     Baseline CTR NN        0.0411        0.719   14 hrs (1 P100))            sults by training a model on the following four datasets/classification
     Baseline PCCVR NN     0.0602        0.824    8 hrs (1 P100))           tasks: 1. listing images to top level taxonomy. 2. listing images to
                                                                           fine grained taxonomy. 3. listing images to seller-input primary
    adSformer CTR        +6.65%     +2.16%   11 hrs (1 A100)
                                                                                 color. 4. user-uploaded review photos to fine grained taxonomy. For    adSformer PCCVR    +12.70%     +1.81%    16hrs (1 P100)
                                                                   the top level taxonomy and primary color tasks we sampled 16K
                                                             images for a set of 15 labels each. For fine grained taxonomy we
                                                              sampled 200 images for a set of 1000 taxonomy nodes. We replaced
                                                                     the final convolutional layer of the EfficienetNetB0 backbone with
representation from ADPM in adSformer CTR leads to a drop in      a 256-dimension layer to output representations of the same size.
ROC AUC but an increase in PR AUC. We have a better idea of     The model was trained by first freezing the backbone and training
online to offline correlations between offline test ROC AUC and      only classification heads for one epoch using a 0.001 learning rate,
online CTR, so we select the increased ROC AUC model. Lowering     and then unfreezing the final 50 layers of the backbone and training
the size of the learned listing representations has a similar effect.      for an additional 8 epochs using the same learning rate. We used
The addition of one head to the adSformer encoder component of    Adam optimizer with values of 0.9, 0.999 and 1.0e-7 for beta1, beta2
ADPM increases both metrics and so does the removal of dropout.     and epsilon respectively.
  We performed similar ablation studies for the adSformer PCCVR
model and Table 13 depicts the final hyperparameter settings for       A.5.2   Ads Computer Vision: Visually Similar Ads Additional Infor-
the winning adSformer PCCVR.                                       mation. The listing-to-listing experience does not require real-time
   Finally, Table 14 presents one more set of the winning adSformer       predictions, so we implemented a daily batch inference pipeline
CTR and PCCVR offline performance results against production      to generate image representations for our entire listing inventory.
baseline NN.                                             Our pipeline first extracts the primary image for each Etsy listing,

Awad, Roberts, Dolev, and Heyman, et al.


                                                            Table 15: Online AIR A/B experiment results showing lift in
                                                   CTR.

                                                                                          fastText Dimension  CTR Lift

                                                                                   128d          +2.79%
                                                                                   256d          +2.88%


                                                 A.6  Multimodal Representations: Learning AIR
                                                       Additional Information
                                                                        In addition to parameterizing the ADPM module in adSformer CTR
                                                                         use-case, we use AIR representations to retrieve recommendation-
                                                                              style ads for listing-to-listing requests, across various types of pages
                                                          on both mobile and web. For example, the sash of sponsored recom-
                                                               mendations appearing at the bottom of the listing page is backed by
                                                         AIR representations. In listing-to-listing requests candidates are re-
                                                                          trieved using a query representation generated from the features of
Figure 12: Additional example of candidate retrieval using
                                                                     the viewed listing. Typically, we refer to the listing used to generate
multitask visual representations. Left column: query image
                                                                    the query representation as the source listing.
used. Right column: top-5 nearest neighbors retrieved
                                                                            A.6.1  Additional Training Details. Our final representation model
                                                      was trained using 30M of historical click pairs, from a look-back
                                                      window of 45 days. For training we used the Adam optimizer, with
                                                                  a learning rate, beta1, beta2, and epsilon values of 0.0001, 0.9, 0.999,
then passes those forward through the frozen multitask visual rep-     and 1e-7, respectively. We trained using a batch size of 4096, and
resentation model to generate representations. Representations for      sample 1500 negative labels to calculate the loss.
all listings are saved to a scalable key-value store. representations
                                                                          A.6.2  Evaluating AIR: Online Results. Online A/B experimentsare also filtered down by active ad campaigns. These candidate
                                                            were run against the control of neural IR representations extractedrepresentations are indexed into an Approximate Nearest Neighbor
                                                             from the listing tower of a model trained on search purchases (a less(ANN) inverted file (IVF) index. IVF approximates a nearest neigh-
                                                                        relevant objective for ads). Two treatments were tested to measurebor search by first splitting the representation space to N clusters,
                                                                     the effect of different dimensions of the input text representations,and at inference time only searching the K nearest clusters. Thus
                                                             128d and 256d, since the text representation lookup table makeswe can efficiently search the large space of representations.
                                                                          for the majority of trainable parameters in the overall AIR model.
                                                                   Table 15 show online CTR gains.
A.5.3   Ads Computer Vision: Search by Image. Another application
of the multitask visual representations was a brand new search
                                                 A.7  Text Representations Additionalby image shopping experience, built by the Etsy Ads team, and
available on the BOE app. Users can search using photos taken with         Information
their phone. We leverage the multitask dataset sampler to train on    Raw text inputs are first preprocessed to standardize casing and
an additional task to classify review photos to their corresponding      punctuation, mask stop-words and numbers, and remove extra-
listing’s taxonomy. Review photos are photos of purchased items     neous spaces and symbols. To reduce the size of the final lookup
taken “in the wild” by users. Our hypothesis is that these images       table we filter out tokens which have less than 10 occurrences. To
should serve as a proxy for user-taken query images.                 maintain relevance to the ad use case, we keep tokens which ap-
  The search by image experience requires generating the repre-     peared at least once in the last 30 days of ad interactions even if
sentation of the query image on the fly. To enable fast inference on      they occur less than 10 times in the data. The final lookup table
a large CNN such as the visual representations model, we partnered      contains roughly one million tokens.
with the ML platform team to deploy the representation model as      We trained the skip-gram word representations for five epochs.
the first GPU service in production at Etsy.                  We used a learning rate of 0.05, a context window of five, and a
   Similarly to the visually similar ads module, the candidate repre-    minimum and maximum character n-grams lengths of three and
sentations of the search by image retrieval system are pre-computed       six respectively. We trained using negative sampling with five sam-
by generating representations for primary listing images on a re-      pled negatives. We experimented with outputting both 128 and 256
curring basis. However, since we are serving ads as well as organic      dimension representations. We have found that the larger repre-
results, the ANN is indexed with the full inventory of nearly 100M      sentations perform slightly better in most downstream use cases.
active Etsy listings. At query time, the user-uploaded image is in-     However, the number of trainable parameters of the lookup table
ferenced on the GPU-backed model to compute the representation,     grows significantly with larger representations, and thus requires
which is used to search the ANN index for the most visually similar     more expensive infrastructure to fine tune during training of down-
listings.                                                         stream task, which we have seen in the adSformer CTR case.

adSformers: Personalization from Short-Term Sequences and Diversity of Representations in Etsy Ads


A.8  Skip-Gram Representations Additional           skip-gram representations learned with hierarchical softmax nearly
     Information                                                 perfectly captured the listing taxonomy attribute.
The objective of the model is to predict, given a listing 𝑙𝑖in the
corpus, the probability that another listing 𝑙𝑖+𝑗will be observed
within a fixed-length contextual window. The probability 𝑝(𝑙𝑖+𝑗|𝑙𝑖)
is defined mathematically according to the softmax formula

                            exp(vT𝑙𝑖v′𝑙𝑖+𝑗)
                    𝑝(𝑙𝑖+𝑗|𝑙𝑖) =                                  ,               (14)
                       Í|V|                               exp(vT𝑙𝑖v′𝑙𝑘)                             𝑘=1
  where vl and v′l are the input and output vector representations
of a listing𝑙, respectively, and V is the vocabulary of unique listings.
   In our training data, we use two months’ worth of user sessions,
and we upsample sessions that included a purchase at a rate of
5:1. We chose representation dimension 𝑑= 64 after observing
that higher dimensions tend to improve representation quality but
with diminishing returns and with trade offs in model training and
inference cost. We use a context window size of five. Interestingly,
increasing the window size had a positive impact for negative
sampling models but had mixed results for hierarchical softmax
models.
  As a gut check on representation quality and to better understand
what signals our representations were learning, we compared the
cosine similarity of groups of listings segmented by various listing      Figure 13: The skip-gram listing representation model nearly
attributions. For example, listings which are co-viewed in a session      perfectly encodes listing taxonomy.
are likely to belong to the same taxonomy node, so we would expect
listings with the same taxonomy to have a higher cosine similarity       To evaluate our representations, we ran batch data inference jobs
than those with different taxonomies. Figure 13 shows that our      with Apache Beam and Dataflow to compute the search ranking and
                                                                          attribute cosine similarity metrics, which we visualized in Colab
                                                                  notebooks.
