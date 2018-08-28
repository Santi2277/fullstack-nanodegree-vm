from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
import datetime
from flask import session as login_session
import random
import string

# using flask micro-framework, creating app
app = Flask(__name__)

# start session with database itemcatalog.db
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User identification with google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # get username and email
    data = request.get_data()
    splitdata = data.split("#~#")
    username = splitdata[0]
    email = splitdata[1]
    login_session['username'] = username
    login_session['email'] = email
    # connect to database
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # add user if it doesn't exists (in database)
    userfind = session.query(User).filter_by(email=email).all()
    if len(userfind) == 0:
        newUser = User(name=username, email=email)
        session.add(newUser)
        session.commit()
    return ""+login_session['username']+"connected"

# Disconnect user login session (google)
@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    login_session['username'] = None
    login_session['email'] = None
    login_session['login'] = 0
    return "no user connected now"

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
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    itemssize = len(items)


    return render_template('category.html', category = category, items = items, itemssize=itemssize)

# 3) New category
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    # POST method add the new category then go to homepage
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':
        if ('username' not in login_session):
            return redirect('/')
        else:
            if login_session['username'] == None:
                return redirect('/')
            else:
                user = session.query(User).filter_by(name = login_session['username']).one()
                newCategory = Category(name = ""+request.form['name'], user = user)
                session.add(newCategory)
                session.commit()
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
        #if (editcategory.user.email == login_session['email']) and (editcategory.user.name == login_session['name']):
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
    # you must delete items of that category
    categoryitems = session.query(Item).filter_by(category_id = category_id).all()
    # POST delete that category and return to homepage
    if request.method == 'POST':
        # delete items of that category
        for ci in categoryitems:
            session.delete(ci)
            session.commit()
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
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    categories = session.query(Category).all()
    Categories = []
    for i in categories:
        Categories.append(i.serialize)
    for c in Categories:
        # TO FILTER
        items = session.query(Item).filter_by(category_id = c['id']).all()
        Items=[i.serialize for i in items]
        c['items'] = Items
    return jsonify(Categories=Categories)

# 1) Show users
@app.route('/users/')
def showUsers():
    # find all users to pass to html template
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    users = session.query(User).all()
    return render_template('users.html', users=users)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=8000)
