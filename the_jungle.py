from bs4 import BeautifulSoup
import requests
import re
import time
import random
import os

def get_cpython_lines():
    """
    Gets some source code for cPython to print out to look busy
    :return:
    """
    cpython_url = 'https://github.com/python/cpython/blob/master/Python/pythonrun.c'
    soup = BeautifulSoup(requests.get(cpython_url).text, 'html.parser')
    cpython_soup = soup.find("div",{"itemprop":"text", "class":"Box-body p-0 blob-wrapper data type-c"})
    tds = cpython_soup.find_all('td', {"class":"blob-code blob-code-inner js-file-line"})
    cpython_code_lines = []
    for td in tds:
        cpython_code_lines.append(
            ''.join([thing.text+" " for thing in td.find_all('span') if len(thing.text)>1]))
    return(cpython_code_lines)

def get_jungle():
    """
    Gets text of "The Jungle" from project gutenberg
    :return:
    """
    url = "http://www.gutenberg.org/files/140/140-h/140-h.htm#link2HCH0002"
    book = requests.get(url)
    chapters = {}
    chapters_raw = re.compile('</h2>(.*?)<h2>', re.DOTALL).findall(book.text)
    chapters_soup = [BeautifulSoup(text, 'html.parser') for text in chapters_raw]
    for i in range(1, len(chapters_soup)):
        pars = chapters_soup[i].find_all('p')
        chapters[i] = pars
    return(chapters)

if __name__=='__main__':

    print("""
     /$$$$$$$$/$$                    /$$$$$                               /$$          
    |__  $$__/ $$                   |__  $$                              | $$          
       | $$  | $$$$$$$   /$$$$$$       | $$ /$$   /$$ /$$$$$$$   /$$$$$$ | $$  /$$$$$$ 
       | $$  | $$__  $$ /$$__  $$      | $$| $$  | $$| $$__  $$ /$$__  $$| $$ /$$__  $$
       | $$  | $$  \ $$| $$$$$$$$ /$$  | $$| $$  | $$| $$  \ $$| $$  \ $$| $$| $$$$$$$$
       | $$  | $$  | $$| $$_____/| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$| $$_____/
       | $$  | $$  | $$|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$| $$|  $$$$$$$
       |__/  |__/  |__/ \_______/ \______/  \______/ |__/  |__/ \____  $$|__/ \_______/
                                                                /$$  \ $$              
                                                               |  $$$$$$/              
                                                                \______/               
    """)
    print("")
    print("")
    print("By Upton Sinclair")
    print("Thanks to project Gutenberg")


    print("Type q to quit")
    print("Type b to look busy")
    print("Type c to skip to chapter")
    print("Type any other key to continue reading")
    print("Enjoy!")

    x = 'y'
    pars_counter = 0
    if os.path.exists('bookmark.txt'):
        with open('bookmark.txt') as fle:
            for line in fle.readlines():
                exec(line)
        first_read = False
    else:
        first_read = True

    cpython_code_lines = get_cpython_lines()
    chapters = get_jungle()
    while(True):

        while(first_read == True):
            chapter = input("Start reading chapter: ")
            try:
                chapter = int(chapter)
                first_read = False
            except ValueError:
                continue

        x = input("continue: ")

        if x == 'q':
            break
        elif x == 'c':
            first_read = True
            continue
        while(x == 'b'):
            i = random.randint(0, len(cpython_code_lines))
            for j in range(100):
                print(cpython_code_lines[(i+j)%len(cpython_code_lines)])
                time.sleep(.03)
            x = input("jungle_reader.busy_flag .. ..")
        try:
            print(chapters[chapter][pars_counter].prettify())
            pars_counter+=1
        except IndexError:
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            cont_str = input("Chapter completed. Continue? y for yes: ")
            if cont_str == 'y' or cont_str == '':
                chapter += 1
                pars_counter = 0
            else:
                break

    print("Goodbye!")
    with open('bookmark.txt', 'w') as fle:
        fle.write(f"chapter = {chapter}\n")
        fle.write(f"pars_counter = {pars_counter}")

