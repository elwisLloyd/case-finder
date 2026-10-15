# Grammatical Error Correction: Tag, Not Rewrite

Источник: https://www.grammarly.com/blog/engineering/gec-tag-not-rewrite/

Grammarly’s writing assistant helps with a wide variety of language and communication issues. One important aspect of this is addressing mistakes in spelling, punctuation, grammar, and word choice—an area known broadly in natural language processing (NLP) research as grammatical error correction. A GEC system takes in a sentence with mistakes and outputs a corrected version. Over the past eleven years, Grammarly has built one of the world’s best GEC systems as a core component of our product.
| Input | Output | 
| A ten years old boy go school | A ten-year-old boy goes to school. | 
In the NLP research community, the preferred approach to GEC has recently been to treat it as a translation problem, where sentences with mistakes are the “source language” and mistake-free sentences are the “target language.” By combining neural machine translation (NMT) with transformer-based sequence-to-sequence (seq2seq) models, research teams have achieved state-of-the-art performance on standard GEC benchmarks. The focus of GEC research has now shifted toward generating training data for these NMT-based systems.
However, these systems are better suited to academic research than to real-world applications. NMT systems usually use encoder-decoder architecture, where the encoder function is language understanding and the decoder function is language generation. Language generation is a more complex task than language understanding. As such, NMT-based systems require large amounts of training data and generate inferences rather slowly. Furthermore, without additional functionality, it’s not possible to explain what types of mistakes were made in the original sentence—a neural network is essentially a black box.
To solve these problems, Grammarly’s research team has experimented with a different approach: Instead of doing language generation explicitly and attempting to rewrite the sentence in its correct form all in one go, we tag the sequence of words with custom transformations describing corrections to be made.
Sequence-tagging reduces the task to a language-understanding problem, meaning we can just use an encoder and basic linear layers for our model. This allows us to parallelize the inference so it runs faster, which simplifies training. The tags also make it possible (though not trivial!) to describe the changes being made to the text in a human-readable manner. And we’re proud to say that with this “tag, not rewrite” approach, we are able to achieve state-of-the-art performance on our model evaluations.
This is also the subject of a new paper from the Grammarly research team, which was presented at the 15th Workshop on Innovative Use of NLP for Building Educational Applications (BEA), co-located with the Association for Computational Linguistics (ACL) conference.
Transformation tags
Our sequence-tagging approach relies on custom transformation tags—you can think of these as abstract versions of Grammarly’s suggestions. We define these tags on tokens, which in NLP are units of text (usually words, sometimes punctuation marks, depending on how tokenization is done).
For example, if a token is tagged with $DELETE, that means it should be removed. The tag $APPEND_{,} means that a comma should be appended to this token to make the text more correct.
The number of tags was an important consideration in our research. If our “vocabulary” for describing corrections was too big, our model would be unwieldy and slow; too small, and we wouldn’t cover enough errors. We compromised on 5,000 different transformation tags to cover the most common mistakes, such as spelling, noun number, subject-verb agreement, and verb form—a tag vocabulary of this size covers 98% of the errors present in CoNLL-2014 (test), one of the two GEC data sets we used to evaluate our model.
Basic tags
The majority of our tags are of four basic types:
- $KEEP indicates that this token is correct and should remain unchanged in the output text.
- $DELETE indicates that this token should be removed from the output text.
- $APPEND_{t1} describes a set of tags that append a new token to the existing one. The “transformation suffix” in the braces describes what should be appended. There are 1,167 unique APPEND tags in our model’s vocabulary.
- $REPLACE_{t2} describes a set of tags that replace the source token with a different one in the output. Our model contains 3,802 unique REPLACE tags.
G-transformations
The rest of our tags are what we call g-transformations, which perform more complex operations, such as changing the case of the current token (CASE tags), merging the current token and the next token into a single one (MERGE tags), and splitting the current token into two new ones (SPLIT tags).
With the g-transformations NOUN NUMBER and VERB FORM, we can convert singular nouns to plural ones and even change the form of verbs to express a different number or tense. The VERB FORM transformation includes twenty different tags that describe the starting and ending verb form, which our model derives using conjugation dictionaries. For example, to represent changing the word “went” to the word “gone,” the appropriate tag would be $VERB FORM VBD VBN; in our tagging shorthand, VBD VBN encodes the idea that we have a verb in the past tense and want the past participle instead.
While these g-transformation tags are small in number, they help immensely with the task. In one test, using only the top 100 basic tags, our model achieved 60% error coverage; adding in the g-transformations bumped our error coverage up to 80%.
Model training
Our GEC sequence-tagging model, called GECToR, is an encoder made up of a pre-trained BERT-like transformer, stacked with two linear layers, with softmax layers on the top. The two linear layers are responsible for mistake detection and token-tagging, respectively.
We pre-trained our model in three stages. In the first stage, we used a synthetic data set containing 9 million source/target sentence pairs with mistakes. In the second and third stages, we fine-tuned the model on several real-world data sets from English-language learners: about 500,000 sentences for stage 2, and just 34,000 for stage 3. We found that having two fine-tuning stages, the final stage containing some sentences with no mistakes at all, was crucial for our model’s performance.
Preprocessing
For each source/target pair in our training and evaluation data sets, our preprocessing algorithm generates transformation tags, one tag for each token in the source sequence. (In NLP research, a series of tokens is called a sequence—it may or may not be a complete sentence.)
Let’s return to our original example to briefly illustrate how this works; for more details, you can view the preprocessing script in our repository.
Source sequence: A ten years old boy go school
Target sequence: A ten-year-old boy goes to school.
Step 1
First, we roughly align each token in the source sequence with one or more tokens from the target sequence.
[A → A], [ten → ten, –], [years → year, –], [old → old], [go → goes, to], [school → school, .].
To achieve this, we minimize the overall Levenshtein distance of possible transitions between the source tokens and the target tokens. In essence, this means we try to minimize the number of edits that it would take to transform the source into the target.
Step 2
Next, we convert each mapping into the tag that represents the transformation.
[A → A]: $KEEP, [ten → ten, –]: $KEEP, $MERGE HYPHEN, [years → year, –]: $NOUN NUMBER SINGULAR, $MERGE HYPHEN], [old → old]: $KEEP, [go → goes, to]: $VERB FORM VB VBZ, $APPEND to, [school → school, .]: $KEEP, $APPEND {.}].
Step 3
Because we use an iterative approach to tagging (more on this in the next section), we can only have one tag for each token. So in the final step, if there are multiple tags for a token, we hold on to the first tag that is not a $KEEP.
A ⇔ $KEEP, ten ⇔ $MERGE HYPHEN, years ⇔ $NOUN NUMBER SINGULAR, old ⇔ $KEEP, go ⇔ $VERB FORM VB VBZ, school ⇔ $APPEND {.}.
Inference using iterative sequence-tagging
Our model predicts the tag-encoded transformations for each token in the input sequence; we can then apply these transformations to get the modified output sequence. But since some corrections in a sentence may depend on others, applying the GEC sequence-tagger only once may not be enough to fully correct the sentence. Therefore, we use an iterative correction approach: We modify the sentence, run our tagger on it again, and repeat. Here’s what that looks like using our previous example, with corrections in bold:
Source sequence: A ten years old boy go school
Iteration 1: A ten–years old boy goes school (2 total corrections)
Iteration 2: A ten-year-old boy goes to school (5 total corrections)
Iteration 3: A ten-year-old boy goes to school. (6 total corrections)
Usually, the number of corrections decreases with each successive iteration, and most of the corrections are performed during the first two iterations. We tested our model with as few as 1 and as many as 5 iterations—we found that limiting the number of iterations speeds up the overall pipeline while trading off the quality of the corrections.
To tweak our model for better results, we also introduced two inference hyperparameters. First, we added a permanent positive confidence bias to the probability of the $KEEP tag, which is responsible for not changing the source token. Second, we added a sentence-level minimum error probability threshold for the output of the error detection layer, which increased precision by trading off recall. These hyperparameters were found by a random search method on BEA-2019 (dev), a standard GEC data set.
Results
Model quality
On the canonical evaluation data sets for the GEC task, we achieved state-of-the-art F-score results with a single model: an F0.5 of 65.3 on CoNLL-2014 (test) and an F0.5 of 72.4 on BEA-2019 (test). With an ensemble approach, where we simply averaged output probabilities from 3 single models, we can do even better, achieving F0.5 scores of 66.5 and 73.6 on those same respective data sets.
Inference speed
When we measured our GECToR model’s average inference time, we found that it is up to 10 times as fast as the state-of-the-art NMT-based systems.
| GEC system | Time (sec) | 
| Transformer-NMT, beam size = 12 | 4.35 | 
| Transformer-NMT, beam size = 4 | 1.25 | 
| Transformer-NMT, beam size = 1 | 0.71 | 
| GECToR, 5 iterations | 0.40 | 
| GECToR, 1 iteration | 0.20 | 
NMT-based approaches are usually autoregressive, meaning each predicted token relies on all previous tokens and corrections must be predicted one-by-one. GECToR’s approach is non-autoregressive, with no dependencies between predictions. It’s naturally parallelizable and therefore runs many times faster.
Pushing the boundaries of GEC
This research shows that a faster, simpler, and more efficient GEC system can be developed by taking a road less traveled. Rather than following the trend (in this case, NMT-based GEC), it’s worth asking yourself whether you should try something radically different. There’s a chance you might fail—but an uncharted path could also lead you to interesting findings and better results.
NLP research is the backbone of everything we build at Grammarly. If you’re interested in joining our research team and helping millions of people around the world wherever they write, get in touch—we’re hiring!
Kostiantyn Omelianchuk presented this research at the 15th Workshop on Innovative Use of NLP for Building Educational Applications (co-located with ACL 2020), which took place on July 10, 2020. The accompanying research paper, “GECToR – Grammatical Error Correction: Tag, Not Rewrite,” written by Kostiantyn Omelianchuk, Vitaliy Atrasevych, Artem Chernodub, and Oleksandr Skurzhanskyi, will be published in the Proceedings of the 15th Workshop on Innovative Use of NLP for Building Educational Applications.
