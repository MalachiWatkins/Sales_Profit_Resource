import requests
import json
import time
import pdb
from statistics import mean
# pdb.set_trace()

####################################################
############# TO-DO ############################
####################################################


# Finish Prediction Generator
# Start Django Rest API
# Start Django Site; Apps, Users, Main

###################################################


Bids = []  # Number of Bids
Top_20 = []  # First 20 Results
prices = []  # Price for all Listings

MinPrice = []  # Minimum Price for Listings
AvgPrice = []  # Average Price for Listings
HighestPrice = []  # Highest Price for Listings
SellThrough = []  # Sell Through Percentage

####################################################
############# Data Base ############################
####################################################

############ Place Holder for django model #########

####################################################
############# Key word Flagging ####################
####################################################


def keyword_flagging_Check():  # Checks if Current Keyword flagged

    return


def keyword_flagging_new():  # Create a new Kewword flag

    return

####################################################
############# Grabs Key Data #######################
####################################################


def get_key_data():
    ############# Global Vars for api payload ################
    Key_word = "Test"  # Keyword for Seacrch
    pages_to_search = 5  # Number of Pages to Search
    page_number = 1  # Starting Page Number
    ##########################################################

    ############ API Call ##############
    while page_number < pages_to_search:  # Search all pages up to pages_to_search

        #### Json Payload for searching API #####
        Keyword_payload = {"isSize": False, "isWeddingCatagory": "False", "isMultipleCategoryIds": False, "isFromHeaderMenuTab": False, "layout": "", "searchText": Key_word, "selectedGroup": "", "selectedCategoryIds": "", "selectedSellerIds": "", "lowPrice": "0", "highPrice": "999999", "searchBuyNowOnly": "", "searchPickupOnly": "False", "searchNoPickupOnly": "False", "searchOneCentShippingOnly": "False", "searchDescriptions": "False",
                           "searchClosedAuctions": "true", "closedAuctionEndingDate": "6/16/2022", "closedAuctionDaysBack": "150", "searchCanadaShipping": "False", "searchInternationalShippingOnly": "False", "sortColumn": "1", "page": page_number, "pageSize": "40", "sortDescending": "true", "savedSearchId": 0, "useBuyerPrefs": "true", "searchUSOnlyShipping": "true", "categoryLevelNo": "1", "categoryLevel": 1, "categoryId": 0, "partNumber": "", "catIds": ""}

        response = requests.post('https://buyerapi.shopgoodwill.com/api/Search/ItemListing',
                                 json=Keyword_payload)  # Json response from API
        json_response = response.json()

        ######## Parse all listings and get the key data used for Prediction ########
        Results = json_response["searchResults"]

        for individual_listing in Results['items']:
            Bids.append(individual_listing["numBids"])  # Gets Number of Bids
            prices.append(individual_listing["currentPrice"])  # Get Prices
            if len(Top_20) == 19:  # Gets Top 20 Results for Dislpay
                null = 'null'
            else:
                Top_20.append(individual_listing)
        page_number += 1
    return

####################################################
####### Parsing Data Needed for Weighting ##########
####################################################


def weight():
    ####### Parsing Data #########
    min_price = min(prices)
    max_price = max(prices)
    avg_price = mean(prices)

    ######## Appends Parsed Data for use in Prediction function ##########
    MinPrice.append(min_price)
    HighestPrice.append(max_price)
    AvgPrice.append(avg_price)

    ###### Sell Through Calculation #####
    sold_listings = []
    for bid in Bids:
        if bid == 0 or bid == 1: ## Change to an if not statment
            null = ''
        else:
            sold_listings.append(bid)


    ######## Sell Through Percentage Calculator###############
    sell_through = len(sold_listings) / len(Bids)
    sell_through_percent = sell_through * 100
    SellThrough.append(sell_through_percent)
    return

####################################################
########## Return Prediction #######################
####################################################


# THIS IS TEMP AND WILL BE A DJANGO REST API ONCE TESTING IS DONE
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
        'Zero': 10,
        'Max': 15,
        'Weight': {
            'Value': 1,
            'Added_Weight': 1.00,
        },
    },
    'HighestPrice': {
        'Type': "USD",
        'Total_Weight': 1.50,
        'Zero': 10,
        'Max': 15,
        'Weight': {
            'Value': 1,
            'Added_Weight': 0.3,
        }
    },
    'SellThrough': {
        'Type': "%",
        'Total_Weight': 2.50,
        'Zero': 37,
        'Max': 57,
        'Weight': {
            'Value': 1,
            'Added_Weight': 0.125
        }
    },
    'Prediction': {
        'TOTAL': 9,
        'Sell Max': 9.00,
        'Sell Min': 4.32,
        'User Discretion Max': 4.31,
        'User Discretion Min': 3.83,
        'No Sell Max': 3.82,
        'No Sell Min': 0.00,

    },
}

Final_Weight = []


def return_Prediction():
    Master_List = [MinPrice[0], AvgPrice[0], HighestPrice[0], SellThrough[0]]
    Master_Cat_List = ['MinPrice', 'AvgPrice', 'HighestPrice', 'SellThrough']

    ######## Min Weight ###############

    x=0
    while x < len(Master_List):
        ConfigEntry = Weight_Config[Master_Cat_List[x]]
        data = Master_List[x]

        if data >= ConfigEntry['Max']:
            Final_Weight.append(ConfigEntry['Total_Weight'])
        elif data >= ConfigEntry['Zero']:
            Weight_Calc_P1 = data - ConfigEntry['Zero']
            Weight_Calc_Final = Weight_Calc_P1 * ConfigEntry['Weight']['Added_Weight']
            Final_Weight.append(Weight_Calc_Final)
        else:
            Final_Weight.append(0.00)

        x+=1




    return


get_key_data()
weight()
return_Prediction()
print(Final_Weight)
time.sleep(1000)
