from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load product data from JSON
def load_products():
    with open('products.json') as f:
        return json.load(f)

@app.route('/')
def home():
    products = load_products()
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        with open('submissions.txt', 'a') as f:
            f.write(f"{name} ({email}) interested in {product['title']}\n")
        return redirect(url_for('home'))

    return render_template('product.html', product=product)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contacts.txt', 'a') as f:
            f.write(f"{name} ({email}): {message}\n")
        return redirect(url_for('home'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
