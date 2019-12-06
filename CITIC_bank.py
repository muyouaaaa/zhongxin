# -*- coding: utf-8 -*-
import os, time
import flask
from flask import Flask, render_template, flash, request, g, session, redirect, url_for, send_from_directory, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Length, Email
from datetime import datetime
import model
import hashlib

app = Flask(__name__)
app.secret_key = 'iamaprogrammer,thisismyproject'

# 配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@106.13.141.103/citic_system'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:950108@127.0.0.1/flask_citic_system'
#
# 跟踪数据库的修改 --> 不建议开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.String(50), nullable=False)
    realname = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(18), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    role = db.Column(db.Integer)
    address = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return "<User:%s,%s,%s,%s,%s,%s,%s,%s>" \
               %(self.username, self.password, self.realname, self.user_id, self.phone,
                self.role, self.create_time, self.update_time)


class Product(db.Model):

    __tablename__ = 'products'

    goods_id = db.Column(db.String(18), primary_key=True, unique=True)
    category_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    productor = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(500))
    price = db.Column(db.Float(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return "<User:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s>" \
               %(self.goods_id, self.category_id, self.name, self.productor, self.detail,
                self.price, self.stock, self.status, self.create_time, self.update_time)



class Employee(db.Model):

    __tablename__ = 'employees'

    employee_id = db.Column(db.String(20), primary_key=True, unique=True)
    employeename = db.Column(db.String(20), nullable=False)
    performance = db.Column(db.Float(20), nullable=False, default=0.0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return "<User:%s,%s,%s,%s,%s,%s,%s>" \
               %(self.employee_id, self.employeename, self.performance,
                self.create_time, self.update_time)



class Order(db.Model):

    __tablename__ = 'orders'

    order_no = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    goods_id = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    employee_id = db.Column(db.String(20), nullable=True)
    payment = db.Column(db.Float(20), nullable=False)
    address = db.Column(db.String(50))
    payment_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return "<User:%s,%s,%s,%s,%s,%s,%s>" \
               %(self.order_no, self.goods_id, self.username, self.payment, self.payment_time,
                self.create_time, self.update_time)


@app.route('/')
def hello_world():
    users = User.query.all()
    pros = Product.query.filter_by(price = 699.0).all()
    orders = Order.query.all()
    return render_template('test1.html', dict_list01=users, dict_list02=pros, dict_list03=orders)
    # return render_template('test1.html', dict_list01=users)

    # response = make_response(jsonify(response=response1))
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'POST'
    # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    # return Response(jsonify())

# 注册
@app.route('/user/register_user', methods=['POST', 'GET'])
def registerUser():
    messages = {}
    data = request.form.to_dict()
    pwd_temp = hashlib.md5(data['password'].encode("utf8"))
    password = pwd_temp.hexdigest()
    user = User.query.filter(User.username == data['username']).first()
    if user:
        messages['status'] = 1
        messages['msg'] = "用户已存在"
    else:
        u = User(username=data['username'], password=password, realname=data['realName'],
                 user_id=data['userId'])

        try:
            db.session.add(u)
            db.session.commit()
            messages['status'] = 0
            messages['msg'] = "注册成功"
            # session
            session['username'] = data['username']
        #
        except:
            # 回滚rollback
            messages['status'] = 2
            messages['msg'] = "网络错误"


    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

# 登录
@app.route('/login', methods=['POST', 'GET'])
def login():
    messages = {}
    data = request.form.to_dict()
    pwd_temp = hashlib.md5(data['password'].encode("utf8"))
    password = pwd_temp.hexdigest()
    if data:
        user = User.query.filter(User.username == data['username']).first()
        if user.password == password:

            messages['status'] = 0
            messages['msg'] = "登录成功"
            # session 缓存数据
            session['username'] = data['username']
            messages['username'] = data['username']
        #     资产信息
            orders = Order.query.filter(User.username == data['username']).all()
            payment = 0
            for order in orders:
                payment += order.payment
            messages['payment'] = payment

        else:
            messages['status'] = 1
            messages['msg'] = "密码错误"

    else:
        messages['status'] = 2
        messages['msg'] = "缺少参数"
    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


# 判断某用户是否处于登录状态
@app.route('/user/islogin/', methods=['POST'])
def isLogin():
    messages = {}

    username = request.form.get('username')

    if username == session.get('username'):
        messages['status'] =  0
        messages['msg'] = '该用户已登录'

    else:
        messages['status'] = 1
        messages['msg'] = '该用户未登录'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


# 支付
@app.route('/product/payProduction', methods=['POST', 'GET'])
def payProduction():
    messages = {}
    data = request.form.to_dict()
    if data:
        username = session['username']

        product = Product.query.filter_by(goods_id=data['goods_id']).first()
        if not product:
            messages['status'] = 3
            messages['msg'] = "商品不存在"
            response = make_response(jsonify(response=messages))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
            return response
        else:
            # 默认数量一个/后期可改为count
            payment = product.price * 1
            stock = product.stock - 1
            if stock < 0:
                messages['status'] = 1
                messages['msg'] = "商品库存不足"
                response = make_response(jsonify(response=messages))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                return response
        order = Order(goods_id=data['goods_id'], username=username, payment=payment, address=data['address'])
        try:
            # 向员工表里更新销售额度
            Employee.query.filter_by(employee_id=data['employee_id']).update({'performance': payment})
            # 对应的商品表中将库存减1。
            Product.query.filter_by(goods_id=data['goods_id']).update({'stock': stock})
            # 向User表添加Address
            User.query.filter_by(username=username).update({'address': data['address']})
            # 向订单表里加入订单
            db.session.add(order)

            db.session.commit()
            messages['status'] = 0
            messages['msg'] = "购买成功"
        except:
            # 回滚rollback(没做)
            messages['status'] = 2
            messages['msg'] = "网络错误"

    else:
        messages['status'] = 2
        messages['msg'] = "缺少参数"
    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


#银行管理员根据goodsId从数据库中删除产品
@app.route('/product/deleteproduction/', methods=['GET','POST'])
def deleteProduction():
    #查询数据库确定该商品是否还存在
    messages = {}
    if request.method == 'GET':
        return render_template('goodsManager.html')
    else:
        goodsId = request.form.get('goods_id')
        goods = Product.query.filter_by(goods_id = goodsId).first()
        if goods:
            print(goods.name)
            try:
                db.session.delete(goods)
                db.session.commit()
                messages['status'] = 0
                messages['msg'] = '删除成功'
            except Exception as e:
                print(e)
                flash('删除货物出错')
                db.session.rollback()
                messages['status'] = 1
                messages['msg'] = '删除失败'
        else:
            # flash('不存在需要删除的货物')
            messages['status'] = 1
            messages['msg'] = '删除失败，不存在需要删除的货物'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response

#银行管理员添加新的货物
@app.route('/product/addproduction/', methods=['GET','POST'])
def addProduction():
    messages = {}

    goods_id = request.form.get('goods_id')
    category_id = request.form.get('category_id')
    name = request.form.get('name')
    productor = request.form.get('productor')
    detail = request.form.get('detail')
    price = request.form.get('price')
    stock = request.form.get('stock')
    tempProdution = Product(goods_id = goods_id, category_id = category_id, name = name,
                  productor = productor, detail = detail, price = price, stock = stock)
    try:
        db.session.add(tempProdution)
        db.session.commit()
        messages['status'] = 0
        messages['msg'] = '添加成功！'
    except Exception as e:
        print(e)
        # flash('添加货物失败')
        db.session.rollback()
        messages['status'] = 1
        messages['msg'] = '添加货物失败！'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


#管理员更新货物信息
@app.route('/product/updateproduction/', methods=['GET','POST'])
def updateProduction():
    messages = {}

    goods_id = request.form.get('goods_id')
    category_id = request.form.get('category_id')
    name = request.form.get('name')
    productor = request.form.get('productor')
    detail = request.form.get('detail')
    price = request.form.get('price')
    stock = request.form.get('stock')

    updatedProduct = Product.query.filter_by(goods_id = goods_id).first()

    if updatedProduct:
        updatedProduct.goods_id = goods_id
        updatedProduct.category_id = category_id
        updatedProduct.name = name
        updatedProduct.productor = productor
        updatedProduct.detail = detail
        updatedProduct.price = price
        updatedProduct.stock = stock

        try:
            db.session.commit()
            messages['status'] = 0
            messages['msg'] = '更新成功'
        except:
            flash('更新失败')
            messages['status'] = 1
            messages['msg'] = '更新失败'

    else:
        flash('goods_id不存在')
        messages['status'] = 1
        messages['msg'] = 'goods_id不存在'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


#查询用户个人资产
@app.route('/user/assets', methods=['POST','GET'])
def userAssets():

    messages = {}
    username = request.form.get('username')

    all_orders = Order.query.filter_by(username = username).all()

    if all_orders:
        assets = 0

        for orderByname in all_orders:
            assets = assets + orderByname.payment
        messages['status'] = 0
        messages['msg'] = '查询成功'
        messages['assets'] = assets
    else:
        flash('查询失败')
        messages['status'] = 1
        messages['msg'] = '查询失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


#金牌客户统计排名
@app.route('/manage/userrank', methods=['GET','POST'])
def userRank():

    messages = {}
    data = []
    dic = {}
    temp = {}

    for item in User.query.all():#想将所有的用户的资产设为0
        temp[item.username] = 0.0

    all_orders = Order.query.all()

    if all_orders:
        for item in all_orders:
            temp[item.username] = temp[item.username] + item.payment

        count = 0
        for item in sorted(temp,key=temp.__getitem__, reverse=True):#按各个用户的资产排序，资产高的在前边
            # print(item, temp[item])
            count += 1
            dic[item] = temp[item]
            if count==5:#输出资产排名前5的用户的资产情况
                break

        for item in dic:
            temp01 = {}
            temp01['username'] = item
            temp01['assets'] = dic[item]
            data.append(temp01)


        messages['status'] = 0
        messages['msg'] = '获取金牌用户排名成功'
        messages['data'] = data

    else:
        messages['status'] = 1
        messages['msg'] = '获取金牌用户失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response




# 银行销售统计
@app.route('/manage/salestatistic', methods=['POST', 'GET'])
def saleStatistic():
    messages = {}
    data = []
    orders = db.session.query(Order.goods_id, func.sum(Order.payment), func.count(Order.payment)).group_by(Order.goods_id).order_by(func.sum(Order.payment).desc()).limit(5).all()

    for order in orders:
        temp = {}
        temp['goodsname'] = Product.query.filter_by(goods_id=order[0]).first().name
        temp['totalCount'] = order[2]
        temp['totalPrice'] = order[1]
        data.append(temp)
    messages['status'] = 0
    messages['data'] = data
    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response

#################################################33
# 查询库存大于0的货物清单
@app.route('/product/getAllProductions/', methods=['POST', 'GET'])
def getAllProductions():
    messages = {}
    data = []
    all_orders = Product.query.all()

    if all_orders:
        stock_ = 0
        for every_order in all_orders:
            if every_order.stock > 0:
                stock_ = 1
                temp = {}
                temp['goods_id'] = every_order.goods_id
                temp['category_id'] = every_order.category_id
                temp['name'] = every_order.name
                temp['productor'] = every_order.productor
                temp['detail'] = every_order.detail
                temp['price'] = every_order.price
                temp['stock'] = every_order.stock
                data.append(temp)
        if stock_:
            messages['status'] = 0
            messages['msg'] = '查询成功'
            messages['data'] = data
        else:
            messages['status'] = 0
            messages['msg'] = '查询成功,但库存为0，返回data数据为空'
            messages['data'] = data
    else:
        messages['status'] = 1
        messages['msg'] = '查询失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


# 银行查看所有的商品清单
@app.route('/manage/getAllProductions/', methods=['POST', 'GET'])
def manageGetAllProductions():
    messages = {}
    data = []
    all_orders = Product.query.all()

    if all_orders:
        for every_order in all_orders:
            temp = {}
            temp['goods_id'] = every_order.goods_id
            temp['category_id'] = every_order.category_id
            temp['name'] = every_order.name
            temp['productor'] = every_order.productor
            temp['detail'] = every_order.detail
            temp['price'] = every_order.price
            temp['stock'] = every_order.stock
            data.append(temp)

        if len(data) > 0:
            messages['status'] = 0
            messages['msg'] = '查询成功'
            messages['data'] = data
        else:
            messages['status'] = 1
            messages['msg'] = '查询到商品,但返回商品记录失败'
            messages['data'] = data
    else:
        messages['status'] = 1
        messages['msg'] = '未查询到商品，查询失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response

#查看某商品的详情
@app.route('/product/detail/', methods=['GET','POST'])
def getProductionDetail():
    messages = {}

    goodsid = request.form.get('goods_id')
    username = request.form.get('username')
    the_good = Product.query.filter_by(goods_id = goodsid).first()

    if the_good:
        temp = {}
        temp['goods_id'] = the_good.goods_id
        temp['category_id'] = the_good.category_id
        temp['name'] = the_good.name
        temp['productor'] = the_good.productor
        temp['detail'] = the_good.detail
        temp['price'] = the_good.price
        temp['stock'] = the_good.stock
        temp['address'] = User.query.filter_by(username = username).first().address

        messages['status'] = 0
        messages['msg'] = '查询该商品的详情成功'
        messages['data'] = temp

    else:
        messages['status'] = 1
        messages['msg'] = '未查询到商品，查询失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response



#查看某用户的所有订单
@app.route('/order/getuserorders/', methods=['GET', 'POST'])     #方法名
def getUserOrders():  #方法

    messages = {}
    data = []

    username = request.form.get('username')

    orders = Order.query.filter_by(username = username).all()

    for item in orders:
        temp = {}
        temp['order_no'] = item.order_no
        temp['goods_id'] = item.goods_id
        temp['name'] = Product.query.filter_by(goods_id = item.goods_id).first().name
        temp['address'] = item.address
        temp['price'] = item.payment
        temp['payment_time'] = item.payment_time

        data.append(temp)

    if len(data) > 0:
        messages['status'] = 0
        messages['msg'] = '查询该用户的订单成功'
        messages['data'] = data
    else:
        messages['status'] = 1
        messages['msg'] = '查询该用户的订单失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


#银行查看所有用户的订单
@app.route('/manage/getallorders/', methods=['GET', 'POST'])     #方法名
def getAllOrders():  #方法

    messages = {}
    data = []

    orders = Order.query.all()

    for item in orders:
        temp = {}
        temp['order_no'] = item.order_no
        temp['goods_id'] = item.goods_id
        temp['name'] = Product.query.filter_by(goods_id = item.goods_id).first().name
        temp['address'] = item.address
        temp['price'] = item.payment
        temp['payment_time'] = item.payment_time

        data.append(temp)

    if len(data) > 0:
        messages['status'] = 0
        messages['msg'] = '查询所有用户的订单成功'
        messages['data'] = data
    else:
        messages['status'] = 1
        messages['msg'] = '查询所有用户的订单失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response

#员工业绩
@app.route('/manage/employeerank/', methods=['GET','POST'])
def employeeRank():
    messages = {}
    data = []
    dic = {}
    temp = {}

    all_employees = Employee.query.all()

    if all_employees:
        for item in all_employees:
            temp[item.employeename] = item.performance

        count = 0
        for item in sorted(temp, key=temp.__getitem__, reverse=True):  # 按各个用户的资产排序，资产高的在前边
            # print(item, temp[item])
            count += 1
            dic[item] = temp[item]
            if count == 5:  # 输出资产排名前5的用户的资产情况
                break

        for item in dic:
            temp01 = {}
            temp01['employeename'] = item
            temp01['performance'] = dic[item]
            data.append(temp01)

        messages['status'] = 0
        messages['msg'] = '获取员工业绩排名成功'
        messages['data'] = data

    else:
        messages['status'] = 1
        messages['msg'] = '获取员工业绩失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response

#获取地址
@app.route('/queryUserAddress', methods=['GET', 'POST'])
def queryUserAddress():
    messages = {}
    data = {}
    username = request.form.get('username')

    tempuser = User.query.filter_by(username = username).first()

    if tempuser:
        messages['status'] = 0
        messages['msg'] = '查询成功'
        data['address'] = tempuser.address;
        data['phone'] = tempuser.username
        data['realname'] = tempuser.realname
        messages['data'] = data
    else:
        messages['status'] = 1
        messages['msg'] = '查询失败'

    response = make_response(jsonify(response=messages))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


if __name__ == '__main__':
    # db.drop_all()
    #
    # db.create_all()
    #
    # us0 = User(username='20120000', password='111111',
    #            realname='Malo', user_id='123456789012345678', phone='18381880000', role='1', address='四川成都武侯区1003号')
    #
    # us1 = User(username='20120001', password='111111',
    #            realname='Mick', user_id='123456789012345678', phone='18381880010', role='1', address='北京市朝阳区3号')
    #
    # us2 = User(username='20120010', password='111111',
    #            realname='Malo', user_id='123456789012345678', phone='18300000000', role='1')
    #
    #
    # db.session.add_all([us0, us1, us2])
    # db.session.commit()
    #
    #
    # pr0 = Product(goods_id='12345678', category_id='1', name='MMMMM',
    #               productor='DDD', detail='很好看的小兔子，兔年快乐', price='699.0', stock='10')
    #
    # pr1 = Product(goods_id='00345678', category_id='0', name='小兔子戒指',
    #               productor='DDD', detail='很好看的小兔子戒指', price='399.9', stock='20')
    #
    # pr2 = Product(goods_id='10345678', category_id='3', name='金砖',
    #               productor='Dkk', detail='1KG金砖', price='6699.0', stock='5')
    #
    # pr3 = Product(goods_id='34567890', category_id='1', name='小狗吊坠',
    #               productor='DW', detail='狗年快乐', price='699.0', stock='10')
    #
    # db.session.add_all([pr0, pr1, pr2, pr3])
    # db.session.commit()
    #
    # pro_1 = Product(goods_id='1', category_id='100001', name='罗小黑黄金吊坠',
    #                 productor='北京保利艺术有限公司', detail='罗小黑黄金珠宝长命锁金锁足金黄金吊坠精品，经典福锁造型，福气福字，大气装饰，寓意福气满满，古代金锁意义在于锁命，祈愿无灾无祸，平安长大',
    #                 price='1234.22', stock='200')
    # pro_2 = Product(goods_id='2', category_id='100001', name='黄金小鹿吊坠',
    #                 productor='北京汉今国际文化发展有限公司', detail='Q萌小鹿鲁道夫转运珠足金黄金吊坠精品，一“鹿”有你，幸福寓意，快陪伴，陪伴你看春暖花开，陪你度过美好时光',
    #                 price='1345.22', stock='200')
    # pro_3 = Product(goods_id='3', category_id='100002', name='珠宝手镯',
    #                 productor='北京保利艺术有限公司', detail='珠宝实心黄金手镯光面推拉大人足金手镯，将精致华丽的艺术，融入东方式的低调，让个人魅力脱颖而出，整体呈现哑光质感，厚重而不失内涵',
    #                 price='2345.65', stock='123')
    # pro_4 = Product(goods_id='4', category_id='100002', name='999足金手镯',
    #                 productor='北京汉今国际文化发展有限公司', detail='简约大方光身足金黄金手镯，寓意是遇见你是命运的安排，环环相扣，真情深爱交集，爱情与甜蜜，前世今生永不分离，是时髦精的最爱。',
    #                 price='3232.12', stock='324')
    # pro_5 = Product(goods_id='5', category_id='100003', name='黄金耳钉',
    #                 productor='北京汉今国际文化发展有限公司', detail='珠宝首饰蜂房花朵足金黄金耳钉，简约时尚，经典百搭。一款饰品，展现与众不同，百般风情，独特气质的你',
    #                 price='3543.23', stock='425')
    # pro_6 = Product(goods_id='6', category_id='100003', name='黄金耳环',
    #                 productor='北京汉今国际文化发展有限公司', detail='黄金耳饰吉祥孔雀女款足金耳环金耳环新款珠宝首饰，该款耳环设计了舒适的耳圈，吉祥灵雀的华丽造型，优雅魅力，寓意吉祥',
    #                 price='432.22', stock='344')
    # pro_7 = Product(goods_id='7', category_id='100004', name='镂空绣球项链',
    #                 productor='北京汉今国际文化发展有限公司', detail='黄金古法吊坠新款足金镂空绣球项链，该款项链由古法金工艺打造，醇厚哑光的表面质感，耐脏耐看，不易划损。镂空造型，花丝工艺打造，花丝根根分明、层层叠叠，呈现传统而繁复的美感。',
    #                 price='825.22', stock='525')
    # pro_8 = Product(goods_id='8', category_id='100004', name='罗小黑黄金吊坠',
    #                 productor='北京汉今国际文化发展有限公司', detail='黄金素链正品999足金新款锁骨链，做工精细，烧蓝坠子增加了灵动感。首饰盒也古典雅致，真正的无可挑剔，精雕细琢。',
    #                 price='782.21', stock='325')
    #
    # db.session.add_all([pro_1, pro_2, pro_3, pro_4, pro_5, pro_6, pro_7, pro_8])
    # db.session.commit()
    #
    # employee_id = db.Column(db.Integer, primary_key=True, unique=True)
    # employeename = db.Column(db.String(20), nullable=False)
    # performance = db.Column(db.Float(), nullable=False)
    #
    # emp0 = Employee(employee_id='100001', employeename='张三', performance='699.0')
    # emp1 = Employee(employee_id='100002', employeename='李四', performance='0.0')
    # emp2 = Employee(employee_id='100003', employeename='王五', performance='399.0')
    # emp3 = Employee(employee_id='100004', employeename='赵六', performance='0.0')
    #
    # db.session.add_all([emp0, emp1, emp2, emp3])
    # db.session.commit()
    #
    #
    # or0 = Order(order_no = '1912030001', goods_id = '12345678', username='20120000', employee_id='00001', payment='699.0')
    #
    # or1 = Order(order_no = '1912030002', goods_id = '10345678', username='20120001', employee_id='', payment='6699.0')
    #
    # or2 = Order(order_no = '1912030003', goods_id = '00345678', username='20120000', employee_id='00003', payment='399.9')
    #
    # db.session.add_all([or0, or1, or2])
    # db.session.commit()

    # print(flask.__version__)




    app.run()
