# [PAPER] Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering

Источник: https://arxiv.org/pdf/2404.17723

Retrieval-Augmented Generation with Knowledge Graphs for
               Customer Service Question Answering

                  Zhentao Xu              Mark Jerome Cruz            Matthew Guevara
                   zhexu@linkedin.com               marcruz@linkedin.com             mguevara@linkedin.com
                   LinkedIn Corporation                 LinkedIn Corporation                 LinkedIn Corporation
                    Sunnyvale, CA, USA                  Sunnyvale, CA, USA                  Sunnyvale, CA, USA

                    Tie Wang                Manasi Deshpande              Xiaofeng Wang
                  tiewang@linkedin.com            madeshpande@linkedin.com           xiaofwang@linkedin.com
                   LinkedIn Corporation                 LinkedIn Corporation                 LinkedIn Corporation
                    Sunnyvale, CA, USA                  Sunnyvale, CA, USA                  Sunnyvale, CA, USA
2024                                       Zheng Li
                                                          zeli@linkedin.com
                                                       LinkedIn Corporation
                                                        Sunnyvale, CA, USAMay
6  ABSTRACT                           KEYWORDS
           In customer service technical support, swiftly and accurately re-     Large Language Model, Knowledge Graph, Question Answering,
            trieving relevant past issues is critical for efficiently resolving cus-     Retrieval-Augmented Generation
          tomer inquiries. The conventional retrieval methods in retrieval-
         augmented generation (RAG) for large language models (LLMs)    ACM Reference Format:
            treat a large corpus of past issue tracking tickets as plain text, ig-      Zhentao Xu, Mark Jerome Cruz, Matthew Guevara, Tie Wang, Manasi[cs.IR]          noring the crucial intra-issue structure and inter-issue relations,      Deshpande, Xiaofeng Wang, and Zheng Li. 2024. Retrieval-Augmented
         which limits performance. We introduce a novel customer service      Generation with Knowledge Graphs for Customer Service Question An-
           question-answering method that amalgamates RAG with a knowl-      swering. In Proceedings of the 47th International ACM SIGIR Conference
                                                                              on Research and Development in Information Retrieval (SIGIR ’24), July          edge graph (KG). Our method constructs a KG from historical issues
                                                                                          14–18, 2024, Washington, DC, USA. ACM, New York, NY, USA, 5 pages.
            for use in retrieval, retaining the intra-issue structure and inter-
                                                                                             https://doi.org/10.1145/3626772.3661370
            issue relations. During the question-answering phase, our method
           parses consumer queries and retrieves related sub-graphs from the
       KG to generate answers. This integration of a KG not only im-
           proves retrieval accuracy by preserving customer service structure    1  INTRODUCTION
           information but also enhances answering quality by mitigating the       Effective technical support in customer service underpins prod-
             effects of text segmentation. Empirical assessments on our bench-      uct success, directly influencing customer satisfaction and loyalty.
         mark datasets, utilizing key retrieval (MRR, Recall@K, NDCG@K)     Given the frequent similarity of customer inquiries to previously
          and text generation (BLEU, ROUGE, METEOR) metrics, reveal that      resolved issues, the rapid and accurate retrieval of relevant past
          our method outperforms the baseline by 77.6% in MRR and by 0.32      instances is crucial for the efficient resolution of such inquiries. Re-
            in BLEU. Our method has been deployed within LinkedIn’s cus-      cent advancements in embedding-based retrieval (EBR), large lan-
          tomer service team for approximately six months and has reduced     guage models (LLMs), and retrieval-augmented generation (RAG)arXiv:2404.17723v2    the median per-issue resolution time by 28.6%.                           [8] have significantly enhanced retrieval performance and question-
                                                                          answering capabilities for the technical support of customer service.
      CCS CONCEPTS                                             This process typically unfolds in two stages: first, historical issue
              • Computing methodologies →Information extraction; Nat-       tickets are treated as plain text, segmented into smaller chunks to
            ural language generation.                                      accommodate the context length constraints of embedding models;
                                                                           each chunk is then converted into an embedding vector for retrieval.
             Permission to make digital or hard copies of all or part of this work for personal or      Second, during the question-answering phase, the system retrieves
              classroom use is granted without fee provided that copies are not made or distributed      the most relevant chunks and feeds them as contexts for LLMs to
                for profit or commercial advantage and that copies bear this notice and the full citation      generate answers in response to queries. Despite its straightforward            on the first page. Copyrights for components of this work owned by others than the
               author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or      approach, this method encounters several limitations:
                republish, to post on servers or to redistribute to lists, requires prior specific permission
             and/or a fee. Request permissions from permissions@acm.org.                       • Limitation 1 - Compromised Retrieval Accuracy from
              SIGIR ’24, July 14–18, 2024, Washington, DC, USA                                   Ignoring Structures: Issue tracking documents such as Jira
         © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
         ACM ISBN 979-8-4007-0431-4/24/07                                                     [2] possess inherent structure and are interconnected, with
               https://doi.org/10.1145/3626772.3661370                                               references such as "issue A is related to/copied from/caused

SIGIR ’24, July 14–18, 2024, Washington, DC, USA                                                                                         Zhentao Xu, et al.

      by issue B." The conventional approach of compressing doc-     3.1  Knowledge Graph Construction
     uments into text chunks leads to the loss of vital informa-       3.1.1  Graph Structure Definition. In defining the knowledge graph
        tion. Our approach parses issue tickets into trees and further       structure for historical issue representation, we employ a dual-level
      connects individual issue tickets to form an interconnected       architecture that segregates intra-issue and inter-issue relations, as
      graph, which maintains this intrinsic relationship among       illustrated in Figure 1. The Intra-issue Tree T𝑖(N, E, R) models
        entities, achieving high retrieval performance.                 each ticket 𝑡𝑖as a tree, where each node 𝑛∈N, identified by a
    • Limitation 2 - Reduced Answer Quality from Segmen-     unique combination (𝑖,𝑠), corresponds to a distinct section 𝑠of
       tation: Segmenting extensive issue tickets into fixed-length       ticket 𝑡𝑖, and each edge 𝑒∈E and 𝑟∈R signifies the hierarchi-
      segments to accommodate the context length constraints of       cal connection and type of relations between these sections. The
      embedding models can result in the disconnection of related      Inter-issue Graph G(T, E, R) represents the network of connec-
       content, leading to incomplete answers. For example, an is-      tions across different tickets, incorporating both explicit links Eexp,
      sue ticket describing an issue at its beginning and its solution      defined in issue tracking tickets, and implicit connections Eimp,
       at the end may be split during the text segmentation process,      derived from semantic similarity between tickets. For implicit con-
       resulting in the omission of critical parts of the solution. Our      nections, we leverage cosine similarity between the embedding
      graph-based parsing method overcomes this by preserving      vectors of ticket titles, a method adaptable to specific use cases.
       the logical coherence of ticket sections, ensuring the delivery        For instance, Figure 1 portrays ticket ENT-22970 as a tree struc-
       of complete and high-quality responses.                          ture with nodes representing sections such as Summary, Description,
                                                          and Priority. It exhibits a direct clone linkage to PORT-133061,
                                                                       indicating an explicit clone relationship. Additionally, it’s implic-
2  RELATED WORK
                                                                                     itly connected with ENT-1744 and ENT-3547 due to the semantic
Question answering (QA) with knowledge graphs (KGs) can be       similarities.
broadly classified into retrieval-based, template-based, and semantic
parsing-based methods. Retrieval-based approaches utilize relation       3.1.2  Knowledge Graph Construction. Graph construction is de-
extraction [19] or distributed representations [5] to derive answers       lineated into two phases: intra-ticket parsing and inter-ticket con-
from KGs, but they face difficulties with questions involving multi-      nection. 1) Intra-Ticket Parsing Phase: This phase transforms
ple entities. Template-based strategies depend on manually-created      each text-based ticket 𝑡𝑖into a tree representation T𝑖. We employ
templates for encoding complex queries, yet are limited by the      a hybrid methodology, initially utilizing rule-based extraction for
scope of available templates [16]. Semantic parsing methods map      predefined fields, such as code sections identified via keywords.
text to logical forms containing predicates from KGs [4] [14] [21].      Subsequently, for text not amenable to rule-based parsing, we en-
   Recent advancements in large language models (LLMs) integra-     gage an LLM for parsing. The LLM is directed by a YAML template
tion with Knowledge Graphs (KGs) have demonstrated notable       Ttemplate, representing in graph the ticket sections routinely utilized
progress. Jin et al. [7] provide a comprehensive review of this in-     by customer support. 2) Inter-Ticket Connection Phase: Here,
tegration, categorizing the roles of LLMs as Predictors, Encoders,      individual trees T𝑖are amalgamated into a comprehensive graph G.
and Aligners. For graph-based reasoning, Think-on-Graph [15] and       Explicit connections Eexp are delineated as specified within tickets,
Reasoning-on-Graph [10] enhance LLMs’ reasoning abilities by      exemplified by designated fields in Jira [2]. Implicit connections
integrating KGs. Yang et al. [20] propose augmenting LLMs’ factual      Eimp are inferred from textual-semantic similarities across ticket
reasoning across various training phases using KGs. For LLM-based         titles, employing embedding techniques and a threshold mechanism
question answering, Wen et al.’s Mindmap [18] and Qi et al. [13]       to discern the most relevant tickets for each issue ticket.
employ KGs to boost LLM inference capabilities in specialized do-
                                                                             𝑡𝑖= 𝑡𝑖,rule ∪𝑡𝑖,llmmains such as medicine and food. These contributions underscore
the increasing efficacy of LLM and KG combinations in enhancing
                                                        T𝑖= RuleParse(𝑡𝑖,rule) + LLMParse(𝑡𝑖,llm, Ttemplate, prompt)information retrieval and reasoning tasks.
                                                                         Eexp = {(T𝑖, T𝑗)  | T𝑖explicitly connected to T𝑗}
3 METHODS
                                                                    Eimp = {(T𝑖, T𝑗)  | cos(embed(T𝑖), embed(T𝑗)) ≥𝜃}
We introduce an LLM-based customer service question answering
system that seamlessly integrates retrieval-augmented generation        3.1.3  Embedding Generation. To support online embedding-based
(RAG) with a knowledge graph (KG). Our system (Figure 1) com-       retrieval, we generate embeddings for graph node values using
prises two phases: First, during the KG construction phase, our      pre-trained text-embedding models like BERT [6] and E5 [17],
system constructs a comprehensive knowledge graph from histor-      specifically targeting nodes for text-rich sections such as "issue
ical customer service issue tickets. It integrates a tree-structured      summary", "issue description", and "steps to reproduce",
representation of each issue and interlinks them based on relational       etc. These embeddings are then stored in a vector database (for
context. It also generates embedding for each node to facilitate later       instance, QDrant [12])). For most cases the text-length within each
semantic searching. Second, during the question-answering phase,     node can meet the text-embedding model’s context length con-
our method parses consumer queries to identify named entities       straints, but for certain lengthy texts,we can safely divide the text
and intents. It then navigates within the KG to identify related      into smaller chunks for individual embedding without worrying
sub-graphs for generating answers.                                 about quality since the text all belong to the same section.

Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering                      SIGIR ’24, July 14–18, 2024, Washington, DC, USA


         Knowledge Graph Construction                                Retrieval and Question Answering

                                           CLONE_FROM
         Ti cket           Ti cket          Ti cket                                                                                  Ti cket             Quest i on Quer y: How  t o  r epr oduce  t he   i ssue wher e user saw " csv upl oad er r or    i n updat i ng
       ENT- 1744     ENT- 3547     PORT- 133061   CLONE_TO   ENT- 22970         user  emai  l " and has maj or  pr i or i t y   t hat  was caused by dat a   i ssue?
                                                                          4   Ent i t y Det ect i on                    4   I nt ent  Cl assi f i cat i on
          2     iconnectnt er - t ii cketon                 1      it ntr eer a-part i cketsi ng              Summar y:   " CSV upl oad er r or    i n         Pr i or i t y:        Root  Cause:                   I nt ent :   " St eps   t o
                          ( i mpl  i ci t  EBR,                                                  updat i ng user  emai  l "                            " Maj or "               " Dat a  I ssue"         Repr oduce"                 expl  i ci t )
                                                                 5  Embedding-based Retrieval       5   Filtering      5  Filtering       5  Question Intent

                                                               Graph Database
                inter-ticket connections                                                            intra-ticket tree representation
                       Ti cket  PORT- 133061            CLONE_FROM             Ti cket  ENT- 22970
                           " CSV upl oad er r or ,                               CSV upl oad er r or ,
                  updat i ng user  emai  l "           CLONE_TO            updat i ng user  emai  l


                                  . . .               . . .               . . .             SI MI LAR_TO                                                                                                   HAS_FI ELDS        HAS_COMMENTS

                       Ti cket  ENT- 1744                             HAS_SUMMARY
                HTTP POST csv upl oad                                                                                                 Fi el ds                                                   [ " user - 1" : " Do we know how
                     er r or - i nt er nal  er r or                                                                                                                                                                                                               t hese dupl  i cat ed pr of i  l es
                                                             SI MI LAR_TO                                     HAS_PRI ORI TY            HAS_I MPACT_AREA     got  cr eat ed?" ,
                                                                            HAS_DESCRI PTI ON                                                                                                . . . .
                                                                                                    HAS_ROOT_CAUSE                             " user - 2" :   " cl eaned up 228                                                                                  " CSV upl oad er r or ,
                                  . . .               . . .               . . .             updat i ng user  emai  l "       Descr i pt i on           Maj or      Dat a  I ssue       St r at egi c      duplr esoli catved"e , pr of i  l es,
                                                                                                                                                                                                                              " user - 1" :   " t hanks,   t i cket
                       Ti cket  ENT- 3547                                                                                                                                                   cl osed" ]
                  Lear ni ng   ' upl oad csv'                            HAS_I SSUE_DESCRI PTI ON                 HAS_STEPS_TO_REPRODUCE
                    opt i on  f ai  l s
                                                                                  " Admi n seei ng sever al  er r or s when          Ref er   t o  t he CSV:  ht t ps: / / mi cr osof t . shar epoi nt . com/ xxx:  1.  Open  t he
                                                                   at t empt i ng updat e of  user  emai  l s on       Dashboar d  I D xxxxx;  2.  Cl  i ck on  I nst ances > Pr of i  l e;  3.  Sear ch  f or
                                  . . .               . . .               . . .            dashboarnumber  ofd  IuserD " sxxxxxxxxx'af f ect ed . ~'Totyyy'al . "          user s  f r om t he CSV  f i  l e and not e  t hat   t her e ar e 2 pr of i  l es exi st .


     3   Text - embeddi ng Gener at i on                                                                     6    Answer  Gener at i on                     f or Node Val ues
                                                                                                          Fi nal  Answer :  based on  t he  t i cket  ENT- 22970,   t he  st eps   t o  r epr oduce  t he   i ssue   i s  " 1.  Ref er
                                                                                                                                                             t o  t he CSV:  ht t ps: / / mi cr osof t . shar epoi nt . com/ xxx  2.  Open  t he Dashboar d  I D xxxxxxxxx  3.
                            Vector Database                                           Cl  i ck on  I nst ances > Pr of i  l e 4.  Sear ch  f or  user s   f r om t he CSV  f i  l e and not e  t hat   t her e ar e
                                                                               2 pr of i  l es   t hat  come up.

                                     Legends
                                                                                                   issue-tracking ticket          1-6     step with step numbers    Vector DB

                                                                                      graph nodes with links            Step with LLM             Graph DB



Figure 1: An overview of our proposed retrieval-augmented generation with knowledge graph framework. The left side of this
diagram illustrates the knowledge graph construction; the right side shows the retrieval and question answering process.


3.2  Retrieval and Question Answering               by leveraging the LLM’s extensive understanding and interpretive
3.2.1  Query Entity Identification and Intent Detection. In this step,       capabilities.
we extract the named entities P of type Map(N →V) and the                         𝑃, 𝐼= LLM(𝑞,𝑇template, prompt)
query intent set I from each user query 𝑞. The method involves
parsing each query 𝑞into a key-value pair, where each key 𝑛, men-       3.2.2  Embedding-based Retrieval of Sub-graphs. Our method ex-
tioned within the query, corresponds to an element in the graph       tracts pertinent sub-graphs from the knowledge graph, aligned with
template Ttemplate, and the value 𝑣represents the information ex-      user-provided specifics such as "issue description" and "issue
tracted from the query. Concurrently, the query intents I include      summary", as well as user intentions like "fix solution". This pro-
the entities mentioned in the graph template Ttemplate that the      cess consists of two primary steps: EBR-based ticket identification
query aims to address. We leverage LLM with a suitable prompt     and LLM-driven subgraph extraction.
in this parsing process. For instance, given the query 𝑞= "How         In the EBR-based ticket identification step, the top 𝐾ticket
to reproduce the login issue where a user can’t log in to LinkedIn?",     most relevant historical issue tickets are pinpointed by harnessing
the extracted entity is P = Map("issue summary" →"login issue",      the named entity set P derived from user queries. For each entity
"issue description" →"user can’t log in to LinkedIn"), and the      pair (𝑘, 𝑣) ∈P, cosine similarity is computed between the entity
intent set is I=Set("fix solution"). This method demonstrates      value 𝑣and all graph nodes 𝑛corresponding to section 𝑘via pre-
notable flexibility in accommodating varied query formulations      trained text embeddings. Aggregating these node-level scores to
                                                                             ticket-level by summing contributions from nodes belonging to

SIGIR ’24, July 14–18, 2024, Washington, DC, USA                                                                                         Zhentao Xu, et al.

 the same ticket, we rank and select the top 𝐾ticket tickets. This                  Table 1: Retrieval Performance
method presupposes that the occurrence of multiple query entities
 is indicative of pertinent links, thus improving retrieval precision.                 MRR    Recall@K    NDCG@K
                                                                             K=1   K=3   K=1   K=3
                                                                            Baseline      0.522   0.400   0.640   0.400   0.520
 𝑆𝑇𝑖=  ∑︁  ∑︁ I{𝑛.sec = 𝑘} · cos(embed(𝑣), embed(𝑛.text))                                                                    Experiment  0.927  0.860  1.000  0.860  0.946
       (𝑘,𝑣)∈P  𝑛∈𝑇𝑖                                                                                                                                                                                                                                                                                                                                                                                                                                             
                                                                    Table 2: Question Answering Performance   In the LLM-driven subgraph extraction step, the system first
 rephrases the original user query 𝑞to include the retrieved ticket
 ID; the modified query 𝑞′ is then translated into a graph data-                      BLEU  METEOR  ROUGE
 base language, such as Cypher for Neo4j for question answering.                                                                                 Baseline      0.057     0.279      0.183
 For instance, from the initial query 𝑞="how to reproduce the is-
                                                                        Experiment  0.377    0.613     0.546
 sue where user saw ’csv upload error in updating user email’ with
 major priority due to a data issue", the query is reformulated to
"how to reproduce ’ENT-22970’ and thereafter transposed into the                                                5 PRODUCTION USE CASE
Cypher query MATCH (j:Ticket {ticket_ID: ’ENT-22970’})
-[:HAS_DESCRIPTION]-> (description:Description)          We deployed our method within LinkedIn’s customer service team,
-[:HAS_STEPS_TO_REPRODUCE]-> (steps_to_reproduce:            covering multiple product lines. The team was split randomly into
StepsToReproduce) RETURN steps_to_reproduce.value. It is     two groups: one used our system, while the other stuck to tradi-
                                                                           tional manual methods. As shown in Table 3, the group using our noteworthy that the LLM-driven query formulation is sufficiently
                                                               system achieved significant gains, reducing the median resolution versatile to retrieve information across subgraphs, whether they
                                                                  time per issue by 28.6%. This highlights our system’s effectiveness originate from the same tree or distinct trees within the knowledge
                                                                         in enhancing customer service efficiency. graph.

 3.2.3  Answer Generation. Answers are synthesized by correlating          Table 3: Customer Support Issue Resolution Time
 retrieved data from Section 3.2.2 with the initial query. The LLM
 serves as a decoder to formulate responses to user inquiries given                                                               Group        Mean      P50      P90
 the retrieved information. For robust online serving, if query execu-
                                                                         Tool Not Used  40 Hours   7 Hours   87 Hours tion encounters issues, a fallback mechanism reverts to a baseline
                                                                         Tool Used      15 hours  5 hours  47 hours text-based retrieval method

4  EXPERIMENT
                                                6  CONCLUSIONS AND FUTURE WORK
4.1  Experiment Design
                                                                        In conclusion, our research significantly advances automated ques-
Our evaluation employed a curated "golden" dataset comprising                                                                         tion answering systems for customer service. Integrating retrieval
 typical queries, support tickets, and their authoritative solutions.                                                          augmented generation (RAG) with a knowledge graph (KG) has
The control group operated with conventional text-based EBR,                                                              improved retrieval and answering metrics, and overall service effec-
while the experimental group applied the methodology outlined in                                                                              tiveness. Future work will focus on: developing an automated mech-
 this study. For both groups, we utilized the same LLM, specifically                                                             anism for extracting graph templates, enhancing system adaptabil-
GPT-4 [1], and the same embedding model, E5 [17]. We measured                                                                                        ity; investigating dynamic updates to the knowledge graph based
 retrieval efficacy using Mean Reciprocal Rank (MRR), recall@K,                                                        on user queries to improve real-time responsiveness; and explor-
 and NDCG@K. MRR gauges the average inverse rank of the initial                                                                   ing the system’s applicability in other contexts beyond customer
 correct response, recall@K determines the likelihood of a relevant                                                                             service.
 item’s appearance within the top K selections, and NDCG@K ap-
 praises the rank quality by considering both position and pertinence    7 COMPANY PORTRAIT
 of items. For question-answering performance, we juxtaposed the
                                                      About LinkedIn: Founded in 2003, LinkedIn connects the world’s "golden" solutions against the generated responses, utilizing metrics
                                                                        professionals to make them more productive and successful. With such as BLEU [11], ROUGE [9], and METEOR [3] scores.
                                                          more than 1 billion members worldwide, including executives from
                                                                every Fortune 500 company, LinkedIn is the world’s largest pro-
4.2  Result and Analysis                                       fessional network. The company has a diversified business model
The retrieval and question-answering performances are presented      with revenue coming from Talent Solutions, Marketing Solutions,
 in Table 1 and Table 2, respectively. Across all metrics, our method      Sales Solutions and Premium Subscriptions products. Headquar-
 demonstrates consistent improvements. Notably, it surpasses the       tered in Silicon Valley, LinkedIn has offices across the globe. Please
 baseline by 77.6% in MRR and by 0.32 in BLEU score, substantiating        visit https://www.linkedin.com/company/linkedin/about/ for more
 its superior retrieval efficacy and question-answering accuracy.         information.

Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering                      SIGIR ’24, July 14–18, 2024, Washington, DC, USA

8  PRESENTER BIO                                                                preprint arXiv:2310.01061 (2023).
                                                                                            [11] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. Bleu: a
Zhentao Xu is a Senior Software Engineer at LinkedIn. He received           method for automatic evaluation of machine translation. In Proceedings of the
his M.S. in Robotics and B.S. in Electrical Engineering and Computer             40th annual meeting of the Association for Computational Linguistics. 311–318.
Science (EECS) from University of Michigan. His research interests        [12] Qdrant Team. 2024. Qdrant - Vector Database. https://qdrant.tech/. Accessed:
                                                                                                2024-01-08.
lie in large language models and natural language generation.             [13] Zhixiao Qi, Yijiong Yu, Meiqi Tu, Junyi Tan, and Yongfeng Huang. 2023. Foodgpt:
                                                         A large language model in food testing domain with incremental pre-training
REFERENCES                                                            and knowledge graph prompt. arXiv preprint arXiv:2308.10173 (2023).                                                                                            [14] Haitian Sun, Bhuwan Dhingra, Manzil Zaheer, Kathryn Mazaitis, Ruslan Salakhut-
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-              dinov, and William Cohen. 2018. Open Domain Question Answering Using Early
      cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal            Fusion of Knowledge Bases and Text. In Proceedings of the 2018 Conference on
     Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774             Empirical Methods in Natural Language Processing, Ellen Riloff, David Chiang,
      (2023).                                                                                              Julia Hockenmaier, and Jun’ichi Tsujii (Eds.). Association for Computational
 [2] Atlassian. 2024. Jira | Issue & Project Tracking Software.  https://www.atlassian.              Linguistics, Brussels, Belgium, 4231–4242. https://doi.org/10.18653/v1/D18-1455
     com/software/jira Accessed: 2024-01-04.                                               [15] Jiashuo Sun, Chengjin Xu, Lumingyuan Tang, Saizhuo Wang, Chen Lin, Yeyun
 [3] Satanjeev Banerjee and Alon Lavie. 2005. METEOR: An automatic metric for           Gong, Heung-Yeung Shum, and Jian Guo. 2023.  Think-on-graph: Deep and
   MT evaluation with improved correlation with human judgments. In Proceedings             responsible reasoning of large language model with knowledge graph. arXiv
      of the acl workshop on intrinsic and extrinsic evaluation measures for machine              preprint arXiv:2307.07697 (2023).
      translation and/or summarization. 65–72.                                               [16] Christina Unger, Lorenz Bühmann, Jens Lehmann, Axel-Cyrille Ngonga Ngomo,
 [4] Nikita Bhutani, Xinyi Zheng, Kun Qian, Yunyao Li, and H Jagadish. 2020. Answer-            Daniel Gerber, and Philipp Cimiano. 2012. Template-based question answering
     ing complex questions by combining information from curated and extracted             over RDF data. In Proceedings of the 21st international conference on World Wide
    knowledge bases. In Proceedings of the first workshop on natural language inter-           Web. 639–648.
      faces. 1–10.                                                                            [17] Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang,
 [5] Antoine Bordes, Jason Weston, and Nicolas Usunier. 2014. Open question an-           Rangan Majumder, and Furu Wei. 2022. Text embeddings by weakly-supervised
     swering with weakly supervised embedding models. In Machine Learning and              contrastive pre-training. arXiv preprint arXiv:2212.03533 (2022).
     Knowledge Discovery in Databases: European Conference, ECML PKDD 2014, Nancy,        [18] Yilin Wen, Zifeng Wang, and Jimeng Sun. 2023. Mindmap: Knowledge graph
      France, September 15-19, 2014. Proceedings, Part I 14. Springer, 165–180.                   prompting sparks graph of thoughts in large language models. arXiv preprint
 [6] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert:             arXiv:2308.09729 (2023).
     Pre-training of deep bidirectional transformers for language understanding. arXiv        [19] Kun Xu, Yansong Feng, Songfang Huang, and Dongyan Zhao. 2016. Hybrid
      preprint arXiv:1810.04805 (2018).                                                          question answering over knowledge base and free text. In Proceedings of COLING
 [7] Bowen Jin, Gang Liu, Chi Han, Meng Jiang, Heng Ji, and Jiawei Han. 2023.             2016, the 26th International Conference on Computational Linguistics: Technical
     Large Language Models on Graphs: A Comprehensive Survey. arXiv preprint              Papers. 2397–2407.
     arXiv:2312.02783 (2023).                                                               [20] Linyao Yang, Hongyang Chen, Zhao Li, Xiao Ding, and Xindong Wu. 2023.
 [8] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,          ChatGPT is not Enough: Enhancing Large Language Models with Knowledge
    Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel,           Graphs for Fact-aware Language Modeling.  arXiv preprint arXiv:2306.11489
      et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp tasks.              (2023).
     Advances in Neural Information Processing Systems 33 (2020), 9459–9474.               [21] Scott Wen-tau Yih, Ming-Wei Chang, Xiaodong He, and Jianfeng Gao. 2015. Se-
 [9] Chin-Yew Lin. 2004. Rouge: A package for automatic evaluation of summaries.            mantic parsing via staged query graph generation: Question answering with
     In Text summarization branches out. 74–81.                                         knowledge base. In Proceedings of the Joint Conference of the 53rd Annual Meet-
[10] Linhao Luo, Yuan-Fang Li, Gholamreza Haffari, and Shirui Pan. 2023. Reasoning             ing of the ACL and the 7th International Joint Conference on Natural Language
    on graphs: Faithful and interpretable large language model reasoning. arXiv              Processing of the AFNLP.
