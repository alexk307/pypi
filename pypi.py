import requests
import re
import mechanize
from bs4 import BeautifulSoup
from httplib import OK
from time import sleep
from shutil import copy
from subprocess import call
from dotenv import load_dotenv, find_dotenv

import gmail
import random
import string
import os

from build_files import build_pypirc, build_setup


load_dotenv(find_dotenv())

EMAIL = os.environ.get('email')
PASSWORD = os.environ.get('password')


def random_string(x):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(x))


def register(username, password):
    br = mechanize.Browser()
    br.open("https://pypi.python.org/pypi?%3Aaction=register_form")
    user_form = br.forms()[1]
    br.form = user_form

    br.form['name'] = username
    br.form['password'] = password
    br.form['confirm'] = password
    br.form['email'] = '{}+{}@gmail.com'.format(EMAIL, random_string(8))

    # TODO verify status code
    br.submit()
    br.close()


def confirm(confirmation_url):
    br = mechanize.Browser()
    br.open(confirmation_url)
    br.form = br.forms()[1]
    br.form.find_control(type='checkbox').items[0].selected = True
    br.submit()


def email():
    g = gmail.login(EMAIL, PASSWORD)
    message = g.inbox().mail()[-1]
    message.fetch()
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.body)
    return urls[0]


def _strip_html(text):
    """
    Strips tags from HTML
    :param text: The text to strip from
    :return: Cleaned text
    """
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))


def get_top_packages(page=1):
    resp = requests.get('http://pypi-ranking.info/alltime?page={}'.format(page))
    soup = BeautifulSoup(resp.text)
    tags = soup.find_all('span', {'class': 'list_title'})
    return [_strip_html(tag) for tag in tags]


def is_registered(module_name):
    pypi_location = 'https://pypi.python.org/pypi/{}'.format(module_name)
    resp = requests.get(pypi_location)
    return True if resp.status_code == OK else False

if __name__ == '__main__':
    username = random_string(10)
    password = random_string(16)
    print 'Registering user: %s with password: %s...' % (username, password)
    register(username, password)
    print 'Registered.'
    print 'Checking email for activation link...'
    print 'Sleeping to wait for email'
    sleep(10)
    link = email()
    confirm(link)
    print 'Activated.'

    pypirc = build_pypirc(username, password)

    # Package name same as username for now
    setuppy = build_setup(name=username)

    directory = random_string(10)
    os.mkdir(directory)
    os.chdir(directory)

    f = file('.pypirc', 'w')
    f.write(pypirc)
    f.close()

    # Move .pypirc auth file to home directory
    home_dir = os.path.expanduser('~')
    copy('.pypirc', home_dir)

    # Copy over setup bash script
    copy('../setup.sh', '.')

    f = file('setup.py', 'w')
    f.write(setuppy)
    f.close()

    print 'Created user: %s with password: %s.' % (username, password)

    # Call setup bash script to prepare and upload to pypi
    call('./setup.sh')
