# crawl-news

1. The use of python3.5 or later is recommended.

2. Potential enhancements are indicated with the TODO comments.

## install the dependencies

```console
pip3 install -r requirements.txt
```

or

```console
pip install -r requirements.txt
```

## run the following command to scrape bcc.com

```console
cd news
scrapy crawl bbc
```

## run the flask app to start up the api.

```console

python3 main.py
```

or

```console

python main.py
```

## send a get-request to the api.

- The accepted query parameters are title, tag, and days_old.

- The days_old parameter only accepts an integer.

```console
curl 'localhost:5000/bbc?tag=US&days_old=0'
```

### contact Daiki Nakashita(daiki815@gmail.com) for the database credentials.