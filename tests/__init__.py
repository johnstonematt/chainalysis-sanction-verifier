import os
import time
import asyncio
from dotenv import load_dotenv

from chainalysis_sanction_verifier.client import Client


# such that the tests run regardless of where they are run from:
if os.path.exists(".env"):
    load_dotenv(".env")

elif os.path.exists("../.env"):
    load_dotenv("../.env")

else:
    load_dotenv()

SANCTIONED_ADDRESSES = [
    "LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd",
    "qznpd2tsk0l3hwdcygud3ch4tgxjwg5ptqa93ltwj4",
]

NON_SANCTIONED_ADDRESSES = [
    "0x00da2de23e3b1eb0c9c8273e3b32239807753efce0cf907d833d54e07464acb4",
]


async def test_rate_limiting() -> None:
    async with Client(rate_limit_delay=3) as client:
        start_time = time.time()
        coroutines = [
            client.check_address_sanction_identifications(
                address=address,
            )
            for address in SANCTIONED_ADDRESSES
        ]
        await asyncio.gather(*coroutines)
        assert time.time() - start_time >= 3


async def test_sanctioned_address() -> None:
    async with Client() as client:
        for sanctioned_address in SANCTIONED_ADDRESSES:
            identifications = await client.check_address_sanction_identifications(
                address=sanctioned_address
            )
            # check correct response:
            assert isinstance(identifications, list)
            for identification in identifications:
                assert isinstance(identification, dict)
                for key in ("category", "name", "description", "url"):
                    assert key in identification
                    value = identification[key]  # noqa
                    if value is not None:
                        assert isinstance(value, str)


async def test_non_sanctioned_address() -> None:
    async with Client() as client:
        for non_sanctioned_address in NON_SANCTIONED_ADDRESSES:
            identifications = await client.check_address_sanction_identifications(
                address=non_sanctioned_address
            )
            # check empty list:
            assert isinstance(identifications, list)
            assert len(identifications) == 0
