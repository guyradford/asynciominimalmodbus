import asyncio
from unittest import mock, TestCase
from unittest.mock import Mock

import pytest
from minimalmodbus import MODE_ASCII, BYTEORDER_BIG, BYTEORDER_LITTLE, BYTEORDER_BIG_SWAP

from asyncioinstrument import AsyncioInstrument

loop = asyncio.get_event_loop()


def data_provider_test_write_value_with_defaults():
    return [
        ('write_bit', 100, 1, {'functioncode': 5}),
        ('write_register', 100, 1, {'functioncode': 16, 'number_of_decimals': 0, 'signed': False}),
        ('write_long', 100, 12345678, {'signed': False, 'byteorder': BYTEORDER_BIG}),
        ('write_float', 100, 123.456, {'number_of_registers': 2, 'byteorder': BYTEORDER_BIG}),
        ('write_float', 100, 321, {'number_of_registers': 2, 'byteorder': BYTEORDER_BIG}),
    ]


@pytest.mark.parametrize("method, registeraddress, expected, defaults", data_provider_test_write_value_with_defaults())
def test_write_value_with_defaults(method, registeraddress, expected, defaults):
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock()
        setattr(async_instrument.instrument, method, method_mock)

        async def test_function():
            cal_method = getattr(async_instrument, method)
            await cal_method(registeraddress, expected)

            method_mock.assert_called_once_with(registeraddress=registeraddress, value=expected, **defaults)

        loop.run_until_complete(test_function())


def test_write_string_with_defaults():
    registeraddress = 200
    expected = "Testing"

    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock()
        async_instrument.instrument.write_string = method_mock

        async def test_function():
            await async_instrument.write_string(registeraddress, expected)

            method_mock.assert_called_once_with(registeraddress=registeraddress, textstring=expected,
                                                number_of_registers=16)

        loop.run_until_complete(test_function())


def data_provider_test_write_values_with_defaults():
    return [
        ('write_bits', 200, [1, 0, 1], {}),
        ('write_registers', 200, [4, 5, 6], {}),
    ]


@pytest.mark.parametrize("method, registeraddress, expected, defaults",
                         data_provider_test_write_values_with_defaults())
def test_write_calues_with_defaults(method, registeraddress, expected, defaults):
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock()
        setattr(async_instrument.instrument, method, method_mock)

        async def test_function():
            cal_method = getattr(async_instrument, method)
            await cal_method(registeraddress, expected)

            method_mock.assert_called_once_with(registeraddress=registeraddress, values=expected, **defaults)

        loop.run_until_complete(test_function())


def data_provider_test_write_values_override_defaults():
    return [
        ('write_bit', {'registeraddress': 300, 'value': 3, 'functioncode': 2}),
        ('write_bit', {'registeraddress': 400, 'value': 4, 'functioncode': 1}),

        ('write_bits', {'registeraddress': 300, 'values': [4]}),
        ('write_bits', {'registeraddress': 400, 'values': [1, 2, 3, 4]}),

        ('write_register',
         {'registeraddress': 300, 'value': 4, 'number_of_decimals': 1, 'functioncode': 1, 'signed': True}),
        ('write_register',
         {'registeraddress': 400, 'value': 5, 'number_of_decimals': 5, 'functioncode': 2, 'signed': False}),

        ('write_long',
         {'registeraddress': 300, 'value': 4, 'signed': True, 'byteorder': BYTEORDER_LITTLE}),
        ('write_long',
         {'registeraddress': 400, 'value': 6, 'signed': False, 'byteorder': BYTEORDER_BIG_SWAP}),

        ('write_float',
         {'registeraddress': 300, 'value': 4.4, 'number_of_registers': 1, 'byteorder': BYTEORDER_LITTLE}),
        ('write_float',
         {'registeraddress': 400, 'value': 6.88, 'number_of_registers': 2, 'byteorder': BYTEORDER_BIG_SWAP}),

        ('write_string', {'registeraddress': 300, 'textstring': "Testing", 'number_of_registers': 10}),
        ('write_string', {'registeraddress': 400, 'textstring': "Test 1 2 3", 'number_of_registers': 20}),

        ('write_registers', {'registeraddress': 300, 'values': [4]}),
        ('write_registers', {'registeraddress': 400, 'values': [4, 5, 6, 7]}),
    ]


@pytest.mark.parametrize("method, params",
                         data_provider_test_write_values_override_defaults())
def test_write_with_values_override_defaults(method, params):
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock()
        setattr(async_instrument.instrument, method, method_mock)

        async def test_function():
            cal_method = getattr(async_instrument, method)
            await cal_method(**params)

            method_mock.assert_called_once_with(**params)

        loop.run_until_complete(test_function())
