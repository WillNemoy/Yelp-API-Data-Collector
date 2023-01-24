import os
from dotenv import load_dotenv
from pprint import pprint
import json

from yelpapi import YelpAPI
import pandas as pd
import numpy as np

from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS






def yelpAPI(YELP_API_KEY_parameter, search_term, location_parameter):

    nlp = English() # Load English tokenizer, tagger, parser, NER and word vectors
    
    with YelpAPI(YELP_API_KEY_parameter, timeout_s = 3.0) as yelp_api:
        data = yelp_api.search_query(term=search_term, location=location_parameter, limit=50)

        all_reviews = []
        places_data = data["businesses"]

        for place in places_data:
            place_review_data = yelp_api.reviews_query(id=place["alias"])
            all_reviews.append(place_review_data)

    
    #Sheet 1 - businesses
    df = pd.DataFrame(places_data)

    df = df.reset_index()

    def city(x):
        city = x["city"]
        return city

    def zip_code(x):
        zip_code = x["zip_code"]
        return zip_code

    df["city"] = df["location"].apply(lambda x: city(x))
    df["zip_code"] = df["location"].apply(lambda x: zip_code(x))

    def lat(x):
        latitude = x["latitude"]
        return latitude

    def long(x):
        longitude = x["longitude"]
        return longitude

    df["latitude"] = df["coordinates"].apply(lambda x: lat(x))
    df["longitude"] = df["coordinates"].apply(lambda x: long(x))


    #Sheet 2 - Business Categories
    df_sheet2 = df[['index', 'categories']]

    categories_list = []
    for i in range(len(df_sheet2)):
        for x in range(len(df_sheet2['categories'].loc[i])):
            categories = [i, df_sheet2['categories'].loc[i][x]['title']]
            categories_list.append(categories)
            
    df_sheet2 = pd.DataFrame(categories_list)
    df_sheet2 = df_sheet2.rename(columns={0:"Business Id", 1:"Categories"})

    

    #Sheet 3 - Reviews
    df_reviews_draft = pd.DataFrame(all_reviews)

    reviews_id_list = []
    ratings_list = []
    text_list = []
    i = 0
    
    for three_reviews in df_reviews_draft["reviews"]:
        for review in three_reviews:

            reviews_id_list.append(i)
            ratings_list.append(review["rating"])
            text_list.append(review["text"])

            i += 1

    df_sheet3 = pd.DataFrame({'Id': reviews_id_list,
                       'Rating': ratings_list,
                       'Review': text_list})

    #Sheet 4 - Reviews Words
    
    #turn a review's text into a list and remove grammer and non-letter/non-numbers
    def prepareReviewText(reviewListNumber):

        reviewTextString = str(yelp_reviews_list[reviewListNumber].getText())

        #replace ... and \n
        reviewTextString = reviewTextString.replace("\n"," ")
        reviewTextString = reviewTextString.replace("..."," ")


        #remove non-letters and non-numbers
        newReviewTextString = ""
        for character in reviewTextString:
            if (character.isalnum() 
                or character == " " 
                or character == "#" 
                or character == "'" 
                or character == "-"):

                newReviewTextString += character.lower()

        reviewTextList = newReviewTextString.split()

        reviewTextKeywords = []

        for word in reviewTextList:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False:
                reviewTextKeywords.append(word) 

        return reviewTextKeywords
    
    #create a class and list of the Yelp data
    class yelpReview:
        def __init__(self, idParameter, ratingParameter, textParameter):
            self.id = idParameter
            self.rating = ratingParameter
            self.text = textParameter

        def getId(self):
            return self.id

        def getRating(self):
            return self.rating

        def getText(self):
            return self.text

    yelp_reviews_list = []

    for i in range(len(reviews_id_list)):
        yelp_review = yelpReview(reviews_id_list[i], ratings_list[i], text_list[i])
        yelp_reviews_list.append(yelp_review)
    
    #create the review words df
    data_list_for_df_reviews = []

    for i in range(len(yelp_reviews_list)):
        listOfWords = prepareReviewText(i)
        for x in range(len(listOfWords)):
            data_entry = []

            id = i
            word = listOfWords[x]
            
            data_entry.append(id)
            data_entry.append(word)
            
            data_list_for_df_reviews.append(data_entry)
            
    df_sheet4 = pd.DataFrame(data_list_for_df_reviews, columns=["Id", "Review Words"])

    
    
    #to an Excel file!
    excel_file_name = "Yelp Data" + ", " + location_parameter + ", " + search_term + ".xlsx"

    with pd.ExcelWriter(excel_file_name) as writer:  
        df.to_excel(writer, sheet_name='Data')
        df_sheet2.to_excel(writer, sheet_name='Categories')
        df_sheet3.to_excel(writer, sheet_name='Reviews')
        df_sheet4.to_excel(writer, sheet_name='Review Words')
    
    
    
    

#run the function
load_dotenv() #look in the ".env" file for env vars

YELP_API_KEY = os.getenv("YELP_API_KEY")

user_search_term = input("What type of businesses are you interested in? ")
user_location = input("What area should we focus on? ")

yelpAPI(YELP_API_KEY, user_search_term, user_location)


#https://www.analyticsvidhya.com/blog/2019/08/how-to-remove-stopwords-text-normalization-nltk-spacy-gensim-python/
"""
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = English()

text = "He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and 
fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had 
indeed the vaguest idea where the wood and river in question were."

#  "nlp" Object is used to create documents with linguistic annotations.
my_doc = nlp(text)

# Create list of word tokens
token_list = []
for token in my_doc:
    token_list.append(token.text)


# Create list of word tokens after removing stopwords
will_test = ["this", "is", "my", "list", "of", "words"]
filtered_sentence =[] 

for word in will_test:
    lexeme = nlp.vocab[word]
    if lexeme.is_stop == False:
        filtered_sentence.append(word) 

print(will_test)
print(filtered_sentence)
"""
