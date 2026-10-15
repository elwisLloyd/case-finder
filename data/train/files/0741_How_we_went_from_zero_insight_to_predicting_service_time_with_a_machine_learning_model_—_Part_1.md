# How we went from zero insight to predicting service time with a machine learning model — Part 1

Источник: https://medium.com/oda-product-tech/how-we-went-from-zero-insight-to-predicting-service-time-with-a-machine-learning-model-part-1-516b9545d02f

How we went from zero insight to predicting service time with a machine learning model — Part 1
This is the first of two blog posts in this series
When I started as a Data Analyst in Oda (then Kolonial.no) in November 2019, one of the first tasks I was asked to help out with was to improve the way we set the planned service time.
Before I continue, let me just explain how we define service time in Oda:
Service time is basically the non-driving time a driver spends serving customers on his or her route.
Service time includes the time spent to find a place to park, picking and scanning of the order, delivering the order, maybe some tidying in the van, and any other activities before the driver starts driving to the next customer on the route.
Service time makes up around 50% of the total time spent on our routes, which means it’s really important that we plan for a realistic amount of time.
It’s important for many reasons:
- It affects our customers’ experience through our ability to deliver on time and to tell them precisely when we will arrive
- It affects the stress level of our drivers, which again affects their wellbeing, sick leave, accident rate and turnover
- It affects our distribution cost and profitability, since unnecessarily long service times result in inefficient routes.
But let’s go back to the task I was given by the Product Manager in my team when I joined Oda, Mike:
“Can you find a way to improve how we plan for service time?”
Well, of course I could try to help, and it didn’t sound like that big of a challenge, to be honest. We basically planned for seven minutes with each customer, with some adjustments. It was kind of a given that there were only potential upsides here.
There was just one problem: we didn’t have any (good) data on the service time we actually spent serving each customer. So we didn’t have much insight into whether the planned service time was a good or bad approximation. However, feedback from our drivers and our KPIs clearly indicated there was room for improvement.
So we either had to utilize the data we already had and try to make a good proxy for the service time spent on each customer, or we had to find a better way to measure it.
Choosing the geofencing technology
By investigating the data we already had, it became clear that we needed more data points to get a better picture of the service time spent.
I was put on a team with a software engineer, Magnus, and together we evaluated several alternatives. Some of them were:
- Continuous GPS tracking
- More buttons for the drivers to press when delivering orders (giving us more data points)
- Timestamps from Google Maps/direction apps the drivers use
- Geofencing
We evaluated the pros and cons of each alternative, and concluded that utilizing geofencing to measure service time would most likely give us a good proxy for the service time spent with affordable effort from our software engineers. It would also be much less intrusive to our drivers’ privacy than, for instance, continuous GPS tracking, and it would not provide the drivers with any extra work in the form of extra buttons to push.
Geofencing is actually the technology used in Pokémon Go.
Get Siri Bruskeland’s stories in your inbox
Join Medium for free to get updates from this writer.
A geofence is a virtual way of representing a real geographic area. Typically, it can be a circle around the GPS coordinates (longitude and latitude) of a specific address, and the radius of the circle (geofence) can be set to a desired size.
By using geofencing, we could get a time stamp for when the driver enters the geofence around a customer, and when they exit it again.
But before we started to build anything, we wanted to:
- Test the technology on some of our routes to see if it was a good proxy of the service time; and
- Involve our drivers as early as possible so that we were sure they felt comfortable with this solution.
Testing geofencing for our purpose
There are a lot of applications out there using Geofence technology. Many of them are targeted to parents that want to monitor where their kids are. I found an app called EgiGeoZone in Google Play that I downloaded to one of the Zebra devices that our drivers use. With this app I could add the latitude and longitude of customers we were going to deliver to on a route, enter a geofence radius of minimum 50 meters, and then bring the Zebra with me on a route to check how the stored timestamps matched the service times I manually registered for each customer. The timestamps matched the manually measured service times really well, and as long as we found a way to handle edge cases (like situations where the driver passes a geofence on their way to another customer, or situations where two or more customers are located within the same geofence, and so on), we believed geofencing could give us a very good proxy of the actual service time spent on routes.
Involving our drivers and ensuring their privacy
As I mentioned, we involved the drivers before we built anything. We also included in-house privacy experts so we could make sure everything we did was compliant with privacy laws. It was really important to us that our drivers felt comfortable being monitored when they cross a geofence.
We had several meetings with the drivers, and we sent them information about the solution with clear statements of what we would use the data for, and more importantly, what the data would not be used for:
We also made sure the timestamps would only be stored in the production database for 30 days, and that we in the analytical database only would store durations, since that’s what’s relevant for predicting service times.
Together with the drivers, we sketched a solution they felt comfortable with, which probably saved us a lot of work had we started building the solution before we involved them.
Building a solution we truly believed would create value
After this Magnus, the software engineer, started to build the solution. We tested it early on by having me join routes. I compared the geofence service times to the actual service time that I measured using a stopwatch. This way, we got an impression of the quality of the timestamps, and also which edge cases we needed to handle.
The results were promising and we kept improving the solution until we thought it was good enough.
Once we got service time data in place, we could start to improve how we set the planned service time. With simple methods, we could investigate how much different variables seemed to impact the service time, such as:
- floor number
- presence of an elevator
- number of boxes to deliver
- the weight of the order, etc.
Based on this data, we were able to make adjustments to improve the situation even before the data scientist started to work their magic. This manual prediction of service time actually turned out to be a pretty good estimation.
Even so, we wanted to get even better at predicting our planned service time. In part two of this series, Tarjei, our data scientist, will talk about the work he’s done to build a machine-learning model to predict service time.
Read the article here.
