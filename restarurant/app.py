import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"
conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()


orders = []

menu = [

# 🍛 BIRYANI
{"id":1,"name":"Chicken Biryani","category":"Biryani","price":250,"img":"https://images.unsplash.com/photo-1603894584373-5ac82b2ae398"},
{"id":2,"name":"Mutton Biryani","category":"Biryani","price":350,"img":"https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a"},
{"id":3,"name":"Veg Biryani","category":"Biryani","price":180,"img":"https://images.unsplash.com/photo-1627308595229-7830a5c91f9f"},
{"id":4,"name":"Egg Biryani","category":"Biryani","price":200,"img":"https://images.unsplash.com/photo-1596797038530-2c107229654b"},
{"id":5,"name":"Prawn Biryani","category":"Biryani","price":400,"img":"/static/images/Prawn-Biryani.webp"},
{"id":6,"name":"Hyderabadi Dum Biryani","category":"Biryani","price":300,"img":"https://images.unsplash.com/photo-1628294895950-9805252327bc"},

# 🥤 BEVERAGES
{"id":7,"name":"Coke","category":"Beverages","price":50,"img":"/static/images/coke.jpeg"},
{"id":8,"name":"Pepsi","category":"Beverages","price":50,"img":"https://images.unsplash.com/photo-1613478223719-2ab802602423"},
{"id":9,"name":"Lassi","category":"Beverages","price":60,"img":"https://images.unsplash.com/photo-1625944525533-473f1e4b4c0c"},
{"id":10,"name":"Fresh Lime Soda","category":"Beverages","price":70,"img":"https://images.unsplash.com/photo-1551024709-8f23befc6f87"},
{"id":11,"name":"Cold Coffee","category":"Beverages","price":120,"img":"https://images.unsplash.com/photo-1509042239860-f550ce710b93"},
{"id":12,"name":"Milkshake","category":"Beverages","price":150,"img":"https://images.unsplash.com/photo-1572490122747-3968b75cc699"},

# 🍗 STARTERS
{"id":13,"name":"Chicken 65","category":"Starters","price":200,"img":"https://images.unsplash.com/photo-1608039755401-742074f0548d"},
{"id":14,"name":"Chicken Lollipop","category":"Starters","price":220,"img":"/static/images/chicken.jpg"},
{"id":15,"name":"Paneer Tikka","category":"Starters","price":180,"img":"https://images.unsplash.com/photo-1603894584373-5ac82b2ae398"},
{"id":16,"name":"Veg Manchurian","category":"Starters","price":150,"img":"static/images/Veg Manchurian.jpg"},
{"id":17,"name":"Spring Rolls","category":"Starters","price":140,"img":"https://images.unsplash.com/photo-1544025162-d76694265947"},
{"id":18,"name":"Chilli Chicken","category":"Starters","price":230,"img":"https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec"},

# 🍛 MAIN COURSE
{"id":19,"name":"Butter Chicken","category":"Main Course","price":300,"img":"static/images/Butter-Chicken.jpg"},
{"id":20,"name":"Paneer Butter Masala","category":"Main Course","price":250,"img":"https://images.unsplash.com/photo-1631452180519-c014fe946bc7"},
{"id":21,"name":"Dal Tadka","category":"Main Course","price":180,"img":"https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec"},
{"id":22,"name":"Chicken Curry","category":"Main Course","price":280,"img":"https://images.unsplash.com/photo-1588166524941-3bf61a9c41db"},
{"id":23,"name":"Naan","category":"Main Course","price":40,"img":"https://images.unsplash.com/photo-1628294895950-9805252327bc"},
{"id":24,"name":"Roti","category":"Main Course","price":30,"img":"https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56"},

# 🍰 DESSERTS
{"id":25,"name":"Ice Cream","category":"Desserts","price":90,"img":"https://images.unsplash.com/photo-1580910051074-3eb694886505"},
{"id":26,"name":"Chocolate Cake","category":"Desserts","price":120,"img":"https://images.unsplash.com/photo-1578985545062-69928b1d9587"},
{"id":27,"name":"Gulab Jamun","category":"Desserts","price":80,"img":"/static/images/Gulab jamun.jpeg"},
{"id":28,"name":"Rasgulla","category":"Desserts","price":80,"img":"https://images.unsplash.com/photo-1627308595229-7830a5c91f9f"},
{"id":29,"name":"Brownie","category":"Desserts","price":150,"img":"https://images.unsplash.com/photo-1606312619070-d48b4c652a52"},
{"id":30,"name":"Fruit Custard","category":"Desserts","price":100,"img":"/static/images/FruitCustard.jpeg"},

# 🍎 FRUITS
{"id":31,"name":"Fruit Salad","category":"Fruits","price":120,"img":"https://images.unsplash.com/photo-1574226516831-e1dff420e37f"},
{"id":32,"name":"Apple Bowl","category":"Fruits","price":100,"img":"https://images.unsplash.com/photo-1567306226416-28f0efdc88ce"},
{"id":33,"name":"Banana Plate","category":"Fruits","price":60,"img":"https://images.unsplash.com/photo-1574226516831-e1dff420e37f"},
{"id":34,"name":"Mixed Fruits","category":"Fruits","price":150,"img":"https://images.unsplash.com/photo-1502741338009-cac2772e18bc"},
{"id":35,"name":"Watermelon","category":"Fruits","price":80,"img":"https://images.unsplash.com/photo-1563114773-84221bd62daa"},

]
   

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = c.fetchone()

        conn.close()

        if user:
            session["user"] = username
            session["email"] = username
            session["cart"] = []
            return redirect("/home")

        return "Invalid login"

    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (request.form["username"], request.form["password"]))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("signup.html")

@app.route("/home")
def home():
    # 🔥 ADD THIS CHECK
    if "user" not in session:
        return redirect("/")   # redirect to login

    cart = session.get("cart", [])

    # total cart count
    cart_count = sum(item["qty"] for item in cart)

    # mapping
    cart_map = {}
    for cart_item in cart:
        cart_map[cart_item["item"]["id"]] = cart_item["qty"]

    return render_template(
        "home.html",
        menu=menu,
        cart_count=cart_count,
        cart_map=cart_map
    )
@app.route("/decrease_home/<int:item_id>")
def decrease_home(item_id):
    cart = session.get("cart", [])

    for i, cart_item in enumerate(cart):
        if cart_item["item"]["id"] == item_id:
            if cart_item["qty"] > 1:
                cart_item["qty"] -= 1
            else:
                cart.pop(i)
            break

    session["cart"] = cart
    return redirect("/home")

@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    item = next(x for x in menu if x["id"] == item_id)

    cart = session.get("cart", [])

    # check if item already exists
    for cart_item in cart:
        if cart_item["item"]["id"] == item_id:
            cart_item["qty"] += 1   # 🔥 increase quantity
            session["cart"] = cart
            return redirect("/home")

    # if not exists → add new
    cart.append({
        "item": item,
        "qty": 1
    })

    session["cart"] = cart
    return redirect("/home")

@app.route("/increase/<int:index>")
def increase(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        cart[index]["qty"] += 1
    session["cart"] = cart
    return redirect("/cart")
@app.route("/decrease/<int:index>")
def decrease(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        if cart[index]["qty"] > 1:
            cart[index]["qty"] -= 1
        else:
            cart.pop(index)
    session["cart"] = cart
    return redirect("/cart")

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])

    # ✅ correct calculation
    total = sum(item["item"]["price"] * item["qty"] for item in cart_items)

    return render_template("cart.html", cart=cart_items, total=total)



@app.route("/checkout")
def checkout():
    orders.append({
        "user": session["user"],
        "items": session["cart"]
    })
    session["cart"] = []
    return "Payment Successful! Order Placed."

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/remove/<int:index>")
def remove_item(index):
    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session["cart"] = cart
    return redirect("/cart")

@app.route("/logout")
def logout():
    session.clear()   # 🔥 removes user, cart, everything
    return redirect("/")   # go back to login page

if __name__ == "__main__":
    app.run(debug=True)

