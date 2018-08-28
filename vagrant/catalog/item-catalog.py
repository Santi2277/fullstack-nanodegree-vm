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
    # check if user is authenticated
    if ('username' not in login_session):
        login = 0
    else:
        if login_session['username'] == None:
            login = 0
        else:
            login = 1
    return render_template('category.html', category = category, items = items, itemssize=itemssize, login=login)

# 3) Item page
@app.route('/categories/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # find item descriptionpage
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    # check if user is item creator
    if ('username' not in login_session):
        creator = 0
    else:
        if login_session['username'] == None:
            creator = 0
        else:
            if (item.user.name == login_session['username']) and (item.user.email == login_session['email']):
                creator = 1
            else:
                creator = 0
    return render_template('item.html', category = category, item = item, creator=creator)

# 4) New item
@app.route('/categories/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newItem(category_id):
    # POST method add the new item then go to homepage
    # category = session.query(Category).filter_by(id = category_id).one()
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        # only add item if user is authenticated
        if ('username' not in login_session):
            # flash("Must be logged in to add items")
            return redirect(url_for('showCategory', category_id=category_id))
        else:
            if login_session['username'] == None:
                # flash("Must be logged in to add items")
                return redirect(url_for('showCategory', category_id=category_id))
            else:
                category = session.query(Category).filter_by(id = category_id).one()
                user = session.query(User).filter_by(email = login_session['email']).one()
                newItem = Item(name = ""+request.form['name'], description = ""+request.form['description'], user = user, category = category, created_at = datetime.datetime.now())
                session.add(newItem)
                session.commit()
                return redirect(url_for('showCategory', category_id=category_id))
    # GET method show add new category template
    else:
        category = session.query(Category).filter_by(id = category_id).one()
        return render_template('item-new.html', category = category)

# 5) Edit item
@app.route('/categories/<int:category_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    edititem = session.query(Item).filter_by(id = item_id).one()
    # POST edit the item with the form given and return to category
    if request.method == 'POST':
        if ('username' not in login_session):
            # flash("Must be logged in and item owner to edit item")
            return redirect(url_for('showCategory', category_id=category_id))
        else:
            if login_session['username'] == None:
                # flash("Must be logged in and item owner to edit item")
                return redirect(url_for('showCategory', category_id=category_id))
            else:
                if (edititem.user.name == login_session['username']) and (edititem.user.email == login_session['email']):
                    category = session.query(Category).filter_by(name = ""+request.form['categorybox']).one()
                    edititem.name = ""+request.form['name']
                    edititem.description = ""+request.form['description']
                    edititem.category = category
                    session.add(edititem)
                    session.commit()
                    # flash("Item edited")
                    return redirect(url_for('showItem', category_id=category_id, item_id=item_id ))
                else:
                    # flash("Must be logged in and item owner to edit item")
                    return redirect(url_for('showCategory', category_id=category_id))
    # GET pass item to edit item template
    else:
        category1 = session.query(Category).filter_by(id = category_id).one()
        categories = session.query(Category).all()
        return render_template('item-edit.html', item = edititem, category=category1, categories = categories)

# 6) Delete item
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteitem = session.query(Item).filter_by(id = item_id).one()
    # POST delete that item and return to homepage
    if request.method == 'POST':
        if ('username' not in login_session):
            # flash("Must be logged in and item owner to delete item")
            return redirect(url_for('showCategory', category_id=category_id))
        else:
            if login_session['username'] == None:
                # flash("Must be logged in and item owner to delete item")
                return redirect(url_for('showCategory', category_id=category_id))
            else:
                if (deleteitem.user.name == login_session['username']) and (deleteitem.user.email == login_session['email']):
                    session.delete(deleteitem)
                    session.commit()
                    # flash("Item deleted")
                    return redirect(url_for('showCategory', category_id=category_id))
                else:
                    # flash("Must be logged in and item owner to delete item")
                    return redirect(url_for('showCategory', category_id=category_id))

    # GET pass item to delete item template
    else:
        return render_template('item-delete.html', item = deleteitem, category_id=category_id)

# 7) JSON endpoint
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

# 8) Show users
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
