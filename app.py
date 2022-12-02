import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.secret_key = 'SUPERSEKRETKEY'

def db_get_conn():
    db_connect = sqlite3.connect('database.db')
    db_connect.row_factory = sqlite3.Row
    return db_connect

def get_entry(entry_id):
    db_connect = db_get_conn()
    blog_entry = db_connect.execute('SELECT * FROM entries WHERE id = ?',
                        (entry_id,)).fetchone()
    db_connect.close()
    if blog_entry is None:
        abort(404)
    return blog_entry

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/display/')
def display():
    db_connect = db_get_conn()
    display_entries = db_connect.execute('SELECT * FROM entries').fetchall()
    db_connect.close()
    return render_template('display.html', posts = display_entries)


@app.route('/post_entry/', methods=('GET', 'POST'))
def post_entry():
    if request.method == 'POST':
        entry_title = request.form['title']
        content = request.form['content']
        feeling_rating = request.form['feeling_rating']
        greatful = request.form['greatful']

        if not entry_title:
            flash('A Title is Needed!')
        elif not content:
            flash('An Entry is Needed!')
        elif not feeling_rating:
            flash('A Rating is Needed!')
        elif not greatful:
            flash('Please Enter What You Are Greatful For!')
        else:
            db_connect = db_get_conn()
            db_connect.execute('INSERT INTO entries (entry_title, content, feeling_rating, greatful) VALUES (?, ?, ?, ?)',
                    (entry_title, content, feeling_rating, greatful))
            db_connect.commit()
            db_connect.close()
            return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/<int:id>/edit_entry/', methods=('GET', 'POST'))
def edit_entry(id):
    blog_entry = get_entry(id)

    if request.method == 'POST':
        entry_title = request.form['title']
        content = request.form['content']
        feeling_rating = request.form['feeling_rating']
        greatful = request.form['greatful']

        if not entry_title:
            flash('A Title is Needed!')
        elif not content:
            flash('An Entry is Needed!')
        elif not feeling_rating:
            flash('A Rating is Needed!')
        elif not greatful:
            flash('Please Enter What You Are Greatful For!')
        else:
            db_connect = db_get_conn()
            db_connect.execute('UPDATE entries SET entry_title = ?, content = ? , feeling_rating = ?, greatful = ?'' WHERE id = ?',
                    (entry_title, content, feeling_rating, greatful, id))
            db_connect.commit()
            db_connect.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post =blog_entry)

@app.route('/<int:id>/delete_entry/', methods=('POST',))

def delete_entry(id):
    blog_entry = get_entry(id)
    db_connect = db_get_conn()
    db_connect.execute('DELETE FROM entries WHERE id = ?', (id,))
    db_connect.commit()
    db_connect.close()
    flash('"{}" was successfully deleted!'.format(blog_entry['entry_title']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
