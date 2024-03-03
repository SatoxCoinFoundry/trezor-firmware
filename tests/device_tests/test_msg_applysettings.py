# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

from pathlib import Path

import pytest

from trezorlib import btc, device, exceptions, messages, misc
from trezorlib.debuglink import TrezorClientDebugLink as Client
from trezorlib.tools import parse_path

HERE = Path(__file__).parent.resolve()


EXPECTED_RESPONSES_NOPIN = [
    messages.ButtonRequest(),
    messages.Success,
    messages.Features,
]
EXPECTED_RESPONSES_PIN_T1 = [messages.PinMatrixRequest()] + EXPECTED_RESPONSES_NOPIN
EXPECTED_RESPONSES_PIN_TT = [messages.ButtonRequest()] + EXPECTED_RESPONSES_NOPIN

EXPECTED_RESPONSES_EXPERIMENTAL_FEATURES = [
    messages.ButtonRequest,
    messages.Success,
    messages.Features,
]

PIN4 = "1234"

# All the tests are starting with a setup client!
pytestmark = pytest.mark.setup_client(pin=PIN4)

T1_HOMESCREEN = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x00\x00\x00\x00\x04\x80\x00\x00\x00\x00\x00\x00\x00\x00\x04\x88\x02\x00\x00\x00\x02\x91\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x90@\x00\x11@\x00\x00\x00\x00\x00\x00\x08\x00\x10\x92\x12\x04\x00\x00\x05\x12D\x00\x00\x00\x00\x00 \x00\x00\x08\x00Q\x00\x00\x02\xc0\x00\x00\x00\x00\x00\x00\x00\x10\x02 \x01\x04J\x00)$\x00\x00\x00\x00\x80\x00\x00\x00\x00\x08\x10\xa1\x00\x00\x02\x81 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\tP\x00\x00\x00\x00\x00\x00 \x00\x00\xa0\x00\xa0R \x12\x84\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x08\x00\tP\x00\x00\x00\x00 \x00\x04 \x00\x80\x02\x00@\x02T\xc2 \x00\x00\x00\x00\x00\x00\x00\x10@\x00)\t@\n\xa0\x80\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x80@\x14\xa9H\x04\x00\x00\x88@\x00\x00\x00\x00\x00\x02\x02$\x00\x15B@\x00\nP\x00\x00\x00\x00\x00\x80\x00\x00\x91\x01UP\x00\x00 \x02\x00\x00\x00\x00\x00\x00\x02\x08@ Z\xa5 \x00\x00\x80\x00\x00\x00\x00\x00\x00\x08\xa1%\x14*\xa0\x00\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00@\xaa\x91 \x00\x05E\x80\x00\x00\x00\x00\x00\x02*T\x05-D\x00\x00\x05 @\x00\x00\x00\x00\x00%@\x80\x11V\xa0\x88\x00\x05@\xb0\x00\x00\x00\x00\x00\x818$\x04\xabD \x00\x06\xa1T\x00\x00\x00\x00\x02\x03\xb8\x01R\xd5\x01\x00\x00\x05AP\x00\x00\x00\x00\x08\xadT\x00\x05j\xa4@\x00\x87ah\x00\x00\x00\x00\x02\x8d\xb8\x08\x00.\x01\x00\x00\x02\xa5\xa8\x10\x00\x00\x00*\xc1\xec \n\xaa\x88 \x02@\xf6\xd0\x02\x00\x00\x00\x0bB\xb6\x14@U"\x80\x00\x01{`\x00\x00\x00\x00M\xa3\xf8 \x15*\x00\x00\x00\x10n\xc0\x04\x00\x00\x02\x06\xc2\xa8)\x00\x96\x84\x80\x00\x00\x1b\x00\x00\x80@\x10\x87\xa7\xf0\x84\x10\xaa\x10\x00\x00D\x00\x00\x02 \x00\x8a\x06\xfa\xe0P\n-\x02@\x00\x12\x00\x00\x00\x00\x10@\x83\xdf\xa0\x00\x08\xaa@\x00\x00\x01H\x00\x05H\x04\x12\x01\xf7\x81P\x02T\t\x00\x00\x00 \x00\x00\x84\x10\x00\x00z\x00@)* \x00\x00\x01\n\xa0\x02 \x05\n\x00\x00\x05\x10\x84\xa8\x84\x80\x00\x00@\x14\x00\x92\x10\x80\x00\x04\x11@\tT\x00\x00\x00\x00\n@\x00\x08\x84@$\x00H\x00\x12Q\x02\x00\x00\x00\x00\x90\x02A\x12\xa8\n\xaa\x92\x10\x04\xa8\x10@\x00\x00\x04\x04\x00\x04I\x00\x04\x14H\x80"R\x01\x00\x00\x00!@\x00\x00$\xa0EB\x80\x08\x95hH\x00\x00\x00\x84\x10 \x05Z\x00\x00(\x00\x02\x00\xa1\x01\x00\x00\x04\x00@\x82\x00\xadH*\x92P\x00\xaaP\x00\x00\x00\x00\x11\x02\x01*\xad\x01\x00\x01\x01"\x11D\x08\x00\x00\x10\x80 \x00\x81W\x80J\x94\x04\x08\xa5 !\x00\x00\x00\x02\x00B*\xae\xa1\x00\x80\x10\x01\x08\xa4\x00\x00\x00\x00\x00\x84\x00\t[@"HA\x04E\x00\x84\x00\x00\x00\x10\x00\x01J\xd5\x82\x90\x02\x00!\x02\xa2\x00\x00\x00\x00\x00\x00\x00\x05~\xa0\x00 \x10\n)\x00\x11\x00\x00\x00\x00\x00\x00!U\x80\xa8\x88\x82\x80\x01\x00\x00\x00\x00\x00\x00H@\x11\xaa\xc0\x82\x00 *\n\x00\x00\x00\x00\x00\x00\x00\x00\n\xabb@ \x04\x00! \x84\x00\x00\x00\x00\x02@\xa5\x15A$\x04\x81(\n\x00\x00\x00\x00\x00\x00 \x01\x10\x02\xe0\x91\x02\x00\x00\x04\x00\x00\x00\x00\x00\x00\x01 \xa9\tQH@\x91 P\x00\x00\x00\x00\x00\x00\x08\x00\x00\xa0T\xa5\x00@\x80\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x00\x00\x00\x00\xa2\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00 T\xa0\t\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00@\x02\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00*\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x10\x00\x00\x10\x02\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00@\x04\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x08@\x10\x00\x00\x00\x00'
TR_HOMESCREEN = b"TOIG\x80\x00@\x00\x0c\x04\x00\x00\xa5RY\x96\xdc0\x08\xe4\x06\xdc\xff\x96\xdc\x80\xa8\x16\x90z\xd2y\xf9\x18{<m\xc9\x02j\xeb\xea_\xddy\xfe~\xf14:\xfc\xe2I\x00\xf8\xff\x13\xff\xfa\xc6>\xc0\xf1\xe5\xc9y\x0f\x95\x7f;C\xfe\xd0\xe1K\xefS\x96o\xf9\xb739\x1a\n\xc7\xde\x89\xff\x11\xd8=\xd5\xcf\xb1\x9f\xf7U\xf2\xa3spx\xb0&t\xe4\xaf3x\xcaT\xec\xe50k\xb4\xe8\nl\x16\xbf`'\xf3\xa7Z\x8d-\x98h\x1c\x03\x07\xf0\xcf\xf0\x8aD\x13\xec\x1f@y\x9e\xd8\xa3\xc6\x84F*\x1dx\x02U\x00\x10\xd3\x8cF\xbb\x97y\x18J\xa5T\x18x\x1c\x02\xc6\x90\xfd\xdc\x89\x1a\x94\xb3\xeb\x01\xdc\x9f2\x8c/\xe9/\x8c$\xc6\x9c\x1e\xf8C\x8f@\x17Q\x1d\x11F\x02g\xe4A \xebO\xad\xc6\xe3F\xa7\x8b\xf830R\x82\x0b\x8e\x16\x1dL,\x14\xce\x057tht^\xfe\x00\x9e\x86\xc2\x86\xa3b~^Bl\x18\x1f\xb9+w\x11\x14\xceO\xe9\xb6W\xd8\x85\xbeX\x17\xc2\x13,M`y\xd1~\xa3/\xcd0\xed6\xda\xf5b\x15\xb5\x18\x0f_\xf6\xe2\xdc\x8d\x8ez\xdd\xd5\r^O\x9e\xb6|\xc4e\x0f\x1f\xff0k\xd4\xb8\n\x12{\x8d\x8a>\x0b5\xa2o\xf2jZ\xe5\xee\xdc\x14\xd1\xbd\xd5\xad\x95\xbe\x8c\t\x8f\xb9\xde\xc4\xa551,#`\x94'\x1b\xe7\xd53u\x8fq\xbd4v>3\x8f\xcc\x1d\xbcV>\x90^\xb3L\xc3\xde0]\x05\xec\x83\xd0\x07\xd2(\xbb\xcf+\xd0\xc7ru\xecn\x14k-\xc0|\xd2\x0e\xe8\xe08\xa8<\xdaQ+{\xad\x01\x02#\x16\x12+\xc8\xe0P\x06\xedD7\xae\xd0\xa4\x97\x84\xe32\xca;]\xd04x:\x94`\xbe\xca\x89\xe2\xcb\xc5L\x03\xac|\xe7\xd5\x1f\xe3\x08_\xee!\x04\xd2\xef\x00\xd8\xea\x91p)\xed^#\xb1\xa78eJ\x00F*\xc7\xf1\x0c\x1a\x04\xf5l\xcc\xfc\xa4\x83,c\x1e\xb1>\xc5q\x8b\xe6Y9\xc7\x07\xfa\xcf\xf9\x15\x8a\xdd\x11\x1f\x98\x82\xbe>\xbe+u#g]aC\\\x1bC\xb1\xe8P\xce2\xd6\xb6r\x12\x1c*\xd3\x92\x9d9\xf9cB\x82\xf9S.\xc2B\xe7\x9d\xcf\xdb\xf3\xfd#\xfd\x94x9p<D?\x0e0\xd0)ufMK\x9d\x84\xbf\x95\x02\x15\x04\xaf\x9b\xd7|\x9f\xf5\xc2\x19D\xe1\xe8pC=\\\xb54\xff\xfd<\xfc\x8b\x83\x19\x9aZ\x99J\x9d\xa2oP6\xb2=\xe0\xe5=Z0\x7f\xb6\xe9\xb1\x98\n\xcc \xdb\x9f\xb6\xf4\xc2\x82Z:\t\xf2\xcd\x88\xe3\x8a0\n\x13\xdd\xf9;\xdbtr\xf4kj\xa6\x90\x9d\x97\x92+#\xf4;t\x1e6\x80\xcd)\xfe\xe1\xabdD(V\xf5\xcc\xcf\xbeY\xd8\xddX\x08*\xc5\xd6\xa1\xa2\xae\x89s]\xafj\x9b\x07\x8d\xcf\xb5\n\x162\xb7\xb0\x02p\xc0.{\xbf\xd6\xc7|\x8a\x8c\xc9g\xa8DO\x85\xf6<E\x05Ek\x8c\xbfU\x13bz\xcf\xd0\x07\xcd^\x0f\x9b\x951\xa1vb\x17u:\xd2X\x91/\x0f\x9a\xae\x16T\x81\xb6\x8e\xdc,\xb0\xa1=\x11af%^\xec\x95\x83\xa9\xb8+\xd0i\xe0+#%\x02\xfd2\x84\xf3\xde\x0c\x88\x8c\x80\xf7\xc2H\xaa#\x80m\xf4\x1e\xd4#\x04J\r\xb6\xf83s\x8c\x0e\x0bx\xabw\xbe\x90\x94\x90:C\x88\x9bR`B\xc02\x1a\x08\xca-M9\xac\xa3TP\xb1\x83\xf2\x8aT\xe9\xc0c9(\xe5d\xd1\xac\xfd\x83\xf3\xb4C\x95\x04doh\xd7M\xed \xd0\x90\xc9|\x8a\x1fX\x1f\x0eI\x12\x8e&\xc3\x91NM-\x02\xeckp\x1a/\x19\x9d\xf2\xb4$\x0eG:\xbe\xb2~\x10(,\x1cd\x07\xbb]n^F@\x173'\xc63\xdf!u\xf4F\xa9\xc3\x96E!e\xc2Iv\xe8zQH=v\x89\x9a\x04a^\x10\x06\x01\x04!2\xa6\x1b\xba\x111/\xfa\xfa\x9c\x15 @\xf6\xb9{&\xcc\x84\xfa\xd6\x81\x90\xd4\x92\xcf\x89/\xc8\x80\xadP\xa3\xf4Xa\x1f\x04A\x07\xe6N\xd2oEZ\xc9\xa6(!\x8e#|\x0e\xfbq\xce\xe6\x8b-;\x06_\x04n\xdc\x8d^\x05s\xd2\xa8\x0f\xfa/\xfa\xf8\xe1x\n\xa3\xf701i7\x0c \x87\xec#\x80\x9c^X\x02\x01C\xc7\x85\x83\x9dS\xf5\x07"


def _set_expected_responses(client: Client):
    client.use_pin_sequence([PIN4])
    if client.features.model == "1":
        client.set_expected_responses(EXPECTED_RESPONSES_PIN_T1)
    else:
        client.set_expected_responses(EXPECTED_RESPONSES_PIN_TT)


def test_apply_settings(client: Client):
    assert client.features.label == "test"

    with client:
        _set_expected_responses(client)
        device.apply_settings(client, label="new label")

    assert client.features.label == "new label"


@pytest.mark.skip_t1
def test_apply_settings_rotation(client: Client):
    assert client.features.display_rotation is None

    with client:
        _set_expected_responses(client)
        device.apply_settings(client, display_rotation=270)

    assert client.features.display_rotation == 270


@pytest.mark.setup_client(pin=PIN4, passphrase=False)
def test_apply_settings_passphrase(client: Client):
    with client:
        _set_expected_responses(client)
        device.apply_settings(client, use_passphrase=True)

    assert client.features.passphrase_protection is True

    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, use_passphrase=False)

    assert client.features.passphrase_protection is False

    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, use_passphrase=True)

    assert client.features.passphrase_protection is True


@pytest.mark.setup_client(passphrase=False)
@pytest.mark.skip_t1
def test_apply_settings_passphrase_on_device(client: Client):
    # enable passphrase
    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, use_passphrase=True)

    assert client.features.passphrase_protection is True

    # enable force on device
    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, passphrase_always_on_device=True)

    assert client.features.passphrase_protection is True
    assert client.features.passphrase_always_on_device is True

    # turning off the passphrase should also clear the always_on_device setting
    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, use_passphrase=False)

    assert client.features.passphrase_protection is False
    assert client.features.passphrase_always_on_device is False

    # and turning it back on does not modify always_on_device
    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, use_passphrase=True)

    assert client.features.passphrase_protection is True
    assert client.features.passphrase_always_on_device is False


@pytest.mark.skip_t1
@pytest.mark.skip_t2
def test_apply_homescreen_tr_toif_good(client: Client):
    with client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=TR_HOMESCREEN)

        # Revert to default settings
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, homescreen=b"")


@pytest.mark.skip_t1
@pytest.mark.skip_t2
@pytest.mark.setup_client(pin=None)  # so that "PIN NOT SET" is shown in the header
def test_apply_homescreen_tr_toif_with_notification(client: Client):
    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, homescreen=TR_HOMESCREEN)


@pytest.mark.skip_t1
@pytest.mark.skip_t2
def test_apply_homescreen_tr_toif_with_long_label(client: Client):
    with client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=TR_HOMESCREEN)

    # Showing longer label
    with client:
        device.apply_settings(client, label="My long label")

    # Showing label that will not fit on the line
    with client:
        device.apply_settings(client, label="My even longer label")


@pytest.mark.skip_t1
@pytest.mark.skip_t2
def test_apply_homescreen_tr_toif_wrong_size(client: Client):
    # 64x64 img
    img = b"TOIG@\x00@\x009\x02\x00\x00}R\xdb\x81$A\x08\"\x03\xf3\xcf\xd2\x0c<\x01-{\xefc\xe6\xd5\xbbU\xa2\x08T\xd6\xcfw\xf4\xe7\xc7\xb7X\xf1\xe3\x1bl\xf0\xf7\x1b\xf8\x1f\xcf\xe7}\xe1\x83\xcf|>\x8d%\x14\xa5\xb3\xe9p5\xa1;~4:\xcd\xe0&\x11\x1d\xe9\xf6\xa1\x1fw\xf54\x95eWx\xda\xd0u\x91\x86\xb8\xbc\xdf\xdc\x008f\x15\xc6\xf6\x7f\xf0T\xb8\xc1\xa3\xc5_A\xc0G\x930\xe7\xdc=\xd5\xa7\xc1\xbcI\x16\xb8s\x9c&\xaa\x06\xc1}\x8b\x19\x9d'c\xc3\xe3^\xc3m\xb6n\xb0(\x16\xf6\xdeg\xb3\x96:i\xe5\x9c\x02\x93\x9fF\x9f-\xa7\"w\xf3X\x9f\x87\x08\x84\"v,\xab!9:<j+\xcb\xf3_\xc7\xd6^<\xce\xc1\xb8!\xec\x8f/\xb1\xc1\x8f\xbd\xcc\x06\x90\x0e\x98)[\xdb\x15\x99\xaf\xf2~\x8e\xd0\xdb\xcd\xfd\x90\x12\xb6\xdd\xc3\xdd|\x96$\x01P\x86H\xbc\xc0}\xa2\x08\xe5\x82\x06\xd2\xeb\x07[\r\xe4\xdeP\xf4\x86;\xa5\x14c\x12\xe3\xb16x\xad\xc7\x1d\x02\xef\x86<\xc6\x95\xd3/\xc4 \xa1\xf5V\xe2\t\xb2\x8a\xd6`\xf2\xcf\xb7\xd6\x07\xdf8X\xa7\x18\x03\x96\x82\xa4 \xeb.*kP\xceu\x9d~}H\xe9\xb8\x04<4\xff\xf8\xcf\xf6\xa0\xf2\xfcM\xe3/?k\xff\x18\x1d\xb1\xee\xc5\xf5\x1f\x01\x14\x03;\x1bU\x1f~\xcf\xb3\xf7w\xe5\nMfd/\xb93\x9fq\x9bQ\xb7'\xbfvq\x1d\xce\r\xbaDo\x90\xbc\xc5:?;\x84y\x8a\x1e\xad\xe9\xb7\x14\x10~\x9b@\xf8\x82\xdc\x89\xe7\xf0\xe0k4o\x9a\xa0\xc4\xb9\xba\xc56\x01i\x85EO'e6\xb7\x15\xb4G\x05\xe1\xe7%\xd3&\x93\x91\xc9CTQ\xeb\xcc\xd0\xd7E9\xa9JK\xcc\x00\x95(\xdc.\xd2#7:Yo}y_*\x1a\xae6)\x97\x9d\xc0\x80vl\x02\\M\xfe\xc9sW\xa8\xfbD\x99\xb8\xb0:\xbc\x80\xfd\xef\xd3\x94\xbe\x18j9z\x12S\xa1\xec$\x1c\xe3\xd1\xd0\xf4\xdd\xbfI\xf1rBj\x0f\x1cz\x1d\xf7\xa5tR\xb3\xfc\xa4\xd0\xfah\xc3Mj\xbe\x14r\x9d\x84z\xd2\x7f\x13\xb4w\xce\xa0\xaeW\xa4\x18\x0b\xe4\x8f\xe6\xc3\xbeQ\x93\xb0L<J\xe3g9\xb5W#f\xd1\x0b\x96|\xd6z1;\x85\x7f\xe3\xe6[\x02A\xdc\xa4\x02\x1b\x91\x88\x7f"
    with pytest.raises(exceptions.TrezorFailure), client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=img)


@pytest.mark.skip_t1
@pytest.mark.skip_t2
def test_apply_homescreen_tr_upload_jpeg_fail(client: Client):
    with open(HERE / "test_bg.jpg", "rb") as f:
        img = f.read()
        with pytest.raises(exceptions.TrezorFailure), client:
            _set_expected_responses(client)
            device.apply_settings(client, homescreen=img)


@pytest.mark.skip_t1
@pytest.mark.skip_t2
def test_apply_homescreen_tr_upload_t1_fail(client: Client):
    with pytest.raises(exceptions.TrezorFailure), client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=T1_HOMESCREEN)


@pytest.mark.skip_t1
@pytest.mark.skip_tr
def test_apply_homescreen_toif(client: Client):
    img = b"TOIf\x90\x00\x90\x00~\x00\x00\x00\xed\xd2\xcb\r\x83@\x10D\xc1^.\xde#!\xac31\x99\x10\x8aC%\x14~\x16\x92Y9\x02WI3\x01<\xf5cI2d\x1es(\xe1[\xdbn\xba\xca\xe8s7\xa4\xd5\xd4\xb3\x13\xbdw\xf6:\xf3\xd1\xe7%\xc7]\xdd_\xb3\x9e\x9f\x9e\x9fN\xed\xaaE\xef\xdc\xcf$D\xa7\xa4X\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0OV"

    with pytest.raises(exceptions.TrezorFailure), client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=img)


@pytest.mark.skip_t1
@pytest.mark.skip_tr
def test_apply_homescreen_jpeg(client: Client):
    with open(HERE / "test_bg.jpg", "rb") as f:
        img = f.read()
        with client:
            _set_expected_responses(client)
            device.apply_settings(client, homescreen=img)

            client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
            device.apply_settings(client, homescreen=b"")


@pytest.mark.skip_t1
@pytest.mark.skip_tr
def test_apply_homescreen_jpeg_progressive(client: Client):
    img = (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01,\x01,"
        b"\x00\x00\xff\xdb\x00C\x00\x02\x01\x01\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x03\x05\x03\x03\x03\x03"
        b"\x03\x06\x04\x04\x03\x05\x07\x06\x07\x07\x07\x06\x07\x07\x08\t\x0b\t\x08\x08\n\x08\x07\x07\n\r\n\n\x0b"
        b"\x0c\x0c\x0c\x0c\x07\t\x0e\x0f\r\x0c\x0e\x0b\x0c\x0c\x0c\xff\xdb\x00C\x01\x02\x02\x02\x03\x03\x03\x06\x03"
        b"\x03\x06\x0c\x08\x07\x08\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c"
        b"\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c"
        b"\x0c\x0c\x0c\x0c\xff\xc2\x00\x11\x08\x00\xf0\x00\xf0\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00"
        b"\x15\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\xff\xc4\x00\x14\x01\x01"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03"
        b"\x10\x00\x00\x01\x9f\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x03\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x90\xff\xda\x00\x08\x01\x01\x00\x01\x05\x02a?\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x90\xff\xda\x00\x08\x01\x03\x01\x01?\x01a?\xff\xc4\x00\x14\x11\x01\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\xff\xda\x00\x08\x01\x02\x01\x01?\x01a?\xff\xc4"
        b"\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\xff\xda\x00\x08\x01\x01"
        b"\x00\x06?\x02a?\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90"
        b"\xff\xda\x00\x08\x01\x01\x00\x01?!a?\xff\xda\x00\x0c\x03\x01\x00\x02\x00\x03\x00\x00\x00\x10\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xc4\x00"
        b"\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\xff\xda\x00\x08\x01\x03\x01"
        b"\x01?\x10a?\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\xff"
        b"\xda\x00\x08\x01\x02\x01\x01?\x10a?\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x90\xff\xda\x00\x08\x01\x01\x00\x01?\x10a?\xff\xd9"
    )

    with pytest.raises(exceptions.TrezorFailure), client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=img)


@pytest.mark.skip_t1
@pytest.mark.skip_tr
def test_apply_homescreen_jpeg_wrong_size(client: Client):
    img = (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01,\x01,"
        b"\x00\x00\xff\xdb\x00C\x00\x02\x01\x01\x02\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x03\x05\x03\x03\x03\x03"
        b"\x03\x06\x04\x04\x03\x05\x07\x06\x07\x07\x07\x06\x07\x07\x08\t\x0b\t\x08\x08\n\x08\x07\x07\n\r\n\n\x0b"
        b"\x0c\x0c\x0c\x0c\x07\t\x0e\x0f\r\x0c\x0e\x0b\x0c\x0c\x0c\xff\xdb\x00C\x01\x02\x02\x02\x03\x03\x03\x06\x03"
        b"\x03\x06\x0c\x08\x07\x08\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c"
        b"\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c"
        b"\x0c\x0c\x0c\x0c\xff\xc0\x00\x11\x08\x00\xf0\x00\xdc\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00"
        b"\x15\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xff\xc4\x00\x14\x10\x01"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\x9f\xf0\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x1f\xff\xd9"
    )

    with pytest.raises(exceptions.TrezorFailure), client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=img)


@pytest.mark.skip_t2
@pytest.mark.skip_tr
def test_apply_homescreen(client: Client):
    with client:
        _set_expected_responses(client)
        device.apply_settings(client, homescreen=T1_HOMESCREEN)


@pytest.mark.setup_client(pin=None)
def test_safety_checks(client: Client):
    def get_bad_address():
        btc.get_address(client, "Bitcoin", parse_path("m/44h"), show_display=True)

    assert client.features.safety_checks == messages.SafetyCheckLevel.Strict

    with pytest.raises(exceptions.TrezorFailure, match="Forbidden key path"), client:
        client.set_expected_responses([messages.Failure])
        get_bad_address()

    if client.features.model != "1":
        with client:
            client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
            device.apply_settings(
                client, safety_checks=messages.SafetyCheckLevel.PromptAlways
            )

        assert client.features.safety_checks == messages.SafetyCheckLevel.PromptAlways

        with client:
            client.set_expected_responses(
                [messages.ButtonRequest, messages.ButtonRequest, messages.Address]
            )
            get_bad_address()

    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(client, safety_checks=messages.SafetyCheckLevel.Strict)

    assert client.features.safety_checks == messages.SafetyCheckLevel.Strict

    with pytest.raises(exceptions.TrezorFailure, match="Forbidden key path"), client:
        client.set_expected_responses([messages.Failure])
        get_bad_address()

    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_NOPIN)
        device.apply_settings(
            client, safety_checks=messages.SafetyCheckLevel.PromptTemporarily
        )

    assert client.features.safety_checks == messages.SafetyCheckLevel.PromptTemporarily

    with client:
        client.set_expected_responses(
            [messages.ButtonRequest, messages.ButtonRequest, messages.Address]
        )
        get_bad_address()


@pytest.mark.skip_t1
def test_experimental_features(client: Client):
    def experimental_call():
        misc.get_nonce(client)

    assert client.features.experimental_features is None

    # unlock
    with client:
        _set_expected_responses(client)
        device.apply_settings(client, label="new label")

    assert not client.features.experimental_features

    with pytest.raises(exceptions.TrezorFailure, match="DataError"), client:
        client.set_expected_responses([messages.Failure])
        experimental_call()

    with client:
        client.set_expected_responses(EXPECTED_RESPONSES_EXPERIMENTAL_FEATURES)
        device.apply_settings(client, experimental_features=True)

    assert client.features.experimental_features

    with client:
        client.set_expected_responses([messages.Nonce])
        experimental_call()

    # relock and try again
    client.lock()
    with client:
        client.use_pin_sequence([PIN4])
        client.set_expected_responses([messages.ButtonRequest, messages.Nonce])
        experimental_call()


@pytest.mark.setup_client(pin=None)
def test_label_too_long(client: Client):
    with pytest.raises(exceptions.TrezorFailure), client:
        client.set_expected_responses([messages.Failure])
        device.apply_settings(client, label="A" * 33)
