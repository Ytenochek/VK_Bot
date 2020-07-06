import aiohttp
import asyncio
import json
import sys

# from logic import *  # сделать обработку сообщений


class VkBot:
    def __init__(self, client, loop):
        self.group_info = self.get_group_info()
        self.client = client
        self.loop = loop

    def get_group_info(self):
        with open("info.txt", "r") as file:
            info = file.read().split(";")
            return dict(group_id=info[0], access_token=info[1], v=info[2])

    def __del__(self):
        self.loop.stop()
        self.client.close()
        sys.exit(0)

    async def get(self, server, method_name, parameters):
        url = f"{server}{method_name}?{'&'.join(['='.join(item) for item in parameters.items() if item[1]])}"
        async with self.client.get(url) as response:
            data = await response.read()
            return json.loads(data.decode("utf-8"))

    async def get_long_poll_server(self):
        server_data = await self.get(
            "https://api.vk.com/method/", "groups.getLongPollServer", self.group_info
        )
        server_data = server_data["response"]
        server_data["ts"] = str(server_data["ts"])
        return server_data

    async def connect_to_server(self):
        params = {
            "act": "a_check",
            "key": self.server_data["key"],
            "ts": self.server_data["ts"],
            "wait": "25",
        }
        return await self.get(self.server_data["server"], "", params)

    async def get_user_info(self, user_id):
        return self.get("https://api.vk.com/method/", "users.get", {"user_id": user_id, **self.group_info})["response"][0]

    async def send_message(self, **params):
        params.update(self.group_info)
        return await self.get("https://api.vk.com/method/", "messages.send", params)

    async def run(self):  # ну чё народ погнали нахуй
        self.server_data = await self.get_long_poll_server()
        while True:
            answers = await self.connect_to_server()
            if "error" in answers:
                print("Ошибка:" + answers["error"]["error_msg"])
                print(
                    "Возможно данные в info.txt неверны, проверьте их и свяжитесь с нами"
                )
            elif "failed" in answers:
                self.server_data = await self.get_long_poll_server()
            elif answers["updates"]:
                self.server_data["ts"] = answers["ts"]
                for answer in answers["updates"]:
                    print(answer)
                    sender_id = str(answer["object"]["message"]["from_id"])
                    await self.send_message(
                        peer_id=sender_id,
                        message=None,
                        random_id="0",
                        sticker_id="8801",
                        lat=None,
                        long=None,
                        attachment=None,
                        reply_to=None,
                        forward_messages=None,
                        payload=None,
                        keyboard=None,
                    )


loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)
bot = VkBot(client, loop)
asyncio.ensure_future(bot.run())
loop.run_forever()
