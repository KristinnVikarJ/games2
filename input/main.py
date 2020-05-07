import os
import shutil
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

POSTS = {}

for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])


POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

env = Environment(loader=PackageLoader('main', 'templates'))
home_template = env.get_template('home.html')
contact_template = env.get_template('contact.html')
logo_template = env.get_template('logo.html')
post_template = env.get_template('post.html')

posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in posts_metadata]
home_html = home_template.render(posts=posts_metadata, tags=tags)
contact_html = contact_template.render()
logo_template = logo_template.render(posts=posts_metadata, tags=tags)

print("rendering index.html")
with open('../output/index.html', 'w') as file:
    file.write(home_html)

print("rendering contact.html")
with open('../output/contact.html', 'w') as file:
    file.write(contact_html)

print("rendering logo.html")
with open('../output/logo.html', 'w') as file:
    file.write(logo_template)

print("copying css")
shutil.copyfile("./css/out.css", "../output/css/main.css")

for post in POSTS:
    post_metadata = POSTS[post].metadata
    print("Rendering", post_metadata['title'])

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'tags': post_metadata['tags']
    }

    post_html = post_template.render(post=post_data)
    post_file_path = '../output/posts/{slug}.html'.format(
        slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)
