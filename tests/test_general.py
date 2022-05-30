import asyncio
from unittest import mock
from unittest.mock import Mock

import pytest
from minimalmodbus import MODE_ASCII

from asyncioinstrument import AsyncioInstrument

loop = asyncio.get_event_loop()


def test_init_with_defaults():
    port = "Test Port"
    slave_address = 0x99

    with mock.patch('asyncioinstrument.Instrument') as instrument:
        AsyncioInstrument(port, slave_address)

        instrument.assert_called_once_with(port, slave_address, 'rtu', False, False)


def test_init_override_defaults():
    port = "Test Port"
    slave_address = 0x99

    with mock.patch('asyncioinstrument.Instrument') as instrument:
        AsyncioInstrument(
            port,
            slave_address,
            MODE_ASCII,
            True,
            True
        )

        instrument.assert_called_once_with(port, slave_address, 'ascii', True, True)


def test_init_with_loop():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("Test Port", 0x99, loop=loop)

        assert loop == async_instrument.loop


def test_init_without_loop():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("Test Port", 0x99)

        assert loop == async_instrument.loop


@pytest.mark.skip(reason="Still need to drill down into ids etc.")
def test___repr__():
    with mock.patch('asyncioinstrument.Instrument') as instrument:
        instrument.__repr__ = Mock(
            return_value="minimalmodbus.Instrument<id=0x254dfd4e708, address=99, mode=rtu, close_port_after_each_call=False, precalculate_read_size=True, clear_buffers_before_each_transaction=True, handle_local_echo=False, debug=False, serial=Serial<id=0x254dfd4e888, open=True>(port='COMx', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.05, xonxoff=False, rtscts=False, dsrdtr=False)>")  # pylint: disable=C0301
        async_instrument = AsyncioInstrument("COMx", 0x99)

        assert "asyncioinstrument.AsyncioInstrument<id=0x23f4a898248, instrument=<MagicMock name='Instrument()' id='2470856721096'>>" == repr(  # pylint: disable=C0301
            async_instrument)


def test_serial_property():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        expected_serial = Mock()
        async_instrument.instrument.serial = expected_serial

        assert expected_serial == async_instrument.serial


def test_precalculate_read_size_property():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        expected = True
        async_instrument.instrument.precalculate_read_size = expected

        assert expected == async_instrument.precalculate_read_size


def test_clear_buffers_before_each_transaction_property():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        expected = True
        async_instrument.instrument.clear_buffers_before_each_transaction = expected

        assert expected == async_instrument.clear_buffers_before_each_transaction


def test_handle_local_echo_property():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        expected = True
        async_instrument.instrument.handle_local_echo = expected

        assert expected == async_instrument.handle_local_echo


def test_roundtrip_time_property():
    with mock.patch('asyncioinstrument.Instrument'):
        async_instrument = AsyncioInstrument("COMx", 0x99)

        expected = 12.3
        async_instrument.instrument.roundtrip_time = expected

        assert expected == async_instrument.roundtrip_time
