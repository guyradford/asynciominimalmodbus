# Asyncio Minimal Modbus

![Build Status](https://github.com/guyradford/asynciominimalmodbus/actions/workflows/pipeline.yml/badge.svg)

Async library wrapping the Easy-to-use Modbus RTU and Modbus ASCII implementation 
[Minimal Modbus](https://github.com/pyhys/minimalmodbus).

This library is purely an asyncio wrapper for Minimal Modbus, it supports the same interface, and should be 100% 
drop in other than needing to add `await`.

Supports Python 3.6, 3.7, 3.8. 3.9 and 3.10

## Installation

```shell
pip install asynciominimalmodbus
```

### Dependencies
* Minimal Modbus v2.0.1 or greater, 
* pySerial 3.0 or greater.


## Features as described by Minimal Modbus
>MinimalModbus is an easy-to-use Python module for talking to instruments (slaves)
>from a computer (master) using the Modbus protocol, and is intended to be running on th*e mast*er.
>The only dependence is the pySerial module (also pure Python).
>
>There are convenience functions to handle floats, strings and long integers
>(in different byte orders).
?
>This software supports the 'Modbus RTU' and 'Modbus ASCII' serial communication
>versions of the protocol, and is intended for use on Linux, OS X and Windows platforms.

Minimal Modbus Documentation: [https://minimalmodbus.readthedocs.io/en/stable/](https://minimalmodbus.readthedocs.io/en/stable/)


## Contributing

* Issues: https://github.com/guyradford/asynciominimalmodbus/issues
* Github: https://github.com/guyradford/asynciominimalmodbus
