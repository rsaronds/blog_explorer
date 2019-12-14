import datetime
import json

import requests
import collections


Post = collections.namedtuple('Post', 'id title content published view_count')
base_url = 'http://consumer_services_api.talkpython.fm/api/restricted/blog/'
user = 'aronds'
password = 'super_lockdown'
def main():
    while True:
        action = input("What do you want to do with this blog api? [l]ist, [a]dd, [u]pdate, [d]elete, e[x]it: ")
        if action == 'x':
            print('Exiting...')
            break
        if action == 'l':
            posts = get_posts()
            show_posts(posts)
        if action == 'a':
            add_post()
        if action == 'u':
            update_post()
        if action == 'd':
            delete_post() 


def show_posts(posts):
    if not posts:
        print('Sorry, no posts to show.')
        return
    print('---------------------------- BLOG POSTS ----------------------------')
    max_width = max((len('{:,}'.format(int(p.view_count))) for p in posts))
    for idx, p in enumerate(posts):
        padded = ' ' * (max_width - len('{:,}'.format(int(p.view_count))))
        print('{}. {} [{}{:,}]: {}'.format(idx + 1, p.id, padded, int(p.view_count), p.title))


def get_posts():
    url = base_url
    headers = {'Accept': 'application/json'}
    resp = requests.get(url, headers=headers, auth=(user, password))

    if resp.status_code != 200:
        print("Error donwloading posts: {} {}".format(resp.status_code, resp.text))
        return []

    return [Post(**post) for post in resp.json()]

def add_post():
    now = datetime.datetime.now()
    published_text = '{}-{}-{}'.format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

    title = input('title: ')
    content = input('content: ')
    view_count = int(input('view count: '))

    post_data = dict(title=title, content=content, view_count=view_count, published=published_text)
    url = base_url
    # headers = {'content-type': 'application/json'}

    resp = requests.post(url, json=post_data, auth=(user, password))

    if resp.status_code != 201:
        print("Error creating post: {} {}".format(resp.status_code, resp.text))
        return

    post = resp.json()
    print("You created the below post: ")
    print(post)


def update_post():
    print("To update a post, choose the number from the list below.")
    posts = get_posts()
    show_posts(posts)
    print()

    post = posts[int(input('number of post to update: '))-1]

    title = input('title: ['+post.title+']')
    title = title if title else post.title

    content = input('content: ['+post.content+']')
    content = content if content else post.content

    view_count = input('view count: ['+str(post.view_count)+']')
    view_count = view_count if view_count else post.view_count

    post_data = dict(title=title, content=content, view_count=view_count, published=post.published)

    url = base_url + post.id
    resp = requests.put(url, data=json.dumps(post_data), auth=(user, password))

    if resp.status_code != 204:
        print("Error updating post: {} {}".format(resp.status_code, resp.text))
        return

    print("Successfuly updated {}".format(post.title))


def delete_post():
    print("To update a post, choose the number from the list below.")
    posts = get_posts()
    show_posts(posts)
    print()

    post = posts[int(input('number of post to delete: '))-1]

    print("Deleting {} ...".format(post.title))

    url = base_url + post.id
    resp = requests.delete(url, auth=(user, password))

    if resp.status_code != 202:
        print("Error deleting post: {} {}".format(resp.status_code, resp.text))
        return


if __name__ == "__main__":
    main()
