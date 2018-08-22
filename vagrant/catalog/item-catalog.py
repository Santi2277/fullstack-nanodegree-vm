from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

app = Flask(__name__)



# 1) Show homepage (categories)
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = ["baseball", "soccer", "running"]
    return render_template('categories-home.html', categories = categories)

# 2) Category page
@app.route('/categories/<int:category_id>/')
def showCategory(category_id):
    return "show category"

# 3) New category
@app.route('/categories/new/')
def newCategory():
    return "new category"

# 4) Edit category
@app.route('/categories/<int:category_id>/edit/')
def editCategory(category_id):
    return "edit category"

# 5) Delete category
@app.route('/categories/<int:category_id>/delete/')
def deleteCategory(category_id):
    return "delete category"

# 6) Item page
@app.route('/categories/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    return "show item description"

# 7) New item
@app.route('/categories/items/<int:item_id>/new/')
def newItem(item_id):
    return "new item"

# 8) Edit item
@app.route('/categories/items/<int:item_id>/edit/')
def editItem(item_id):
    return "edit item"

# 9) Delete item
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
    return "delete item"

# 10) JSON endpoint
@app.route('/catalog/JSON/')
def catalogJSON():
    return "JSON catalog"





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=8000)
