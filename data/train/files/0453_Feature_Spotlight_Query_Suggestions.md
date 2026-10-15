# Feature Spotlight: Query Suggestions

Источник: https://www.algolia.com/blog/product/feature-spotlight-query-suggestions/

Your users are spoiled. They’re used to Google’s refined and convenient search interface, so they have high expectations for yours. They expect it to be lightning-fast, they expect it to surface relevant and personalized results, and they expect to get query suggestions.
The problem is, while 80% of e-commerce sites have search integrations with query suggestions, only 19% are actually doing it right. Don’t worry though, Algolia’s got you covered. Since February 2018, we’ve been helping our customers use the data they’re already collecting to serve the most relevant autocomplete suggestions to their users.
The first step is to make sure that the data powering query suggestions is being collected in the first place. That’s accomplished largely by sending click and conversion events to Algolia’s servers as the searches are run. It’s fairly straightforward to implement if you’re using Algolia’s widget-based UI library InstantSearch. It comes in all sorts of flavors to fit your favorite framework, so it won’t stress out your developers too much 😊
Then, you’ll be creating a new index specifically for Query Suggestions. There are a couple ways of doing this, the simplest being through the dashboard. That’ll take you to a bunch of configuration options, including some tools to ban inappropriate suggestions. That’s a problem with which a lot of search implementations are plagued – too many users search for something not so nice and suddenly your users are getting racist, sexist, or otherwise unacceptable suggestions.
Algolia gives you all the tools you need to prevent this. You also get to decide how many results a query needs to be a good suggestion, something that could help reduce friction, especially on mobile devices.
Once everything is configured, the index will start to build itself, letting you focus on displaying the data it sends to the frontend. To dive deeper into the details I’m skipping over here for clarity’s sake, check out this tutorial section from the docs. In your app’s code, you’ll need to import the plugin that handles connecting Autocomplete with the Query Suggestions index you just created.
You can find a more detailed tutorial on that here, but your JavaScript is going to look like this:
import { autocomplete } from '@algolia/autocomplete-js';
import { createQuerySuggestionsPlugin } from '@algolia/autocomplete-plugin-query-suggestions';
const searchClient = algoliasearch('YOUR_APP_ID', 'YOUR_PUBLIC_API_KEY');
autocomplete({
     container: 'CSS_SELECTOR_OF_YOUR_AUTOCOMPLETE_CONTAINER',
     plugins: [
          createQuerySuggestionsPlugin({
                searchClient,
                indexName: 'YOUR_QUERY_SUGGESTIONS_INDEX_NAME'
          })
     ],
     openOnFocus: true
});
The key thing to notice here is the `plugins` array inside the autocomplete instantiation – that’s where we load in the Query Suggestions plugin, tie it to our new index, and let Algolia build the needed UI.
A lot of companies building with Autocomplete and Query Suggestions particularly love to include scoped, or category-specific, suggestions in the list. Notice how Amazon includes this, especially when suggesting you return to recent searches:
They let you pick queries by the category of product they belong to. They also include other filters directly inside the query suggestions box – while it might be displayed differently, it’s likely the same filtering setup under the hood:
These additions remove a ton of friction from the Amazon search experience. You can implement them in your application, too! Here’s an interactive demo of a codebase that’s running something similar, and a guide about adding categories (and other filters) directly into the search suggestions box.
The best part about it is that it’s not gated for only enterprise users either! Whether you’re pitching it to your managers at a Fortune 500 company or just tinkering for fun, you have the power to build classy, frictionless UIs with Algolia’s Query Suggestions.
Powered by Algolia AI Recommendations
