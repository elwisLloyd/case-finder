# Balancing Revenue and Relevance: Optimizing TLD Ad Rankings

Источник: https://www.godaddy.com/resources/news/balancing-revenue-and-relevance-optimizing-tld-ad-rankings

Key takeaways
- GoDaddy replaced its simple "highest bid wins" TLD ad ranking with DeepAd, a neural model that balances advertiser bids with relevance signals to improve user experience and long-term revenue.
- The model leverages transfer learning from GoDaddy's organic search engine (DeepRank) and trains on real user behavior data from domain purchases and clicks rather than synthetic labels.
- A/B testing showed that optimizing for both relevance and revenue delivers better conversion rates while giving niche TLDs fair exposure alongside well-funded registries.
When you search for a domain name on GoDaddy you often see sponsored suggestions for particular top‑level domains (TLDs)— for example, “.cafe” or “.auction”. Deciding which TLD ad should appear in the limited space available is a classic ranking problem. Until recently we solved it the uncomplicated way— show the advertiser with the highest bid. That policy maximized short‑term revenue but ignored whether the TLD was actually useful to the shopper. The result? Frustrated users, missed clicks, and a missed opportunity to promote niche but relevant domains.
In this post we describe the journey from that bid‑only system to DeepAd, a deep‑learning model that simultaneously optimizes for relevance and revenue. Along the way we will cover:
- why the traditional approach broke down,
- how we transferred knowledge from our organic search model,
- the behavioral data that powers the new model, and
- the business impact we have measured so far.
Ranking purely by bid is appealingly simple— no features to engineer, no parameters to tune— but it comes with three major drawbacks:
- No context awareness – A user researching cafés in Toronto could be shown “.auction” simply because it paid more, hurting engagement and trust.
- Low diversity – Well‑funded registries dominate every impression, leaving emerging or niche TLDs invisible.
- Revenue myopia – Click‑through rates fall over time when ads feel irrelevant, eventually reducing the very revenue the strategy was meant to maximize.
These issues became more pronounced as our catalog of possible TLDs grew beyond the familiar .com, .net, and .org.
To correct course we built DeepAd, a neural ranking model that produces a composite score for each candidate ad by blending monetary bid with dozens of contextual and behavioral signals.
Instead of relying solely on bid price, DeepAd leverages a rich set of features to predict the most suitable TLDs for a given context. These include:
- Semantic Relevance: Measures how closely a TLD aligns with the page content, search query, or user intent.
- Popularity Signals: Historical impressions, click-through rates, and engagement metrics.
- User Behavior: Aggregated signals from shopper interaction history and trends.
- Bid Price: Still included as a key signal, but no longer the sole driver of ranking.
At a high level, the serving workflow is:
- Generate candidates – For the current query we assemble the set of eligible TLDs.
- Score with DeepAd – The model consumes semantic, behavioral, and bid‑related features and returns a relevance‑aware score.
- Filter for availability – Only ads that are active in our ad‑serving platform are retained.
- Serve – The highest‑scoring available ad is shown.
By design, bid still matters— it is one of the model’s inputs— but now it competes with signals that capture what the shopper is really looking for.
We did not start from scratch. Our organic search engine is powered by DeepRank, a model trained on billions of domain‑search interactions. We initialize DeepAd with DeepRank’s learned representations and then fine‑tune on ad‑specific data. The transfer‑learning approach:
- gives the ad model a strong prior about domain semantics,
- shortens training time, and
- helps niche TLDs that have little historical ad data.
The following table lists some key features of DeepAd:
| Category | Examples | Purpose | 
|---|---|---|
| Semantic | Query tokens, page language, SLD/TLD tokens | Match ad to intent | 
| Behavioral | Historical clicks, purchases, portfolio makeup | Personalize ranking | 
| Temporal & Trend | Recent impression velocity, query popularity spikes | Capture fresh interest | 
| Monetization | Advertiser bid, auction outcome signals | Balance revenue | 
(Internally, we group many of these into a framework called ReTiRe (short for Relevance, Time, Revenue) but the principles are common to most modern ad systems.)
DeepAd is then fine-tuned on Media Solutions–specific (GoDaddy's GoDaddy's online ad program) ad engagement data, with additional features such as:
- ReTiRe signals: Custom signals reflecting short-term trends, ad freshness, and monetization potential.
- Auction outcomes and bid signals, which are unique to the paid ecosystem.
The result is a specialized ranking model tailored for TLD ads that blends deep semantic understanding with monetization awareness.
At the heart of DeepAd’s success is rich, behavior-driven training data sourced from the domain suggestion (or "spin") interface— where users are shown multiple domain name options based on their query.
Each interaction is logged in a structured format:
<Query, Suggested TLD, User Action>
For example:
<zoespizza.cafe, zoespizza.shop, buy>
This indicates that the user was shown .cafe and .shop domains after searching for "zoespizza", and chose to purchase .cafe. These labeled outcomes provide powerful supervision signals that reflect actual user preferences.
This matters because, unlike synthetic or heuristic labels, these are grounded in real user actions - purchases, clicks, or dismissals. It also provides multiple contexts— data spans a wide range of verticals (for example, food, tech, lifestyle), making the model more generalizable. Additionally, it provides implicit relevance signals— purchase or click behavior acts as a proxy for relevance, helping the model learn fine-grained user preferences even across niche TLDs. By training on this structured behavioral data, DeepAd becomes highly attuned to what users actually want - not just what advertisers pay for.
The strength of the DeepAd model lies in its ability to learn from a rich and diverse set of features derived from multiple sources. These features capture both contextual relevance and long-term user behavior, enabling personalized and high-performing ad rankings.
These are real-time and semantic features extracted from the current query and its context:
- Query Text and Tokens - Raw and tokenized forms of the user’s search string.
- Second-level domain and TLD Tokens - Semantic components of suggested domains (for example, zoespizza and .cafe).
- Country Code - Geo-location derived from IP or shopper settings.
- Language - User’s locale, browser language, or query language.
These features help DeepAd understand what the user is searching for - and how well a TLD fits the query.
These are behavioral and longitudinal features mined from the shopper’s interaction history:
- Query History - Prior searches made by the same user or user cohort.
- Active Domains - Domains currently owned or managed by the shopper.
- Purchase History - Previously purchased TLDs or domain categories.
- Portfolio Distribution - Frequency and diversity of TLDs in the shopper’s domain portfolio.
These features allow DeepAd to personalize ad rankings by factoring in what the user tends to engage with or buy.
To ensure DeepAd delivers real value, we conduct both offline and online evaluations— measuring performance from both modeling and business perspectives.
During model development and training, we rely on standard ranking metrics to assess performance using historical labeled data:
- Precision and Recall: Measure the model's ability to correctly identify relevant TLDs.
- Area Under Curve: Evaluates the quality of the ranking over positive vs. negative labels.
- Normalized Discounted Cumulative Gain: Accounts for the position of relevant items, rewarding highly ranked correct predictions.
These metrics guide iterative improvements before any model goes live.
For live traffic, we run rigorous A/B tests against the production system. Our key business-focused KPIs include:
- Conversion Rate: Percentage of ad impressions that lead to purchases.
- Revenue per Mille: Monetization effectiveness based on real user actions.
- Cost per Acquisition: Efficiency of spend relative to actual conversions.
By combining these two evaluation layers, we ensure DeepAd is both technically sound and business-effective.
Moving from a bid‑only heuristic to a machine‑learned ranking system has unlocked a better experience for developers and registries alike. Shoppers see TLDs that actually fit their projects, niche extensions get fair exposure, and GoDaddy continues to meet its revenue goals.
We did not start from scratch. Our organic search engine is powered by DeepRank, a model trained on billions of domain‑search interactions. We initialize DeepAd with DeepRank’s learned representations and then fine‑tune on ad‑specific data. The transfer‑learning approach. DeepAd is then fine-tuned on Media Solutions, with specific ad engagement data and additional features.
