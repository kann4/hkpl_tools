from flask import Flask, render_template, request
from inserting_data_to_db import insertIntoTables, getCopies, updateCopies, lastUpdate, getBookTable, listOfLibraries, delBook
import datetime
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

libraries = listOfLibraries()

@app.route("/", methods=['POST', 'GET'])
def home():
    try:
        lastupdate = lastUpdate()
        if request.method == 'GET':        
            return render_template('index.html', lastupdate=f'Last Update: {lastupdate}', libraries=libraries)
        if request.method == 'POST':
            if 'bib' in request.form:
                bib = request.form['bib']
                message = insertIntoTables(bib)
                return render_template('index.html',save_msg=f'{message}', lastupdate=f'Last Update: {lastupdate}', libraries=libraries)
            elif 'library' in request.form: 
                # if request.form['library'] == '':
                #     return render_template('index.html', lastupdate=f'lastupdate: {lastupdate}', error_msg = 'please select a library', libraries=libraries)
                library = request.form['library']
                print(library)
                copies = getCopies(library)
                print('finish getCopies')
                # print(copies)
                library_msg = f'{len(copies)} copies available in {library} Library'
                return render_template('index.html', copies=copies, library_msg=library_msg, lastupdate=f'Last Update: {lastupdate}', libraries=libraries, selection=library)
            else:    #update
                books_failed_to_update = updateCopies()
                if books_failed_to_update == []:
                    update_msg = f'Update successful at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.'
                else:
                    update_msg = f'The following books: {books_failed_to_update} has failed to update.'
                return render_template('index.html', update_msg = update_msg, libraries=libraries)
    except Exception as e:
        print(e)
        return render_template('index.html', error_msg='An error occurred. Please try again.', libraries=libraries)

@app.route("/Saved_Books", methods=['GET','POST'])
def savedBooks():

    if request.method == 'GET':
        table = getBookTable()
        return render_template('books.html', column_names=table[0], books=table[1])
    if request.method == 'POST' and 'book_ids' in request.form:
        book_ids = request.form.getlist('book_ids')
        delBook(book_ids)
        table = getBookTable()
        return render_template('books.html', column_names=table[0], books=table[1], msg=f'{book_ids} has been deleted')
# @app.route("/Delete_Books", methods=['POST'])
# def deleteBook():

    
