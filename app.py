import instabot
import praw
import json
import time
import urllib.request
import random
from PIL import Image
from resizeimage import resizeimage
import os

# insta docs https://instagrambot.github.io/docs/en/For_developers.html#login
# insta lib https://github.com/instagrambot/instabot
# reddit docs https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html

reddit = praw.Reddit(client_id='',
                     client_secret="",
                     user_agent='')


def main(data, data_file):
    username = data['user']
    password = data['password']
    proxy = data['proxy']
    caption_list_1 = data['caption_list_1']
    caption_list_2 = data['caption_list_2']
    sub_reddit_1 = data['sub_reddit_1']
    sub_reddit_2 = data['sub_reddit_2']
    count = data['count']
    follow_hash = data['follow_hash']
    hashlist = data['hashlist']
    directory = data['directory']
    post_ids = data['post_ids']

    bot = instabot.Bot()


    def findpost(subredditpage):
        for post in reddit.subreddit(subredditpage).hot(limit=1000):
            if post.score > 5 and post.is_self is False and post.id not in post_ids:
                # Check if post is an image
                url = post.url
                request = urllib.request.urlopen(url)
                mime = request.info()['Content-type']
                if mime.endswith("png") or mime.endswith("jpeg") or mime.endswith("jpg") or mime.endswith("gif"):
                    # success link is an image
                    credit = post.author.name
                    # save picture
                    image = f"{directory}posts/post{count}.jpg"
                    urllib.request.urlretrieve(url, image)
                    # return dictionary with required info to post located picture
                    if subredditpage == sub_reddit_1:
                        caption = random.choice(caption_list_1)
                        post_ids.append(post.id)
                        result = {"credit": credit, "image": image, "caption": caption}
                        return result
                    elif subredditpage == sub_reddit_2:
                        caption = random.choice(caption_list_2)
                        post_ids.append(post.id)
                        result = {"credit": credit, "image": image, "caption": caption}
                        return result


    def imgresize(photo):
        with open(photo, 'r+b') as f:
            with Image.open(f) as image:
                width, height = image.size
                if width == height:
                    return
                elif width > height:
                    refsize = height
                else:
                    refsize = width
                if refsize >= 1080:
                    refsize = 1080
                cover = resizeimage.resize_cover(image, [refsize, refsize])
                cover.save(photo, image.format)
                return


    def postresult(result):
        fullcaption = f"{result['caption']}\n" \
                      f"Follow @{bot.username}\n" \
                      f"Follow @{bot.username}\n" \
                      f"📷: /u/{result['credit']}\n" \
                      f".\n.\n.\n.\n.\n.\n.\n.\n.\n.\n" \
                      f"{hashlist}"
        try:
            # ensure image has 1:1 aspect ratio
            imgresize(result['image'])
            media = bot.upload_photo(result['image'], caption=fullcaption)
            bot.upload_story_photo(media['pk'])
            # delete image
            os.remove(f'{result["image"]}.REMOVE_ME')
        except:
            os.remove(result['image'])


    def dumptojson(variable, file):
        dump = json.dumps(variable)
        with open(file, 'w') as d:
            d.write(dump)
            d.close()


    def cleanse(string):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        # remove punctuation from the string
        puncremoved = ""
        for char in string:
            if char not in punctuations:
                puncremoved = puncremoved + char
        string = puncremoved
        string = string.lower()  # make everything lowercase
        string = string.split(' ')  # divide up words into list
        return string


    def ackcomments():
        start = time.time()
        try:
            medias = bot.get_user_medias(bot.user_id, is_comment=True)
            posadjs = ['good', 'great', 'nice', 'awesome', 'epic', 'poggers', 'cool', 'lit', 'mint', 'yum', '10', '9', '8', '7',
                       'interesting', 'love', 'amazing', 'gorgeous', 'beautiful', 'delicious', '11', 'thanks', 'thank', 'cute']
            replies = ['Thanks!', 'Glad you like it', 'glad you like it!', 'thank you', '❤', 'cheers', ':)', ':D']
            maxactions = random.randint(20, 40)
            actions = 0
            for media in medias:
                comments = bot.get_media_comments(media)
                for comment in comments:
                    words = cleanse(comment['text'])
                    if actions == maxactions:
                        break
                    elif any(item in posadjs for item in words) and comment['has_liked_comment'] is False and comment["user"]["username"] != bot.username:
                        # like and reply to comment
                        bot.like_comment(comment['pk'])
                        bot.comment(media, f'@{comment["user"]["username"]} {random.choice(replies)}')
                        actions += 1
        except Exception as e:
            print(e)
        end = time.time()
        result = {'functime': end - start, 'actions': actions}
        return result


    def is_follower(userid):
        if userid in bot.get_user_followers(bot.user_id):
            return True
        else:
            return False


    def is_following(userid):
        if userid in bot.get_user_following(bot.user_id):
            return True
        else:
            return False


    def followbot():
        start = time.time()
        medias = bot.get_hashtag_medias(follow_hash, filtration=False)
        media = medias[random.randint(0, 19)]
        acc = bot.get_media_info(media)
        followers = bot.get_user_followers(acc[0]['user']['pk'])
        c = 0
        for follower in followers:
            if is_following(follower):
                continue
            elif c != random.randint(25, 40):
                c += 1
                bot.follow(follower)
            else:
                break
        end = time.time()
        result = {'actions': c, 'functime': end-start}
        return result


    # login
    bot.login(username=username, password=password, proxy=proxy)
    count += 1
    if count % 10 == 0:
        post = findpost(sub_reddit_2)
        postresult(post)
    else:
        post = findpost(sub_reddit_1)
        postresult(post)

    data['count'] = count
    data['post_ids'] = post_ids
    dumptojson(data, data_file)

    # find good comment and acknowledge them
    comment = ackcomments()
    # follow accounts in similar niche
    #  follow = followbot()  # needs improvement

    # code in here /\

    print(f'{comment["actions"]} comments were acknowledged')
    #  print(f'{follow["actions"]} accounts were followed')

    bot.logout()


def get_data(acc):
    with open(f"accounts/{acc}/data.json") as f:
        info = json.load(f)
        f.close()
        return info


sub_dirs = os.listdir('accounts')
total_accounts = len(sub_dirs)


while True:
    first_repeat = True
    start = time.time()
    for sub in sub_dirs:
        data = get_data(sub)
        if first_repeat:
            main(data, f"{data['directory']}data.json")
            first_repeat = False
        else:
            main(data, f"{data['directory']}data.json")

    end = time.time()
    time.sleep(3600-end-start)
