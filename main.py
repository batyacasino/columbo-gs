import requests
import json
import time

...




def write_json(data):
    with open('posts.json', 'w') as file:
        json.dump(data, file, indent=2)  #, ensure_ascii=False)


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


def one_eyer_post():
    token = 'c770884ac770884ac770884a07c71c626fcc770c770884a9af08adc82c250e7f204d346'
    base_url = 'https://api.vk.com/method/wall.get?&v=5.101&access_token=' + token

    offset = 0
    all_posts = []
    date_x = int(time.time()) - 31556926

    while True:
        time.sleep(1)
        r = requests.get(
            base_url,
            params={
                'owner_id': -82827166,
                'count': 100,
                'offset': offset
            })
        posts = r.json()['response']['items']
        all_posts.extend(posts)
        oldest_post_date = posts[-1]['date']
        if oldest_post_date < date_x:
            break
        offset += 100

    data_post = []
    for post in all_posts:
        data_post.append(get_data(post))

    return data_post


def top_post():
    data_group = one_eyer_post()
    likes = []

    for like in data_group:
        likes.append(like['likes'])
    sort_like = sorted(likes)

    for top_like in data_group:
        if sort_like[-1] == top_like['likes']:
            top_post = like

    print(top_post['artist'] + ' ' + top_post['track'])


def main():
    print(int(time.time()) - 31556926)


if __name__ == '__main__':
    main()
