from api.users import users
from api.admin import admin
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
import werkzeug
import qrcode
import PIL
import os
from random import randint



app=Flask(__name__)
app.secret_key='secret'
@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def inject_random():
    return {"random": lambda: randint(1, 10000)}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        name = request.form['name']
        password = request.form['password']
        Users = users()
        details = Users.select_using_name(name)  
        
        if details:
            if password == details[1]:
                session['name'] = name  # Store name in session
                return redirect(url_for('bookings'))
            else:
                return '<h3>Invalid Username or password</h3>'
        else:
            return '<h3>Invalid Username or password</h3>'
    else:
        return render_template('login.html')


@app.route('/signup')
def signup():
    if request.args:
        
        
        name=request.args['name']
        password=request.args['password']
        Users=users()
        res=Users.insert_record(name,password)
        return res
    else:
      return render_template('signup.html')    



@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    name = session.get('name')
    Admin=admin()
    
    if not name:
        return redirect(url_for('login'))

    if request.method == 'POST':
        tables = request.form.getlist('tables') 
        date_booked = request.form.get('date')  
        from_time = request.form.get('time')   
        hours = int(request.form.get('hours'))  
        
        if not tables:
            return f'<h3>{name}, please select at least one table.</h3>'
       
        for tableno in tables:
             Admin.update_table_status(int(tableno),'booked',date_booked,int(from_time),int(from_time)+int(hours))



        # Ensure the images directory exists
        image_dir = "static/images"
        os.makedirs(image_dir, exist_ok=True)
        
        # Booking details
        details = f"""Name: {name}
        Tables booked: {', '.join(tables)}
        Date: {date_booked}
        From: {from_time}
        To: {int(from_time) + int(hours)}"""

        # Generate and save QR code
        image = qrcode.make(details)
        image_path = os.path.join(image_dir, f"{name}.jpg")
        image.save(image_path)

        print(f"QR code saved at: {image_path}")

        
        return render_template('ticket.html',name=name,tables=' '.join(tables),date=date_booked,from_time=from_time,to_time=int(from_time)+int(hours))
    
    Admin=admin()
    
    empty_tables=Admin.select_empty_tables()
    empty_tables=list(map(lambda x: x[0],empty_tables))

    total_tables=Admin.total_no_of_tables()
    return render_template('bookings.html', name=name,empty_tables=empty_tables,total_tables=total_tables)

    

    

@app.route('/admin_dashboard')
def admin_dashboard():
    pass


if __name__=='__main__':
    app.run(debug=True)
