import json
import http.client

host = "applications002.brest-metropole.fr"
page = "/WIPOD01/Transport/REST/getVersion?format=json"
cookie = ""

while True:
    h = http.client.HTTPSConnection(host)
    h.putrequest('GET', page)
    h.putheader('user-agent', 'MDL-bibus')

    h.putheader('Cookie', cookie)
    h.endheaders()
    
    resp = h.getresponse()

    #If cookie isn't set
    if resp.code == 302:
        cookie = ""
        #Get new cookie
        for header in resp.getheaders():
            if header[0] == "Set-cookie":
                cookie += header[1].split(";")[0]
                cookie += ";"

    elif resp.code == 200:
        j = json.loads(resp.read().strip().decode('utf-8'))
        print(j)
        break
    else:
        print(resp.code, "Error not handled")
        break

