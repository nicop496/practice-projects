from requests import get as http_request
from bs4 import BeautifulSoup


ebook_name = input('Enter book name: ')
file_type = input('Enter desired file type (epub, pdf, mobi, azw3, doc, etc.): ').lower()

URL_DOMAIN = 'https://b-ok.lat'
url = f'{URL_DOMAIN}/s/{ebook_name.lower()}/?extensions%5B0%5D={file_type}&order=bestmatch'
soup = BeautifulSoup(http_request(url).text, 'lxml')

book_a_tag = soup.find('h3', itemprop='name').a
book_url = URL_DOMAIN + book_a_tag['href']
book_soup = BeautifulSoup(http_request(book_url).text, 'lxml')

print(f'\nTitle: "{book_a_tag.text}"\nURL if you want to check: {book_url}\n')


if input('Is this book correct? (y/n): ') == 'y':
    download_url = book_soup.find('i', class_='zlibicon-download').parent['href']
    content = http_request(URL_DOMAIN + download_url, allow_redirects=True).content

    if b'Daily limit reached' in content:
        print('Daily limit of downloads (5) reached')
    else:
        with open(f'{ebook_name.capitalize()}.{file_type}', 'wb') as file:
            file.write(content)
            print('Book downloaded succesfully')
else:
    print('Book not found. Try searching with another type.')
