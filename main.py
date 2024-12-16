from flask import Flask, g, render_template, request
from database import get_db, init_db
import requests

app = Flask("app", static_folder="public", template_folder="views")

with app.app_context():
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stock-prices", methods=["GET"])
def check_stocks():
    stocks = [stock.upper() for stock in request.args.getlist("stock")]
    if len(stocks) == 0:
        return "No stocks sent"
    if len(stocks) > 2:
        return "Maximum is 2 stocks"

    try:
        stock_data = {}
        for stock in stocks:
            stock_data[stock] = requests.get(
                f"https://repeated-alpaca.glitch.me/v1/stock/{stock}/quote"
            ).json()
    except:
        return "Stock API error"

    fake_stocks = [
        name for name, data in stock_data.items() if data == "Unknown symbol"
    ]
    if len(fake_stocks) == 1:
        return f"'{fake_stocks[0]}' is not a NASDAQ symbol"
    elif len(fake_stocks) == 2:
        return f"Neither '{fake_stocks[0]}' nor '{fake_stocks[1]}' are NASDAQ symbols"

    try:
        db = get_db()
        c = db.cursor()

        if request.args.get("like") == "true":
            c.executemany(
                "INSERT OR IGNORE INTO like(stock, ip) VALUES(?, ?)",
                [(stock, request.remote_addr) for stock in stocks],
            )
            db.commit()

        query = "SELECT stock, count(ip) AS likes FROM like WHERE stock == ?"
        if len(stocks) == 2:
            query += " OR stock == ?"
        query += " GROUP BY stock"
        c.execute(query, tuple(stocks))
        likes = {}
        for stock in stocks:
            # Set default value in case no likes have been recorded
            likes[stock] = 0
        for row in c.fetchall():
            likes[row[0]] = row[1]

        if len(stocks) == 1:
            return {
                "stockData": {
                    "stock": stocks[0],
                    "price": stock_data[stocks[0]]["latestPrice"],
                    "likes": likes[stocks[0]],
                }
            }
        else:
            return {
                "stockData": [
                    {
                        "stock": stocks[0],
                        "price": stock_data[stocks[0]]["latestPrice"],
                        "rel_likes": likes[stocks[0]] - likes[stocks[1]],
                    },
                    {
                        "stock": stocks[1],
                        "price": stock_data[stocks[1]]["latestPrice"],
                        "rel_likes": likes[stocks[1]] - likes[stocks[0]],
                    },
                ]
            }

    except:
        "Database error"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
