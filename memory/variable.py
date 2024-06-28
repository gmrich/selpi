from email.headerregistry import Address
import struct
from memory import convert
from memory import Range

def create(arg):
    if type(arg) is str:
        return Variable(arg, MAP[arg][ADDRESS])
    if type(arg) is int:
        return Variable(address_to_name(arg), arg)
    raise NotImplementedError("Unable to create Variable from %s" % type(arg))

def address_to_name(address):
    for name in MAP.keys():
        if MAP[name][ADDRESS] == address:
            return name
    return 'Unknown'

ADDRESS = 'address'
TYPE = 'type'
DESCRIPTION = 'description'
UNITS = 'units'
CONVERSION = 'conversion'
FORMAT = 'format'
WORDS = 'words'

MAP = {
    "CommonScaleForAcVolts": {
        ADDRESS: 41000,
        TYPE: "ushort",
    },
    "CommonScaleForAcCurrent": {
        ADDRESS: 41001,
        TYPE: "ushort",
    },
    "CommonScaleForDcVolts": {
        ADDRESS: 41002,
        TYPE: "ushort",
    },
    "CommonScaleForDcCurrent": {
        ADDRESS: 41003,
        TYPE: "ushort",
    },
    "CommonScaleForTemperature": {
        ADDRESS: 41004,
        TYPE: "ushort",
    },
    "CommonScaleForInternalVoltages": {
        ADDRESS: 41005,
        TYPE: "ushort",
    },
    "TotalKacokWhTotalAcc": {
        DESCRIPTION: 'AC Lifetime Solar Energy',
        ADDRESS: 41519,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "ac_wh",
    },
    "CombinedKacoAcPowerHiRes": {
        DESCRIPTION: 'AC Solar Power',
        ADDRESS: 0xa3a8,
        TYPE: "uint",
        UNITS: "W",
        CONVERSION: "ac_w",
    },
    "LoadAcPower": {
        DESCRIPTION: 'AC Load Power',
        ADDRESS: 41107,
        TYPE: "uint",
        UNITS: "W",
        CONVERSION: "ac_w",
    },
    "ACGeneratorPower": {
        DESCRIPTION: 'AC Generator Power',
        ADDRESS: 41098,
        TYPE: "uint",
        UNITS: "W",
        CONVERSION: "ac_w",
    },
    "ACLoadkWhTotalAcc": {
        DESCRIPTION: 'AC Lifetime Load Energy',
        ADDRESS: 41438,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "ac_wh",
    },
    "BatteryVolts": {
        DESCRIPTION: 'Battery Volts',
        ADDRESS: 0xa05c,
        TYPE: "ushort",
        UNITS: "V",
        CONVERSION: "dc_v",
    },
    "DCBatteryPower": {
        DESCRIPTION: 'Battery Power',
        ADDRESS: 0xa02f,
        TYPE: "int",
        UNITS: "W",
        CONVERSION: "dc_w",
    },
    "Shunt1Power": {
        DESCRIPTION: 'Shunt 1 Power',
        ADDRESS: 0xa088,
        TYPE: "short",
        UNITS: "W",
        CONVERSION: "dc_w",
    },
    "Shunt2Power": {
        DESCRIPTION: 'Shunt 2 Power',
        ADDRESS: 0xa089,
        TYPE: "short",
        UNITS: "W",
        CONVERSION: "dc_w",
    },
    "Shunt1Name": {
        DESCRIPTION: 'Shunt 1 Name',
        ADDRESS: 0xc109,
        TYPE: "short",
        UNITS: "",
        CONVERSION: "shunt_name",
    },
    "Shunt2Name": {
        DESCRIPTION: 'Shunt 2 Name',
        ADDRESS: 0xc10a,
        TYPE: "short",
        UNITS: "",
        CONVERSION: "shunt_name",
    },
    "BatteryTemperature": {
        DESCRIPTION: "Battery Temperature",
        ADDRESS: 0xa03c,
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },
    "DCkWhOut": {
        ADDRESS: 41257,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "DCkWhOutToday": {
        ADDRESS: 41137,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "DCkWhInToday": {
        ADDRESS: 41135,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhAcc": {
        ADDRESS: 41143,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "QuickView_BattOutkWhAcc": {
        ADDRESS: 41178,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhPreviousAcc": {
        DESCRIPTION: "Battery Out Energy Today",
        ADDRESS: 41356,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWh7DayAcc": {
        ADDRESS: 41358,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWh7DayAccAvg": {
        ADDRESS: 41360,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWh30DayAcc": {
        ADDRESS: 41362,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWh30DayAccAvg": {
        ADDRESS: 41364,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWh365DayAcc": {
        ADDRESS: 41366,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWh365DayAccAvg": {
        ADDRESS: 41368,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhYearAcc": {
        ADDRESS: 41370,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhYearAccAvg": {
        ADDRESS: 41372,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhResetableAcc": {
        ADDRESS: 41374,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhResetableAccAvg": {
        ADDRESS: 41376,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattOutkWhTotalAcc": {
        DESCRIPTION: "Battery Out Energy Total Accumulated",
        ADDRESS: 41381,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattInkWhTotalAcc": {
        DESCRIPTION: "Battery In Energy Total Accumulated",
        ADDRESS: 41354,
        TYPE: "uint",
        UNITS: "Wh",
        CONVERSION: "dc_wh",
    },
    "BattSocPercent": {
        DESCRIPTION: "Battery State of Charge",
        ADDRESS: 41089,
        TYPE: "ushort",
        UNITS: "%",
        CONVERSION: "percent",
    },
    "ACInputWhTotalAcc": {
        DESCRIPTION: "Input energy accumulated total",
        ADDRESS: 41459,
        TYPE: "uint",
        CONVERSION: "ac_wh",
    },
    "ACInputWhTodayAcc": {
        DESCRIPTION: "Input energy accumulated today",
        ADDRESS: 41151,
        TYPE: "ushort",
        CONVERSION: "ac_wh",
    },
    "ACExportWhTotalAcc": {
        DESCRIPTION: "Export energy accumulated total",
        ADDRESS: 41499,
        TYPE: "uint",
        CONVERSION: "ac_wh",
    },
    "ACExportWhTodayAcc": {
        DESCRIPTION: "Export energy accumulated today",
        ADDRESS: 41154,
        TYPE: "ushort",
        CONVERSION: "ac_wh",
    },
    "ACLoadWhAcc": {
        DESCRIPTION: "Load energy accumulated today",
        ADDRESS: 41150,
        TYPE: "ushort",
        CONVERSION: "ac_wh",
    },
    "ACSolarWhTotalAcc": {
        DESCRIPTION: "AC coupled solar energy accumulated total",
        ADDRESS: 41519,
        TYPE: "uint",
        CONVERSION: "ac_wh",
    },
    "Shunt1WhTotalAcc": {
        DESCRIPTION: "Shunt 1 energy accumulated total",
        ADDRESS: 41305,
        TYPE: "int",
        CONVERSION: "dc_wh",
    },
    "ACSolarWhTodayAcc": {
        DESCRIPTION: "AC coupled solar energy accumulated today",
        ADDRESS: 41157,
        TYPE: "short",
        CONVERSION: "ac_wh",
    },
    "Shunt1WhTodayAcc": {
        DESCRIPTION: "Shunt 1 energy accumulated today",
        ADDRESS: 41146,
        TYPE: "short",
        CONVERSION: "dc_wh",
    },
    "ACGeneratorPower": {
        ADDRESS: 41098,
        TYPE: "short",
        CONVERSION: "ac_w_signed",
    },
    "LoginHash": {
        ADDRESS: 0x1f0000,
        TYPE: ""
    },
    "LoginStatus": {
        ADDRESS: 0x1f0010,
        TYPE: "ushort"
    },
    "GeneratorStatus": {
        ADDRESS: 41110,
        TYPE: "ushort",
        UNITS: ""  
    },
    "ChargeMode": {
        ADDRESS: 41755,
        TYPE: "ushort",
        UNITS: ""  
    },
    "AcSourceStatus": {
        ADDRESS: 41088,
        TYPE: "ushort",
        UNITS: ""  
    },
    "GeneratorStartReason": {
        ADDRESS: 41086,
        TYPE: "ushort",
        UNITS: ""
    },
    "GeneratorRunningReason": {
        ADDRESS: 41087,
        TYPE: "ushort",
        UNITS: ""
    },
    "AcOutStatus": {
        ADDRESS: 41085,
        TYPE: "ushort",
        UNITS: ""
    },      
    "DigitalInStatus1": {
        ADDRESS: 41042,
        TYPE: "ushort",
        UNITS: ""
    },                   
    "DigitalInStatus2": {
        ADDRESS: 41043,
        TYPE: "ushort",
        UNITS: ""
    },  
    "DigitalInStatus3": {
        ADDRESS: 41044,
        TYPE: "ushort",
        UNITS: ""
    },  
    "DigitalInStatus4": {
        ADDRESS: 41045,
        TYPE: "ushort",
        UNITS: ""
    },    
    "DigitalOutStatus1": {
        ADDRESS: 41035,
        TYPE: "ushort",
        UNITS: ""        
    },  
    "DigitalOutStatus2": {
        ADDRESS: 41036,
        TYPE: "ushort",
        UNITS: ""        
    }, 
    "DigitalOutStatus3": {
        ADDRESS: 41037,
        TYPE: "ushort",
        UNITS: ""        
    }, 
    "DigitalOutStatus4": {
        ADDRESS: 41038,
        TYPE: "ushort",
        UNITS: ""        
    }, 
    "DigitalOutStatus5": {
        ADDRESS: 41039,
        TYPE: "ushort",
        UNITS: ""        
    }, 
    "DigitalOutStatus6": {
        ADDRESS: 41040,
        TYPE: "ushort",
        UNITS: ""        
    }, 
    "DigitalOutStatus7": {
        ADDRESS: 41041,
        TYPE: "ushort",
        UNITS: ""        
    },
    "ActiveSchedule": {
        ADDRESS: 41072,
        TYPE: "ushort",
        UNITS: ""      
    }, 
    "FloatMinutesToday": {
        ADDRESS: 41148,
        TYPE: "ushort",
        UNITS: "Minutes"   
    },   
    "ACLoadVoltage": {
        ADDRESS: 41234,
        TYPE: "ushort",
        UNITS: "V",
        CONVERSION: "ac_v"
    },        
    "AcHz": {
        ADDRESS: 41101,
        TYPE: "ushort",
        UNITS: "Hz",
        CONVERSION: "ac_hz"   
    }, 
    "AnalogueDcVoltage1": {
        ADDRESS: 41046,
        TYPE: "ushort",
        UNITS: "V",
        CONVERSION: "dc_v"   
    },
    "AnalogueDcVoltage2": {
        ADDRESS: 41047,
        TYPE: "ushort",
        UNITS: "V",
        CONVERSION: "dc_v"   
    },   
    "ServiceRequiredReason0": { 
        ADDRESS: 41533, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason1": { 
        ADDRESS: 41534, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason2": { 
        ADDRESS: 41535, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason3": { 
        ADDRESS: 41536, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason4": { 
        ADDRESS: 41537, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason5": { 
        ADDRESS: 41538, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason6": { 
        ADDRESS: 41539, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason7": { 
        ADDRESS: 41540, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason8": { 
        ADDRESS: 41541, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason9": { 
        ADDRESS: 41542, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason10": { 
        ADDRESS: 41543, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason11": { 
        ADDRESS: 41544, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason12": { 
        ADDRESS: 41545, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason13": { 
        ADDRESS: 41546, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason14": { 
        ADDRESS: 41547, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason15": { 
        ADDRESS: 41548, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason16": { 
        ADDRESS: 41549, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason17": { 
        ADDRESS: 41550, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason18": { 
        ADDRESS: 41551, 
        TYPE: "ushort",
        UNITS: ""
    },
    "ServiceRequiredReason19": { 
        ADDRESS: 41552, 
        TYPE: "ushort",
        UNITS: ""
    },  
    "PowerModuleAirTemperature": { 
        DESCRIPTION: "Power Module (Inlet) Air Temperature",
        ADDRESS: 41022, 
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },
    "TransformerTemperature": { 
        DESCRIPTION: "Transformer Temperature",
        ADDRESS: 41021, 
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },
    "InternalTemperature": { 
        DESCRIPTION: "Control Board (Internal) Temperature",
        ADDRESS: 41019, 
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },  
    "HalfBridge1HeatsinkTemperature": { 
        DESCRIPTION: "Half Bridge 1 Heatsink Temperature",
        ADDRESS: 41015, 
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },  
    "HalfBridge2HeatsinkTemperature": { 
        DESCRIPTION: "Half Bridge 2 Heatsink Temperature",
        ADDRESS: 41016, 
        TYPE: "ushort",
        UNITS: "°C",
        CONVERSION: "temperature",
    },          
    "FanSpeed": { 
        DESCRIPTION: "Fan Speed",
        ADDRESS: 41026, 
        TYPE: "ushort",
        UNITS: "%",
        CONVERSION: "percent",
    },      
}

TYPES = {
    "ushort": {
        FORMAT: "<H",
        WORDS: 1,
    },
    "short": {
        FORMAT: "<h",
        WORDS: 1,
    },
    "uint": {
        FORMAT: "<I",
        WORDS: 2,
    },
    "int": {
        FORMAT: "<i",
        WORDS: 2,
    },
}

class Variable:
    def __init__(self, name: str, address: int, bytes: bytes=b'\x00\x00'):
        self.__name = name
        self.__address = address
        self.__bytes = bytes

    def get_name(self):
        return self.__name

    """
    Get the memory range for this variable
    """
    @property
    def range(self):
        return Range(self.__address, TYPES[self.get_type()][WORDS])

    def get_type(self):
        if not self.__name in MAP:
            return 'ushort'
        return MAP[self.__name][TYPE]

    """
    Set the internal bytes
    """
    @property
    def bytes(self):
        return self.__bytes

    @bytes.setter
    def bytes(self, bytes):
        self.__bytes = bytes

    """
    Get the converted value
    """
    def get_value(self, scales: dict):
        if not self.is_known():
            raise Exception("Can not convert value for unknown variable type")
        mem_info = MAP[self.__name]
        type_info = TYPES[self.get_type()]
        format = type_info["format"]
        unscaled = struct.unpack(format, self.__bytes)[0]
        if not CONVERSION in mem_info:
            return unscaled
        return convert(mem_info[CONVERSION], unscaled, scales)

    def is_known(self):
        return self.__name in MAP
