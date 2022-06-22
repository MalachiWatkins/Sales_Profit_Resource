import requests
import json
import time
import pdb
from statistics import mean
#pdb.set_trace()



Bids = [] # Number of Bids
Top_20 = [] # First 20 Results
prices = [] # Price for all Listings
MinPrice = []
AvgPrice = []
HighestPrice = []
SellThrough = []

####################################################
############# Grabs Key Data #######################
####################################################
def get_key_data():
    Key_word = "Test"
    page_number = 1
    pages_to_search = 5 # Number of Pages to Search

    while page_number < pages_to_search:
        print(page_number)
        Keyword_payload = {"isSize":False,"isWeddingCatagory":"False","isMultipleCategoryIds":False,"isFromHeaderMenuTab":False,"layout":"","searchText":Key_word,"selectedGroup":"","selectedCategoryIds":"","selectedSellerIds":"","lowPrice":"0","highPrice":"999999","searchBuyNowOnly":"","searchPickupOnly":"False","searchNoPickupOnly":"False","searchOneCentShippingOnly":"False","searchDescriptions":"False","searchClosedAuctions":"true","closedAuctionEndingDate":"6/16/2022","closedAuctionDaysBack":"150","searchCanadaShipping":"False","searchInternationalShippingOnly":"False","sortColumn":"1","page":page_number,"pageSize":"40","sortDescending":"true","savedSearchId":0,"useBuyerPrefs":"true","searchUSOnlyShipping":"true","categoryLevelNo":"1","categoryLevel":1,"categoryId":0,"partNumber":"","catIds":""}

        response = requests.post('https://buyerapi.shopgoodwill.com/api/Search/ItemListing', json=Keyword_payload)
        json_response = response.json()

        Results = json_response["searchResults"]

        for individual_listing in Results['items']:
            Bids.append(individual_listing["numBids"]) # Gets Number of Bids
            prices.append(individual_listing["currentPrice"])
            if len(Top_20) == 19: # Gets Top 20 Results for Dislpay
                null = 'null'
            else:
                Top_20.append(individual_listing)

        page_number += 1
    return


def weight():

    min_price = min(prices)
    max_price = max(prices)
    avg_price = mean(prices) #round(avg_price)

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

get_key_data()
weight()
time.sleep(1000)

# Keyword Flagging
def keyword_flagging():

    return
# Prediction Calculator


##### CFG goes here #######
def return_Prediction():

    return
def data_base():
    # Key_Word_Flag_Approved_Document = {
    #     Key_word: 'Test',
    #     Key_word_DesL: 'Flagged for EXAMPLE REASON',
    #     Key_word_Rating: '4', # 4/5
    # }
    # Key_Word_Flag_Pending_Document = {
    #     Key_word: 'Pending',
    #     Key_word_Des: 'Flagged for EXAMPLE REASON',
    # }
    # Weight_Config = {
    #     MinPrice: {
    #     Type: "USD",
    #     Total_Weight: 1.00,
    #     Zero: 5,
    #     Max: 15,
    #     Weight: {
    #         Value: 1,
    #         Added_Weight: 0.1,
    #         }
    #     },
    #     AvgPrice: {
    #     Type: "USD",
    #     Total_Weight: 5.00,
    #     Zero: ,
    #     Max: ,
    #     Weight: {
    #         Value: ,
    #         Added_Weight: ,
    #         }
    #     },
    #     HighestPrice: {
    #     Type: "USD",
    #     Total_Weight: 1.50,
    #     Zero: ,
    #     Max: ,
    #     Weight: {
    #         Value: ,
    #         Added_Weight: ,
    #         }
    #     },
    #     SellThrough: {
    #         Type: "%",
    #         Total_Weight" 2.50,
    #         Zero: 37,
    #         Max: 57,
    #         Weight: {
    #             Value: 1,
    #             Weight: 0.125
    #         }
    #     },
    # }
    #
    # User = {
    #     User_Name = 'MWatkins',
    #     Pass_Word_Hashed = '',
    #     Is_Admin = True,
    # }

    return
