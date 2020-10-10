#from random import choice


def processing(obj):
    print(obj)
    return f"https://api.vk.com/method/messages.send?user_id={obj['message']['from_id']}&message=lol&v=5.124&access_token=13bc742a3298c8b4d0a91d1201a2371273d9c80a216176f4df92790a32bc1d42362a6c37c461cfab3f8a9&random_id=0"


#ANSWERS = {"hi": ["hello"], "hello": ["hi"]}
