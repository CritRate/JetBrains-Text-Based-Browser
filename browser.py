import os
import argparse
import re
from bs4 import BeautifulSoup
from colorama import init, Fore

import requests

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

websites = {
    'bloomberg.com': bloomberg_com,
    'nytimes.com': nytimes_com
}

shortcuts = []
history = []

position_in_history = 0

init()


def save_site(directory, filename, site):
    with open(f'{directory}/{filename}', 'w', encoding='utf-8') as file:
        file.write(site)


def open_site(directory, filename):
    with open(f'{directory}/{filename}', 'r', encoding='utf-8') as file:
        print(file.read())


# write your code here
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='the directory for saved websites', type=str, )
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.mkdir(args.dir)

    while True:
        website = input()

        if website == 'exit':
            break
        if website == 'back':
            position_in_history -= 1
            website = history[position_in_history - 1]

        if re.match(r'\w+\.\w+', website) is None and website.split('.')[0] not in shortcuts:
            print('error: wrong website')
            continue

        if website in shortcuts:
            history.append(website)
            position_in_history += 1
            open_site(args.dir, website)
            continue

        if not website.startswith('https://'):
            website = 'https://' + website

        request = requests.get(url=website)
        soup = BeautifulSoup(request.content, 'html.parser')
        text = []
        for s in soup.find_all():
            if s.name in ['a']:
                text.append(Fore.BLUE + s.text + Fore.RESET)
            elif s.name in ['p']:
                text.append(s.text)
        print('\n'.join(text))

        history.append(website)
        position_in_history += 1
        name = website.split('.')[1]
        save_site(args.dir, name, '\n'.join(text))
        shortcuts.append(name)
