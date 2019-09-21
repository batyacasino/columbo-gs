import requests
import json
import time

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def user_oauth():
    vk_session = vk_api.VkApi('+79854159202', '929227007Asdec#@')
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    return vk_session.get_api()

def get_data(post):
    try:
        post_id = post['id']
    except:
        post_id = 0
    try:
        likes = post["likes"]["count"]
    except:
        likes = 'zero'
    try:
        reposts = post["reposts"]["count"]
    except:
        reposts = 'zero'
    try:
        post_type = post["attachments"][1]["type"]
    except:
        post_type = 'zero'
    try:
        artist = post["attachments"][1]["audio"]["artist"]
    except:
        artist = 'zero'
    try:
        title = post["attachments"][1]["audio"]["title"]
    except:
        title = 'zero'

    data = {
        'id': post_id,
        'likes': likes,
        'reposts': reposts,
        'post_type': post_type,
        'artist': artist,
        'track': title
    }

    return data



def get_group(user_id):
    vk = user_oauth()
    return vk.groups.get(user_id=user_id, count=50, extended=True, v=5.101)['items']

def wall_get(owner_group_id):
    vk = user_oauth()
    offset = 0
    all_posts = []
    date_x = int(time.time()) - 31556926 


    while True:
        time.sleep(1)
        print("Выгружаю посты: " + str(offset))
        posts = vk.wall.get(owner_id=owner_group_id, count=100, offset=offset, v=5.101)['items']
        all_posts.extend(posts)
        try:
            print(posts[-1]['date'])
            oldest_post_date = posts[-1]['date']
            offset += 100           
        except:
            return 0
        if oldest_post_date < date_x:
            break   
    print("Подготавливаю словарь")
    data_post = []
    for post in all_posts:
        data_post.append(get_data(post))
    return data_post

def top_post(group_id):
    print('top_post')
    data_group = wall_get(group_id)
    if data_group == 0:
        return 0
    likes = []
    for like in data_group:
        likes.append(like['likes'])
    sort_like = sorted(likes)
    like_reverse = sort_like[::-1]
    top_id = []
    i = 0
    while i < 10:
        for top_like in data_group:            
            if like_reverse[i] == top_like['likes']:
                top_id.append(top_like['id'])
                print("Топ лайков: " + str(top_like['id']))
                i += 1
    return top_id

def wall_rep(attach):
    vk = user_oauth()
    vk.wall.repost(
        object=attach,
        message='Пост собравший за год в данной группе наибольшее колличество лайков',
        group_id=137819222      
        ) 

def main():
    vk_session = vk_api.VkApi(token='5ffe6fe3f6eed9755f09611d9e639a4e36617ad7f8f88ff8565304f9a77c007faddb872194ec0ca48c831')
    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    keyboard = VkKeyboard(one_time=True)

    complite = 'bad'
    while True:
        for event in longpoll.listen():  
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

                u_id = event.user_id
                group_name = ''
                group_id = []
                screen_name = []
                numbers_group = []
                i = 1
                for group in get_group(u_id):
                    group_name += str(i) + '.' + group['name'] + '\n'
                    group_id.append(group["id"])
                    numbers_group.append(i)
                    screen_name.append(group["screen_name"])
                    i += 1
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=group_name
                    )
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Выберите номер группы от 1 до ' + str(len(group_id))
                    )               
                for event in longpoll.listen():
                    complite = 'bad'
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        for group_number in numbers_group:
                            if event.text == str(group_number):
                                vk.messages.send(
                                    user_id=event.user_id,
                                    random_id=get_random_id(),
                                    message='Это займёт немного времени...'
                                    )
                                num = int(group_number) - 1
                                group = 0 - group_id[num]
                                posts = top_post(group)
                                if posts == 0:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        random_id=get_random_id(),
                                        message='На стене этого сообщества постов не найденно'
                                        )
                                    break
                                whath_post = []                     
                                for post in posts:                           
                                    answear = 'wall' + str(group) +  '_' + str(post)
                                    whath_post.append(answear) 
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        random_id=get_random_id(),
                                        attachment=answear
                                        )
                                                  
                                wall_rep(whath_post[0])
                                complite = 'ok'
                                #vk.messages.removeChatUser(user_id=event.user_id)
                        if complite == 'bad':
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message=group_name
                            )
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message='Введите число от 1 до ' + str(len(group_id)) 
                                )                            
                        if complite == 'ok':
                            break

if __name__ == '__main__':
    main()



'''

            response = session.get(
                'http://api.duckduckgo.com/',
                params={
                    'q': event.text,
                    'format': 'json'
                }
            ).json()

            text = response.get('AbstractText')
            image_url = response.get('Image')

            if not text:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='No results'
                )
                print('no results')
                continue

            attachments = []

            if image_url:
                image = session.get(image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]

                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
'''