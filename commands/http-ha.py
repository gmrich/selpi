import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import datetime
from spdata import SpData

def add_parser(subparsers):
    parser = subparsers.add_parser('http-ha', help='custom ha')
    parser.set_defaults(func=run)

def run(args):
    server_address = ('', 8001) # start port diff to other http so can run at same time
    logging.info("Starting server on port 8001")
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    httpd.serve_forever()

class ServerState():
    def __init__(self):
        self.AllowSpProAccess = True

class ResponseResult():
    def __init__(self):
        self.Success = True
        self.Message = ""

class Constants():
    def __init__(self):
        self.CMD_HA_VALUES = "havalues"  
        self.CMD_SELECT_LIVE = "selectlive"  
        self.CMD_HTTP_STOP = "stop" 
        self.CMD_HTTP_START = "start" 
        self.CMD_HTTP_STATE = "state" 

constants = Constants()
state =  ServerState()
spdata = SpData()

routes = {
    "/": constants.CMD_HTTP_STATE,
    "/state": constants.CMD_HTTP_STATE,
    "/http/start": constants.CMD_HTTP_START,
    "/http/stop": constants.CMD_HTTP_STOP,
    "/selectlive": constants.CMD_SELECT_LIVE,
    "/havalues": constants.CMD_HA_VALUES
}

class HTTPRequestHandler(BaseHTTPRequestHandler):

    # override base class method
    def log_message(self, format, *args): 
        logging.info("%s - - [%s] %s" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))   

    def do_GET(self):
        cmd = self.getCommandFromPath(self.path, constants.CMD_HTTP_STATE)  

        response = None

        if state.AllowSpProAccess and cmd in [constants.CMD_HA_VALUES, constants.CMD_SELECT_LIVE]:
            if cmd == constants.CMD_HA_VALUES:
                response = self.getHaValues()
            elif cmd == constants.CMD_SELECT_LIVE:
                response = self.getSelectLiveEmulated()
        elif cmd == constants.CMD_HTTP_STATE:
            response = self.getState()
        else:
            response = self.noSpProAccessResult()
             
        return response

    def getCommandFromPath(self, path, defaultCmd):
        cmd = defaultCmd
        if path.lower() in routes:
            cmd = routes[path.lower()]
        return cmd    
    
    def getState(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        stateData = {
            "AllowSpProAccess": state.AllowSpProAccess,
            "Result": ResponseResult()
        }

        data = json.dumps(
            obj=stateData,
            indent=2,
            separators=(',', ':'),
            default=lambda x: x.__dict__
        )
        self.wfile.write(bytes(data, "utf-8"))
        self.wfile.write(b'\n')    
    
    def getHaValues(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            dataObj = {}
            result = ResponseResult()
            startGet = datetime.datetime.now()

            try:
                dataObj = spdata.get_ha()
            except Exception as ex:
                result.Success = False
                result.Message = f"Failure getting ha values from server - {ex}"
                logging.error('getHaValues', exc_info = ex)

            endGet = datetime.datetime.now()
            elapsedTime = endGet - startGet
            logging.info(f"getHaValues-SpProQuery Time = {elapsedTime.total_seconds()} secs")

            dataObj["Result"] = result
    
            data = json.dumps(
                obj = dataObj,
                indent = 2,
                separators = (',', ':'),
                default=lambda x: x.__dict__
            )
            self.wfile.write(bytes(data, "utf-8"))
            self.wfile.write(b'\n')

    
    def getSelectLiveEmulated(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        dataObj = {}
        result = ResponseResult()
        
        try:
            dataObj = spdata.get_select_live()
        except Exception as ex:
            result.Success = False
            result.Message = f"Failure getting selectlive emulation from server - {ex}"
            logging.error('getSelectLiveEmulated', exc_info = ex)

        dataObj["Result"] = result

        data = json.dumps(
            obj=dataObj,
            indent=2,
            separators=(',', ':'),
            default=lambda x: x.__dict__
        )
        self.wfile.write(bytes(data, "utf-8"))
        self.wfile.write(b'\n')

    def do_POST(self):
        cmd = self.getCommandFromPath(self.path, "")  

        if cmd == constants.CMD_HTTP_STOP:
            state.AllowSpProAccess = False
        elif cmd == constants.CMD_HTTP_START:
            state.AllowSpProAccess = True

        return self.getState()

    def noSpProAccessResult(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        data = ResponseResult()
        data.Success = False
        data.Message = "Http Access To Sp Pro Stopped"

        result = {
            "Result": data
        }

        logging.info('Access to Sp Pro Stopped')

        self.wfile.write(bytes(json.dumps(
            obj = result,
            default=lambda x: x.__dict__), 
            "utf-8"))
        self.wfile.write(b'\n')  


