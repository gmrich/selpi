import datetime
import time
from muster import Muster
from memory import variable

class SpData():

    def __init__(self):
        self.__muster = Muster()
        self.__scale_variables = [
            variable.create('CommonScaleForAcVolts'),
            variable.create('CommonScaleForAcCurrent'),
            variable.create('CommonScaleForDcVolts'),
            variable.create('CommonScaleForDcCurrent'),
            variable.create('CommonScaleForTemperature'),
            variable.create('CommonScaleForInternalVoltages'),
        ]
        self.__scales = None

        self.__selectLive_variables = {
            "DCkWhInToday": variable.create("DCkWhInToday"),
            "BattInkWhTotalAcc": variable.create('BattInkWhTotalAcc'),            
            "DCkWhOutToday": variable.create("DCkWhOutToday"),
            "BattOutkWhTotalAcc": variable.create('BattOutkWhTotalAcc'),
            "BattSocPercent": variable.create('BattSocPercent'),
            "Shunt1Power": variable.create('Shunt1Power'),
            "DCBatteryPower": variable.create('DCBatteryPower'),
            "LoadAcPower": variable.create('LoadAcPower'),
            "CombinedKacoAcPowerHiRes": variable.create('CombinedKacoAcPowerHiRes'),
            "ACLoadkWhTotalAcc": variable.create("ACLoadkWhTotalAcc"),
            "ACInputWhTodayAcc": variable.create("ACInputWhTodayAcc"),
            "ACInputWhTotalAcc": variable.create("ACInputWhTotalAcc"),
            "ACExportWhTodayAcc": variable.create("ACExportWhTodayAcc"),
            "ACExportWhTotalAcc": variable.create("ACExportWhTotalAcc"),
            "ACLoadWhAcc": variable.create("ACLoadWhAcc"),
            "ACSolarWhTotalAcc": variable.create("ACSolarWhTotalAcc"),
            "Shunt1WhTotalAcc": variable.create("Shunt1WhTotalAcc"),
            "ACSolarWhTodayAcc": variable.create("ACSolarWhTodayAcc"),
            "Shunt1WhTodayAcc": variable.create("Shunt1WhTodayAcc"),
            "ACGeneratorPower": variable.create("ACGeneratorPower"),
            "GeneratorStatus": variable.create("GeneratorStatus")            
        }

        self.__custom_variables = {
            "DCkWhInToday": variable.create("DCkWhInToday"),
            "BattInkWhTotalAcc": variable.create('BattInkWhTotalAcc'),
            "DCkWhOutToday": variable.create("DCkWhOutToday"),
            "BattOutkWhTotalAcc": variable.create('BattOutkWhTotalAcc'),
            "BattSocPercent": variable.create('BattSocPercent'),
            "Shunt1Power": variable.create('Shunt1Power'),
            "DCBatteryPower": variable.create('DCBatteryPower'),
            "LoadAcPower": variable.create('LoadAcPower'),
            "CombinedKacoAcPowerHiRes": variable.create('CombinedKacoAcPowerHiRes'),
            "ACLoadkWhTotalAcc": variable.create("ACLoadkWhTotalAcc"),
            "ACInputWhTodayAcc": variable.create("ACInputWhTodayAcc"),
            "ACInputWhTotalAcc": variable.create("ACInputWhTotalAcc"),
            "ACExportWhTodayAcc": variable.create("ACExportWhTodayAcc"),
            "ACExportWhTotalAcc": variable.create("ACExportWhTotalAcc"),
            "ACLoadWhAcc": variable.create("ACLoadWhAcc"),
            "ACSolarWhTotalAcc": variable.create("ACSolarWhTotalAcc"),
            "Shunt1WhTotalAcc": variable.create("Shunt1WhTotalAcc"),
            "ACSolarWhTodayAcc": variable.create("ACSolarWhTodayAcc"),
            "Shunt1WhTodayAcc": variable.create("Shunt1WhTodayAcc"),
            "ACGeneratorPower": variable.create("ACGeneratorPower"),
            "GeneratorStatus": variable.create("GeneratorStatus"),
            "ChargeMode": variable.create("ChargeMode"),
            "GeneratorStartReason": variable.create("GeneratorStartReason"),
            "GeneratorRunningReason": variable.create("GeneratorRunningReason"),            
            "AcOutStatus": variable.create("AcOutStatus"),   
            "AcSourceStatus": variable.create("AcSourceStatus"),                   
            "DigitalInStatus1": variable.create("DigitalInStatus1"),    
            "DigitalInStatus2": variable.create("DigitalInStatus2"),    
            "DigitalInStatus3": variable.create("DigitalInStatus3"),    
            "DigitalInStatus4": variable.create("DigitalInStatus4"),    
            "DigitalOutStatus1": variable.create("DigitalOutStatus1"),    
            "DigitalOutStatus2": variable.create("DigitalOutStatus2"),    
            "DigitalOutStatus3": variable.create("DigitalOutStatus3"),    
            "DigitalOutStatus4": variable.create("DigitalOutStatus4"),    
            "DigitalOutStatus5": variable.create("DigitalOutStatus5"),    
            "DigitalOutStatus6": variable.create("DigitalOutStatus6"),    
            "DigitalOutStatus7": variable.create("DigitalOutStatus7"),    
            "BatteryVolts": variable.create("BatteryVolts"),    
            "BatteryTemperature": variable.create("BatteryTemperature"),    
            #"PowerModuleAirTemperature": variable.create("PowerModuleAirTemperature"),  
            #"TransformerTemperature": variable.create("TransformerTemperature"), 
            "InternalTemperature": variable.create("InternalTemperature"), 
            #"HalfBridge1HeatsinkTemperature": variable.create("HalfBridge1HeatsinkTemperature"), 
            #"HalfBridge2HeatsinkTemperature": variable.create("HalfBridge2HeatsinkTemperature"), 
            "FanSpeed": variable.create("FanSpeed"),
            "ActiveSchedule": variable.create("ActiveSchedule"),    
            "FloatMinutesToday": variable.create("FloatMinutesToday"),                
            "ACLoadVoltage": variable.create("ACLoadVoltage"),  
            "AnalogueDcVoltage1": variable.create("AnalogueDcVoltage1"),  
            "AnalogueDcVoltage2": variable.create("AnalogueDcVoltage2"),  
            "AcHz": variable.create("AcHz"),  
             # only one ServiceRequiredReason0 retrieved initially as this is used as test if value then get the rest
            "ServiceRequiredReason0": variable.create("ServiceRequiredReason0"),
        }  

    def __update(self, variables):
        if not self.__scales:
            variables = variables + self.__scale_variables

        self.__muster.update(variables)

    def get_select_live(self):
        vars = self.__selectLive_variables
        self.__update(list(vars.values()))
        timestamp = int(time.time())
        items = {
            "battery_in_wh_today": vars["DCkWhInToday"].get_value(self.scales) / 1000,
            "battery_in_wh_total": vars["BattInkWhTotalAcc"].get_value(self.scales) / 1000,
            "battery_out_wh_today": vars["DCkWhOutToday"].get_value(self.scales) / 1000,
            "battery_out_wh_total": vars["BattOutkWhTotalAcc"].get_value(self.scales) / 1000,
            "battery_soc": vars["BattSocPercent"].get_value(self.scales),
            "battery_w": vars["DCBatteryPower"].get_value(self.scales),
            #"fault_code": 0,
            #"fault_ts": 0,
            "gen_status": vars["GeneratorStatus"].get_value(self.scales),
            "grid_in_wh_today": vars["ACInputWhTodayAcc"].get_value(self.scales) / 1000,
            "grid_in_wh_total": vars["ACInputWhTotalAcc"].get_value(self.scales) / 1000,
            "grid_out_wh_today": vars["ACExportWhTodayAcc"].get_value(self.scales) / 1000, # unverified guess
            "grid_out_wh_total": vars["ACExportWhTotalAcc"].get_value(self.scales) / 1000, # unverified guess
            "grid_w": vars["ACGeneratorPower"].get_value(self.scales),
            "load_w": vars["LoadAcPower"].get_value(self.scales),
            "load_wh_today": vars["ACLoadWhAcc"].get_value(self.scales) / 1000,
            "load_wh_total": vars["ACLoadkWhTotalAcc"].get_value(self.scales) / 1000,
            "shunt_w": 0 - vars["Shunt1Power"].get_value(self.scales),
            "solar_wh_today": ( vars["ACSolarWhTodayAcc"].get_value(self.scales) + 0 - vars["Shunt1WhTodayAcc"].get_value(self.scales)) / 1000,            
            "solar_wh_total": (vars["ACSolarWhTotalAcc"].get_value(self.scales) + (0 -vars["Shunt1WhTotalAcc"].get_value(self.scales))) / 1000,
            "solarinverter_w": vars["CombinedKacoAcPowerHiRes"].get_value(self.scales),
            "timestamp": timestamp,
        }
        return {
            "device": {
                "name": "Selectronic SP-PRO",
            },
            "item_count": len(items),
            "items": items,
            "now": timestamp
        }

    def get_ha(self):
        vars = self.__selectLive_variables | self.__custom_variables
        self.__update(list(vars.values()))
        timestamp = int(time.time())
        servReqCodeCsv = self.getServiceRequiredCodeCsvList(vars)
        items = {
            "battery_in_wh_today": vars["DCkWhInToday"].get_value(self.scales) / 1000,
            "battery_in_wh_total": vars["BattInkWhTotalAcc"].get_value(self.scales) / 1000,
            "battery_out_wh_today": vars["DCkWhOutToday"].get_value(self.scales) / 1000,
            "battery_out_wh_total": vars["BattOutkWhTotalAcc"].get_value(self.scales) / 1000,
            "battery_soc": vars["BattSocPercent"].get_value(self.scales),
            "battery_w": vars["DCBatteryPower"].get_value(self.scales),
            "gen_status": vars["GeneratorStatus"].get_value(self.scales),
            "grid_in_wh_today": vars["ACInputWhTodayAcc"].get_value(self.scales) / 1000,
            "grid_in_wh_total": vars["ACInputWhTotalAcc"].get_value(self.scales) / 1000,
            "grid_out_wh_today": vars["ACExportWhTodayAcc"].get_value(self.scales) / 1000, 
            "grid_out_wh_total": vars["ACExportWhTotalAcc"].get_value(self.scales) / 1000, 
            "grid_w": vars["ACGeneratorPower"].get_value(self.scales),
            "load_w": vars["LoadAcPower"].get_value(self.scales),
            "load_wh_today": vars["ACLoadWhAcc"].get_value(self.scales) / 1000,
            "load_wh_total": vars["ACLoadkWhTotalAcc"].get_value(self.scales) / 1000,
            "shunt_w": 0 - vars["Shunt1Power"].get_value(self.scales),
            "solar_wh_today": vars["ACSolarWhTodayAcc"].get_value(self.scales) / 1000,
            "solar_wh_total": vars["ACSolarWhTotalAcc"].get_value(self.scales) / 1000,
            "solarinverter_w": vars["CombinedKacoAcPowerHiRes"].get_value(self.scales),
            "ChargeMode": vars["ChargeMode"].get_value(self.scales),
            "GeneratorStartReason": vars["GeneratorStartReason"].get_value(self.scales),
            "GeneratorRunningReason": vars["GeneratorRunningReason"].get_value(self.scales),
            "AcSourceStatus": vars["AcSourceStatus"].get_value(self.scales),
            "AcOutStatus": vars["AcOutStatus"].get_value(self.scales),
            "DigitalInStatus1": vars["DigitalInStatus1"].get_value(self.scales),
            "DigitalInStatus2": vars["DigitalInStatus2"].get_value(self.scales),
            "DigitalInStatus3": vars["DigitalInStatus3"].get_value(self.scales),
            "DigitalInStatus4": vars["DigitalInStatus4"].get_value(self.scales),            
            "DigitalOutStatus1": vars["DigitalOutStatus1"].get_value(self.scales),            
            "DigitalOutStatus2": vars["DigitalOutStatus2"].get_value(self.scales),
            "DigitalOutStatus3": vars["DigitalOutStatus3"].get_value(self.scales),
            "RelayOutStatus1": vars["DigitalOutStatus4"].get_value(self.scales),
            "RelayOutStatus2": vars["DigitalOutStatus5"].get_value(self.scales),
            "RelayOutStatus3": vars["DigitalOutStatus6"].get_value(self.scales),
            "RelayOutStatus4": vars["DigitalOutStatus7"].get_value(self.scales),
            "AnalogueDcVoltage1": vars["AnalogueDcVoltage1"].get_value(self.scales),
            "AnalogueDcVoltage2": vars["AnalogueDcVoltage2"].get_value(self.scales),
            "BatteryVolts": vars["BatteryVolts"].get_value(self.scales),
            "BatteryTemperature": vars["BatteryTemperature"].get_value(self.scales),
            #"PowerModuleAirTemperature": vars["PowerModuleAirTemperature"].get_value(self.scales),
            #"TransformerTemperature": vars["TransformerTemperature"].get_value(self.scales),
            "InternalTemperature": vars["InternalTemperature"].get_value(self.scales),
            #"HalfBridge1HeatsinkTemperature": vars["HalfBridge1HeatsinkTemperature"].get_value(self.scales),
            #"HalfBridge2HeatsinkTemperature": vars["HalfBridge2HeatsinkTemperature"].get_value(self.scales),
            "FanSpeed": vars["FanSpeed"].get_value(self.scales),
            "ActiveSchedule": vars["ActiveSchedule"].get_value(self.scales),
            "FloatMinutesToday": vars["FloatMinutesToday"].get_value(self.scales),
            "ACLoadVoltage": vars["ACLoadVoltage"].get_value(self.scales),
            "AcHz": vars["AcHz"].get_value(self.scales),
            "ServiceRequiredReasonCodesAsCsv": servReqCodeCsv,
            "timestamp": timestamp,
        }
        
        return {
            "device": {
                "name": "Selectronic SP-PRO",
            },
            "item_count": len(items),
            "items": items,
            "now": timestamp
        }
    
    #read first service req code
    #and if non zero then get all of the rest and create code list 
    def getServiceRequiredCodeCsvList(self, vars):
        servReqCodeCsv = ""

        #get existing reason 0 from first call to sp pro
        servRequired_0 = vars["ServiceRequiredReason0"].get_value(self.scales)

        if servRequired_0 != 0:
            #if there is an error code in the first reason then just get all of the rest
            servReqCodeCsv = servRequired_0
            servRequiredVars = {}
            MaxNumberReasons = 20
            
            #create list of reason variables (1- 19)
            for i in range(1, MaxNumberReasons):
                varName = f"ServiceRequiredReason{i}"
                servRequiredVars[varName] = variable.create(varName)

            #use muster to call sp pro and get results
            self.__update(list(servRequiredVars.values()))

            #loop through results recording any non zero codes, at first zero code finish processing
            for i in range(1,MaxNumberReasons):
                varName = f"ServiceRequiredReason{i}"
                if varName in servRequiredVars:
                    code = servRequiredVars[varName].get_value(self.scales)
                    if code == 0:
                        break
                    else:
                        servReqCodeCsv = servReqCodeCsv + "," + str(code)
                else:
                    break

        return servReqCodeCsv

    @property
    def scales(self):
        if not self.__scales:
            self.__scales = {}
            for variable in self.__scale_variables:
                self.__scales[variable.get_name()] = variable.get_value([])
        return self.__scales
