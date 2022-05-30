# -*- coding: utf-8 -*-
#
#   Copyright 2022 Guy Radford
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""AsyncioMinimalModbus: A Python class that wraps MinimalModbus to add Async functionality."""

__author__ = "Guy Radford"
__license__ = "Apache License, Version 2.0"
__url__ = "https://github.com/pyhys/minimalmodbus"
__version__ = "0.0.0"

import asyncio
import sys

import serial
from minimalmodbus import Instrument, MODE_RTU, BYTEORDER_BIG

if sys.version_info < (3, 6, 0):
    raise ImportError(
        "Your Python version is too old for this version of MinimalModbus"
    )

from typing import List, Optional, Union  # noqa: E402


# ################################ #
# ASYNCIO Modbus instrument object #
# ################################ #


class AsyncioInstrument:
    """Asyncio Instrument class for talking to modbus instruments (slaves).

    This class wraps 'minimalmodbus' ("https://github.com/pyhys/minimalmodbus")
    allowing easy integration into an asyncio project. All the modbus work is
    handled by 'minimalmodbus'.

    Uses the Modbus RTU or ASCII protocols (via RS485 or RS232).

    Args:
        * port: The serial port name, for example ``/dev/ttyUSB0`` (Linux),
          ``/dev/tty.usbserial`` (OS X) or ``COM4`` (Windows).
        * slaveaddress: Slave address in the range 0 to 247 (use decimal numbers,
          not hex). Address 0 is for broadcast, and 248-255 are reserved.
        * mode: Mode selection. Can be :data:`minimalmodbus.MODE_RTU` or
          :data:`minimalmodbus.MODE_ASCII`.
        * close_port_after_each_call: If the serial port should be closed after
          each call to the instrument.
        * debug: Set this to :const:`True` to print the communication details
        * loop: The asyncio loop to run these commands.

    """

    def __init__(
            self,
            port: str,
            slaveaddress: int,
            mode: str = MODE_RTU,
            close_port_after_each_call: bool = False,
            debug: bool = False,
            loop=None
    ) -> None:

        self.instrument = Instrument(
            port,
            slaveaddress,
            mode,
            close_port_after_each_call,
            debug)

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

    def __repr__(self) -> str:
        """Give string representation of the :class:`.Instrument` object."""
        template = (
            "{}.{}<id=0x{:x}, instrument={}>"
        )
        return template.format(
            self.__module__,
            self.__class__.__name__,
            id(self),
            self.instrument,
        )

    @property
    def serial(self) -> serial.Serial:
        """
        :return: serial.Serial
        """
        return self.instrument.serial

    @property
    def precalculate_read_size(self) -> bool:
        return self.instrument.precalculate_read_size

    @property
    def clear_buffers_before_each_transaction(self) -> bool:
        return self.instrument.clear_buffers_before_each_transaction

    @property
    def handle_local_echo(self) -> bool:
        return self.instrument.handle_local_echo

    @property
    def roundtrip_time(self) -> Optional[float]:
        return self.instrument.roundtrip_time

    async def read_bit(self, registeraddress: int, functioncode: int = 2) -> int:
        """
        For method documentation refer to Instrument.read_bit()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_bit(
                registeraddress=registeraddress,
                functioncode=functioncode
            )
        )

    async def write_bit(
            self, registeraddress: int, value: int, functioncode: int = 5
    ) -> None:
        """
        For method documentation refer to Instrument.write_bit()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_bit(
                registeraddress=registeraddress,
                value=value,
                functioncode=functioncode
            )
        )

    async def read_bits(
            self, registeraddress: int, number_of_bits: int, functioncode: int = 2
    ) -> List[int]:
        """
        For method documentation refer to Instrument.read_bits()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_bits(
                registeraddress=registeraddress,
                number_of_bits=number_of_bits,
                functioncode=functioncode
            )
        )

    async def write_bits(self, registeraddress: int, values: List[int]) -> None:
        """
        For method documentation refer to Instrument.write_bits()
        """
        await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_bits(
                registeraddress=registeraddress,
                values=values,
            )
        )

    async def read_register(
            self,
            registeraddress: int,
            number_of_decimals: int = 0,
            functioncode: int = 3,
            signed: bool = False,
    ) -> Union[int, float]:
        """
        For method documentation refer to Instrument.read_register()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_register(
                registeraddress=registeraddress,
                number_of_decimals=number_of_decimals,
                functioncode=functioncode,
                signed=signed
            )
        )

    async def write_register(
            self,
            registeraddress: int,
            value: Union[int, float],
            number_of_decimals: int = 0,
            functioncode: int = 16,
            signed: bool = False,
    ) -> None:
        """
        For method documentation refer to Instrument.write_register()
        """

        await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_register(
                registeraddress=registeraddress,
                value=value,
                number_of_decimals=number_of_decimals,
                functioncode=functioncode,
                signed=signed
            )
        )

    async def read_long(
            self,
            registeraddress: int,
            functioncode: int = 3,
            signed: bool = False,
            byteorder: int = BYTEORDER_BIG,
    ) -> int:
        """
        For method documentation refer to Instrument.read_long()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_long(
                registeraddress=registeraddress,
                functioncode=functioncode,
                signed=signed,
                byteorder=byteorder
            )
        )

    async def write_long(
            self,
            registeraddress: int,
            value: int,
            signed: bool = False,
            byteorder: int = BYTEORDER_BIG,
    ) -> None:
        """
        For method documentation refer to Instrument.write_long()
        """

        await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_long(
                registeraddress=registeraddress,
                value=value,
                signed=signed,
                byteorder=byteorder,
            )
        )

    async def read_float(
            self,
            registeraddress: int,
            functioncode: int = 3,
            number_of_registers: int = 2,
            byteorder: int = BYTEORDER_BIG,
    ) -> float:
        """
        For method documentation refer to Instrument.read_float()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_float(
                registeraddress=registeraddress,
                functioncode=functioncode,
                number_of_registers=number_of_registers,
                byteorder=byteorder
            )
        )

    async def write_float(
            self,
            registeraddress: int,
            value: Union[int, float],
            number_of_registers: int = 2,
            byteorder: int = BYTEORDER_BIG,
    ) -> None:
        """
        For method documentation refer to Instrument.write_float()
        """

        await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_float(
                registeraddress=registeraddress,
                value=value,
                number_of_registers=number_of_registers,
                byteorder=byteorder,
            )
        )

    async def read_string(
            self, registeraddress: int, number_of_registers: int = 16, functioncode: int = 3
    ) -> str:
        """
        For method documentation refer to Instrument.read_string()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_string(
                registeraddress=registeraddress,
                number_of_registers=number_of_registers,
                functioncode=functioncode,
            )
        )

    async def write_string(
            self, registeraddress: int, textstring: str, number_of_registers: int = 16
    ) -> None:
        """
        For method documentation refer to Instrument.write_string()
        """

        await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_string(
                registeraddress=registeraddress,
                textstring=textstring,
                number_of_registers=number_of_registers,
            )
        )

    async def read_registers(
            self, registeraddress: int, number_of_registers: int, functioncode: int = 3
    ) -> List[int]:
        """
        For method documentation refer to Instrument.read_registers()
        """

        return await self.loop.run_in_executor(
            None,
            lambda: self.instrument.read_registers(
                registeraddress=registeraddress,
                number_of_registers=number_of_registers,
                functioncode=functioncode,
            )
        )

    async def write_registers(self, registeraddress: int, values: List[int]) -> None:
        """
        For method documentation refer to Instrument.write_registers()
        """

        await self.loop.run_in_executor(
            None,
            lambda: self.instrument.write_registers(
                registeraddress=registeraddress,
                values=values,
            )
        )
