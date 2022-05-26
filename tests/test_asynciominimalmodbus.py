import asyncio
import unittest
from unittest import mock
from unittest.mock import Mock

from minimalmodbus import MODE_ASCII

from asyncioinstrument import AsyncioInstrument

loop = asyncio.get_event_loop()


class TestAsyncioInstrument(unittest.TestCase):

    def test_init_with_defaults(self):
        port = "Test Port"
        slave_address = 0x99

        with mock.patch('asyncioinstrument.Instrument') as instrument:
            AsyncioInstrument(port, slave_address)

            instrument.assert_called_once_with(port, slave_address, 'rtu', False, False)

    def test_init_override_defaults(self):
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

    def test_init_with_loop(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("Test Port", 0x99)

            self.assertEqual(loop, async_instrument.loop)

    def test_init_without_loop(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("Test Port", 0x99)

            self.assertEqual(loop, async_instrument.loop)

    def test___repr__(self):
        with mock.patch('asyncioinstrument.Instrument') as instrument:
            instrument.__repr__ = Mock(
                return_value="minimalmodbus.Instrument<id=0x254dfd4e708, address=99, mode=rtu, close_port_after_each_call=False, precalculate_read_size=True, clear_buffers_before_each_transaction=True, handle_local_echo=False, debug=False, serial=Serial<id=0x254dfd4e888, open=True>(port='COMx', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.05, xonxoff=False, rtscts=False, dsrdtr=False)>")
            async_instrument = AsyncioInstrument("COMx", 0x99)

            self.assertEqual(
                "asyncioinstrument.AsyncioInstrument<id=0x23f4a898248, instrument=<MagicMock name='Instrument()' id='2470856721096'>>",
                repr(async_instrument))

    def test_serial_property(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            expected_serial = Mock()
            async_instrument.instrument.serial = expected_serial

            self.assertEqual(expected_serial, async_instrument.serial)

    def test_precalculate_read_size_property(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            expected = True
            async_instrument.instrument.precalculate_read_size = expected

            self.assertEqual(expected, async_instrument.precalculate_read_size)

    def test_clear_buffers_before_each_transaction_property(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            expected = True
            async_instrument.instrument.clear_buffers_before_each_transaction = expected

            self.assertEqual(expected, async_instrument.clear_buffers_before_each_transaction)

    def test_handle_local_echo_property(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            expected = True
            async_instrument.instrument.handle_local_echo = expected

            self.assertEqual(expected, async_instrument.handle_local_echo)

    def test_roundtrip_time_property(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            expected = 12.3
            async_instrument.instrument.roundtrip_time = expected

            self.assertEqual(expected, async_instrument.roundtrip_time)

    def test_read_bit(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            read_bit = Mock(return_value=1)
            async_instrument.instrument.read_bit = read_bit

            async def test_function():
                value = await async_instrument.read_bit(100)

                self.assertEqual(1, value)
                read_bit.assert_called_once_with(registeraddress=100, functioncode=2)


            loop.run_until_complete(test_function())


    def test_write_bit(self):
        with mock.patch('asyncioinstrument.Instrument'):
            async_instrument = AsyncioInstrument("COMx", 0x99)

            write_bit = Mock()
            async_instrument.instrument.write_bit = write_bit

            async def test_function():
                await async_instrument.write_bit(100, 1)
                write_bit.assert_called_once_with(registeraddress=100, value=1, functioncode=5)

            loop.run_until_complete(test_function())



if __name__ == '__main__':
    unittest.main()
