# Behind the scenes of Canva's DesignDNA campaign

Источник: https://www.canva.dev/blog/engineering/behind-the-scenes-of-canvas-designdna-campaign/

Machine Learning
Behind the scenes of Canva's DesignDNA campaign
How we used generative AI to build our year-in-review campaign
DesignDNA was Canva's year-in-review campaign launched in December 2024. We wanted to create a memorable, shareable experience for our Canva Community, which celebrates their achievements in Canva over the past 12 months.
We challenged ourselves to use this opportunity to showcase Canva's AI capabilities. We wanted to leverage generative AI to create a personalized and engaging experience that users could easily share on social media and spark a sense of accomplishment and connection with our brand.
This blog post delves into the campaign design process and highlights how we used generative AI to deliver a personalized and engaging experience to millions of Canva users.
Privacy
When generating the year-in-review designs for users, we adhered to Canva's strict internal policies to protect user information. Respecting user privacy is incredibly important to us. We are committed to handling our user's data with the utmost care and transparency. For more detailed information about how we collect, use, and protect user data, see Canva's Privacy Policy(opens in a new tab or window).
The vision
By analyzing millions of searches, favorite elements, and trending templates, our design team pinpointed patterns that revealed the most exciting directions for the coming year. Launched as Canva's 2025 Design Trends(opens in a new tab or window), we forecast 7 emerging design trends and released them as fresh, ready-to-use templates.
We wondered if we could use this information in our end-of-year campaign to create a moment of surprise and delight for our users? What if we could use AI to be a matchmaker and predict a user's emerging design trend?
Thus, we formed our idea for DesignDNA: a year-in-review campaign to celebrate our community's achievements over the past year and to provide a unique, personalized experience that resonates with our users by leveraging generative AI to create content that reflects users' design journeys and aligns with their emerging design trends.
And that's what we did. We matched our users to one of the 7 design trends and used generative AI to create bespoke copy and imagery reflecting their design behaviors in Canva.
The building blocks of DesignDNA
To kick off the campaign, we needed to identify our target audience. Given the campaign related to design behavior, we selected our target audience based on a minimum threshold of user design activity and engagement levels on Canva in the past year, and the user's consent for us to personalize our marketing communications to them.
From there, we gathered data to build each user's personalized DesignDNA. Our intent for DesignDNA was to create a shareable social media story that conveyed specific information across the following pages:
- Page 1: The number of total designs created by the user.
- Page 2: The user's top design type.
- Page 3: A fun poem based on the user's top design styles.
- Page 4: The user's design personality based on their top design themes.
- Page 5: Revealing the user's emerging design trend.
For this, we needed the following 6 key pieces of information that we could use as the building blocks to create the DesignDNA for each user:
- User locale
- Number of designs created
- Design type ranking
- Design personality
- Design poem
- Emerging design trend.
Following our data and privacy policies, for users who allowed their data to be available for personalized marketing purposes, we could retrieve a user's locale, the total number of designs they created, and infer their top-created design type (for example, "Presentations").
However, understanding the user's top styles and themes from their design activity and using them to infer their design trend and personality was a bit more complicated. To ensure privacy compliance, accessing personal Canva designs is strictly off-limits. So, how did we predict a user's top styles or themes for the past year?
Although we couldn't access personal design content, Canva has a vast library of public templates users use. These templates are tagged with style and theme metadata (you can even search by these in the Marketplace!). So, we used this template metadata to infer the user's top themes and styles. We then used these to match a user to a design trend and design personality.
Determine a user's design trend
Our Content Creative team defined each design trend by a set of keywords. The template metadata also contains style and theme keywords, so our first step was to trial a keyword-matching approach. We developed an algorithm to give each user a score for each design trend based on the keywords that matched the design trend from the templates they had used. The highest-scoring design trend would be considered the user's emerging design trend for 2025.
Using this approach, we matched 95% of the users in our target cohort to a design trend.
To find a design trend match for the remaining 5% of users, we iterated on the existing keyword-matching method by curating a list of the most commonly appearing template keywords in our user base that didn't directly match a keyword for a design trend. Then, for each design trend, we used generative AI to expand the set of keywords in each trend and select the most contextually relevant keywords from our curated list. We did this to optimize our matching process and make sure we weren't matching against new words that had no chance of being in the template usage dataset of the remaining 5%.
Using this approach, we matched 99% of the users in our target audience to a design trend. The remaining 1% of our users had too few designs created using templates and hence could not be matched due to the limited template usage information available.
Determine a user's design personality
Next, we analyzed each user's design personality. But, what is a design personality?
We categorized our community into 10 audience groups based on the most frequent themes in the templates they've used throughout the year or their user journey. Example audience groups could be "Celebrations" or "Innovation".
We created personality segments defined by each design trend and audience group combination. For example, the trend "Analog meets AI" combined with the audience group "Teacher (Education)" would be a personality segment for teachers who used AI.
We then used Magic Write for each segment to define a design personality name and description, translating the content for different locales using AI. We used Canva's Dream Lab to generate a hero image that aligned with the content of the design personality. These were our design personalities.
Each design personality had an associated list of keywords, so we used a keyword-matching approach similar to the one used to match design trends, but this time using just the themes of the user's most used templates to match them to a design personality.
Generate personalized poems
We also wanted personalized poems based on the user's top design styles. We retrieved the style metadata tags from the templates and aggregated this usage data to infer each user's top 3 design styles. This gave a good balance of identifying some unique style behaviors across users while making sure we weren't trying to include too much information into a short poem.
When considering both locales and the top 3 styles of users, we had just over a million different combinations. We couldn't manually write a million poems, but we could use generative AI to generate these poems at scale.
We created unique prompts for each locale and then provided the top 3 styles we wanted to generate a poem for. The result was a million generated poems across 9 different locales.
For our AI-generated content, a proper review process was critical to ensure what we were sending out to users was appropriate. Reviewing a million poems was impossible, but we took all reasonable steps to review the output.
Our review process consisted of:
- Asking our Localisation team to review a sample of poems generated in non-English locales. We took their feedback into account to help fine-tune our prompt for generating the poems.
- Flagging poems containing potentially sensitive words and using generative AI to help identify any poems with a negative tone.
We regenerated any poems flagged during the review process, repeating the review cycle until we had an appropriate alternative.
Putting it all together
With all the building blocks in place, our final task was to combine all the content to create a DesignDNA story for each user. In our data store we had all the required information:
- The user's locale.
- The total number of designs created by the user.
- Their top design type and relative ranking globally or within their country.
- Their design personality based on their top design themes.
- A poem based on their top design styles.
- Their emerging design trend.
In addition to this, we had base Canva templates for each of the 7 design trends. Canva has a feature that allows us to tag elements in a template. We can then dynamically replace these tagged elements with other content provided using URL parameters.
For each user, we added the tailored content to the URL and produced a link the user could access that would generate their personalized copy of the DesignDNA, with all the relevant generated content.
Conclusion
With 95 million unique DesignDNAs created, we released a personalized year-in-review campaign using Canva's generative AI tools to help us creatively tackle the problem of creating something tailored for each targeted user.
Acknowledgements
This campaign was a combined effort across Canva's Personalisation & Engagement, Lifecycle, Brand Marketing, Creative, Localisation, and Content & Discovery teams. Huge thanks to Christine Balili(opens in a new tab or window), Jeremy Sha(opens in a new tab or window), Nathan Shepherd(opens in a new tab or window), Kinsella Bruck(opens in a new tab or window), Maxim Radoczy(opens in a new tab or window), Maria Izvestkina(opens in a new tab or window), Renata Tupynamba(opens in a new tab or window), Simon Hammond(opens in a new tab or window) and everyone else involved.
