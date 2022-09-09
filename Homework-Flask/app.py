import sqlite3, os
from flask import Flask, render_template, request, url_for, flash, redirect

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        zertifizierung = request.form['zertifizierung']

        if not zertifizierung:
            flash('Zertifizierung eingeben!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO cloudzertifizierungen (zertifizierung) VALUES (?)',
                         (zertifizierung,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    else:        
        conn = get_db_connection()
        cloudzertifizierungen = conn.execute('SELECT * FROM cloudzertifizierungen').fetchall()
        conn.close()
    return render_template('index.html', cloudzertifizierungen=cloudzertifizierungen)

    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
    