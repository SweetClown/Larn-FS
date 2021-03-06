from flask import *
from sqlalchemy.orm import sessionmaker
from models import *
import sqlite3 as Db
import os

eng = create_engine('sqlite:///management/database/database.db', echo = True)
app = Flask(__name__, static_folder = 'static')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = str(request.form['username'])
        passwd = str(request.form['password'])

        sess = sessionmaker (bind=eng)
        inputData = sess()
        Qu = inputData.query(User).filter(User.user.in_([uname]), User.passwd.in_([passwd]))
        res = Qu.first()
        if res:

            db = Db.connect('management/database/database.db')
            db.row_factory = Db.Row

            ex = db.cursor()
            ex.execute('select * from post')

            data = ex.fetchall()

            session['logged_in']=True
            flash("hello admin !!")
            return render_template('admin.html', data=data)
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/')
def index():
   con = Db.connect("management/database/database.db")
   con.row_factory = Db.Row
   
   cur = con.cursor()
   cur.execute("select * from post")
   
   rows = cur.fetchall();
   return render_template("index.html",rows = rows)

@app.route('/post', methods = ['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = str(request.form['title'])
        cont = str(request.form['content'])
        date = request.form['pdate']
                
        db = Db.connect('management/database/database.db')
        db.row_factory = Db.Row
        
        if title != '' and cont != '' and date != '':

            ex = db.cursor()
            ex.execute('INSERT INTO post(title, content, p_date) VALUES (?, ?, ?)', (title, cont, date))
            db.commit()
            db.close()
            flash("success add post")
            return redirect(url_for('index'))

        else:

            error = "one form is empty"
        return render_template('post.html', error=error)
    return render_template('post.html')

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(port = 80, host = '0.0.0.0', debug = True)
