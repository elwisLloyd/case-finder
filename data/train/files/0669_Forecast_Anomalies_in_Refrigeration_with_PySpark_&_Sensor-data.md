# Forecast Anomalies in Refrigeration with PySpark & Sensor-data

Источник: https://medium.com/walmartglobaltech/forecast-anomalies-in-refrigeration-with-pyspark-sensor-data-195f23ae24e2

Introduction
Walmart, with its footprint across United States, sells billions of dollars worth of perishable goods annually. Most perishable goods are stored in refrigerator for freshness and longevity. To cater to customer needs and for the betterment of customer experience, refrigeration systems are moderated through remote setting configuration or maintained physically, reducing food waste, high temperature issues, mechanical failures etc.
The problem arises from the perspective of both scale and variety. There are around half a million refrigeration systems of different types, for eg., multi-deck freezer, walk-in freezer, coffin freezer etc. Each of these consists of different types of food (eg. meat, deli, frozen food, ice-cream etc.) and hence runs at different temperature settings. Maintenance at this scale, to avoid malfunctions, requires manpower and it’s time-consuming. Now, as The Flash is not up for hire, so we needed to figure out how best we can solve the problem of high number of simultaneous issues.
In this blog, I will talk about the framework we built to resolve the same.
Telemetry Sensor Information
A refrigeration has four important components : Compressor, Condenser Fan, Evaporator Fan & Expansion Valve. Loosely speaking, together they try to keep the pressure at a reasonable level so as to maintain the temperature within (Remember, PV = nRT). In Walmart, we collect sensor data for all of these components (eg. pressure, fan speed, temperature) at a 10minutes interval along with metrics like if the system is in defrost or not, compressor is locked out or not etc. We also capture outside air temperature as it impacts the condenser fan speed and in turn, the temperature.
Defrosts are very important as temperature goes higher than the default settings in these times to clear off the extra ice in system. If defrost is skipped, then winds of winter will create army of scary stale food. The characteristics related to defrost, for eg., peak defrost temperature, the time it takes to reach the peak and the time it takes to come back to normal temperature — all of these impact the overall health of the system.
Objective
The objective is to minimize the number of malfunctions and suggest probable resolutions of the same to save time. So, we leveraged this telemetry information in order to forecast anomalies in temperature, which would help in prioritizing issues and be proactive rather than reactive.
Data Preparation
We used the telemetry information for last two years and aggregated it on an hourly level from 10minute level. The reason being, the more granular the data is, the more noisy it becomes. Also, like every sensor information, this data is prone to missing and faulty sensor values. So, by aggregating on an hourly level, we tried to minimize the number of imputations for those. As we want to forecast anomalies in temperature, so, modeled temperature as a function of the features I have talked about in telemetry sensor information section and forecasted for the next 72hrs.
The challenge was we didn’t have the future values of any features except for outside air temperature. We used forecasts of air temperature from a third party vendor which were pretty accurate for the next 72hrs. Now, univariate forecasting or forecasting only with air temperature as a feature, could be one option but then, we will be losing information on changes in pressure or fan speed etc. So, for forecasting, we used lags of last 96hrs data and kept a rolling mean of every 6hrs as feature values. For example, if I want to forecast for 1st Jun at 12AM, I will use the average of values from 28th May, 7PM till 29th May, 12AM for a particular feature.
Modeling
We had experimented with different modeling techniques, starting with ARIMAX, then Bayesian Structural Time Series (BSTS) & Prophet. Details of these algorithms can be found here : ARIMAX, BSTS, Prophet. Code snippets are embedded for easy execution of the same.
Pseudo code for ARIMAX & BSTS in R:
library(dplyr)
library(forecast)
library(bsts) # df : dataframe consisting 'ds'(timestamp), 'y' and other exogenous variables
# future_df : dataframe consisting lagged feature variables for forecast ############# ARIMAX ############# Create ts object
train.ts <- ts(df$y, frequency = 24) # Fit & Forecast
fit <- try(auto.arima(train.ts,
xreg = as.matrix(df[, 3:ncol(df)]), seasonal=TRUE), silent = TRUE) if(inherits(fit, "try-error")){
print('Fit Failed')
}else{
# Forecast the model
fc <- forecast(fit,
xreg = future_df %>% as.matrix(), h = nrow(future_df))
y_hat <- fc$mean # forecasted value
} ############# BSTS ############### # ss: state space
ss <- AddLocalLinearTrend(list(), df$y)
ss <- AddSeasonal(ss, df$y, nseasons = 24) # Fit Model
setseed <- 2021
model_fit <- bsts(y~.,
state.specification = ss,
niter = 5000,
data = df[, 3:ncol(df)],
seed = setseed) #, expected.model.size = 5)burn_fit <- SuggestBurn(0.1, model_fit) fc_bsts <- bsts::predict.bsts(model_fit,
horizon = nrow(future_df),
newdata = future_df,
seed = setseed,
burn = burn_fit, quantiles = c(.05, .95))
future_df$bsts_yhat <- fc_bsts$mean
Prophet is the chosen one. Literally!! But in case you don’t believe in Prophet, have a look at the next section for the logic behind it.
Preliminary steps for imputation and multicollinearity checks had been taken care of. We had incorporated both daily and weekly seasonality for the hourly data that we were dealing with.
Each refrigeration system has a predefined favorable temperature band based on its type and food content. Suppose,
Get Riyanka’s stories in your inbox
Join Medium for free to get updates from this writer.
d1: difference of forecasts from the favorable temperature band, d2: difference from recent average temperature
If the recent temperatures were within the band, we measured the forecasts against d1, but if they are already running outside the band, then measured against d2. Forecasts are tagged as anomalies based on these differences when defrost is off (defrost on means high temperature anyway!). Defrost timings stay more or less the same so those time-points are excluded while generating anomalies.
Anomalies are prioritized based on magnitude of these differences and duration (in hrs) of being outside the band.
Model Selection
We had selected a sample of refrigeration systems with good data quality to assess different algorithms. Forecast MAPE on an average was around 4–6%, 2.5–4% & 3.5–5% for ARIMAX, BSTS and Prophet respectively. Usually we use accuracy measures for model selection but here we needed to consider other important factors as well.
In this case, the accuracy was as important as the execution time because we were handling daily forecasts of around half a million systems across ~3600 stores. As BSTS is dependent on MCMC sampling, so the run time was much higher than the rest with little improvement in accuracy. Hence, we dropped BSTS!
Another important aspect was to be able to provide a cause of the anomaly and not just the forecast. We do get a list of significant variables based on p-values in case of any model but it is dependent on whole training data and doesn’t focus on recent changes.
Prophet has a property called change-point detection, i.e., it allows the trend to change its direction through the course of time. Prophet detects change-points by first specifying a large number of potential change-points at which the rate is allowed to change. It then puts a sparse prior on the magnitudes of the rate changes (equivalent to L1 regularization) — this essentially means that Prophet has a large number of possible places where the rate can change, but will use as few of them as possible. More details here.
In the above figure, the vertical black lines are the change-points in temperature. It’s useful as it helps in notifying about any sudden change in temperature pattern. By default, Prophet specifies 25 potential change-points which are uniformly placed in the first 80% of the time series. These hyper-parameters can be changed through n_changepoints and changepoint_range.
Pseudo code for model change-point in Python:
from fbprophet import Prophet
# df : dataframe consisting 'ds'(timestamp), 'y' and other exogenous variables
# future_df : dataframe consisting lagged feature variables for forecast
# features : list of features to be included in the model after multi-collinearity checks # create an expression instead of including each regressor separately all_fea = [str(".add_regressor('") + str(features[i]) + str("')") for i in range(0, len(features))]
all_fea = ''.join(all_fea) # No need to put seasonalities separately.
# Prophet detects the frequency of the data itself
# If the frequency is less than daily, then it includes daily & weekly seasonality automatically exp = str("Prophet(changepoint_prior_scale = 0.05, changepoint_range=0.8)") + all_fea + str(".fit(df)") # Fit & Predictmodel_prophet = eval(exp)
fcst_all = model_prophet.predict(future_df) # It will contain yhat, trend, seasonalities
We have used the same characteristic to detect potential feature which may be the cause of this sudden change. So, each of the features separately will go through the Prophet model and search for recent change-points.
Whenever there’s any change in temperature pattern, we look for changes in the feature variables within a neighborhood of 2–3days and provide them as potential causes. Because of this in-built godly property, we chose Prophet over ARIMAX.
Validation
Model forecast accuracy on validation set was more than 90% for around 85% of the systems. But, to understand how well the model is diagnosing the anomalies, forecast accuracy wasn’t enough. So, we validated the anomaly detection performance through back-testing against the already registered malfunction issues. For back-testing, we used recall to understand how many of the actual issues the model could capture!
On an average, 67% of the times anomalies were getting forecasted accurately, in case recent historical temperature is within band, and 84% if it’s outside band. The later is higher because systems become more prone to be anomalous while running outside favorable temperature band.
Generated anomalies had also been validated by SMEs. This was required because not all anomalies are registered as malfunction issues. Some are minor issues which can be remedied by remote configuration changes.
Scaling & Deployment
Time to Assemble!! An automated framework has been built to generate the anomalies daily via batch processing. Used PandasUDF and parallelized it through PySpark (See here). From data extraction to model storage, Azure Cloud has been leveraged.
The front-end application has been deployed to Walmart Cloud Native Platform (WCNP).
Conclusion
Prediction and prioritization of anomalies streamlined the maintenance process considerably. But there’s still a lot of scope in terms of improving the effectiveness of the maintenance process itself. We are exploring ways to minimize resolution time of each issue and prevent recurring issues by identifying root causes of anomalies at the mechanical level and recommending right action to address the same.
References
Here’s few references on detailed Prophet equations and scaling with PySpark.
