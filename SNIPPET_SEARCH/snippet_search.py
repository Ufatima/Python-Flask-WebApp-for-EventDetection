import http.client, urllib.parse, json


class SNIPPET_SEARCH(object):
    def BingWebSearch(self, search):
        subscriptionKey = "a429f59b225241948333276c10441b53"
        host = "api.cognitive.microsoft.com"
        path = "/bing/v7.0/search"
        headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
        conn = http.client.HTTPSConnection(host)
        search = search + ' ' + 'language:en location:us site:google.com'
        # dtime = dtime + '..' + endDate
        query = urllib.parse.quote(search)
        conn.request("GET", path + "?q=" + query + "&year=", headers=headers)
        response = conn.getresponse()
        headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
        return headers, response.read().decode("utf8")

    def snippets(self, str_input, number):
        # web sends user inputs(term,snippet number) here
        subscriptionKey = "3f13ed3274414d418639faf1c665ff02"
        host = "api.cognitive.microsoft.com"
        path = "/bing/v7.0/search"

        if len(subscriptionKey) == 32:
            headers, result = self.BingWebSearch(str_input)
            resultjson = json.loads(result)
            s = []
            if resultjson:
                with open('snippet_twitter.txt', 'w', encoding="utf-8") as f:
                    for i in range(0, int(number)):
                        f.writelines(resultjson['webPages']['value'][i]['snippet'] + '\n')
                        s.append(resultjson['webPages']['value'][i]['snippet'])
                    return s
            else:
                return s
        else:
            print("Invalid Bing Search API subscription key!")
