from flask import Flask, redirect, request, flash,render_template, url_for ,make_response
from flask_restful import Api, Resource, fields, marshal_with, reqparse,abort

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.Integer)

class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Product(db.Model):
    __tablename__ = 'product'
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_id = db.Column(db.Integer, db.ForeignKey("category.c_id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)    
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    manufacture_date = db.Column(db.Date,  nullable=True)
    

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user.u_id"),nullable=False)
    p_id = db.Column(db.Integer, db.ForeignKey("product.p_id"),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)   
    
    
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("userlogin.html")
    if request.method=="POST":
        users = User.query.all()

        username = request.form["user"]
        password = request.form["pass"]

        for user in users:
            if username == user.username and password == user.password:
                #print("Logged in successfully")
                cuser = User.query.filter(User.username == username).one()
                uid = cuser.u_id
                #print(uid)
                if cuser.user_type ==0:
                    return redirect(url_for("userindex", uid=uid))
                else:
                    return redirect(url_for("alogin"))
            
        else:
            return redirect(url_for("login"))



                
            

@app.route("/userregister", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("userregister.html")

    if request.method=="POST":

        uname = request.form["uname"]
        fname = request.form["fname"]
        passw = request.form["pass"]
        cpass = request.form["cpass"]

        users = User.query.all()
        for user in users:
            if user.username == uname:
                return redirect(url_for("register"))
            
        if passw == cpass:
            new_user = User(username=uname, password=passw, name=fname, user_type = 0)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))

        
@app.route('/admin', methods=["GET", "POST"])
def alogin():
    if request.method=="GET":
        return render_template("adminlogin.html")
    if request.method=="POST":
        users = User.query.all()

        username = request.form["user"]
        password = request.form["pass"]

        for user in users:
            if username == user.username and password == user.password:
                #print("Logged in successfully")
                cuser = User.query.filter(User.username == username).one()
                uid = cuser.u_id
                #print(uid)
                if cuser.user_type ==1:
                    return redirect(url_for("aindex", uid=uid))
                else:
                    return redirect(url_for("login"))
        else:
            return redirect(url_for("alogin"))

                
            

@app.route("/adminregister", methods=["GET", "POST"])
def aregister():
    if request.method=="GET":
        return render_template("adminregister.html")

    if request.method=="POST":

        uname = request.form["uname"]
        fname = request.form["fname"]
        passw = request.form["pass"]
        cpass = request.form["cpass"]

        users = User.query.all()
        for user in users:
            if user.username == uname:
                return redirect(url_for("aregister"))
            
        if passw == cpass:
            new_user = User(username=uname, password=passw, name=fname, user_type = 1)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("alogin"))
        else:
            return redirect(url_for("aregister"))

@app.route('/index/<int:uid>',methods=["GET", "POST"])
def aindex(uid):
    if db.session.query(Category).count() ==0:
        c1 = Category(name ="Fruit")
        db.session.add(c1)
        db.session.commit()
    
    cat = Category.query.first()
    c_id = cat.c_id
    
    if request.method=="GET":
        cat = Category.query.first()
        c_id = cat.c_id
        categories = Category.query.all()
        products = Product.query.filter(Product.c_id == c_id).all()
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name
        cname = cat.name
        return render_template("aindex.html", products=products, categories=categories,  uid=uid, uname=uname, c_id=c_id,cname= cname)
        
    
    if request.method=="POST":
        
        mfd = request.form["mfd"]
        
        mfd = mfd.replace('T',' ')
        mfd = datetime.strptime(mfd, '%Y-%m-%d')
        
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]

        #print(dt,dur,val,notes)

        new_pro = Product(c_id=c_id, name=name, price=price, stock=stock, manufacture_date=mfd)
        db.session.add(new_pro)
        db.session.commit()
        return redirect(url_for("aindex", uid=uid))

@app.route('/category/<int:uid>/<int:c_id>',methods=["GET", "POST"])
def category(uid,c_id):
    if request.method=="GET":
        cat = Category.query.filter(Category.c_id == c_id).one()
        categories = Category.query.all()
        products = Product.query.filter(Product.c_id == c_id).all()
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name
        cname = cat.name
        return render_template("category.html", products=products, categories=categories,  uid=uid, uname=uname, c_id=c_id,cname= cname)
        
    
    if request.method=="POST":
        mfd = request.form["mfd"]
        mfd = mfd.replace('T',' ')
        mfd = datetime.strptime(mfd, '%Y-%m-%d')
        
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]

       

        #print(dt,dur,val,notes)

        new_pro = Product(c_id=c_id, name=name, price=price, stock=stock, manufacture_date=mfd)
        db.session.add(new_pro)
        db.session.commit()
        return redirect(url_for("category", uid=uid, c_id=c_id))







@app.route('/category/create/<int:uid>',methods=["GET", "POST"])
def add_category(uid):
    if request.method=="POST":
        
        
        ccname = request.form["cname"]
        
        #print(dt,dur,val,notes)
        catego  = Category.query.all()
        for c in catego:
            if c.name == ccname:
                flash('Category Already exists', 'error')
                return redirect(url_for("aindex",uid =uid ))

        new_cat = Category(name =ccname)
        db.session.add(new_cat)
        db.session.commit()
        return redirect(url_for("aindex", uid=uid))

    
@app.route('/category/deletecategory/<int:uid>/<int:c_id>',methods=["GET", "POST"])
def deletecategory(uid,c_id):
    if request.method=="GET":
        pro = Product.query.filter(Product.c_id==c_id).all()
        for p in pro:
            db.session.delete(p)
        db.session.commit()
        cat = Category.query.filter(Category.c_id==c_id).one()
        db.session.delete(cat)
        db.session.commit()
        return redirect(url_for("aindex", uid=uid))
    
@app.route('/category/updatecategory/<int:uid>/<int:c_id>',methods=["GET", "POST"])
def updatecategory(uid,c_id):
    if request.method=="GET":
        
        categories = Category.query.all()
        cat_info = Category.query.filter(Category.c_id ==c_id).one()
        cname = cat_info.name
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name
        return render_template("updatecategory.html", uid=uid, categories=categories, uname=uname,  c_id =c_id ,cname = cname)

    if request.method=="POST":
       
        cname= request.form["name"]
        catego  = Category.query.all()
        for c in catego:
            if c.name == cname:
                flash('Category Already exists', 'error')
                return redirect(url_for("updatecategory",uid =uid ,c_id= c_id))
        
        cat = db.session.query(Category).filter_by(c_id=c_id).first()
        cat.name = cname
        
        db.session.commit()

         
        
        
        

        return redirect(url_for("aindex", uid=uid))
    


    


    
@app.route('/category/deleteproduct/<int:uid>/<int:c_id>/<int:p_id>',methods=["GET","POST"])
def delete_product(uid,c_id,p_id):
    if request.method=="GET":
        pro= Product.query.filter(Product.p_id==p_id).one()
        o1 = Order.query.filter(Order.p_id ==p_id).all()
        for orderind in o1:
            db.session.delete(orderind)
        db.session.commit()
        db.session.delete(pro)
        db.session.commit()
        return redirect(url_for("category", uid=uid, c_id=c_id))


@app.route('/category/updateproduct/<int:uid>/<int:c_id>/<int:p_id>',methods=["GET","POST"])
def update_product(uid,c_id,p_id):
    if request.method=="GET":
        product_info = Product.query.filter(Product.p_id == p_id).one()
        categories = Category.query.all()
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name
        return render_template("updatepro.html", uid=uid, categories=categories, uname=uname, p_id=p_id, c_id =c_id,product_info=product_info)

    if request.method=="POST":
        pro = Product.query.filter(Product.p_id == p_id).one()
        name= request.form["name"]
        mfd = request.form["mfd"]
        mfd = mfd.replace('T',' ')
        mfd = datetime.strptime(mfd, '%Y-%m-%d')
        stock = request.form["stock"]
        price = request.form["price"]
        db.session.delete(pro)
        db.session.commit()

         
        
        new_pro = Product(c_id=c_id, name=name, price=price, stock=stock, manufacture_date=mfd)
        db.session.add(new_pro)
        db.session.commit()
        

        return redirect(url_for("category", uid=uid, c_id=c_id))
    
@app.route('/userindex/<int:uid>',methods=["GET", "POST"])
def userindex(uid):
    if request.method=="GET":
        catt =Category.query.all()
        catlist = []
        for c in catt:
            catlist.append((c.c_id,c.name))
        plist = []
     #  pro = Product.order_by(Product.p_id.desc()).all()
        pro = db.session.query(Product).order_by(Product.p_id.desc()).all()
        for p in pro:
            for cat in catlist:
                if p.c_id == cat[0]:
                    if p.stock ==0:
                        sto= "0 out of stock"
                    else:
                        sto= p.stock
                    plist.append((p.name, cat[1],p.price, sto, p.manufacture_date, p.p_id,cat[0]))
        
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name
        return render_template("index.html",cat = catt,plist =plist,uname =uname,uid=uid)
    




    if request.method=="POST":
        catt =Category.query.all()
        catlist = []
        for c in catt:
            catlist.append((c.c_id,c.name))
        plist = []
        if request.form['c_id'] == 'all':
            
            if request.form['price'] =="":
                if request.form.get('stock') :
                    pro = db.session.query(Product).filter(Product.stock>0).all()

                else:
                    pro = Product.query.all()
                
            else:
                price = request.form['price']
                
                if request.form.get('stock') :
                    pro = db.session.query(Product).filter(Product.price<price ,Product.stock>0).all()

                else:
                    pro = db.session.query(Product).filter(Product.price<price).all()
                
        else:
            c_id = request.form['c_id']
            
            if request.form['price'] =="":
                if request.form.get('stock') :
                    pro = db.session.query(Product).filter(Product.stock>0,Product.c_id==c_id).all()

                else:
                    pro = db.session.query(Product).filter_by(c_id=c_id).all()
                
            else:
                price = request.form['price']
                
                if request.form.get('stock') :
                    pro = db.session.query(Product).filter(Product.price<price ,Product.stock>0,Product.c_id==c_id).all()

                else:
                    pro = db.session.query(Product).filter(Product.price<price,Product.c_id==c_id).all()

        for p in pro:
            for cat in catlist:
                if p.c_id == cat[0]:
                    if p.stock ==0:
                        sto= "0 out of stock"
                    else:
                        sto= p.stock
                    plist.append((p.name, cat[1],p.price, sto, p.manufacture_date, p.p_id,cat[0]))
        
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name

        return render_template("index.html",cat = catt,plist =plist,uname =uname,uid=uid)
    
    
@app.route('/viewproduct/<int:uid>/<int:cid>/<int:pid>',methods=["GET", "POST"])
def viewproduct(uid,cid,pid):
    if request.method=="GET":
        
        pro = Product.query.filter(Product.p_id ==pid).one()
        cat = Category.query.filter(Category.c_id == cid).one()
        cname = cat.name
        
        
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name


        return render_template("product.html",uid=uid,uname =uname,pro=pro,cname =cname)
        
    if request.method=="POST":
        quantity = request.form["order_stock"]
        o1 = Order(u_id = uid,p_id= pid,quantity = quantity)
        
        
        
        db.session.add(o1)
        db.session.commit()
        return redirect(url_for("userindex", uid=uid))

@app.route('/viewcart/<int:uid>',methods=["GET", "POST"])
def viewcart(uid):
    if request.method=="GET":
        cuser = User.query.filter(User.u_id == uid).one()
        uname = cuser.name
        orders = Order.query.filter(Order.u_id ==uid).all()
        olist=[]
        sum =0
        for ord in orders:
            
            p = Product.query.filter(Product.p_id ==ord.p_id).one()
            
            olist.append((ord.quantity,p.name,p.price,ord.order_id))
            sum += ord.quantity* p.price
        
        return render_template("cart.html",uid = uid,uname =uname, olist =olist,sum=sum)

    if request.method=="POST":
        pass

@app.route('/deleteorder/<int:uid>/<int:oid>',methods=["GET", "POST"])
def deleteorder(uid,oid):
    if request.method=="GET":
        o1 = Order.query.filter(Order.order_id==oid).one()
        db.session.delete(o1)
        db.session.commit()
    return redirect(url_for("viewcart",uid =uid))

#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
category_req = reqparse.RequestParser()
category_req.add_argument("name",type =str,help='username error')

category_field={
    "c_id":fields.Integer,
    "name": fields.String
    
}

class Catapi(Resource):
    @marshal_with(category_field)
    def get(self , c_id = None):
        if c_id:
            c1 = Category.query.get(c_id)
            if c1:
                return c1
            else:
                return "category not exist"
        
        else:
            c1 = Category.query.all()
            return c1
        
    
    @marshal_with(category_field)
    def post(self,c_id):
        data = category_req.parse_args()
        c1 = Category(c_id = c_id,name =data.name)
        db.session.add(c1)
        db.session.commit()
        return c1
    
    @marshal_with(category_field)
    def put(self,c_id):
        if not c_id:
            abort(400,"id not exist")
        else:
            data = category_req.parse_args()
            cat = Category.query.filter_by(c_id = c_id)
            if cat.first():
                cat.update(data)
                db.session.commit()
            else:
                abort(404,"cat not exist")
            return cat.first()
            
    
    def delete(self,c_id):
        if c_id:
            c1 = Category.query.get(c_id)
            p1 = Product.query.filter(Product.c_id ==c_id).all()
            for p in p1:
                db.session.delete(p)
            db.session.commit()

            if not c1:
                abort(404,"message-caegory not exist")
            db.session.delete(c1)
            db.session.commit()
            return "category deleted ,200"
        else:
            abort(400,"category id required")
api.add_resource(Catapi,'/cate/<int:c_id>','/cate')
#]==================================================================================================================================
#]==================================================================================================================================
#]==================================================================================================================================
#]==================================================================================================================================
#]==================================================================================================================================

#]==================================================================================================================================


product_req = reqparse.RequestParser()
product_req.add_argument("c_id",type =int,help='username error')
product_req.add_argument("name",type =str,help='name error')
product_req.add_argument("price",type =int,help='price error')
product_req.add_argument("stock",type =int,help='stock error')
product_req.add_argument('manufacture_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d') ,help='stock error')


class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')


product_field={
    "p_id":fields.Integer,
    "c_id":fields.Integer,
    "name": fields.String,
    "price":fields.Integer,
    "stock":fields.Integer,
    "manufacture_date": MyDateFormat
    
    
}

class ProductApi(Resource):
    @marshal_with(product_field)
    def get(self , p_id = None):
        if p_id:
            p1 = Product.query.get(p_id)
            if p1:
                return p1
            else:
                return "product not exist"
        
        else:
            p1 = Product.query.all()
            return p1
        
    
    @marshal_with(product_field)
    def post(self,p_id):
        data = product_req.parse_args()
        p1 = Product(p_id = p_id,name =data.name,c_id = data.c_id,price = data.price,stock = data.stock ,manufacture_date = data.manufacture_date)
        db.session.add(p1)
        db.session.commit()
        return p1
    
    @marshal_with(product_field)
    def put(self,p_id):
        if not p_id:
            abort(400,"id not exist")
        else:
            data = product_req.parse_args()
            cat = Product.query.filter_by(p_id = p_id)
            if cat.first():
                cat.update(data)
                db.session.commit()
            else:
                abort(404,"cat not exist")
            return cat.first()
            
    
    def delete(self,p_id):
        if p_id:
            p1 = Product.query.get(p_id)
            o1 = Order.query.filter(Order.p_id ==p_id).all()# order
            for o in o1:
                db.session.delete(o)
            db.session.commit()

            if not p1:
                abort(404,"message product not exist")
            db.session.delete(p1)
            db.session.commit()
            return "product deleted ,200"
        else:
            abort(400,"product id required")
api.add_resource(ProductApi,'/proc/<int:p_id>','/proc')

#]==================================================================================================================================
#]==================================================================================================================================
#]==================================================================================================================================
#]==================================================================================================================================
#]==================================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)