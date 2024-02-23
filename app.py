from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_quotes():
    URL = "http://www.values.com/inspirational-quotes"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    
    quotes = []

    table = soup.find('div', attrs={'id': 'all_quotes'})

    for row in table.findAll('div', attrs={'col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top'}):
        quote = {
            'theme': row.h5.text,
            'url': row.a['href'],
            'img': row.img['src'],
            'lines': row.img['alt'].split(" #")[0],
            'author': row.img['alt'].split(" #")[1]
        }
        quotes.append(quote)

    return quotes

@app.route('/get_quotes', methods=['GET'])
def get_quotes():
    quotes = scrape_quotes()
    return jsonify({'quotes': quotes})

if __name__ == '__main__':
    app.run(debug=True)