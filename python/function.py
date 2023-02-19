import requests

#this function should return a string that is the link to the giphy image based on user input (query)
def getBlockChainFrom(query, key):
    blockchain_get = "https://rest.coinapi.io/v1/exchangerate/USD?apikey={apikey}&invert=true&output_format=csv"
    #converts data into json data structure
    response = requests.get(blockchain_get).json()
    if len(response["data"]) > 0:
    #url after analyzing nested json structure of response
        url = response["data"][0]
        return url
    #else condition deals with possibility user query returns no GIPHY results
    else:
        no_results_img_link = "https://unbxd.com/wp-content/uploads/2014/02/No-results-found.jpg"
        return no_results_img_link