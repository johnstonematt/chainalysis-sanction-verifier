# Chainalysis Sanction Verifier
Python client for [sanction screening](https://www.chainalysis.com/free-cryptocurrency-sanctions-screening-tools/) via Chainalysis API.

## Installation
It is recommended to install `chainalysis-sanction-verifier` within a virtual environment.
#### Pip:
```shell
pip install chainalysis-sanction-verifier
```

#### Poetry:
```shell
poetry add chainalysis-sanction-verifier
```

## Example Usage
It is recommended to use the `Client` as a context manager, thus assuring that the underlying `httpx.AsyncClient` is 
closed.
```python
import asyncio
from chainalysis_sanction_verifier import Client

async def main() -> None:
    async with Client() as client:
        identifications = await client.check_address_sanction_identifications(
            address="LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd",
        )
        print(identifications)


if __name__ == "__main__":
    asyncio.run(main())
```
The above code should output the following JSON:
```json
[
  {
    "category": "sanctions",
    "name": "SANCTIONS: OFAC SDN Dmitrii Karasavidi 2020-09-16 LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd",
    "description": "This specific address LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd within the cluster has been identified as belonging to an individual on OFAC's SDN list. \n\nKARASAVIDI, Dmitrii (Cyrillic: \u041a\u0410\u0420\u0410\u0421\u0410\u0412\u0418\u0414\u0418, \u0414\u043c\u0438\u0442\u0440\u0438\u0439) (a.k.a. KARASAVIDI, Dmitriy), Moscow, Russia; DOB 09 Jul 1985; Email Address 2000@911.af; alt. Email Address dm.karasavi@yandex.ru; Gender Male; Digital Currency Address - XBT 1Q6saNmqKkyFB9mFR68Ck8F7Dp7dTopF2W; alt. Digital Currency Address - XBT 1DDA93oZPn7wte2eR1ABwcFoxUFxkKMwCf; Digital Currency Address - ETH 0xd882cfc20f52f2599d84b8e8d58c7fb62cfe344b; Digital Currency Address - XMR 5be5543ff73456ab9f2d207887e2af87322c651ea1a873c5b25b7ffae456c320; Digital Currency Address - LTC LNwgtMxcKUQ51dw7bQL1yPQjBVZh6QEqsd; Digital Currency Address - ZEC t1g7wowvQ8gn2v8jrU1biyJ26sieNqNsBJy; Digital Currency Address - DASH XnPFsRWTaSgiVauosEwQ6dEitGYXgwznz2; Digital Currency Address - BTG GPwg61XoHqQPNmAucFACuQ5H9sGCDv9TpS; Digital Currency Address - ETC 0xd882cfc20f52f2599d84b8e8d58c7fb62cfe344b; Passport 75 5276391 (Russia) expires 29 Jun 2027 (individual) [CYBER2]. \n\nhttps://home.treasury.gov/policy-issues/financial-sanctions/recent-actions/20200916",
    "url": "https://home.treasury.gov/policy-issues/financial-sanctions/recent-actions/20200916"
  }
]
```

## Developing
Tests can be run using `pytest`:
```shell
pytest
```
Or, in a `poetry` environment:
```shell
poetry run pytest
```

