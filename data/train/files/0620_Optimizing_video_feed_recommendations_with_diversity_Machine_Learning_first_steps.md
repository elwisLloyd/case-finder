# Optimizing video feed recommendations with diversity: Machine Learning first steps

Источник: https://medium.com/dailymotion/optimizing-video-feed-recommendations-with-diversity-machine-learning-first-steps-4cf9abdbbffd

Optimizing video feed recommendations with diversity: Machine Learning first steps
As part of its new mobile experience, Dailymotion redesigned its video recommendation system.
Dailymotion hosts more videos you can watch in several lives, and more are added as we speak. Among all these choices, how can you find the best ones for you? That’s the job of a recommender which automatically presents videos curated to your interests.
Why did we rethink the mobile video recommender?
Use cases drive the existing recommenders on the dailymotion.com website, as most Web users are anonymous. Therefore, the priority is to suggest videos to watch after the current one.
On the native applications, all users are required to log in to use the app, providing an opportunity to display personalized content. Mobile app usage patterns are also different. For instance, users may like to watch short videos on the Dailymotion app while commuting.
How to deliver in a short time?
At that time, the application’s user interface was undergoing a major revamp, and we were changing several underlying APIs and event stores. Crafting something light allowed us to adapt quickly during the journey.
That’s why we decided to keep it simple and iterate fast. Deliver the most needed features first, observe user behavior changes, then repeat. Keeping the solution simple and iterating quickly led to remarkable results in a short time.
The ideal new home feed experience
The home feed is the first screen you see after launching the Dailymotion iOS or Android app. We expect users to “snack” videos by watching them directly on the home feed.
Together with the product team, we formulated the ideal recommender:
- Relevant & diverse: videos come from all the interests of the user.
- Variability of reward: different results at every app start and refresh of the home feed.
- Explainable: recommendations based on transparent features.
- Iterable: this first version should be easy to tune and extend.
Users are more likely to interact with the first results, so we present the most relevant at the top. Moreover, the recommender should ship quickly to receive rapid feedback.
Kickstarting the recommender
The performance of a recommender is usually evaluated on previously collected data. In this case, there were no appropriate historical user interactions to use.
We built a user interface in a notebook using Jupyter Widgets to inspect the results while constructing the recommender.
After each algorithm change, we could immediately see videos like a real user would and evaluate their relevance qualitatively.
Thanks to this, we could conveniently demo an early version to the stakeholders and collect their feedback to drive future improvements.
The Dailymotion’s recommender main components
The new recommender is made of two main parts:
Candidates: retrieve all videos which can be recommended.
Ranking: produce an ordered list of videos for a given user.
This is inspired by the two-stage approach used for Youtube recommendations. First, data analysts defined how to select candidates from quality partners. Then, machine Learning work focused on picking the right videos and assembling a list.
A rankers octopus
For the ranking part, the architecture builds on an extensible Ranker component with the following contract:
We coded several complementary rankers based on this simple Python class. Our final recommender is an ensemble of multiple rankers respecting the diversity of the user interests.
Fresh and best-performing videos
The Freshness & performance ranker selects videos by using several features:
- Freshness: users like watching recent videos, e.g., related to news headlines.
- Real views ratio: number of views lasting 10+ seconds divided by the total views count. Filter out accidental clicks and some clickbait videos.
- Watch ratio: time watched divided by the video duration. Videos with a high ratio tend to be more pertinent.
- Aspect ratio: prefer square and vertical image formats, which fit better on a mobile screen.
The performance ranker computes a weighted sum of these features. Coefficients are tuned by emphasizing freshness to keep learning how new videos can perform when presented to actual users.
Surface new content
Ranking videos only according to their performance leads to users always seeing the same content over and over.
Get Samuel Leonardo Gracio’s stories in your inbox
Join Medium for free to get updates from this writer.
To break this bubble and robustly learn how a video performs, we must give it a chance by showing it to a sample of people.
The Exploration ranker randomly pulls videos within the top 100 of the Freshness & performance and Featured videos rankers results. These videos have an equal chance of selection because all are relevant. This helps surface unseen content from the bottom of the list.
Always something new to watch for the users
One essential requirement is to show something new each time a user opens the app or refreshes the home feed. Discovering new videos is what ensures users keep coming back to Dailymotion.
The videos presented are different each time. The ones from the rankers are combined into a single list. Each ranker is assigned a probability to balance exploration versus historical performance.
“Show me videos from my interests”
New users indicate their interests when setting up their accounts as part of their onboarding process. Learning if they like Movies, Tech or Politics avoids the cold start problem.
However, not all interests have the same volume of uploaded videos. For instance, news and political videos are more frequent than cooking recipe videos.
We devised solutions to prevent some interests from filling up the recommendation slots and ensure we show videos from all the interests of a user.
In the candidate selection phase, the recommender groups videos by interest. Then, it selects a roughly equal number of videos from each interest. This method, named stratified sampling, helps us deliver a balanced experience.
Moreover, to respect the diversity of a user interests list in the final videos list, we re-order them to alternate different topics:
- Compute a similarity score for each pair of videos based on their attributes
- Add the first video to the final list.
- Add the following video, less like those already added to the list.
- Repeat the previous step until the list is complete
Right content = happy users
Imagine for a second that we choose to optimize for money first. Placing advertisements on videos is a significant way to generate revenue. It could be tempting to promote the most-clicked videos to display more ads. But that would often result in low-quality content (clickbait) and a bad user experience.
A healthier goal is to help users in finding exciting content every time.
We optimized watch time per user on the home feed, a measure for engaging content. In this case, we use the median watch time per user, which has many advantages:
Robust to outliers: the median roughly ignores exceptionally long watch times.
Robust to clickbait videos: these videos have a short watch time; users often click on the video and then stop.
More retention and better experience: videos with a good watch time are the videos that have the highest entertainment potential
Download the app on Google Play or App Store and try it yourself! (France only as of writing)
This is only the beginning. What’s next for you?
Our journey is far from over, and we have already identified several improvements:
More personalization: we based recommendations on user interests in this first release. The following version will integrate more users’ actions: watch history, likes, channels’ subscriptions…
Present even more relevant videos to first-time users who had no previous interactions.
Would you like to be part of upcoming meaningful Data and AI products at Dailymotion? Check our open positions.
The video recommender was developed by Denis Angilella and Samuel Leonardo Gracio, Machine Learning engineers at Dailymotion, in collaboration with the Product teams. Denis Angilella and Samuel Leonardo Gracio also co-authored the article.
