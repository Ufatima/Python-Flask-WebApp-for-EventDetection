import http.client, urllib.parse, json

class SNIPPET_SEARCH(object):
    def BingWebSearch(self, search, dtime):
        subscriptionKey = "51f8aeba411e4e86b358d5bb2d998aed"
        host = "api.cognitive.microsoft.com"
        path = "/bing/v7.0/search"
        headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
        conn = http.client.HTTPSConnection(host)
        query = urllib.parse.quote(search, dtime)
        conn.request("GET", path + "?q=" + query + "&year=", headers=headers)
        response = conn.getresponse()
        headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
        return headers, response.read().decode("utf8")

    def snippets(self, str_input, date, number):
        # web sends user inputs(term,date,snippet number) here 
        subscriptionKey = "3f13ed3274414d418639faf1c665ff02"
        # term = "debate2012 language:en location:us site:twitter.com"
        # date_time = "2012-10-16..2012-10-17"
        # number_of_snippet = 10
        host = "api.cognitive.microsoft.com"
        path = "/bing/v7.0/search"

        if len(subscriptionKey) == 32:
            headers, result = self.BingWebSearch(str_input, date)
            resultjson = json.loads(result)
            s = []
            with open('snippet_twitter.txt', 'w', encoding="utf-8") as f:
                for i in range(0, int(number)):
                    f.writelines(resultjson['webPages']['value'][i]['snippet']+'\n')
                    # print(resultjson['webPages']['value'][i]['snippet'])
                    s.append(resultjson['webPages']['value'][i]['snippet'])
                return s
        else:
            print("Invalid Bing Search API subscription key!")