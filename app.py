from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://fakestoreapi.com/products"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("product", "").lower()

    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException:
        return render_template("results.html", products=[], error="API Error. Please try again later.")

    filtered_products = []

    for product in products:
        if query in product["title"].lower():
            filtered_products.append({
                "name": product["title"],
                "price": product["price"],
                "image": product["image"],
                "store": "Demo Store",
                "link": product["image"]
            })

    filtered_products = sorted(filtered_products, key=lambda x: x["price"])

    return render_template("results.html", products=filtered_products, error=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
