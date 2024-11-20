from bs4 import BeautifulSoup
import requests
import time

root = 'https://subslikescript.com'
website = f'{root}/movies'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')

box = soup.find('article', class_='main-article')
ul = box.find('ul', class_='scripts-list')

links = []

for li in ul.find_all('li'):
    for link in li.find_all('a', href=True): 
        links.append(link['href'])

for link in links:
    website = f'{root}{link}'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='main-article')
        
    title = box.find('h1').get_text()
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator= ' ')
    print(transcript)

    with open(f'{title}.txt', 'w') as file:
        file.write(transcript)
    time.sleep(1)  

