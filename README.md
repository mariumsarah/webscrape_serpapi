# Description: Companies Review Scraping with SerpApi

Objective: Given a list of company names, scrape reviews from Yelp and Google. 

Overview: This project focuses on using SerpAPI and utilize 7 searches to per company to append into a dataframe all reviews coming in. 

Key Steps:

1.Data Frame Creation:

Create a dataframe to store all the review info, user info, and company info. 

2. API Searches to find the right Company:

  Complete a Google Map Search to find the right place_id for the company being looked up. 
  Complete a Yelp Search API to find the right data_id for the company being looked up.
  
3. Store Reviews in Dataframe:

  Loop through each review in Google and Yelp Reviews found and append into the dataframe created. 
  In Google Reviews, a single page has maximum of 20 reviews. 3 Loops were used to get 50-60 reviews per company. 
  In Yelp Reviews, a single page can get maximum od 49 reviews. 1 Loop is used to get a maximum of 49 reviews. 

4.Model Training and Validation:

Split the dataset into training and testing sets using stratified sampling to maintain the class distribution.
Implemented GridSearchCV with Stratified K-Fold cross-validation to tune hyperparameters and select the best model configuration.
Evaluated the model using metrics such as accuracy, precision, recall, and F1-score.
