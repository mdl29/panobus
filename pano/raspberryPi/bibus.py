"""
This module is an help to use the Bibus API
"""
import json
import http.client
from urllib.parse import urlencode



def check_types(fct):
    return fct

class APIError(Exception):
    """
    The main class of Bibus exceptions
   """
    def __init__(self, what: str):
        Exception.__init__(self, what)

class UnparsableResultError(APIError):
    """
    An Exception which occur when the data received through the web API isn't a valid JSON
    """
    def __init__(self, result: str):
        APIError.__init__(self, result)

class BadReturnCodeError(APIError):
    """
    An exception which occur when the Bibus API  return a non 200 or 301 error
    """
    def __init__(self, returnCode: int):
        APIError.__init__(self, str(returnCode))

class Bibus:
    """
    Just a simpe wrap around bibus API
    The Bibus web-API looks like :
        https://applications002.brest-metropole.fr/WIPOD01/Transport/REST/methodName?
            argName=arg&anotherArgName=anotherArg
    The Pythonic version should be : bibus.method_name(argName=arg,anotherArgName=anotherArg)
    """
    #Some constants for the Rest API requests
    HOST = "applications002.brest-metropole.fr"
    REST_API_BASE_URI = "/WIPOD01/Transport/REST/"
    REST_API_DEFAULT_FORMAT = "json"

    def __init__(self):
        self.cookie = ""

    @check_types
    def get_json(self, uri: str) -> dict:
        """
        an internal fonction
        """
        try:
            return(self._fetch_json(uri), uri)
        except UnparsableResultError:
            return ([], uri)

    @check_types
    def _fetch_json(self, uri: str) -> dict:
        """
        Intern method and "private" of the API object
        just fetch the web API page and parse the JSON as a dict
        args: * uri  : str -> The uri location of the API page ex :
            WIPOD01/Transport/REST/getVersion?format=json
        return: dict -> the received JSON parsed
        canRaise: * UnparsableResultError if can't parse the webPage
                   * BadReturnCodeError if return code isn't 200 or 302
                   * HTTPException if problem with the uri, the network...
        """
        #retry only once, if we get a 302 return code, otherwise, break
        retry = 0
        while retry <= 1:
            retry += 1
            request = http.client.HTTPSConnection(self.HOST)
            request.putrequest('GET', uri)
            request.putheader('user-agent', 'MDL-bibus')

            if self.cookie:
                request.putheader('Cookie', self.cookie)

            request.endheaders()

            resp = request.getresponse() #submit the request


            #If cookie isn't set
            if resp.code == 302:
                self.cookie = ""
                #Get new cookie
                for header in resp.getheaders():
                    if header[0] == "Set-cookie":
                        self.cookie += header[1].split(";")[0]
                        self.cookie += ";"

                request.close()
                continue

            elif resp.code == 200:
                data_raw = resp.read().strip().decode('utf-8')
                request.close()
                try:
                    return json.loads(data_raw)
                except:
                    raise UnparsableResultError(data_raw)
            else:
                raise BadReturnCodeError(resp.code)

        raise BadReturnCodeError(302) #If here, it should be an error with 302 return code

    @check_types
    def get_uri(self, cmd: str, params: dict=None) -> str:
        """
        Generate the request uri from a command and some parameters.
        args:  * cmd : str, Rest command
                    * params : dict, Rest parameters
        return: full uri (url encoded)
        """
        if params is None:
            params = dict()

        if "format" not in params:
            params["format"] = self.REST_API_DEFAULT_FORMAT

        return self.REST_API_BASE_URI + cmd + "?" + urlencode(params)


    @check_types
    def get_version(self) -> dict:
        """
        return: dict -> should be {"Date":"09/09/2015","Number":"1.1"}
                 uri -> the uri location of the API page (for debug purpose mainly)
        """
        uri = self.get_uri("getVersion")
        return self.get_json(uri)

    @check_types
    def get_remaining_times(self, route_id: str, stop_name: str, trip_headsign: str) -> list:
        """
        args:  *route_id : str -> 2
                *stop_name: str (Malakoff)
                *trip_headsign: str -> direction (oceanopolis)
        return: list -> [{"Advance":"00:00:19","Arrival_time":"16:20:51",
                 uri -> the uri location of the API page (for debug purpose mainly)
            "Delay":"00:00:00","EstimateTime_arrivalRealized":"16:23:33",
                "Remaining_time":"00:13:41"}]
        """


        uri = self.get_uri("getRemainingTimes",
                           {"route_id": route_id, "trip_headsign": trip_headsign,
                            "stop_name": stop_name})
        return self.get_json(uri)



    @check_types
    def get_stop_names(self) -> list:
        """
        return: list -> [  {"Stop_name": "4 Chemins"},{"Stop_name": "4 Moulins"},
                 uri -> the uri location of the API page (for debug purpose mainly)
                            {"Stop_name": "8 mai 1945"},{"Stop_name": "A.France"},
                            ...
                         ]
        """
        uri = self.get_uri("getStopsNames")
        return self.get_json(uri)

    @check_types
    def get_routes(self) -> list:
        """
        return: list -> [  {"Route_id":"A","Route_long_name":"Tramway Est Ouest"},
                 uri -> the uri location of the API page (for debug purpose mainly)
                            {"Route_id":"1","Route_long_name":"Chru < > Montbarrey"},
                            ...
                         ]
        """
        uri = self.get_uri("getRoutes")
        return self.get_json(uri)


    @check_types
    def get_destinations(self, route_id: str) -> list:
        """
        Return the list of all directions of a route
        args: *routeId : str -> A
        return: list -> [{"Trip_headsign":"Porte de Gouesnou"},
                 uri -> the uri location of the API page (for debug purpose mainly)
                         {"Trip_headsign":"Porte de Guipavas"},
                         {"Trip_headsign":"Porte de Plouzané"}]
        """
        uri = self.get_uri("getDestinations", {"route_id": route_id})
        return self.get_json(uri)

    @check_types
    def get_route_stop(self, stop_name: str) -> list:
        """
        args: stop_name the name of the stop
        Return a list of route passing throught the stop
        """
        uri = self.get_uri("getRoutes_Stop", {"stop_name": stop_name})
        return self.get_json(uri)

    @check_types
    def get_stop_vehicles_position(self, route_id: str, trip_headsign: str) -> list:
        """
        Args: route_iD
               trip_headsign : the direction
        Return a list of the arret where the bus is
        """
        uri = self.get_uri("getStopVehiclesPosition",
                           {"route_id": route_id, "trip_headsign": trip_headsign})
        return self.get_json(uri)

    @check_types
    def get_stop(self, stop_name: str) -> list:
        """
        Args: stop_name: the name of the stop
        Return a list of stop's data
        """

        uri = self.get_uri("get_stop", {"stop_name": stop_name})
        return self.get_json(uri)
