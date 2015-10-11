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

                h.close()
                continue

            elif resp.code == 200:
                b = resp.read().strip().decode('utf-8')
                h.close()
                try:
                    return json.loads(b)
                except: 
                    raise UnparsableResult(b)
            else:
                raise BadReturnCode(resp.code)

        raise BadReturnCode(302) #If here, it should be an error with 302 return code

    """
    @return: dict -> should be {"Date":"09/09/2015","Number":"1.1"}
    """
    def getVersion(self) -> dict:
        uri = "/WIPOD01/Transport/REST/getVersion?format=json"
        try:
            return (self.__fetchJson(uri),uri)
        except UnparsableResult:
            return ({},uri)

    """
    @args:  *routeId : str -> 2
            *stopName: str (Malakoff)
            *tripHeadsign: str -> direction (oceanopolis)
    @return: list -> [{"Advance":"00:00:19","Arrival_time":"16:20:51",
        "Delay":"00:00:00","EstimateTime_arrivalRealized":"16:23:33","Remaining_time":"00:13:41"}]
    """
    def getRemainingTimes(self,routeId:str ,stopName:str , tripHeadsign:str) -> list:

        assert(type(stopName) is str)
        assert(type(routeId) is str)
        assert(type(tripHeadsign) is str)

        uri = "/WIPOD01/Transport/REST/getRemainingTimes?format=json&route_id={0}&trip_headsign={1}&stop_name={2}".format(
                    routeId,tripHeadsign,stopName)
        try:
            return (self.__fetchJson(uri),uri)

        except UnparsableResult:
            return ([],uri)

    """
    @return: list -> [  {"Stop_name": "4 Chemins"},{"Stop_name": "4 Moulins"},
                        {"Stop_name": "8 mai 1945"},{"Stop_name": "A.France"},
                        ...
                     ]
    """
    def getStopNames(self) -> list:
        uri = "/WIPOD01/Transport/REST/getStopsNames?format=json"
        try:
            return (self.__fetchJson(uri),uri)
        except UnparsableResult:
            return ([],uri)

    """
    @return: list -> [  {"Route_id":"A","Route_long_name":"Tramway Est Ouest"},
                        {"Route_id":"1","Route_long_name":"Chru < > Montbarrey"},
                        ...
                     ]
    """
    def getRoutes(self) -> list:
        uri = "/WIPOD01/Transport/REST/getRoutes?format=json"
        try:
            return (self.__fetchJson(uri),uri)
        except UnparsableResult:
            return ([],uri)

    """
    Return the list of all directions of a route
    @args: *routeId : str -> A
    @return: list -> [{"Trip_headsign":"Porte de Gouesnou"},
                     {"Trip_headsign":"Porte de Guipavas"},
                     {"Trip_headsign":"Porte de Plouzané"}]
    """
    def getDestinations(self, routeId :str) -> list:
        assert(type(routeId) is str)
        uri =  "/WIPOD01/Transport/REST/getDestinations?format=json&route_id={}".format(routeId)
        try:
            return (self.__fetchJson(uri),uri)
        except UnparsableResult:
            return ([],uri)

    """
    Return a list of route passing throught a stop
    """
    def getRoutesStop(self, stopName :str) -> list:
        assert(type(stopName) is str)
        uri =  "/WIPOD01/Transport/REST/getRoutes_Stop?format=json&stop_name={}".format(stopName)
        try:
            return (self.__fetchJson(uri),uri)
        except UnparsableResult:
            return ([],uri)
