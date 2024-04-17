[DATS 6401 Visualization of Complex Data] Term Project - Name: Brian Kim
Analyzing and Predicting Customer Churn in Auto Insurance
Objective: To understand the key drivers of customer churn in auto insurance, I aim to
use Exploratory Data Analysis (EDA) and visualization techniques to identify the causes
of customer churn in car insurance.

Background:
The reason I chose this dataset is because I worked in South Korea at the insurance
company Carrier. I have experience working at a life insurance company. Analyzing the
causes of customer defection from an insurance company is a very important element in
insurance company management. Companies must retain customers and manage
customers who are likely to churn by predicting customer churn in advance. I would like
to use the skills I learned in class to implement the data visualization needed to predict
customer churn.

SMART Questions:
1. Based on data visualization and analysis, what are the three factors that most
significantly contribute to car insurance customer churn?
2. How does having children affect the likelihood of car insurance customer churn,
taking into account other factors such as age, income, marital status, etc.?
Data information: 1,048k Observations and 22 Features(Numerical 7, Categorical 15)

Plot Plan: Bar, Histogram, Scatter, Heatmaps, Pie, Geographic Map, Stacked Bar

Layout Plan for the interactive dashboard:
Display key metrics such as total customers, churn rate, and average tenure using
gauge charts with interactive hover details.
1. Demographic Insights: Use a histogram or box plot to show the age distribution of
customers, with interactive filters for churned and retained customers.Display a
histogram or box plot for income, with dynamic filters to view data by churn status.
Marital Status and Home Ownership: Present a stacked bar chart or pie charts with the
ability to click and drill down for more details.
2. Churn Analysis: Use bar charts to display churn rates across different categories like
marital status, has_children, and home_owner, with hover details for exact figures.
3. Geographic Insights:Provide a geographic map pinpointing customer locations,
color-coded by churn status

Data Reference:
https://www.kaggle.com/datasets/ameymore/insurance-churn-prediction-machinhack
