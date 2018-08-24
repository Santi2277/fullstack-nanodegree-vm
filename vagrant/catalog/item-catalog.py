from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
import datetime

# using flask micro-framework, creating app
app = Flask(__name__)

# start session with database itemcatalog.db
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# 1) Show homepage (categories)
@app.route('/')
@app.route('/categories/')
def showCategories():
    # find all categories to pass to the main template
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    categories = session.query(Category).all()
    latestitems = session.query(Item).order_by("created_at desc").limit(3)
    return render_template('categories-home.html', categories = categories, latestitems=latestitems)

# 2) Category page
@app.route('/categories/<int:category_id>/')
def showCategory(category_id):
    # find category and its items to show in category template
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category.html', category = category, items = items)

# 3) New category
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    # POST method add the new category then go to homepage
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':
        newUser = User(name="Santi")
        session.add(newUser)
        session.commit()
        newCategory = Category(name = ""+request.form['name'], user = newUser)
        session.add(newCategory)
        session.commit()
        # flash("Category added")
        return redirect(url_for('showCategories'))
    # GET method show add new category template
    else:
        return render_template('category-new.html')


# 4) Edit category
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editcategory = session.query(Category).filter_by(id = category_id).one()
    # POST edit the category with the form given and return to homepage
    if request.method == 'POST':
        editcategory.name = ""+request.form['name']
        session.add(editcategory)
        session.commit()
        # flash("Category edited")
        return redirect(url_for('showCategories'))
    # GET pass category to edit category template
    else:
        return render_template('category-edit.html', category = editcategory)

# 5) Delete category
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletecategory = session.query(Category).filter_by(id = category_id).one()
    # POST delete that category and return to homepage
    if request.method == 'POST':
        session.delete(deletecategory)
        session.commit()
        # flash("Category deleted")
        return redirect(url_for('showCategories'))
    # GET pass category to delete category template
    else:
        return render_template('category-delete.html', category = deletecategory)

# 6) Item page
@app.route('/categories/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    # find item descriptionpage
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', category = category, item = item)

# 7) New item
@app.route('/categories/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id):
    # POST method add the new item then go to homepage
    # category = session.query(Category).filter_by(id = category_id).one()
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':
        category = session.query(Category).filter_by(id = category_id).one()
        user = session.query(User).filter_by(id = category.user_id).one()
        newItem = Item(name = ""+request.form['name'], description = ""+request.form['description'], user = user, category = category, created_at = datetime.datetime.now())
        session.add(newItem)
        session.commit()
        # flash("Category added")
        return redirect(url_for('showCategory', category_id=category_id))
    # GET method show add new category template
    else:
        category = session.query(Category).filter_by(id = category_id).one()
        return render_template('item-new.html', category = category)

# 8) Edit item
@app.route('/categories/<int:category_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    edititem = session.query(Item).filter_by(id = item_id).one()
    # POST edit the item with the form given and return to category
    if request.method == 'POST':
        category = session.query(Category).filter_by(name = ""+request.form['categorybox']).one()
        edititem.name = ""+request.form['name']
        edititem.description = ""+request.form['description']
        edititem.category = category
        session.add(edititem)
        session.commit()
        # flash("Category edited")
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id ))
    # GET pass item to edit item template
    else:
        category1 = session.query(Category).filter_by(id = category_id).one()
        categories = session.query(Category).all()
        return render_template('item-edit.html', item = edititem, category=category1, categories = categories)

# 9) Delete item
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    deleteitem = session.query(Item).filter_by(id = item_id).one()
    # POST delete that item and return to homepage
    if request.method == 'POST':
        session.delete(deleteitem)
        session.commit()
        # flash("Item deleted")
        return redirect(url_for('showCategory', category_id=category_id))
    # GET pass item to delete item template
    else:
        return render_template('item-delete.html', item = deleteitem, category_id=category_id)

# 10) JSON endpoint
@app.route('/catalog/JSON/')
def catalogJSON():
    return "JSON catalog"





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=8000)
