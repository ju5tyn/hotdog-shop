from shop import app, db
from shop.models import Item, User, CartItem, CartSession, ItemReview
from shop.forms import *
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, current_user


shipping_cost = 1.0

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def front_page():
    
    sortingForm = SortingForm()
    searchForm = SearchForm()
    
    if searchForm.validate_on_submit():
        if searchForm.search.data != "":
            items = Item.query.filter(Item.name.contains(searchForm.search.data))
            return render_template('home.html', items=items, user=current_user, sorting_form=None, search_form=searchForm)
    
    #if form.validate_on_submit():
    print(sortingForm.sort_type.data)
    if sortingForm.sort_type.data == "price_high":
        items = Item.query.order_by(Item.price.desc())
    elif sortingForm.sort_type.data == "price_low":
        items = Item.query.order_by(Item.price)
    elif sortingForm.sort_type.data == "eco_low":
        items = Item.query.order_by(Item.eco_rating.desc())
    elif sortingForm.sort_type.data == "default":
        items = Item.query.order_by(Item.id)
    else:
        items = Item.query.order_by(Item.id)
    return render_template('home.html', items=items, user=current_user, sorting_form=sortingForm, search_form=searchForm)
    
    
        
        
    #items = Item.query.all()
    #return render_template('home.html', items=items, user=current_user, form=form)

@app.route("/add/<int:item_id>")
def add_item(item_id):
    user = current_user
    if user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        item = Item.query.get_or_404(item_id)
        session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
        
        cart_item_existing = CartItem.query.filter_by(session_id=session.id, item_id=item.id).first()
        
        
        if cart_item_existing is not None:
            cart_item_existing.quantity += 1
            db.session.add(cart_item_existing)
        else:
            cart_item = CartItem(session_id=session.id, item_id=item.id, quantity=1)
            db.session.add(cart_item)
        db.session.commit()
        
        return redirect(url_for('front_page'))
        
@app.route("/add_one/<int:item_id>")
def add_one(item_id):
    user = current_user
    if user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        item = Item.query.get_or_404(item_id)
        session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
        
        cart_item_existing = CartItem.query.filter_by(session_id=session.id, item_id=item.id).first()
        
        
        if cart_item_existing is not None:
            cart_item_existing.quantity += 1
            db.session.add(cart_item_existing)
        else:
            cart_item = CartItem(session_id=session.id, item_id=item.id, quantity=1)
            db.session.add(cart_item)
        db.session.commit()
        
        return redirect(url_for('cart'))
        
@app.route("/remove_one/<int:item_id>")
def remove_one(item_id):
    user = current_user
    if user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        item = Item.query.get_or_404(item_id)
        session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
        
        cart_item_existing = CartItem.query.filter_by(session_id=session.id, item_id=item.id).first()
        
        
        if (cart_item_existing is not None):
            if cart_item_existing.quantity > 1:
                cart_item_existing.quantity -= 1
                db.session.add(cart_item_existing)
                db.session.commit()
                return redirect(url_for('cart'))
                
        CartItem.query.filter(CartItem.id == cart_item_existing.id).delete()
        
        
        
        #db.session.delete(cart_item)
        db.session.commit()
        return redirect(url_for('cart'))

@app.route("/remove_all/<int:item_id>")
def remove_all_item(item_id):
    user = current_user
    if user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        item = Item.query.get_or_404(item_id)
        session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
        
        cart_item_existing = CartItem.query.filter_by(session_id=session.id, item_id=item.id).first()
        
                
        CartItem.query.filter(CartItem.id == cart_item_existing.id).delete()
        
        
        
        #db.session.delete(cart_item)
        db.session.commit()
        return redirect(url_for('cart'))



@app.route("/cart")
def cart():
    user = current_user
    if user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        calculateTotal()
        session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
        cartitems = CartItem.query.filter_by(session_id=session.id)
        items = Item.query.all()
        
        subtotal=session.total
        total=session.total+shipping_cost
        
        return render_template('cart.html', user=user, items=items, cartitems=cartitems, subtotal=subtotal, shipping_cost=shipping_cost,total=total)
    
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('front_page'))
    else:
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                
                session = CartSession(user_id=user.id)
                
                user.authenticated = True
                
                db.session.add(session)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                #flash('You\'ve successfully logged in,'+' '+ current_user.username +'!')
                return redirect(url_for('front_page'))
            else:   
            #return redirect(url_for('login_error'))
                return render_template('login.html', form=form, user=current_user, show_error=True)
            
    return render_template('login.html', form=form, user=current_user, show_error=False)
        
@app.route("/login/error")
def login_error():
    return render_template('loginerror.html', user=current_user)
        
    
@app.route("/logout")
def logout():
    if current_user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        user = current_user
        current_user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        
        flash('You\'re now logged out. Thanks for your visit!')
        return redirect(url_for('front_page'))

    
@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated == True:
        return redirect(url_for('front_page'))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        return render_template('register.html', form=form, user=current_user)
    
@app.route("/product/<int:item_id>")
def item(item_id):
    
    item=Item.query.get_or_404(item_id)
    reviews = ItemReview.query.filter_by(item_id=item_id)
    users = User.query.all()
    
    return render_template('product.html', item=item, user=current_user, reviews=reviews, users=users)
    
@app.route("/product/review/<int:item_id>", methods=['GET','POST'])
def item_review(item_id):
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    else:
        form = ReviewForm()
        item=Item.query.get_or_404(item_id)
        
        if form.validate_on_submit():
            
            review = ItemReview(item_id=item.id, user_id=current_user.id, subject=form.subject.data, description=form.description.data, rating=form.rating.data)
            
            db.session.add(review)
            db.session.commit()
            
            return redirect(url_for('item', item_id=item.id))
        else:   
            return render_template('productreview.html', form=form, item=item, user=current_user)
        
        
    
@app.route("/checkout", methods=['GET','POST'])
def checkout():
    if current_user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        form = CheckoutForm()
        if form.validate_on_submit():
            return redirect(url_for('checkout_success'))
            
        calculateTotal()
        session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
        
        subtotal=session.total
        total=subtotal+shipping_cost
        
        return render_template("checkout.html", form=form, user=current_user, total=total)
    
@app.route("/checkout/success")
def checkout_success():
    if current_user.is_authenticated == False:
        return redirect(url_for('register'))
    else:
        return render_template("checkoutsuccess.html", user=current_user)
    

def calculateTotal():
    session = CartSession.query.filter_by(user_id=current_user.id).order_by(CartSession.id.desc()).first()
    cartitems = CartItem.query.filter_by(session_id=session.id)
    items = Item.query.all()
    total = 0.0
    for cartitem in cartitems:
        total += (items[cartitem.item_id-1].price * cartitem.quantity)
    #session.total = total + shipping_cost
    session.total=total
    db.session.commit()
    
    