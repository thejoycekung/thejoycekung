import requests, os, re
from xml.etree import ElementTree

def get_book_info():
    api_key = os.getenv('GOODREADS_KEY')
    shelf_xml = requests.get('https://www.goodreads.com/review/list.xml',
                    data = {'v': 2,
                            'key': api_key,
                            'id': '53120380-joyce',
                            'shelf': 'currently-reading'})
    print("Goodreads response:", shelf_xml.status_code)
    tree = ElementTree.fromstring(shelf_xml.content)
    '''
    with ElementTree we can only access things by numerical index:
        2: list of reviews
        0: the first review
        1: the book information
        6: the book title (without the series name)
        21: the authors object
            0: the first author
            2: the first author's name
    for now, since i'm only ever reading 1 book at a time, this is not a problem
    '''
    reviews = tree[2]
    if len(reviews) < 1:
        book_title = "... nothing! maybe I need to start something new ..."
        book_author = None
    else:
        book_title = tree[2][0][1][6].text
        book_author = tree[2][0][1][21][0][1].text
    return book_title, book_author

def modify_bio(text):
    with open("README.md", "r") as f:
        bio = f.read()
    with open("README.md", "w") as f:
        match = re.sub("(reading.*:\s)(.*)\n\n", r"\1" + text + "\n\n", bio)
        f.write(match)
    return

if __name__ == "__main__":
    book_title, book_author = get_book_info()
    if book_author == None:
        new_reading_text = book_title
    else:
        new_reading_text = book_title + " by " + book_author
    print(new_reading_text)
    modify_bio(new_reading_text)
