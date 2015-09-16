import json
import http.client

class APIError(Exception):
    def __init__(self,what:str):
        Exception.__init__(self,what)

class UnparsableResult(APIError):
    def __init__(self,result : str):
        APIError.__init__(self,result)

class BadReturnCode(APIError):
    def __init__(self,returnCode : int):
        APIError.__init__(self,str(returnCode))

"""
Just a simpe wrap around bibus API
The Bibus web-API looks like : https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/methodName?argName=arg&anotherArgName=anotherArg
The Py version should be : bibus.methodName(argName=arg,anotherArgName=anotherArg)
"""
class Bibus:
    def __init__(self):
        self.cookie = ""

    """
        Intern method and "private" of the API object
        just fetch the web API page and parse the JSON as a dict
        @args: * uri  : str -> The uri location of the API page ex : WIPOD01/Transport/REST/getVersion?format=json
        @return: dict -> the received JSON parsed
        @canRaise: * UnparsableResult if can't parse the webPage
                   * BadReturnCode if return code isn't 200 or 302
                   * HTTPException if problem with the uri, the network...
    """
    def __fetchJson(self,uri:str) -> dict:

        #retry only once, if we get a 302 return code, otherwise, break
        retry = 0
        while retry <= 1:
            retry += 1
            host = "applications002.brest-metropole.fr"
            h = http.client.HTTPSConnection(host)
            h.putrequest('GET', uri)
            h.putheader('user-agent', 'MDL-bibus')

            if self.cookie:
                h.putheader('Cookie', self.cookie)

            h.endheaders()
    
            resp = h.getresponse() #submit the request


            #If cookie isn't set
            if resp.code == 302:
                self.cookie = ""
                #Get new cookie
                for header in resp.getheaders():
                    if header[0] == "Set-cookie":
                        self.cookie += header[1].split(";")[0]
                        self.cookie += ";"
                continue

            elif resp.code == 200:
                b = resp.read().strip().decode('utf-8')
                try:
                    h.close() #Needed to close the socket
                    return json.loads(b)
                except: 
                    raise UnparsableResult(b)
            else:
                print(resp.read().strip().decode('utf-8'))
                raise BadReturnCode(resp.code)
            print(resp.read())

        raise BadReturnCode(302) #If here, it should be an error with 302 return code

    """
    @return: dict -> should be {"Date":"09/09/2015","Number":"1.1"}
    """
    def getVersion(self) -> dict:
        try:
            return self.__fetchJson("/WIPOD01/Transport/REST/getVersion?format=json")
        except UnparsableResult:
            return {}
