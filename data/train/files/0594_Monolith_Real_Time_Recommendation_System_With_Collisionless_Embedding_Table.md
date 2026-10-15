# Monolith: Real Time Recommendation System With Collisionless Embedding Table

Источник: https://arxiv.org/pdf/2209.07663.pdf

Monolith: Real Time Recommendation System With
                       Collisionless Embedding Table

                 Zhuoran Liu                     Leqi Zou                  Xuan Zou
                      Bytedance Inc.                      Bytedance Inc.                      Bytedance Inc.

                 Caihua Wang                   Biao Zhang                 Da Tang
                      Bytedance Inc.                      Bytedance Inc.                      Bytedance Inc.

                    Bolin Zhu∗                          Yijie Zhu                    Peng Wu
                   Fudan University                     Bytedance Inc.                      Bytedance Inc.

                              Ke Wang                  Youlong Cheng†2022                                 Bytedance Inc.                      Bytedance Inc.
Sep  ABSTRACT                                  ACMyoulong.cheng@bytedance.comReference Format:
           Building a scalable and real-time recommendation system is vital      Zhuoran Liu, Leqi Zou, Xuan Zou, Caihua Wang, Biao Zhang, Da Tang, Bolin
                                                                                Zhu, Yijie Zhu, Peng Wu, Ke Wang, and Youlong Cheng. 2022. Monolith:27    for many businesses driven by time-sensitive customer feedback,                                                                                       Real Time Recommendation System With Collisionless Embedding Table.
          such as short-videos ranking or online ads. Despite the ubiquitous
                                                                                          In Proceedings of 5th Workshop on Online Recommender Systems and User
          adoption of production-scale deep learning frameworks like Ten-                                                                                       Modeling, in conjunction with the 16th ACM Conference on Recommender
          sorFlow or PyTorch, these general-purpose frameworks fall short       Systems (ORSUM@ACM RecSys 2022). ACM, New York, NY, USA, 10 pages.
            of business demands in recommendation scenarios for various rea-      https://doi.org/XXXXXXX.XXXXXXX
            sons: on one hand, tweaking systems based on static parameters and[cs.IR]    dense computations for recommendation with dynamic and sparse
           features is detrimental to model quality; on the other hand, such    1  INTRODUCTION
          frameworks are designed with batch-training stage and serving                                                                  The past decade witnessed a boom of businesses powered by recom-
           stage completely separated, preventing the model from interacting                                                                      mendation techniques. In pursuit of a better customer experience,
          with customer feedback in real-time. These issues led us to reex-                                                                                     delivering personalized content for each individual user as real-time
          amine traditional approaches and explore radically different design                                                                           response is a common goal of these business applications. To this
            choices. In this paper, we present Monolith1, a system tailored                                                                              end, information from a user’s latest interaction is often used as
            for online training. Our design has been driven by observations                                                                             the primary input for training a model, as it would best depict a
            of our application workloads and production environment that re-                                                                                    user’s portrait and make predictions of user’s interest and future
             flects a marked departure from other recommendations systems.                                                                                  behaviors.
         Our contributions are manifold: first, we crafted a collisionless em-                                                                  Deep learning have been dominating recommendation models
          bedding table with optimizations such as expirable embeddings                                                                                                    [5, 6, 10, 12, 20, 21] as the gigantic amount of user data is a natural
          and frequency filtering to reduce its memory footprint; second, we                                                                                                                   fit for massively data-driven neural models. However, efforts to
           provide an production-ready online training architecture with high                                                                               leverage the power of deep learning in industry-level recommen-
            fault-tolerance; finally, we proved that system reliability could be                                                                               dation systems are constantly encountered with problems arising
            traded-off for real-time learning. Monolith has successfully landed                                                                    from the unique characteristics of data derived from real-worldarXiv:2209.07663v2    in the BytePlus Recommend2 product.                                user behavior. These data are drastically different from those used
                                                                                     in conventional deep learning problems like language modeling or
            ∗Work done during internship at Bytedance Inc.
                                                                      computer vision in two aspects:
             †Corresponding author.
            1Code to be released soon.                                                               (1) The features are mostly sparse, categorical and dynamically
             2https://www.byteplus.com/en/product/recommend
                                                                                   changing;
                                                                                                    (2) The underlying distribution of training data is non-stationary,
             Permission to make digital or hard copies of all or part of this work for personal or
              classroom use is granted without fee provided that copies are not made or distributed                a.k.a. Concept Drift [8].
                for profit or commercial advantage and that copies bear this notice and the full citation
            on the first page. Copyrights for components of this work owned by others than ACM       Such differences have posed unique challenges to researchers
            must be honored. Abstracting with credit is permitted. To copy otherwise, or republish,     and engineers working on recommendation systems.
               to post on servers or to redistribute to lists, requires prior specific permission and/or a
                 fee. Request permissions from permissions@acm.org.
         ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA                 1.1  Sparsity and Dynamism
         © 2022 Association for Computing Machinery.
         ACM ISBN 978-1-4503-XXXX-X/18/06...$15.00                           The data for recommendation mostly contain sparse categorical
            https://doi.org/XXXXXXX.XXXXXXX                                             features, some of which appear with low frequency. The common

ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA                            Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong



                                          Training                                                                                             Model          Data                         Data                                                                         Training PS      Serving PS                                                                                                                         User           (Batch                  Training)       (Online                                         Training)                                      Worker                                                                                                             Server

                            Historical batch data                                                                                                        Batch
                                                                     Feature IDs                                                                             Training
                                                                                                                                                  Stage
                                                                   Embedding table
                                                                          lookup
                                                                 Feature embeddings

                                 Model forward
                                 and backward pass
                                                               Feature IDs and gradients

                                                                          Apply gradient
                                                                            updates

                                     Online streaming                                           Parameter                                                    Online
                                           data                                                  Sync                                                      Training
                                                                     Feature IDs                                                       User Request                Stage
                                                                  Embedding table                         Feature IDs
                                                                         lookup
                                                                 Feature embeddings               Embedding
                                                                                                               table lookup                                                                                                                       Feature
                                Model forward                                                           embeddings
                                and backward pass                                            Sync
                                                               Feature IDs and gradients             interval                 Model
                                                                                                                      forward
                                                                               Apply                                 pass        Ranking Result
                                                                                      gradient
                                       Data of                                  updates                                            User Actions                                          features and
                                       user reactions

                                                                                            Parameter
                                                                                             Sync





                                   Figure 1: Monolith Online Training Architecture.


practice of mapping them to a high-dimensional embedding space     1.2  Non-stationary Distribution
would give rise to a series of issues:                                  Visual and linguistic patterns barely develop in a time scale of
                                                                         centuries, while the same user interested in one topic could shift
    • Unlike language models where number of word-pieces are       their zeal every next minute. As a result, the underlying distribution
       limited, the amount of users and ranking items are orders of       of user data is non-stationary, a phenomenon commonly referred
      magnitude larger. Such an enormous embedding table would       to as Concept Drift [8].
      hardly fit into single host memory;                                    Intuitively, information from a more recent history can more
    • Worse still, the size of embedding table is expected to grow       effectively contribute to predicting the change in a user’s behavior.
      over time as more users and items are admitted, while frame-     To mitigate the effect of Concept Drift, serving models need to be
     works like [1, 17] uses a fixed-size dense variables to repre-     updated from new user feedback as close to real-time as possible to
       sent embedding table.                                                 reflect the latest interest of a user.

                                                                       In light of these distinction and in observation of issues that arises   In practice, many systems adopt low-collision hashing [3, 6] as a
                                                            from our production, we designed Monolith, a large-scale recom-way to reduce memory footprint and to allow growing of IDs. This
                                                            mendation system to address these pain-points. We did extensiverelies on an over-idealistic assumption that IDs in the embedding
                                                               experiments to verify and iterate our design in the productiontable is distributed evenly in frequency, and collisions are harmless
                                                                 environment. Monolith is able toto the model quality. Unfortunately this is rarely true for a real-
world recommendation system, where a small group of users or           (1) Provide full expressive power for sparse features by design-
items have significantly more occurrences. With the organic growth             ing a collisionless hash table and a dynamic feature eviction
of embedding table size, chances of hash key collision increases           mechanism;
and lead to deterioration of model quality [3].                                  (2) Loop serving feedback back to training in real-time with
   Therefore it is a natural demand for production-scale recommen-            online training.
dation systems to have the capacity to capture as many features in       Empowered by these architectural capacities, Monolith consis-
its parameters, and also have the capability of elastically adjusting       tently outperforms systems that adopts hash-tricks with collisions
the number of users and items it tries to book-keep.                  with roughly similar memory usage, and achieves state-of-the-art

Monolith: Real Time Recommendation System With Collisionless Embedding Table             ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA


online serving AUC without overly burdening our servers’ compu-      operations for sparse parameters. As an complement to Tensor-
tation power.                                                     Flow’s limitation that arises from separation of training and in-
  The rest of the paper is organized as follows. We first elaborate       ference, Monolith’s elastically scalable online training is designed
design details of how Monolith tackles existing challenge with colli-      to efficiently synchronize parameters from training-PS to online
sionless hash table and realtime training in Section 2. Experiments      serving-PS within short intervals, with model robustness guarantee
and results will be presented in Section 3, along with production-      provided by fault tolerance mechanism.
tested conclusions and some discussion of trade-offs between time-
sensitivity, reliability and model quality. Section 4 summarizes re-     2.1  Hash Table
lated work and compares them with Monolith. Section 5 concludes    A first principle in our design of sparse parameter representation
this work.                                                                             is to avoid cramping information from different IDs into the same
                                                                            fixed-size embedding. Simulating a dynamic size embedding table
                                                               with an out-of-the-box TensorFlow Variable inevitably leads to ID
                                                                               collision, which exacerbates as new IDs arrive and table grows.
                                               Worker             Worker           . . .                                                                 Therefore instead of building upon Variable, we developed a new
                                                                  key-value HashTable for our sparse parameters.
           Client            Master                                       Our HashTable utilizes Cuckoo Hashmap [16] under the hood,
                                                           which supports inserting new keys without colliding with existing
                                                 Parameter           Parameter          . . .        ones. Cuckoo Hashing achieves worst-case 𝑂(1) time complexity
                                                       Server                Server                    for lookups and deletions, and an expected amortized 𝑂(1) time for
                                                                           insertions. As illustrated in Figure 3 it maintains two tables 𝑇0,𝑇1
                                                              with different hash functions ℎ0(𝑥),ℎ1(𝑥), and an element would
                                                              be stored in either one of them. When trying to insert an element
            Figure 2: Worker-PS Architecture.                 𝐴into 𝑇0, it first attempts to place 𝐴at ℎ0(𝐴); If ℎ0(𝐴) is occupied
                                                           by another element 𝐵, it would evict 𝐵from 𝑇0 and try inserting 𝐵
                                                                        into 𝑇1 with the same logic. This process will be repeated until all
                                                               elements stabilize, or rehash happens when insertion runs into a
2  DESIGN                                                             cycle.
The overall architecture of Monolith generally follows TensorFlow’s       Memory footprint reduction is also an important consideration
distributed Worker-ParameterServer setting (Figure 2). In a Worker-      in our design. A naive approach of inserting every new ID into
PS architecture, machines are assigned different roles; Worker ma-      the HashTable will deplete memory quickly. Observation of real
chines are responsible for performing computations as defined by      production models lead to two conclusions:
the graph, and PS machines stores parameters and updates them           (1) IDs that appears only a handful of times have limited con-
according to gradients computed by Workers.                                 tribution to improving model quality. An important obser-
   In recommendation models, parameters are categorized into two            vation is that IDs are long-tail distributed, where popular
sets: dense and sparse. Dense parameters are weights/variables in           IDs may occur millions of times while the unpopular ones
a deep neural network, and sparse parameters refer to embedding            appear no more than ten times. Embeddings corresponding
tables that corresponds to sparse features. In our design, both dense             to these infrequent IDs are underfit due to lack of training
and sparse parameters are part of TensorFlow Graph, and are stored            data and the model will not be able to make a good estima-
on parameter servers.                                                         tion based on them. At the end of the day these IDs are not
   Similar to TensorFlow’s Variable for dense parameters, we de-              likely to affect the result, so model quality will not suffer
signed a set of highly-efficient, collisionless, and flexible HashTable           from removal of these IDs with low occurrences;
                                                                                       (2) Stale IDs from a distant history seldom contribute to the
                                                                             current model as many of them are never visited. This could
                                                                           possibly due to a user that is no longer active, or a short-
                     A                                                    video that is out-of-date. Storing embeddings for these IDs
                                  h0(A)                                                   could not help model in any way but to drain our PS memory
                                                                               in vain.
                     B A                D C          G      T0             Based on these observation, we designed several feature ID fil-
                                                                       tering heuristics for a more memory-efficient implementation of
                                       h1(D)              h1(B)          h0(C)                      HashTable:
                                                                                       (1) IDs are filtered before they are admitted into embedding
            D                E        F           C B           T1                     tables. We have two filtering methods: First we filter by
                                                                                     their occurrences before they are inserted as keys, where the
                                                                          threshold of occurrences is a tunable hyperparameter that
                                                                               varies for each model; In addition we utilize a probabilistic
               Figure 3: Cuckoo HashMap.                                      filter which helps further reduce memory usage;

ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA                            Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong





                                Actions
          User                           Log Kafka                                        Training Example           Dump Batch Data
                                  (Click, Like,                                                              Kafka
                             Convert …)



                                                                         Joiner                          Online                       Batch Training Data
                                                                      Flink Job                        Training                       HDFS




                                                                                                                                 Batch Training
                              Generate
                                Features
      Model Server                         Feature Kafka                                        Training Worker





                                                  Parameter Synchronization
        Serving PS                                                                                 Training PS


                                             Figure 4: Streaming Engine.
The information feedback loop from [User →Model Server →Training Worker →Model Server →User] would spend a long time when taking the Batch Training
                                              path, while the Online Training will close the loop more instantly.


   (2) IDs are timed and set to expire after being inactive for a       2.2.1  Streaming Engine. Monolith is built with the capability of
      predefined period of time. The expire time is also tunable for      seamlessly switching between batch training and online training.
      each embedding table to allow for distinguishing features      This is enabled by our design of streaming engine as illustrated by
      with different sensitivity to historical information.              Figure 4.
                                                                          In our design, we use one Kafka [13] queue to log actions of users   In our implementation, HashTable is implemented as a Tensor-
                                                                                    (E.g. Click on an item or like an item etc.) and another Kafka queueFlow resource operation. Similar to Variable, look-ups and updates
                                                                            for features. At the core of the engine is a Flink [4] streaming job forare also implemented as native TensorFlow operations for easier
                                                                     online feature Joiner. The online joiner concatenates features withintegration and better compatibility.
                                                                              labels from user actions and produces training examples, which are
                                                                then written to a Kafka queue. The queue for training examples is
2.2  Online Training
                                                         consumed by both online training and batch training:
In Monolith, training is divided into two stages (Figure 1):
                                                               • For online training, the training worker directly reads data
   (1) Batch training stage. This stage works as an ordinary Tensor-
                                                                 from the Kafka queue;
     Flow training loop: In each training step, a training worker
                                                               • For batch training, a data dumping job will first dump data
      reads one mini-batch of training examples from the stor-
                                                                             to HDFS [18]; After data in HDFS accumulated to certain
       age, requests parameters from PS, computes a forward and
                                                                  amount, training worker will retrieve data from HDFS and
      a backward pass, and finally push updated parameters to
                                                                    perform batch training.
      the training PS. Slightly different from other common deep
       learning tasks, we only train our dataset for one pass. Batch                                                           Updated parameters in training PS will be pushed to serving PS
       training is useful for training historical data when we modify                                                                  according to the parameter synchronization schedule.
      our model architecture and retrain the model;
   (2) Online training stage. After a model is deployed to online                                                                                 2.2.2  Online Joiner. In real-world applications, user actions log
       serving, the training does not stop but enters the online train-                                                           and features are streamed into the online joiner (Figure 5) without
      ing stage. Instead of reading mini-batch examples from the                                                                guarantee in time order. Therefore we use a unique key for each
       storage, a training worker consumes realtime data on-the-fly                                                                     request so that user action and features could correctly pair up.
      and updates the training PS. The training PS periodically syn-                                                         The lag of user action could also be a problem. For example, a
      chronizes its parameters to the serving PS, which will take                                                                  user may take a few days before they decide to buy an item they
       effect on the user side immediately. This enables our model                                                            were presented days ago. This is a challenge for the joiner because
       to interactively adapt itself according to a user’s feedback in                                                                                                      if all features are kept in cache, it would simply not fit in memory.
       realtime.                                                                     In our system, an on-disk key-value storage is utilized to store
                                                                         features that are waiting for over certain time period. When a user
                                                                      action log arrives, it first looks up the in-memory cache, and then
                                                                    looks up the key-value storage in case of a missing cache.

Monolith: Real Time Recommendation System With Collisionless Embedding Table             ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA



       Log Kafka                          Feature Kafka
      (User Actions)





                       In-memory                                                                                                  Negative                  Training Example                                                                             Join
                            Cache                                                          Sampling                      Kafka


                                                Found in Cache





                           On-disk
                          KV-Store

                                                 Read from KV-Store



                                               Figure 5: Online Joiner.


  Another problem that arise in real-world application is that           (1) Sparse parameters are dominating the size of recommenda-
the distribution of negative and positive examples are highly un-             tion models;
even, where number of the former could be magnitudes of order           (2) Given a short range of time window, only a small subset of
higher than the latter. To prevent positive examples from being            IDs gets trained and their embeddings updated;
overwhelmed by negative ones, a common strategy is to do negative           (3) Dense variables move much slower than sparse embeddings.
sampling. This would certainly change the underlying distribution            This is because in momentum-based optimizers, the accumu-
of the trained model, tweaking it towards higher probability of              lation of momentum for dense variables is magnified by the
making positive predictions. As a remedy, we apply log odds cor-            gigantic size of recommendation training data, while only
rection [19] during serving, making sure that the online model is            a few sparse embeddings receives updates in a single data
an unbiased estimator of the original distribution.                             batch.

2.2.3  Parameter Synchronization. During online training, the Mono-      (1) and (2) allows us to exploit the sparse updates across all feature
lith training cluster keeps receiving data from the online serving       IDs. In Monolith, we maintain a hash set of touched keys, repre-
module and updates parameters on the training PS. A crucial step      senting IDs whose embeddings get trained since the last parameter
to enable the online serving PS to benefit from these newly trained      synchronization. We push the subset of sparse parameters whose
parameters is the synchronization of updated model parameters. In      keys are in the touched-keys set with a minute-level time interval
production environment, we are encountered by several challenges:     from the training PS to the online serving PS. This relatively small
                                                             pack of incremental parameter update is lightweight for network
    • Models on the online serving PS must not stop serving when
                                                                   transmission and will not cause a sharp memory spike during the
      updating. Our models in production is usually several ter-
                                                                     synchronization.
      abytes in size, and as a result replacing all parameters takes a
                                              We also exploit (3) to further reduce network I/O and memory
       while. It would be intolerable to stop an online PS from serv-
                                                              usage by setting a more aggressive sync schedule for sparse pa-
      ing the model during the replacement process, and updates
                                                                    rameters, while updating dense parameters less frequently. This
     must be made on-the-fly;
                                                                   could render us a situation where the dense parameters we serve is
    • Transferring a multi-terabyte model of its entirety from train-
                                                                a relatively stale version compared to sparse part. However, such
      ing PS to the online serving PS would pose huge pressure
                                                                      inconsistency could be tolerated due to the reason mentioned in (3)
       to both the network bandwidth and memory on PS, since it
                                                                      as no conspicuous loss has been observed.
       requires doubled model size of memory to accept the newly
       arriving model.
  For the online training to scale up to the size of our business     2.3  Fault Tolerance
scenario, we designed an incremental on-the-fly periodic parameter     As a system in production, Monolith is designed with the ability to
synchronization mechanism in Monolith based on several notice-      recover a PS in case it fails. A common choice for fault tolerance is
able characteristic of our models:                                       to snapshot the state of a model periodically, and recover from the

ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA                            Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong

latest snapshot when PS failure is detected. The choice of snapshot            by treating scores ≥3.5 as positive samples and the rest
frequency has two major impacts:                                              as negative samples.
                                                                 • Model and metrics. We implemented a standard DeepFM    (1) Model quality. Intuitively, model quality suffers less from
       loss of recent history with increased snapshot frequency.                   [9] model, a commonly used model architecture for recom-
    (2) Computation overhead. Snapshotting a multi-terabyte model             mendation problems. It consist of an FM component and a
        is not free. It incurs large chunks of memory copy and disk              dense component (Figure 6). Predictions are evaluated by
       I/O.                                            AUC [2] as this is the major measurement for real models.
                                                                 • Embedding collisions. This dataset contains approximately
  As a trade-off between model quality and computation overhead,
                                                                160K user IDs and 60K movie IDs. To compare with the
Monolith snapshots all training PS every day. Though a PS will lose
                                                                                       collisionless version of embedding table implementation,
one day’s worth of update in case of a failure, we discover that the
                                                         we performed another group of experiment where IDs are
performance degradation is tolerable through our experiments. We
                                                                         preprocessed with MD5 hashing and then mapped to a
will analyze the effect of PS reliability in the next section.
                                                                            smaller ID space. As a result, some IDs will share their
                                                                 embedding with others. Table 1 shows detailed statistics
                                                      Output                                             of user and movie IDs before and after hashing.



                                                                            MLP
                    FM                                                                   User IDs  Movie IDs
                                 . . .                                                # Before Hashing     162541       59047
                                                                          # After Hashing     149970       57361
                                                                                      Collision rate      7.73%      2.86%

     Embeddings                                                       Table 1: Statistics of IDs Before and After Hashing.
          IDs                                                   . . .


                                                                                       (2) Internal Recommendation dataset.
          Figure 6: DeepFM model architecture.
                                                  We also performed experiments on a recommendation model
                                                                               in production environment. This model generally follows a
                                                                       multi-tower architecture, with each tower responsible for
3  EVALUATION                                                     learning to predict a specialized kind of user behavior.
                                                                 • Each model has around 1000 embedding tables, and distri-For a better understanding of benefits and trade-offs brought about
                                                                           bution of size of embedding tables are very uneven;by our proposed design, we conducted several experiments at pro-
                                                                 • The original ID space of embedding table was 248. In ourduction scale and A/B test with live serving traffic to evaluate and
                                                                                   baseline, we applied a hashing trick by decomposing toverify Monolith from different aspects. We aim to answer the fol-
                                                                         curb the size of embedding table. To be more specific, welowing questions by our experiments:
                                                                       use two smaller embedding tables instead of a gigantic
    (1) How much can we benefit from a collisionless HashTable?                                                                    one to generate a unique embedding for each ID by vector
    (2) How important is realtime online training?
                                                                          combination:
    (3) Is Monolith’s design of parameter synchronization robust
     enough in a large-scale production scenario?                               𝐼𝐷𝑟= 𝐼𝐷% 224
   In this section, we first present our experimental settings and                     𝐼𝐷𝑞= 𝐼𝐷÷ 224
then discuss results and our findings in detail.                              𝐸= 𝐸𝑟+ 𝐸𝑞,
                                                                where 𝐸𝑟, 𝐸𝑞are embeddings corresponding to 𝐼𝐷𝑟, 𝐼𝐷𝑞.
3.1  Experimental Setup
                                                                        This effectively reduces embedding table sizes from 248
3.1.1  Embedding Table. As described in Section 2.1, embedding                                                                                 to 225;
tables in Monolith are implemented as collisionless HashTables.                                                                 • This model is serving in real production, and the perfor-
To prove the necessity of avoiding collisions in embedding tables                                                                mance of this experiment is measured by online AUC with
and to quantify gains from our collisionless implementation, we                                                                                       real serving traffic.
performed two groups of experiments on the Movielens dataset
and on our internal production dataset respectively:                       3.1.2  Online Training. During online training, we update our on-
    (1) MovieLens ml-25m dataset [11]. This is a standard public       line serving PS with the latest set of parameters with minute-level
       dataset for movie ratings, containing 25 million ratings that       intervals. We designed two groups of experiments to verify model
      involves approximately 162000 users and 62000 movies.         quality and system robustness.
      • Preprocessing of labels. The original labels are ratings from           (1) Update frequency. To investigate the necessity of minute-
         0.5 to 5.0, while in production our tasks are mostly re-              level update frequency, we conducted experiments that syn-
         ceiving binary signals from users. To better simulate our            chronize parameters from training model to prediction model
        production models, we convert scale labels to binary labels           with different intervals.

Monolith: Real Time Recommendation System With Collisionless Embedding Table             ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA



Algorithm 1 Simulated Online Training.
   1: Input: 𝐷𝑏𝑎𝑡𝑐ℎ;                                                                   /* Data for batch training. */
                                                           /* Data for online training, split into 𝑁shards.  */   2: Input: 𝐷𝑜𝑛𝑙𝑖𝑛𝑒𝑖=1···𝑁;
   3: 𝜃𝑡𝑟𝑎𝑖𝑛←𝑇𝑟𝑎𝑖𝑛(𝐷𝑏𝑎𝑡𝑐ℎ,𝜃𝑡𝑟𝑎𝑖𝑛) ;                                                              /* Batch training. */
   /* Online training.                                                                                        */
   4: for 𝑖= 1 · · · 𝑁do
   5:   𝜃𝑠𝑒𝑟𝑣𝑒←𝜃𝑡𝑟𝑎𝑖𝑛;                                              /* Sync training parameters to serving model. */
   6:  𝐴𝑈𝐶𝑖= Evaluate(𝜃𝑠𝑒𝑟𝑣𝑒, 𝐷𝑜𝑛𝑙𝑖𝑛𝑒𝑖      ) ;                                 /* Evaluate online prediction on new data. */
   7:   𝜃𝑡𝑟𝑎𝑖𝑛←𝑇𝑟𝑎𝑖𝑛(𝐷𝑜𝑛𝑙𝑖𝑛𝑒𝑖     ,𝜃𝑡𝑟𝑎𝑖𝑛) ;                                                      /* Train with new data. */
   8: end for


     The dataset we use is the Criteo Display Ads Challenge
       dataset3, a large-scale standard dataset for benchmarking
    CTR models. It contains 7 days of chronologically ordered                              collision-free hash
                                                                                          0.825       hash w/ collision      data recording features and click actions. For this experiment,
     we use a standard DeepFM [9] model as described in 6.
     To simulate online training, we did the following preprocess-           0.820
      ing for the dataset. We take 7 days of data from the dataset,
      and split it to two parts: 5 days of data for batch training, and                                                                                        auc
      2 days for online training. We further split the 2 days of data            0.815                                                                                                                     test
       into 𝑁shards chronologically. Online training is simulated
     by algorithm 1.
                                                                                          0.810     As such, we simulate synchronizing trained parameters to
       online serving PS with an interval determined by number of
      data shards. We experimented with 𝑁= 10, 50, 100, which                                                                                          0.805
      roughly correspond to update interval of 5ℎ𝑟, 1ℎ𝑟, and 30𝑚𝑖𝑛.
    (2) Live experiment. In addition, we also performed a live ex-                  1     2     3     4     5     6     7     8     9    10
                                                                                                                     epoch      periment with real serving traffic to further demonstrate the
      importance of online training in real-world application. This
     A/B experiment compares online training to batch training          Figure 7: Effect of Embedding Collision On DeepFM,
      one one of our Ads model in production.                                        MovieLens


3.2  Results and Analysis
                                                                                          0.790       hash w/ collision
3.2.1  The Effect of Embedding Collision. Results from MovieLens                              collisionless hash table
dataset and the Internal recommedation dataset both show that
embedding collisions will jeopardize model quality.                                                                                          0.785
    (1) Models with collisionless HashTable consistently outper-        AUC
      forms those with collision. This conclusion holds true re-
       gardless of                                                                                                                                                            serving 0.780
      •         Increase                  of number                             of training                                     epochs. As shown                                                          in                                                         Figure                 Online           7,           the model                   with collisionless                                embedding                                                     table has                                                        higher
                                                                                          0.775     AUC from the first epoch and converges at higher value;
      • Change of distribution with passage of time due to Con-
        cept Drift. As shown in Figure 8, models with collision-
                                                                                          0.770
          less embedding table is also robust as time passes by and
         users/items context changes.                                                     2        4        6        8        10       12
                                                                                                             Day
    (2) Data sparsity caused by collisionless embedding table will
      not lead to model overfitting. As shown in Figure 7, a model
      with collisionless embedding table does not overfit after it             Figure 8: Effect of Embedding Collision On A
      converges.                                                Recommendation Model In Production
                                                      We measure performance of this recommendation model by online serving AUC,
                                                                     which is fluctuating across different days due to concept-drift.

3https://www.kaggle.com/competitions/criteo-display-ad-challenge/data

ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA                            Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong




                                                      w/ online training                                                                 w/ online training                                                                                  0.8075                                                     w/o online training                                                              w/o online training
    0.798                                                                         0.8050

                                                                                  0.8025
    0.796                                                                                  0.8000
 AUC                                                                             AUC
                                                                                  0.7975
    0.794
                                                                                  0.7950

                                                                                  0.7925
    0.792
                                                                                  0.7900

          0         10         20         30         40         50                 0         10         20         30         40         50
                                      Hours                                                                          Hours

                (a) Online training with 5 hrs sync interval                                (b) Online training with 1 hr sync interval


                                            0.810                                             w/ online training
                                                                                            w/o online training

                                            0.805


                                            0.800
                                         AUC

                                            0.795


                                            0.790


                                              0         10         20         30         40         50
                                                                             Hours

                                                            (c) Online training with 30 min sync interval


                              Figure 9: Online training v.s. Batch training on Criteo dataset.
                Blue lines: AUC of models with online training; Yellow lines: AUC of batch training models evaluated against streaming data.


3.2.2  Online Training: Trading-offReliability For Realtime. We dis-           • Models with smaller parameter synchronization interval
covered that a higher parameter synchronization frequency is al-             performs better that those with larger interval. Figure 10
ways conducive to improving online serving AUC, and that online             and Table 2 compares online serving AUC for models with
serving models are more tolerant with loss of a few shard of PS              sync interval of 5ℎ𝑟, 1ℎ𝑟, and 30𝑚𝑖𝑛respectively.
than we expect.
    (1) The Effect of Parameter Synchronization Frequency.       Sync Interval  Average AUC (online)  Average AUC (batch)
       In our online streaming training experiment (1) with Criteo
                                                                     5 hr            79.66 ± 0.020           79.42 ± 0.026      Display Ads Challenge dataset, model quality consistently
                                                                     1 hr            79.78 ± 0.005           79.44 ± 0.030      improves with the increase of parameter synchronization
                                                                    30 min          79.80 ± 0.008           79.43 ± 0.025      frequency, as is evident by comparison from two perspec-
        tives:                                                             Table 2: Average AUC comparison for DeepFM model on
      • Models with online training performs better than models                                                                                   Criteo dataset.
         without. Figure 9a, 9b, 9c compares AUC of online training
       models evaluated by the following shard of data versus
        batch training models evaluated by each shard of data;

Monolith: Real Time Recommendation System With Collisionless Embedding Table             ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA


                               Day     1       2       3       4       5       6       7

               AUC Improvement %   14.443   16.871   17.068   14.028   18.081   16.404   15.202

        Table 3: Improvement of Online Training Over Batch Training from Live A/B Experiment on an Ads Model.



                                                               model quality. We also did quite some exploration in this
                                                                           regard and to our surprise, model quality is more robust than
    0.810                                          Sync Interval 5 hr                   expected. With a 0.01% failure rate of PS machine per day,
                                                  Sync Interval 1 hr              we find a model from the previous day works embarrassingly
                                                  Sync Interval 30 min
                                                                                     well. This is explicable by the following calculation: Suppose
    0.805                                                                      a model’s parameters are sharded across 1000 PS, and they
                                                                     snapshot every day. Given 0.01% failure rate, one of them
    0.800                                                                           will go down every 10 days and we lose all updates on this
 AUC                                                           PS for 1 day. Assuming a DAU of 15 Million and an even
                                                                                  distribution of user IDs on each PS, we lose 1 day’s feedback
    0.795                                                                 from 15000 users every 10 days. This is acceptable because
                                                                                           (a) For sparse features which is user-specific, this is equiv-
    0.790                                                                       alent to losing a tiny fraction of 0.01% DAU; (b) For dense
                                                                                   variables, since they are updated slowly as we discussed in
                                                                                              2.2.3, losing 1 day’s update out of 1000 PS is negligible.
          0         10         20         30         40         50              Based on the above observation and calculation, we radically
                                      Hours                                    lowered our snapshot frequency and thereby saved quite a
                                                                                         bit in computation overhead.
   Figure 10: Comparison of different sync intervals for
                    online training.



     The live A/B experiment between online training and batch
       training on an Ads model in production also show that there    4  RELATED WORK
        is a significant bump in online serving AUC (Table 3).          Ever since some earliest successful application of deep learning to
       Inspired by this observation, we synchronize sparse parame-      industry-level recommendation systems [6, 10], researchers and
       ters to serving PS of our production models as frequent as      engineers have been employing various techniques to ameliorate
      possible (currently at minute-level), to the extent that the       issues mentioned in Section 1.
      computation overhead and system reliability could endure.       To tackle the issue of sparse feature representation, [3, 6] uses
       Recall that dense variables requires a less frequent update as       fixed-size embedding table with hash-trick. There are also attempts
      discussed in 2.2.3, we update them at day-level. By doing so,      in improving hashing to reduce collision [3, 7]. Other works directly
     we can bring down our computation overhead to a very low       utilize native key-value hash table to allow dynamic growth of table
        level. Suppose 100,000 IDs gets updated in a minute, and the       size [12, 15, 20, 21]. These implementations builds upon TensorFlow
      dimension of embedding is 1024, the total size of data need      but relies either on specially designed software mechanism [14,
       to be transferred is 4𝐾𝐵× 100, 000 ≈400𝑀𝐵per minute.      15, 20] or hardware [21] to access and manage their hash-tables.
      For dense parameters, since they are synchronized daily, we     Compared to these solutions, Monolith’s hash-table is yet another
      choose to schedule the synchronization when the traffic is      native TensorFlow operation. It is developer friendly and has higher
      lowest (e.g. midnight).                                          cross-platform interoperability, which is suitable for ToB scenarios.
   (2) The Effect of PS reliability.                       An organic and tight integration with TensorFlow also enables
     With a minute-level parameter synchronization, we initially       easier optimizations of computation performance.
      expect a more frequent snapshot of training PS to match the        Bridging the gap between training and serving and alleviation
      realtime update. To our surprise, we enlarged the snapshot       of Concept Drift [8] is another topic of interest. To support online
       interval to 1 day and still observed nearly no loss of model      update and avoid memory issues, both [12] and [20] designed fea-
       quality.                                                         ture eviction mechanisms to flexibly adjust the size of embedding
      Finding the right trade-off between model quality and com-       tables. Both [12] and [14] support some form of online training,
      putation overhead is difficult for personalized ranking sys-     where learned parameters are synced to serving with a relatively
      tems since users are extremely sensitive on recommendation      short interval compared to traditional batch training, with fault tol-
       quality. Traditionally, large-scale systems tend to set a fre-      erance mechanisms. Monolith took similar approach to elastically
      quent snapshot schedule for their models, which sacrifices      admit and evict features, while it has a more lightweight parameter
      computation resources in exchange for minimized loss in      synchronization mechanism to guarantee model quality.

ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA                            Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong

5  CONCLUSION                                                   XDL: an industrial deep learning framework for high-dimensional sparse data.
                                                                                                Proceedings of the 1st International Workshop on Deep Learning Practice for High-
In this work, we reviewed several most important challenges for            Dimensional Sparse Data (2019).
industrial-level recommendation systems and present our system        [13] Jay Kreps. 2011. Kafka : a Distributed Messaging System for Log Processing.
in production, Monolith, to address them and achieved best perfor-        [14] Xiangru Lian, Binhang Yuan, Xuefeng Zhu, Yulong Wang, Yongjun He, Honghuan
                                                                      Wu, Lei Sun, Haodong Lyu, Chengjun Liu, Xing Dong, Yiqiao Liao, Mingnan
mance compared to existing solutions.                                            Luo, Congfei Zhang, Jingru Xie, Haonan Li, Lei Chen, Renjie Huang, Jianying
  We proved that a collisionless embedding table is essential for              Lin, Chengchun Shu, Xue-Bo Qiu, Zhishan Liu, Dongying Kong, Lei Yuan, Hai
                                                                              bo Yu, Sen Yang, Ce Zhang, and Ji Liu. 2021. Persia: An Open, Hybrid System
model quality, and demonstrated that our implementation of Cuckoo             Scaling Deep Learning-based Recommenders up to 100 Trillion Parameters. ArXiv
HashMap based embedding table is both memory efficient and help-             abs/2111.05897 (2021).
ful for improving online serving metrics.                                        [15] Meituan. 2021. Distributed Training Optimization for TensorFlow in Recom-
                                                                            mender Systems (in Chinese).  https://tech.meituan.com/2021/12/09/meituan-
  We also proved that realtime serving is crucial in recommenda-            tensorflow-in-recommender-systems.html
tion systems, and that parameter synchronization interval should        [16] R. Pagh and Flemming Friche Rodler. 2001. Cuckoo Hashing. In ESA.
be as short as possible for an ultimate model performance. Our        [17] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory
                                                                                 Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban
solution for online realtime serving in Monolith has a delicately            Desmaison, Andreas Köpf, Edward Yang, Zach DeVito, Martin Raison, Alykhan
designed parameter synchronization and a fault tolerance mecha-              Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith
                                                                                                   Chintala. 2019. PyTorch: An Imperative Style, High-Performance Deep Learning
nism: In our parameter synchronization algorithm, we showed that              Library. In NeurIPS.
consistency of version across different parts of parameters could be        [18] Konstantin V. Shvachko, Hairong Kuang, Sanjay R. Radia, and Robert J. Chansler.
traded-off for reducing network bandwidth consumption; In fault             2010. The Hadoop Distributed File System. 2010 IEEE 26th Symposium on Mass
                                                                                                Storage Systems and Technologies (MSST) (2010), 1–10.
tolerance design, we demonstrated that our strategy of trading-off        [19] HaiYing Wang, Aonan Zhang, and Chong Wang. 2021. Nonuniform Negative
PS reliability for realtime-ness is a robust solution.                             Sampling and Log Odds Correction with Rare Events Data. In Advances in Neural
  To conclude, Monolith succeeded in providing a general solution             Information Processing Systems.
                                                                                            [20] Minhui Xie, Kai Ren, Youyou Lu, Guangxu Yang, Qingxing Xu, Bihai Wu, Jiazhen
for production scale recommendation systems.                                        Lin, Hongbo Ao, Wanhong Xu, and Jiwu Shu. 2020. Kraken: Memory-Efficient
                                                                                       Continual Learning for Large-Scale Real-Time Recommendations. SC20: Inter-
                                                                                               national Conference for High Performance Computing, Networking, Storage and
ACKNOWLEDGMENTS                                                       Analysis (2020), 1–17.
                                                                                            [21] Weijie Zhao, Jingyuan Zhang, Deping Xie, Yulei Qian, Ronglai Jia, and Ping Li.
Hanzhi Zhou provided useful suggestions on revision of this paper.             2019. AIBox: CTR Prediction Model Training on a Single Node. Proceedings of the
                                                                                             28th ACM International Conference on Information and Knowledge Management
REFERENCES                                                                               (2019).
 [1] Martín Abadi, Paul Barham, Jianmin Chen, Z. Chen, Andy Davis, Jeffrey Dean,
     Matthieu Devin, Sanjay Ghemawat, Geoffrey Irving, Michael Isard, Manjunath
     Kudlur, Josh Levenberg, Rajat Monga, Sherry Moore, Derek Gordon Murray,
     Benoit Steiner, Paul A. Tucker, Vijay Vasudevan, Pete Warden, Martin Wicke,
    Yuan Yu, and Xiaoqiang Zhang. 2016. TensorFlow: A system for large-scale
    machine learning. ArXiv abs/1605.08695 (2016).
 [2] Andrew P. Bradley. 1997. The use of the area under the ROC curve in the
     evaluation of machine learning algorithms. Pattern Recognit. 30 (1997), 1145–
     1159.
 [3] Thomas Bredillet. 2019.  Core modeling at Instagram.    https://instagram-
     engineering.com/core-modeling-at-instagram-a51e0158aa48
 [4] Paris Carbone, Asterios Katsifodimos, Stephan Ewen, Volker Markl, Seif Haridi,
    and Kostas Tzoumas. 2015. Apache Flink™: Stream and Batch Processing in a
     Single Engine. IEEE Data Eng. Bull. 38 (2015), 28–38.
 [5] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra,
     Hrishikesh B. Aradhye, Glen Anderson, Gregory S. Corrado, Wei Chai, Mustafa
      Ispir, Rohan Anil, Zakaria Haque, Lichan Hong, Vihan Jain, Xiaobing Liu, and
    Hemal Shah. 2016. Wide & Deep Learning for Recommender Systems. Proceedings
      of the 1st Workshop on Deep Learning for Recommender Systems (2016).
 [6] Paul Covington, Jay K. Adams, and Emre Sargin. 2016. Deep Neural Networks
     for YouTube Recommendations.  Proceedings of the 10th ACM Conference on
    Recommender Systems (2016).
 [7] Alexandra Egg. 2021. Online Learning for Recommendations at Grubhub. Fif-
     teenth ACM Conference on Recommender Systems (2021).
 [8] João Gama, Indr˙e Žliobait˙e, Albert Bifet, Mykola Pechenizkiy, and A. Bouchachia.
     2014. A survey on concept drift adaptation. ACM Computing Surveys (CSUR) 46
      (2014), 1 – 37.
 [9] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, and Xiuqiang He. 2017.
    DeepFM: A Factorization-Machine based Neural Network for CTR Prediction. In
     IJCAI.
[10] Udit Gupta, Xiaodong Wang, Maxim Naumov, Carole-Jean Wu, Brandon Reagen,
     David M. Brooks, Bradford Cottel, Kim M. Hazelwood, Bill Jia, Hsien-Hsin S. Lee,
    Andrey Malevich, Dheevatsa Mudigere, Mikhail Smelyanskiy, Liang Xiong, and
    Xuan Zhang. 2020. The Architectural Implications of Facebook’s DNN-Based
     Personalized Recommendation.  2020 IEEE International Symposium on High
     Performance Computer Architecture (HPCA) (2020), 488–501.
[11]  F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History
    and Context. ACM Trans. Interact. Intell. Syst. 5 (2015), 19:1–19:19.
[12] Biye Jiang, Chao Deng, Huimin Yi, Zelin Hu, Guorui Zhou, Yang Zheng, Sui
    Huang, Xinyang Guo, Dongyue Wang, Yue Song, Liqin Zhao, Zhi Wang, Peng
     Sun, Yu Zhang, Di Zhang, Jinhui Li, Jian Xu, Xiaoqiang Zhu, and Kun Gai. 2019.
