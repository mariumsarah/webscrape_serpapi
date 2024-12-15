#!/usr/bin/env python3
# pip install selenium
"""
Script Name: webscraping.py
Description: Web Scrape business Reviews
Author: Sarah Marium
Date: Dec 2024
"""



# #pip install serpapi
# # import os 
import json
from serpapi import GoogleSearch
import requests
import re 
import pandas as pd 
def serpapi_run(engine,q): # 7 search per company 
    if engine == 'google':
        params = {
            "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
            "engine":"google",
            "q":q
        }
    elif engine == 'yelp_place':

        params = {
            "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
            "engine":"yelp_place",
            "place_id":q
        }
    elif engine == 'yelp_reviews':

        params = {
            "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
            "engine":"yelp_reviews",
            "place_id":q,
            "num":"49"
        }
    elif engine == "google_maps":
        params = {
            "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
            "engine":"google_maps",
            "q":q
        }
    elif engine == "google_maps_reviews":
        params = {
            "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
            "engine":"google_maps_reviews",
            "data_id":q
        }

    search = GoogleSearch(params)
    return search.get_dict()


def main(): 


    # --------------------------------------------------------------
    # Store Review Results in Database 
    # --------------------------------------------------------------
    # Step 1: Create an empty DataFrame
    columns = ["Company Name", "data_id", "type", "service_options", "Overall Rating",
           "Overall Address", "Overall Reviews", "parameter", "place_id", "Review",
           "Engine", "Rating", "date", "User Name", "User Friends", "User Photos",
           "User Reviews", "User Likes"]

    # Create an empty DataFrame with the defined columns
    df = pd.DataFrame(columns=columns)

    # List of all companies 
    company_name_list = ["Precision Home Pros Austin TX","United State Solutions Hollywood FL","United State Solutions Hollywood FL"] #input()
    
    counter_top = 0
    # FOR EACH COMPANY ADD TO THE DATAFRAME 
    for company_name in company_name_list:
        print('Company Name: '+company_name)
        # Get the name on Yelp from GOOGLE SEARCH API : 
        yelp_search_param = ''
        link_found_yelp = ''
        for x in serpapi_run('google',company_name)['organic_results']: 
            if 'www.yelp.com' in x['link']:
                link_found_yelp = x['link']
        yelp_search_param = link_found_yelp.split('/')[-1]

        # Get the Yelp PLACE ID from YELP PLACE API :
        results = serpapi_run('yelp_place',yelp_search_param)
        place_id = results['place_results']['directions'].split('/')[-1]
        yelp_reviews = str(results['place_results']['reviews'])
        yelp_ratings = str(results['place_results']['rating'])
        yelp_address = str(results['place_results']['address'])
        #print(results['place_results'])
        yelp_categories = "" #str(",".join([x['title'] for x in results['place_results']['categories']]))

        # Get all YELP REVIEWS
        retrieved_dict = serpapi_run('yelp_reviews',place_id)
        length_of_reviews = len(retrieved_dict['reviews'])
        print("YELP")
        for x in range(length_of_reviews):
            print(counter_top)
            df.loc[counter_top] = ({"Company Name": company_name,"data_id":"","type":yelp_categories,"service_options":"","Overall Rating":yelp_ratings,"Overall Address":yelp_address,"Overall Reviews":yelp_reviews,"parameter":yelp_search_param,"place_id":place_id , "Review": retrieved_dict['reviews'][x]['comment']['text'] , "Engine": "Yelp","Rating":str(retrieved_dict['reviews'][x]['rating']),"date":str(retrieved_dict['reviews'][x]['date']),"User Name":str(retrieved_dict['reviews'][x]['user']['name']),"User Friends":str(retrieved_dict['reviews'][x]['user']['friends']),"User Photos":str(retrieved_dict['reviews'][x]['user']['photos']),"User Reviews":str(retrieved_dict['reviews'][x]['user']['reviews']),"User Likes":""})
            counter_top+=1
        # GET data_id from GOOGLE MAPS :
        retrieved_dict = serpapi_run('google_maps',company_name)
        type =(retrieved_dict['place_results']['type'])
        service_options =""# (retrieved_dict['place_results']['service_options'])
        google_reviews_data_id = (retrieved_dict['place_results']['data_id'])
            
        # GET GOOGLE REVIEWS  :
        retrieved_dict = serpapi_run('google_maps_reviews',google_reviews_data_id)
        rating = str(retrieved_dict['place_info']['rating'])
        address = retrieved_dict['place_info']['address']
        reviews = str(retrieved_dict['place_info']['reviews'])
        print("GOOGLE")
        counter = 0
        for x in retrieved_dict['reviews']: 
            print(counter)  
            df.loc[counter_top] =({"Company Name": company_name,"data_id":google_reviews_data_id,"type":type,"service_options":service_options,"Overall Rating":rating,"Overall Address":address,"Overall Reviews":reviews,"parameter":company_name,"place_id":"" , "Review": x['snippet'], "Engine": "Google","Rating":str(x['rating']),"date":x['date'],"User Name":x['user']['name'],"User Friends":"","User Photos":"","User Reviews":str(x['user']['reviews']),"User Likes":str(x['likes'])})
        
            counter+= 1
            counter_top+= 1
        next_page_token = retrieved_dict['serpapi_pagination']['next_page_token']
        if counter <= 40 and not retrieved_dict['serpapi_pagination']['next_page_token'] == '':
            params = {
                "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
                "engine":"google_maps_reviews",
                "data_id":google_reviews_data_id,
                "num":"20",
                "next_page_token": next_page_token
            }

            search = GoogleSearch(params)
            retrieved_dict = search.get_dict()
            next_page_token = retrieved_dict['serpapi_pagination']['next_page_token']
            for x in retrieved_dict['reviews']: 
                print(counter)
                df.loc[counter_top] =({"Company Name": company_name,"data_id":google_reviews_data_id,"type":type,"service_options":service_options,"Overall Rating":rating,"Overall Address":address,"Overall Reviews":reviews,"parameter":company_name,"place_id":"" , "Review": x['snippet'], "Engine": "Google","Rating":str(x['rating']),"date":x['date'],"User Name":x['user']['name'],"User Friends":"","User Photos":"","User Reviews":str(x['user']['reviews']),"User Likes":str(x['likes'])})
            
                counter+= 1
                counter_top+= 1

        if counter <= 40 and not retrieved_dict['serpapi_pagination']['next_page_token'] == '':
            params = {
                "api_key":'eaf876cc57a439c6ac7dc9e97791c3e8bd959f2c79e8ac1b1ef414a53f90f230',
                "engine":"google_maps_reviews",
                "data_id":google_reviews_data_id,
                "num":"20",
                "next_page_token": next_page_token
            }

            search = GoogleSearch(params)
            retrieved_dict = search.get_dict()
            for x in retrieved_dict['reviews']: 
                print(counter)
                df.loc[counter_top] =({"Company Name": company_name,"data_id":google_reviews_data_id,"type":type,"service_options":service_options,"Overall Rating":rating,"Overall Address":address,"Overall Reviews":reviews,"parameter":company_name,"place_id":"" , "Review": x['snippet'], "Engine": "Google","Rating":str(x['rating']),"date":x['date'],"User Name":x['user']['name'],"User Friends":"","User Photos":"","User Reviews":str(x['user']['reviews']),"User Likes":str(x['likes'])})
                counter+= 1
                counter_top+= 1

    df.to_csv('output.csv', index=False)

    print("DataFrame has been exported to 'output.csv'")
        
if __name__ == "__main__":
    main()


# #     with open("data.json", "r") as file:
# #         retrieved_dict = json.load(file)
# #     all_links = retrieved_dict['organic_results']
# #     link_found_bbb = ''
# #     for x in all_links: 
# #         if 'www.bbb.org' in x['link']:
# #             link_found_bbb = x['link']
# #     print("BBB Link found "+link_found_bbb)

# #     driver=webdriver.Firefox()
# #     source=0
# #     driver.get("https://www.bbb.org/us/wa/seattle/profile/ecommerce/amazoncom-1296-7039385/complaints")
# # time.sleep(5)