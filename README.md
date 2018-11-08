# crawl-news

## install the dependencies

```console
pip3 install -r requirements.txt
```

or

```console
pip install -r requirements.txt
```

## run the following command in the top root directory to scrape bcc.com

```console
cd news
scrapy crawl bbc
```

## run the following command in the top root directory to run the program to start up the api

```console

python3 main.py
```

or

```console

python main.py
```

## send a get-request to the api

- The accepted query parameters are title, tag, and days_old.

- The days_old parameter only accepts an integer.

```console
curl 'localhost:5000/bbc?tag=US&days_old=0'
```

## How to run the tests

```console
python3 -m unittest tests/test.py
```

## Comments

    - The program is written in Python 3.
    - Potential enhancements are indicated by TODO comments.

### contact Daiki Nakashita(daiki815@gmail.com) for the database credentials
