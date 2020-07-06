import aiohttp
import asyncio
import json
import sys
#from logic import *  # сделать обработку сообщений


class VkBot:
    def __init__(self, client, loop):  # я радился
        self.group_info = self.get_group_info()
        self.client = client
        self.loop = loop
    
    def get_group_info(self):  # для тупых одменав, кто не шарит за коддинг
        with open("info.txt", "r") as file:
            info = file.read().split(";")
            return dict(group_id=info[0], access_token=info[1], v=info[2])
    
    
    def __del__(self):  # помер
        self.loop.stop()
        self.client.close()
        sys.exit(0)


    async def get(self, server, method_name, parameters):  # ахуеть, функция делает запрос!!!
        url = f"{server}{method_name}?{'&'.join(['='.join(item) for item in parameters.items()])}"
        async with self.client.get(url) as response:
            data = await response.read()
            return json.loads(data.decode('utf-8'))


    async def get_long_poll_server(self):  # шо бы фсё работало
        server_data = await self.get("https://api.vk.com/method/", "groups.getLongPollServer", self.group_info)
        server_data = server_data["response"]
        server_data["ts"] = str(server_data["ts"])
        return server_data


    async def connect_to_server(self):  # подключаемся к серверу, чтоб получать сообщения от тупых подписщиков
        params = {"act": "a_check", "key": self.server_data["key"], "ts": self.server_data["ts"], "wait": "25"}
        return await self.get(self.server_data["server"], "", params)


    """async def get_user_info(self, user_id):  # если одмену понадобится инфа о челике
        return get("https://api.vk.com/method/", "users.get", {"user_id": user_id, **self.group_info})["response"][0]"""


    async def send_message(self, user_id, message):  # шлю тупым подписщикам сообщение
        params = {"user_id": user_id, "message": message, **self.group_info, "random_id": "0", "sticker_id": "8801"}
        return await self.get("https://api.vk.com/method/", "messages.send", params)

    
    async def run(self):  # ну чё народ погнали нахуй
        self.server_data = await self.get_long_poll_server()
        while True:
            answers = await self.connect_to_server()
            if "error" in answers:
                print("Ошибка:" + answers["error"]["error_msg"])
                print("Возможно данные в info.txt неверны, проверьте их и свяжитесь с нами")
            elif "failed" in answers:
                self.server_data = await get_long_poll_server()
            elif answers["updates"]:
                self.server_data["ts"] = answers["ts"]
                for answer in answers["updates"]:
                    print(answer)
                    user_id = str(answer["object"]["message"]["from_id"])
                    await self.send_message(user_id, "")
            

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)                
bot = VkBot(client, loop)
asyncio.ensure_future(bot.run())
loop.run_forever()