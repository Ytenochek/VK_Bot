import aiohttp
import asyncio
import json


loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)


async def get(
    server, method_name, parameters, client
):  # ахуеть, функция делает запрос!!!
    url = f"{server}{method_name}?{'&'.join(['='.join(item) for item in parameters.items()])}"
    async with client.get(url) as response:
        data = await response.read()
        return json.loads(data.decode("utf-8"))


def get_group_info():  # для тупых одменав, кто не шарит за коддинг
    with open("info.txt", "r") as file:
        info = file.read().split(";")
        return dict(group_id=info[0], access_token=info[1], v=info[2])


async def get_long_poll_server(group_info, client):  # шо бы фсё работало
    server_data = await get(
        "https://api.vk.com/method/", "groups.getLongPollServer", group_info, client
    )
    print(server_data)
    server_data = server_data["response"]
    server_data["ts"] = str(server_data["ts"])
    return server_data


async def connect_to_server(
    server_data, client
):  # подключаемся к серверу, чтоб получать сообщения от тупых подписщиков
    return await get(
        server_data["server"],
        "",
        {
            "act": "a_check",
            "key": server_data["key"],
            "ts": server_data["ts"],
            "wait": "25",
        },
        client,
    )


"""def get_user_info(group_info, user_id):
    return get("https://api.vk.com/method/", "users.get", {"user_ids": user_id, **group_info})["response"][0]"""


async def send_message(group_info, user_id, message, client):
    return await get(
        "https://api.vk.com/method/",
        "messages.send",
        {"user_id": user_id, "message": message, **group_info, "random_id": "0"},
        client,
    )


# TODO: проверять ошибки; чекнуть потоки;
async def main(client):
    group_info = get_group_info()
    server_data = await get_long_poll_server(group_info, client)
    while True:
        answers = await connect_to_server(server_data, client)
        if answers["updates"]:
            server_data["ts"] = answers["ts"]
            for answer in answers["updates"]:
                user_id = str(answer["object"]["message"]["from_id"])
                await send_message(group_info, user_id, "HI", client)


asyncio.ensure_future(main(client))
loop.run_forever()
