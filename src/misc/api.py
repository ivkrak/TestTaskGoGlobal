import json
import aiohttp


async def get_dollar_exchange() -> float:
    """
    Выдаёт курс доллара в рублях на данный момент
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.coinbase.com/v2/prices/USD-RUB/spot') as response:
            resp = await response.text()
            resp = json.loads(resp)
    return round(float(resp["data"]["amount"]), 2)
