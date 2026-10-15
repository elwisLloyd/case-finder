# Fighting Spam using Clustering and Automated Rule Creation

Источник: https://medium.com/pinterest-engineering/fighting-spam-using-clustering-and-automated-rule-creation-1c01d8c11a05

Fighting Spam using Clustering and Automated Rule Creation
Cathy Yang | Software Engineer, Trust & Safety
One of our biggest priorities at Pinterest is keeping Pinners safe, and that includes protecting them from spam. The Trust & Safety team’s goal is not only to catch spam, but to remove it as quickly as possible to minimize Pinner impact.
The goal of spammers is to make money, and the best way to do this is to spam at scale. It’s a numbers game: one million spam emails are much more effective than one spam email. In order to remove spam quickly, we look at common trends in spam attacks to identify suspect behavior.
To achieve the scale required to be effective, spammers must automate their actions, and each of these “attacks” can be thought of as a cluster. Each event within the attack cluster may share some common features, but different clusters will have a different set of common features.
For example, during an attack where a large number of Pins are created, a spammer might point all Pins to the same domain. While the domain may change between attacks, spammers are still trying to direct traffic to the same spam site.
One of our spam mitigation tactics is our rule engine, Guardian, which helps to identify common features in spam attacks.
Motivation
Previously, when a spam attack happened:
- An alert would fire in our system statsboard, and an on-call analyst would investigate
- The analyst would identify the common trends of that attack
- The analyst would create a “patch rule” (a specific and temporary rule to address the attack) then apply it retroactively to catch old and future spammers
This process was problematic for many reasons: it was very manual for the analyst, there was a delay between the spam attack and our response, and it was a potential negative impact to Pinners.
However, what if we could automatically detect the bulk actions from spammers, find the shared common features within each cluster, create those patch rules, and catch these kinds of spam attacks?
Patch Rule
Patch rules are intended to be short lived and highly specific to an attack. The following is an example of a patch rule designed to deactivate spam users that:
- Are new accounts
- Are creating Pins with an Android device
- Begin the Pin descriptions with text “Check out our website”
This rule would be very effective in catching the spam attack and unlikely to impact any good users. In GSQL, our custom variant of SQL, the rule looks like this:
Guardian makes it pretty easy to create SQL-like rules. Just by using the where clause, we can deactivate users with those conditions. To automate the creation of such a rule, we only need to focus on the where clause, or the conditions, of the user deactivation.
As mentioned above, most simple attacks have some common features even though they are using different accounts. Thus, our goal is to extract the common features from a set of users.
Anomaly Detection and Clustering
One of the tactics to detect bursts of activity in spam attacks is time-series anomaly detection. Anomaly detection is good for detecting spiky activities (like the ones in Figure 1) which are highly likely to be spam activity.
At Pinterest, we have an internal real-time anomaly detection system. We will provide the model with a time series of events from which the model can learn. If the model’s expected value is different from the actual value by a certain threshold, there’s an anomaly.
However, if we do anomaly detection on the time series of all events with all features, there would be too much noise with normal user activity, and the burst might be neglected by anomaly-detection algorithms.
Instead, we alert on certain event types with certain features. For example, to alert on Pin creation events, we might do anomaly detection on IP address, Pin details, geo location, or some other features. The goal here is to narrow down the events that we want to cluster on without introducing too much noise from normal user activities.
Take Pin creation time series divided by city as an example:
Yellow line: model expected count per hr
Blue line: actual Pin creation event count per hr
Get Pinterest Engineering’s stories in your inbox
Join Medium for free to get updates from this writer.
The graph on the left shows the number of Pin creation events was at almost 0 for quite a long time before suddenly spiking. Since the count spiked so much compared to the moving average, our anomaly detection algorithm told us that Pin creation events from that town during that time period were highly suspicious. That narrowed our focus to the events during that time. We then gathered the relevant data and stored it in S3 to do further clustering.
Clustering
The goal within analyzing the data we store in S3 is to find users that share a certain pattern, as they are very likely coming from one spam campaign. The idea is:
- Group by one feature of interest: if we group by domain, we will have group google.com, group instagram.com, group something.gr, etc.
- For each group, we look at the value distribution of all other interest features
- If there are features that have dominant values (such as 95% of IPs in the group are 1.1.1.1), we know there is a cluster
We see a lot of spammers trying to direct Pinners to their website by creating multiple Pins that link to their own domains. In the following example, let’s consider looking at a Pin’s domain as the feature we’re interested in:
- Anomaly detection tells us that today, starting at 13:00, city A has an anomaly
- We query and get all the data during that time span, then group by domain (ab123.blogspot.com; bc456.blogspot.com; something.gr; google.com; Instagram.com; Other domains)
- For each domain, we calculate the data distributions of several other features such as IP, account age, and Pin details. Then we will know how often each value occurs under that feature.
For domain ab123.blogspot.com:
Compare the results above with a known trustworthy domain, like Google.com:
4. Google.com is a trustworthy domain; all interested features have good random distributions. However, domain ab123.blogspot.com has three dominant features:
5. Now we can create a rule with all the conditions we have using GSQL, our query language, to write rules in Guardian:
6. Some other criteria might also be helpful in reducing false positives, such as only creating the rule when > 10 users meet the criteria, or only when they’ve created more than 100 Pins. We can also make the group by condition be a regex pattern, such as ‘^[a-zA-Z]+[0–9]+[.]blogspot[.]com$’, instead of an exact domain.
Evaluating the Results
Agent review
It’s rare for normal users to have a similar pattern in a certain time span, but there’s still a possibility that the users are good if the cluster size is not very big. To reduce the impact of any false positives, we send sampled users we clustered to PinQueue, our in-house content review tool, so an agent can evaluate the rule’s accuracy before we turn it on and allow it to act autonomously on users.
Create the rule in Guardian
Once we’re confident that the rule’s accuracy meets our standards, we add it in Guardian.
Archive after a certain amount of time
Since these rules are intended to be temporary mitigations of specific spam attacks, we archive the patch rule after a certain amount of time — usually after we see that the attack has died down. Not only is this a matter of good housekeeping, but it also limits the exposure of any false positives. In the future, there might be a good user who meets all these conditions and gets accidentally deactivated by the patch rule if we don’t archive it.
Spammers will mutate, but we can automatically create new patch rules!
When spammers find out that using this IP is not working anymore, they will surely mutate by purchasing other IPs or other domains to try again. But as long as there are some patterns, we can automatically create new patch rules.
Summary
With anomaly detection, clustering, and auto rule creation, we can now react fast, detect most of the naive spam attacks, and then take action on them. Below, Figure 4 shows an overview of the process:
Acknowledgements
This blog post is made possible with a lot of help from Harry Shamansky and Kate Flaming. Thanks to Jiaqi Gu for developing the anomaly detection system. Also, thanks to Preston Guillory, Hongkai Pan, Rundong Liu, Alok Singhal, Dennis Horte, Carmen Dekmezian, Weiqi An, Yuanfang Song and the rest of our very own Trust & Safety team for their help and suggestions!
To learn more about engineering at Pinterest, check out the rest of our Engineering Blog, and visit our Pinterest Labs site. To view and apply to open opportunities, visit our Careers page.
