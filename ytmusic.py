import requests
import lxml.html
from lxml import etree as et


def get_video(name):  # Getting viode from youtube
    name = "+".join(name.split())
    res = requests.get(f'https://www.youtube.com/results?search_query={name}')

    html = lxml.html.fromstring(res.text)
    html.html_code = et.tostring(html)

    s = '{"videoRenderer":{"videoId":"'

    i = str(html.html_code).find(s) + len(s)

    elem = str(html.html_code)[i:i+200].split('"')[0]

    return "https://www.youtube.com/watch?v=" + elem
