import requests
import json
import time
import pdb
from statistics import mean
#pdb.set_trace()

####################################################
############# TO-DO ############################
####################################################

# Add A temp Config
# Finish Prediction Generator
# Start Django Rest API
# Start Django Site; Apps, Users, Main

###################################################


Bids = [] # Number of Bids
Top_20 = [] # First 20 Results
prices = [] # Price for all Listings

MinPrice = [] # Minimum Price for Listings
AvgPrice = [] # Average Price for Listings
HighestPrice = [] # Highest Price for Listings
SellThrough = [] # Sell Through Percentage

####################################################
############# Data Base ############################
####################################################



# DATABASE TO DO INTERNALLY IN DJANGO
# USERs, KEYWORD FLAGGED

    # KEY WORD EXAMPLE

    # Key_Word_Flag_Approved_Document = {
    #     Key_word: 'Test',
    #     Key_word_DesL: 'Flagged for EXAMPLE REASON',
    #     Key_word_Rating: '4', # 4/5
    # }
    #
    # Key_Word_Flag_Pending_Document = {
    #     Key_word: 'Pending',
    #     Key_word_Des: 'Flagged for EXAMPLE REASON',
    # }

####################################################
############# Key word Flagging ####################
####################################################

def keyword_flagging_Check(): # Checks if Current Keyword flagged

    return

def keyword_flagging_new(): # Create a new Kewword flag

    return

####################################################
############# Grabs Key Data #######################
####################################################
def get_key_data():
    Key_word = "Test" # Keyword for Seacrch
    pages_to_search = 5 # Number of Pages to Search
    page_number = 1  # Starting Page Number

    ############ API Call ##############
    while page_number < pages_to_search: # Search all pages up to pages_to_search

        #### Json Payload for searching API #####
        Keyword_payload = {"isSize":False,"isWeddingCatagory":"False","isMultipleCategoryIds":False,"isFromHeaderMenuTab":False,"layout":"","searchText":Key_word,"selectedGroup":"","selectedCategoryIds":"","selectedSellerIds":"","lowPrice":"0","highPrice":"999999","searchBuyNowOnly":"","searchPickupOnly":"False","searchNoPickupOnly":"False","searchOneCentShippingOnly":"False","searchDescriptions":"False","searchClosedAuctions":"true","closedAuctionEndingDate":"6/16/2022","closedAuctionDaysBack":"150","searchCanadaShipping":"False","searchInternationalShippingOnly":"False","sortColumn":"1","page":page_number,"pageSize":"40","sortDescending":"true","savedSearchId":0,"useBuyerPrefs":"true","searchUSOnlyShipping":"true","categoryLevelNo":"1","categoryLevel":1,"categoryId":0,"partNumber":"","catIds":""}

        response = requests.post('https://buyerapi.shopgoodwill.com/api/Search/ItemListing', json=Keyword_payload) # Json response from API
        json_response = response.json()


        ######## Parse all listings and get the key data used for Prediction ########
        Results = json_response["searchResults"]

        for individual_listing in Results['items']:
            Bids.append(individual_listing["numBids"]) # Gets Number of Bids
            prices.append(individual_listing["currentPrice"]) # Get Prices
            if len(Top_20) == 19: # Gets Top 20 Results for Dislpay
                null = 'null'
            else:
                Top_20.append(individual_listing)

        page_number += 1
    return

####################################################
########## Get Data Needed for Weighting ###########
####################################################
# ALL THIS WILL BE A DJANGO REST API



Weight_Config = {
    'MinPrice': {
    'Type': "USD",
    'Total_Weight': 1.00,
    'Zero': 5,
    'Max': 15,
    'Weight': {
        'Value': 1,
        'Added_Weight': 0.1,
        }
    },
    'AvgPrice': {
    'Type': "USD",
    'Total_Weight': 5.00,
    'Zero': 10 ,
    'Max': 15 ,
    'Weight': {
        'Value': 1 ,
        'Added_Weight': 1.00 ,
        },
    },
    'HighestPrice': {
    'Type': "USD",
    'Total_Weight': 1.50,
    'Zero': 10 ,
    'Max': 15 ,
    'Weight': {
        'Value': 1 ,
        'Added_Weight': 0.3 ,
        }
    },
    'SellThrough': {
        'Type': "%",
        'Total_Weight': 2.50,
        'Zero': 37,
        'Max': 57,
        'Weight': {
            'Value': 1,
            'Weight': 0.125
        }
    },
    'Prediction': {
        'TOTAL': 9,
        'Sell Max': 9.00,
        'Sell Min': 4.32,
        'User Discretion Max': 4.31,
        'User Discretion Min': 1,
        'No Sell Max': 3.82,
        'No Sell Min': 0.00,

    },
}

# MinPrice = [] # Minimum Price for Listings
# AvgPrice = [] # Average Price for Listings
# HighestPrice = [] # Highest Price for Listings
# SellThrough = [] # Sell Through Percentage
#

def weight():
    min_price = min(prices)
    max_price = max(prices)
    avg_price = mean(prices) #round(avg_price)
    MinPrice.append(min_price)
    HighestPrice.append(max_price)
    AvgPrice.append(avg_price)
    did_not_sell = []
    for bid in Bids:
        if bid == 0 or bid == 1:
            did_not_sell.append(bid)
        else:
            null = 'null'

    sell_through = len(did_not_sell) / len(Bids)
    sell_through_percent = sell_through * 100
    SellThrough.append(sell_through_percent)
    return

####################################################
########## Return Prediction ###########
####################################################
Final_Weight = []
def return_Prediction():

    # total_weight = Weight_Config[]
    ######## Min Weight ###############

    if MinPrice[0] == Weight_Config['MinPrice']['Max']:
        Final_Weight.append(Weight_Config['MinPrice']['Total_Weight'])
    elif MinPrice[0] == Weight_Config['MinPrice']['Zero']:
        Final_Weight.append(0.00)
    elif MinPrice[0] >= Weight_Config['MinPrice']['Zero']:
        Min_Weight_p_1 = MinPrice[0] - Weight_Config['MinPrice']['Zero']
        Min_Weight_p_2 =  Min_Weight_p_1 * Weight_Config['MinPrice']['Weight']['Added_Weight']
        Final_Weight.append(Min_Weight_p_2)
    else:
        Final_Weight.append(0.00)

    ########### AVG Price ##############

    # Sell Through percent is based on percentage not sold base weight accordingly

    return


get_key_data()
weight()
return_Prediction()
print(Final_Weight)
time.sleep(1000)
