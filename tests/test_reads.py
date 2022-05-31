import asyncio
from unittest import mock
from unittest.mock import Mock

import pytest
from minimalmodbus import BYTEORDER_BIG, BYTEORDER_LITTLE, BYTEORDER_BIG_SWAP

from asyncioinstrument import AsyncioInstrument

loop = asyncio.get_event_loop()


def data_provider_test_read_value_with_defaults():
    return [
        ('read_bit', 100, 1, {'functioncode': 2}),
        ('read_register', 100, 1, {'functioncode': 3, 'number_of_decimals': 0, 'signed': False}),
        ('read_long', 100, 12345678, {'functioncode': 3, 'signed': False, 'byteorder': BYTEORDER_BIG}),
        ('read_float', 100, 123.456, {'functioncode': 3, 'number_of_registers': 2, 'byteorder': BYTEORDER_BIG}),
        ('read_float', 100, 321, {'functioncode': 3, 'number_of_registers': 2, 'byteorder': BYTEORDER_BIG}),
        ('read_string', 100, "Testing", {'number_of_registers': 16, 'functioncode': 3}),
    ]


@pytest.mark.parametrize("method, registeraddress, expected, defaults", data_provider_test_read_value_with_defaults())
def test_read_value_with_defaults(method, registeraddress, expected, defaults):
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock(return_value=expected)
        setattr(async_instrument.instrument, method, method_mock)

        async def test_function():
            cal_method = getattr(async_instrument, method)
            value = await cal_method(registeraddress)

            assert expected == value
            method_mock.assert_called_once_with(registeraddress=registeraddress, **defaults)

        loop.run_until_complete(test_function())


def data_provider_test_read_values_with_defaults():
    return [
        ('read_bits', 200, 3, [1, 0, 1], {'number_of_bits': 3, 'functioncode': 2}),
        ('read_registers', 200, 3, [4, 5, 6], {'number_of_registers': 3, 'functioncode': 3, }),
    ]


@pytest.mark.parametrize("method, registeraddress, number_of_, expected, defaults",
                         data_provider_test_read_values_with_defaults())
def test_read_values_with_defaults(method, registeraddress, number_of_, expected, defaults):
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock(return_value=expected)
        setattr(async_instrument.instrument, method, method_mock)

        async def test_function():
            cal_method = getattr(async_instrument, method)
            value = await cal_method(registeraddress, number_of_)

            assert expected == value
            method_mock.assert_called_once_with(registeraddress=registeraddress, **defaults)

        loop.run_until_complete(test_function())


def data_provider_test_read_values_override_defaults():
    return [
        ('read_bit', {'registeraddress': 300, 'functioncode': 1}, 3),
        ('read_bit', {'registeraddress': 400, 'functioncode': 3}, 4),

        ('read_bits', {'registeraddress': 300, 'number_of_bits': 1, 'functioncode': 1}, [4]),
        ('read_bits', {'registeraddress': 400, 'number_of_bits': 4, 'functioncode': 3}, [1, 2, 3, 4]),

        ('read_register', {'registeraddress': 300, 'number_of_decimals': 1, 'functioncode': 1, 'signed': True}, 4),
        ('read_register', {'registeraddress': 400, 'number_of_decimals': 5, 'functioncode': 2, 'signed': False}, 5),

        ('read_long', {'registeraddress': 300, 'functioncode': 1, 'signed': True, 'byteorder': BYTEORDER_LITTLE}, 4),
        ('read_long', {'registeraddress': 400, 'functioncode': 3, 'signed': False, 'byteorder': BYTEORDER_BIG_SWAP}, 6),

        ('read_float',
         {'registeraddress': 300, 'functioncode': 1, 'number_of_registers': 1, 'byteorder': BYTEORDER_LITTLE}, 4.4),
        ('read_float',
         {'registeraddress': 400, 'functioncode': 3, 'number_of_registers': 2, 'byteorder': BYTEORDER_BIG_SWAP}, 6.88),

        ('read_string', {'registeraddress': 300, 'functioncode': 1, 'number_of_registers': 10, }, "Testing"),
        ('read_string', {'registeraddress': 400, 'functioncode': 3, 'number_of_registers': 20, }, "Test 1 2 3"),

        ('read_registers', {'registeraddress': 300, 'functioncode': 1, 'number_of_registers': 1, }, [4]),
        ('read_registers', {'registeraddress': 400, 'functioncode': 3, 'number_of_registers': 4, }, [4, 5, 6, 7]),
    ]


@pytest.mark.parametrize("method, params, expected",
                         data_provider_test_read_values_override_defaults())
def test_read_with_values_override_defaults(method, params, expected):
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        method_mock = Mock(return_value=expected)
        setattr(async_instrument.instrument, method, method_mock)

        async def test_function():
            cal_method = getattr(async_instrument, method)
            value = await cal_method(**params)

            assert expected == value
            method_mock.assert_called_once_with(**params)

        loop.run_until_complete(test_function())
