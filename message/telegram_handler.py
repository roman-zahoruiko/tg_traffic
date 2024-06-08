import httpx


async def send_telegram_message(bottoken: str, chatid: int, message: str) -> str:

    url = f'https://api.telegram.org/bot{bottoken}/sendMessage'
    payload = {'chat_id': chatid, 'text': message}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

        return f'{response.status_code}: {response.json()}'
