# Selpi

Selpi is woefully incomplete, but in the long run it will hopefully be a collection of basic utilties to monitor a Selectronic SP Pro 2 from a RaspberryPi.

Additional docs:

 * [Connecting](docs/connecting.md)
 * [Protocol](docs/protocol.md)
 * [Developing](docs/developing.md)

# License / Warranty

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

For those unfamiliar please note that this means no warranty OF ANY KIND is granted with this code, further it is possible using this code may impact on any warranty from Selectronic.

# Getting Started

Ensure your device is [connecting](docs/connecting.md) to the SP Pro.

[Pipenv](https://github.com/pypa/pipenv) is used to control managed dependencies, if it's not already installed, install it:

```
$ pip install pipenv
[...]
Successfully installed certifi-2019.9.11 enum34-1.1.6 pip-19.3.1 pipenv-2018.11.26 setuptools-41.4.0 typing-3.7.4.1 virtualenv-16.7.6 virtualenv-clone-0.5.3
```

Install dependencies with:

```
$ pipenv install
```

The `./selpi` will try to launch `selpi` within the pipenv, so just run:

```
$ ./selpi
Loading .env environment variables...
usage: selpi.py [-h] [--log {info,debug,warning,error,critical}] {command} ...

positional arguments:
  {command}             command to run
    dump                dump memory to stdout
    http                start http server
    http-select         select.live http emulation
    proxy               expose SP PRO over TCP proxy
    scan                scan known addresses
    stat                show known stats
    http-ha             additional functionality

options:
  -h, --help            show this help message and exit
  --log {info,debug,warning,error,critical}
                        log level
  --logfile {name of log file, if arg not used file logging does not occur}                        
```

# Commands

Selpi uses a sub command structure meaning the base `selpi` accepts multiple commands that run it in different modes.

See `selpi --help` for a full list of commands, some commands are documented below.

Additional logging output can be printed with `selpi --log=debug ...`.

## http-select

```
$ ./selpi http-select
Loading .env environment variables...
Starting server on port 8000
```

Once running it will respond to all HTTP requests with a payload similar to the point API on select.live devices, e.g:

```
$ curl -s http://localhost:8000/cgi-bin/solarmonweb/devices/SOMEDEVICE/point
{
  "device":{
    "name":"Selectronic SP-PRO"
  },
  "item_count":19,
  "items":{
    "battery_in_wh_today":11.443359375,
    "battery_in_wh_total":6813.32080078125,
    "battery_out_wh_today":8.21337890625,
    "battery_out_wh_total":6789.603515625,
    "battery_soc":99.0859375,
    "battery_w":707.51953125,
    "grid_in_wh_today":0.3416015625,
    "grid_in_wh_total":43.810400390625,
    "grid_out_wh_today":0.0,
    "grid_out_wh_total":0.0,
    "grid_w":-3.558349609375,
    "load_w":678.3103942871094,
    "load_wh_today":22410.514306640624,
    "load_wh_total":15489.325048828125,
    "shunt_w":23.0712890625,
    "solar_wh_today":27.761865234375,
    "solar_wh_total":17579.099853515625,
    "solarinverter_w":56.93359375,
    "timestamp":1664611058
  },
  "comment":"energies are actually in kWh, not Wh",
  "now":1664611058
}
```

Note: `fault_code`, `fault_ts` and `gen_status` are missing.

## proxy

The `proxy` command is used to expose the Selectronic SP PRO over TCP.

The listening address and port can be controlled from `.env.local`.

To start the proxy run:

```
$ ./selpi proxy
```

TP LINK can then be configured to connect to the device `selpi` is started on.

## stat

The `stat` command displays the currently known stats from the SP PRO:

```bash
$ ./selpi stat
[
  {
    "description": "AC Solar Power",
    "name": "CombinedKacoAcPowerHiRes",
    "value": 4707.696533203125,
    "units": "W"
  },
  {
    "description": "Shunt 1 Name",
    "name": "Shunt1Name",
    "value": "Solar",
    "units": ""
  },
...
  {
    "description": "Battery Out Energy Today",
    "name": "BattOutkWhPreviousAcc",
    "value": 5998.53515625,
    "units": "Wh"
  },
  {
    "description": "Battery State of Charge",
    "name": "BattSocPercent",
    "value": 87.55859375,
    "units": "%"
  }
]
```

## http-ha
```
$ ./selpi http-ha
Starting server on port 8001
```

Once running includes the standard select.live emulation plus new call that includes additional variables:
* Service Required Codes
* AC Load Voltage and Hz
* All the digital inputs and outputs
* Charger Mode
* Inverter Mode
* AC Output Status
* AC Source Status
* Generator Start and Run Reason Codes
* Battery and Sp Pro Internal Temperature
* Fan Speed
* Minutes that Batteries have been at float today
* Hybrid Active Schedule (Used for grid connnected systems) 

Summary of Http Calls Available:
* GET: ip_address_selpi_device:8001/havalues
* GET: ip_address_selpi_device:8001/selectlive
* GET: ip_address_selpi_device:8001/state
* POST: ip_address_selpi_device:8001/http/start
* POST: ip_address_selpi_device:8001/http/stop


### HA VALUES: 

GET: ip_address_selpi_device:8001/havalues

Returns following json payload.
Note: Inclusion of Result object that includes Success flag and a message

```json
{
  "device":{
    "name":"Selectronic SP-PRO"
  },
  "item_count":47,
  "items":{
    "battery_in_wh_today":15.2578125,
    "battery_in_wh_total":505.96875,
    "battery_out_wh_today":6.029296875,
    "battery_out_wh_total":503.015625,
    "battery_soc":98.61328125,
    "battery_w":-71.77734375,
    "gen_status":10,
    "grid_in_wh_today":0.11389306640625,
    "grid_in_wh_total":66.85522998046875,
    "grid_out_wh_today":0.6833583984375,
    "grid_out_wh_total":331.54271630859375,
    "grid_w":1869.7445068359375,
    "load_w":384.38909912109375,
    "load_wh_today":5.4668671875,
    "load_wh_total":754.6554580078125,
    "shunt_w":0.0,
    "solar_wh_today":12.0726650390625,
    "solar_wh_total":1171.5040810546875,
    "solarinverter_w":2424.9732055664062,
    "ChargeMode":0,
    "GeneratorStartReason":0,
    "GeneratorRunningReason":0,
    "AcSourceStatus":7,
    "AcOutStatus":3,
    "DigitalInStatus1":0,
    "DigitalInStatus2":0,
    "DigitalInStatus3":0,
    "DigitalInStatus4":1,
    "DigitalOutStatus1":0,
    "DigitalOutStatus2":0,
    "DigitalOutStatus3":0,
    "RelayOutStatus1":0,
    "RelayOutStatus2":0,
    "RelayOutStatus3":0,
    "RelayOutStatus4":1,
    "AnalogueDcVoltage1":0.330047607421875,
    "AnalogueDcVoltage2":0.323638916015625,
    "BatteryVolts":56.396484375,
    "BatteryTemperature":20.71929931640625,
    "InternalTemperature":34.9688720703125,
    "FanSpeed":26.0,
    "ActiveSchedule":8,
    "FloatMinutesToday":0,
    "ACLoadVoltage":246.49658203125,
    "AcHz":50.03,
    "ServiceRequiredReasonCodesAsCsv":"",
    "timestamp":1719558422
  },
  "now":1719558422,
  "Result":{
    "Success":true,
    "Message":""
  }
}
```

### SELECT LIVE:
Same as select live emulation

### STATE
GET: ip_address_selpi_device:8001/state
Returns current http server state

```json
{
  "AllowSpProAccess":true,
  "Result":{
    "Success":true,
    "Message":""
  }
}
```

### HTTP STOP
POST: ip_address_selpi_device:8001/http/stop

Stops access to SP Pro via the web service.
Used to pause access to Sp Pro if you have another process calling at regular interval that you want to prevent access Sp Pro.

```json
{
  "AllowSpProAccess":false,
  "Result":{
    "Success":true,
    "Message":""
  }
}
```

### HTTP START
POST: ip_address_selpi_device:8001/http/start

Allows access to Sp Pro via web service

```json
{
  "AllowSpProAccess":true,
  "Result":{
    "Success":true,
    "Message":""
  }
}
```



# Acknowledgements

This repository is primarily maintained by [David Schoen](http://github.com/neerolyte).

Foundational code and inspirational advice provided by [Justin Stafford](https://www.linkedin.com/in/justin-stafford-blueshift/).
