# import libraries
from flask import render_template , request, redirect, url_for
from models import Agent, Customer, db, app, mail
import shutil
import datetime
import pandas as pd
import webbrowser
import pyautogui

# root page
@app.route("/")
def index():
    # agent = Agent(name="test", mobileNo="123", email="test@test", password="test")
    # db.session.add(agent)
    # customer = Customer(name="test", mobileNo="123", collection=123, closingBalance=123, agentID=10001)
    # db.session.add(customer)
    # db.session.commit()
    with open('/var/www/html/collection-service/report.csv', 'w') as f:
        f.write("Name,Account Number,Mobile Number,Collection,Closing Balance,Agent ID\n")
    f.close()
    return redirect(url_for('login'))

# agent login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        agentID = request.form['agentID']
        password = request.form['password']
        if Agent.query.filter_by(id=int(agentID)-10000).first() is not None:
            if password == (Agent.query.filter_by(id=int(agentID)-10000).first()).password and (Agent.query.filter_by(id=int(agentID)-10000).first()).status == 1:
                return redirect(url_for("dashboard", agentID = agentID, name=(Agent.query.filter_by(id=int(agentID)-10000).first()).name))
            else:
                return render_template("login.html", warn="y")
        else:
            return render_template("login.html", warn="y")
    return render_template("login.html", warn='n')

# agent dashboard page
@app.route("/dashboard/<agentID>/<name>", methods=['GET', 'POST'])
def dashboard(agentID, name):
    if request.method=='POST':
        acNo = request.form['acNo']
        collection = request.form['collection']
        if Customer.query.filter_by(id=int(acNo)-10000).first() is None:
            return render_template("dashboard.html", agentID=agentID, name=name, success="n", warn="y")
        else:
            (Customer.query.filter_by(id=int(acNo)-10000).first()).closingBalance += int(collection)
            (Customer.query.filter_by(id=int(acNo)-10000).first()).collection += int(collection)
            db.session.commit()
            # message = "Dear "+str((Customer.query.filter_by(id=int(acNo)-10000).first()).name)+",\n\nYour account has been credited with Rs."+str(collection)+"\n\nYour closing balance is Rs."+str((Customer.query.filter_by(id=int(acNo)-10000).first()).closingBalance)+"\n\nRegard"
            # send message to customer
            with open('report.csv', 'a') as f:
                f.write(str((Customer.query.filter_by(id=int(acNo)-10000).first()).name)+","+str(acNo)+","+str((Customer.query.filter_by(id=int(acNo)-10000).first()).mobileNo)+","+str(collection)+","+str((Customer.query.filter_by(id=int(acNo)-10000).first()).closingBalance)+","+str(agentID)+"\n")
            f.close()
            return render_template("dashboard.html", agentID=agentID, name=name, success="y", warn="n")
    return render_template("dashboard.html", agentID=agentID, name=name, success="n", warn="n")

# admin login page
@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    if request.method=='POST':
        password = request.form['password']
        if password == "admin":
            return redirect(url_for("admin"))
        else:
            return render_template("admin_login.html", warn="y")
    return render_template("admin_login.html", warn='n')

# admin dashboard page
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    name=[i.name for i in Agent.query.all()]
    mobileNo=[i.mobileNo for i in Agent.query.all()]
    agentID=[10000+i.id for i in Agent.query.all()]
    email=[i.email for i in Agent.query.all()]
    password=[i.password for i in Agent.query.all()]
    status=[i.status for i in Agent.query.all()]
    return render_template("admin_dashboard.html", no = Agent.query.count(), success="n", name=name, number=mobileNo, agentID=agentID, email=email, password=password, status=status)

# add agent page
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        name = request.form['name']
        mobileNo = request.form['mobileNo']
        email = request.form['email']
        password = request.form['password']
        if Agent.query.filter_by(email=email).first() is None:
            agent = Agent(name=name, mobileNo=mobileNo, email=email, password=password)
            db.session.add(agent)
            db.session.commit()
            message = "Your account has been created. Your agent ID is " + str(10000+agent.id) + " and password is " + password
            # send message to agent
            webbrowser.open('https://api.whatsapp.com/send?phone=91'+str(mobileNo)+'&text='+message, new=2)
            pyautogui.press('enter')
            
            mail.send_message('User authentication', sender='vrslightmodecoders@gmail.com', recipients=[str(agent.email)], body=message)
            return render_template("add.html", success="y", warn="n")
        return render_template("add.html", success="n", warn="y")
        
    return render_template("add.html", success="n", warn="n")

# add customer page
@app.route("/add_customer/<agentID>", methods=['GET', 'POST'])
def addCustomer(agentID):
    if request.method=='POST':
        name = request.form['name']
        mobileNo = request.form['mobileNo']
        password = request.form['password']
        if Customer.query.filter_by(mobileNo=int(mobileNo)).first() is None and password == (Agent.query.filter_by(id=int(agentID)-10000).first()).password:
            customer = Customer(name=name, mobileNo=mobileNo, agentID=int(agentID))
            db.session.add(customer)
            db.session.commit()
            message = "Your account has been created. Your account number is " + str(10000+customer.id)
            # send message to customer
            webbrowser.open('https://api.whatsapp.com/send?phone=91'+str(mobileNo)+'&text='+message, new=2)
            pyautogui.press('enter')

            return render_template("add_customer.html", success="y", warn="n", nameAgent=(Agent.query.filter_by(id=int(agentID)-10000).first()).name, agentID=agentID)
        return render_template("add_customer.html", success="n", warn="y", nameAgent=(Agent.query.filter_by(id=int(agentID)-10000).first()).name, agentID=agentID)
    return render_template("add_customer.html", success="n", warn="n", nameAgent=(Agent.query.filter_by(id=int(agentID)-10000).first()).name, agentID=agentID)

# agent search page
@app.route("/search/<agentID>", methods=['GET', 'POST'])
def search_agent(agentID):
    if request.method=='POST':
        search = request.form['search']
        # make case insensitive
        if Customer.query.filter_by(id=int(search)-10000).first() is not None or Customer.query.filter_by(name=search).first() is not None or Customer.query.filter_by(mobileNo=int(search)).first() is not None:
            if search.isnumeric():
                acNo = int(search)
            elif search.isalpha():
                acNo = 10000+(Customer.query.filter_by(name=search).first()).id
            else:
                acNo = 10000+(Customer.query.filter_by(mobileNo=int(search)).first()).id
            return render_template("history.html", agentID=agentID, nameAgent=(Agent.query.filter_by(id=int(agentID)-10000).first()).name, no=1, name=(Customer.query.filter_by(id=int(search)-10000).first()).name , acNo=acNo, number=(Customer.query.filter_by(id=int(search)-10000).first()).mobileNo,  collection=(Customer.query.filter_by(id=int(search)-10000).first()).collection, closingBalance=(Customer.query.filter_by(id=int(search)-10000).first()).closingBalance)
    return render_template("search.html", agentID=agentID)

# admin search page
@app.route("/admin/search", methods=['GET', 'POST'])
def search_admin():
    if request.method=='POST':
        search = request.form['search']
        # make case insensitive
        if Agent.query.filter_by(id=int(search)-10000).first() is not None or Agent.query.filter_by(name=search).first() is not None or Agent.query.filter_by(email=search).first() is not None:
            if search.isnumeric():
                agentID = int(search)
            elif search.isalpha():
                agentID = 10000+(Agent.query.filter_by(name=search).first()).id
            else:
                agentID = 10000+(Agent.query.filter_by(email=search).first()).id
            return redirect(url_for("view", agentID=agentID))
        return redirect(url_for("view", agentID=agentID))
    name=[i.name for i in Agent.query.all()]
    mobileNo=[i.mobileNo for i in Agent.query.all()]
    agentID=[10000+i.id for i in Agent.query.all()]
    email=[i.email for i in Agent.query.all()]
    password=[i.password for i in Agent.query.all()]
    return render_template("admin_dashboard.html", no = Agent.query.count(), success="n", name=name, number=mobileNo, agentID=agentID, email=email, password=password)

# view agent page
@app.route("/view/<agentID>", methods=['GET', 'POST'])
def view(agentID):
    customers = Customer.query.filter_by(agentID=agentID).all()
    name=(Agent.query.filter_by(id=int(agentID)-10000).first()).name
    email=(Agent.query.filter_by(id=int(agentID)-10000).first()).email
    password=(Agent.query.filter_by(id=int(agentID)-10000).first()).password
    mobileNo=(Agent.query.filter_by(id=int(agentID)-10000).first()).mobileNo
    status=(Agent.query.filter_by(id=int(agentID)-10000).first()).status

    cname=[i.name for i in customers]
    acNo=[10000+i.id for i in customers]
    cmobileNo=[i.mobileNo for i in customers]
    collection=[i.collection for i in customers]
    closingBalance=[i.closingBalance for i in customers]

    return render_template("view.html", agentID=agentID, status=status, name=name, email=email, password=password, number=mobileNo, no=len(cname), cname=cname, acNo=acNo, cnumber=cmobileNo, collection=collection, closingBalance=closingBalance)

# admin action page
@app.route("/admin_action", methods=['GET', 'POST'])
def admin_action():
    if request.method=='POST':
        # export
        if "Export" in request.form.getlist('option'):
            shutil.copy('/var/www/html/collection-service/report.csv', '/var/www/html/collection-service/Reports/report-{}.csv'.format(str(datetime.datetime.now())[:10]))
            with open('/var/www/html/collection-service/report.csv', 'w') as f:
                f.write("Name,Account Number,Mobile Number,Collection,Closing Balance,Agent ID\n")
            f.close()
            for i in Customer.query.all():
                i.collection = 0
            db.session.commit()

        # import agent
        if "Add Agents" in request.form.getlist('option'):
            df = pd.read_excel("~/Downloads/agent.xlsx")
            for i in range(1, len(df)):
                agent = Agent(name=df['Name'][i], email=df['Email'][i], password=df['Password'][i], mobileNo=df['Mobile Number'][i], status=df['Status'][i])
                db.session.add(agent)
                db.session.commit()
                message = "Your account has been created. Your agent ID is " + str(10000+agent.id) + " and password is " + agent.password
                # send message to agent
                webbrowser.open('https://api.whatsapp.com/send?phone=91'+str(agent.mobileNo)+'&text='+message, new=2)
                pyautogui.press('enter')

                mail.send_message('User authentication', sender='vrslightmodecoders@gmail.com', recipients=[str(agent.email)], body=message)
            del df

        # import customer
        if "Add Customers" in request.form.getlist('option'):
            df = pd.read_excel("~/Downloads/customer.xlsx")
            for i in range(1, len(df)):
                customer = Customer(name=df['Name'][i], mobileNo=df['Mobile Number'][i], agentID=df['Agent ID'][i])
                db.session.add(customer)
                db.session.commit()
                message = "Your account has been created. Your account number is " + str(10000+customer.id)
                # send message to customer
                webbrowser.open('https://api.whatsapp.com/send?phone=91'+str(customer.mobileNo)+'&text='+message, new=2)
                pyautogui.press('enter')
                
            del df
        return render_template("admin_action.html", success="y")
    return render_template("admin_action.html", success="n")

# agent history page
@app.route("/history/<agentID>", methods=['GET', 'POST'])
def history(agentID):
    customers = Customer.query.filter_by(agentID=agentID).all()
    name = [i.name for i in customers]
    acNo = [10000+i.id for i in customers]
    mobileNo = [i.mobileNo for i in customers]
    collection = [i.collection for i in customers]
    closingBalance = [i.closingBalance for i in customers]
    return render_template("history.html", agentID=agentID, nameAgent=(Agent.query.filter_by(id=int(agentID)-10000).first()).name, no=Customer.query.filter_by(agentID=agentID).count(), name=name, acNo=acNo, number=mobileNo,  collection=collection, closingBalance=closingBalance)

# admin mail page
@app.route("/admin/message", methods=['GET', 'POST'])
def message():
    if request.method=='POST':
        message = request.form['body']
        if request.form.get('toall') == "a":
            emails = [i.email for i in Agent.query.all()]
        else:
            temp = (request.form['to']).split(",")
            emails = [i.email for i in Agent.query.filter(Agent.name.in_(temp)).all()]
        print(message)
        mail.send_message('User authentication', sender='vrslightmodecoders@gmail.com', recipients=emails, body=message)
        return render_template("admin_mail.html", success="y")
    return render_template("admin_mail.html", success="n")

# delete agent funtion
@app.route("/delAgent/<agentID>", methods=['GET', 'POST'])
def delAgent(agentID):
    Agent.query.filter_by(id=int(agentID)-10000).delete()
    db.session.commit()
    name=[i.name for i in Agent.query.all()]
    mobileNo=[i.mobileNo for i in Agent.query.all()]
    agentID=[10000+i.id for i in Agent.query.all()]
    email=[i.email for i in Agent.query.all()]
    password=[i.password for i in Agent.query.all()]
    return render_template("admin_dashboard.html", no = Agent.query.count(), success="y", name=name,number=mobileNo, agentID=agentID, email=email, password=password)

# block agent function
@app.route("/blockAgent/<agentID>", methods=['GET', 'POST'])
def blockAgent(agentID):
    Agent.query.filter_by(id=int(agentID)-10000).update(dict(status=1-int((Agent.query.filter_by(id=int(agentID)-10000).first()).status)))
    db.session.commit()
    return redirect(url_for("view", agentID=agentID))

# change password function
@app.route("/chpass/<agentID>", methods=['GET', 'POST'])
def chpass(agentID):
    if request.method=='POST':
        password = request.form['new']
        Agent.query.filter_by(id=int(agentID)-10000).update(dict(password=password))
        db.session.commit()
        return redirect(url_for("view", agentID=agentID))
    return redirect(url_for("view", agentID=agentID))
    
# default run
if __name__== "__main__":
  app.run(debug=True)