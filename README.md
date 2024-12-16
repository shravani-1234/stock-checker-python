# Python stock price checker

[![Run on Repl.it](https://repl.it/badge/github/tywmick/stock-checker-python)](https://repl.it/github/tywmick/stock-checker-python)

This is a Python port of my [Node.js stock price checker](https://ty-stockchecker.glitch.me/), built with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLite](https://sqlite.org/index.html). The front end API test on the home page also uses [Bootstrap](https://getbootstrap.com/), [jQuery](https://jquery.com/), and [highlight.js](https://highlightjs.org/). The API fulfills the following user stories:

1. I can **GET** `/api/stock-prices` with form data containing a Nasdaq `stock` ticker and recieve back an object `stockData`.
2. In `stockData`, I can see the `stock` (string, the ticker), `price` (decimal in string format), and `likes` (int).
3. I can also pass along field `like` as `true` (boolean) to have my like added to the stock(s). Only 1 like per IP should be accepted.
4. If I pass along 2 stocks, the return object will be an array with both stocks' info, but instead of `likes`, it will display `rel_likes` (the difference between the likes on both) on both.
5. A good way to receive current price is the following external API (replacing 'GOOG' with your stock): `https://finance.google.com/finance/info?q=NASDAQ%3aGOOG`
