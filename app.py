import datetime
import logging
from flask import Flask, render_template, request
from book_service import get_book_table, del_book, add_book_by_bib_or_url, update_all_copies, update_current_copies, get_last_update, get_list_of_libraries, get_copies
from hkpl_service import get_book_list

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

libraries = get_list_of_libraries()
# add attr "fav" to lib1, lib2
fav_libraries = ['Quarry Bay', 'Sham Shui Po', 'Po On Road']
for lib in libraries:
    if lib['englishName'] in fav_libraries:
        lib['fav'] = 1


def get_last_update_text(lastupdate):
    return f'Last Update: {lastupdate}'


# Custom filter to sort libraries by multiple attributes
@app.template_filter('sort_by')
def sort_by(collection, *attributes):
    # Sort the collection based on the provided attributes
    return sorted(collection,
                  key=lambda x: tuple(x[attr] if attr in x else 9999
                                      for attr in attributes))


@app.route("/", methods=['POST', 'GET'])
def home():
    try:
        lastupdate = get_last_update()
        # form_type = request.form.get('form_type')
        if request.method == 'GET':
            return render_template('index.html',
                                   lastupdate=get_last_update_text(lastupdate),
                                   libraries=libraries)
        if request.method == 'POST':
            print(request.form)
            if 'bibOrUrl' in request.form:
                bib_or_url = request.form['bibOrUrl']
                message = add_book_by_bib_or_url(bib_or_url)
                return render_template(
                    'index.html',
                    save_msg=f'{message}',
                    lastupdate=get_last_update_text(lastupdate),
                    libraries=libraries)
            elif 'btnLookup' in request.form: # 'library' in request.form:
                # if request.form['library'] == '':
                #     return render_template('index.html', lastupdate=get_last_update_text(lastupdate), error_msg = 'please select a library', libraries=libraries)
                library = request.form['library']
                libraries_to_remove = request.form.getlist('libraryToRemove')
                print(library)
                copies = get_copies(library, libraries_to_remove)
                print('finish getCopies')
                # print(copies)
                library_msg = f'{len(copies)} copies available in {library} Library'
                # print(libraries_to_remove)
                return render_template(
                    'index.html',
                    copies=copies,
                    library_msg=library_msg,
                    lastupdate=get_last_update_text(lastupdate),
                    libraries=libraries,
                    selection=library,
                    libraries_to_remove=libraries_to_remove)
            # elif form_type == 'library_removal':
            #     # get list of cheeckbox that are checked
            #     libraries_to_remove = request.form.getlist('libraryToRemove')
            #     print(libraries_to_remove)
            #     print(request.form)
            #     return render_template('index.html', libraries_to_remove=libraries_to_remove, libraries=libraries, selection=library)
            elif 'btnUpdateAll' in request.form or 'btnUpdateCurrent' in request.form:  #update
                if 'btnUpdateAll' in request.form:
                    # books_failed_to_update = update_all_copies()
                    pass
                else: # btnUpdateCurrent
                    library = request.form['library']
                    libraries_to_remove = request.form.getlist('libraryToRemove')
                    books_failed_to_update = update_current_copies(library, libraries_to_remove)
                books_failed_to_update = []
                
                if not books_failed_to_update:
                    update_msg = f'Update successful at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.'
                else:
                    update_msg = f'The following books: {books_failed_to_update} has failed to update.'
                return render_template('index.html',
                                       update_msg=update_msg,
                                       libraries=libraries)
            else:
                print(request.form)
                return render_template('index.html',
                                       lastupdate=get_last_update_text(lastupdate),
                                       libraries=libraries,
                                       error_msg='An error occurred. Please try again.')
    except Exception as e:
        print(e)
        logging.exception(e)
        return render_template(
            'index.html',
            error_msg='An error occurred. Please try again.',
            libraries=libraries)


@app.route('/search', methods=['GET', 'POST'])
def search_books():
    try:
        context = {'libraries': libraries}

        if request.method == 'POST':
            search_term = request.form.get('search_term')
            if not search_term or search_term.strip() == '':
                return render_template('search.html',
                                       error_msg='Please enter a search term',
                                       libraries=libraries)

            search_results = get_book_list(search_term)
            # if isinstance(results, str):  # Error message from get_book_list
            #     return render_template('search.html',
            #                         error_msg=results,
            #                         search_term=search_term,
            #                         libraries=libraries)

            context['results'] = search_results
            context['search_term'] = search_term
            return render_template('search.html', **context)
        else:  # GET request
            return render_template('search.html', **context)
    except Exception as e:
        print(e)
        logging.exception(e)
        context[
            'error_msg'] = 'An error occurred during search. Please try again.'
        return render_template('search.html', **context)


@app.route("/Saved_Books", methods=['GET', 'POST'])
def saved_books():
    if request.method == 'GET':
        table = get_book_table()
        return render_template('books.html',
                               column_names=table[0],
                               books=table[1])
    if request.method == 'POST':
        book_ids = request.form.getlist('book_ids')
        if book_ids:
            del_book(book_ids)
            msg = f'{book_ids} has been deleted'
        else:
            msg = 'No books selected for deletion'
        table = get_book_table()
        return render_template('books.html',
                               column_names=table[0],
                               books=table[1],
                               msg=msg)


@app.route('/user_guide')
def user_guide():
    return render_template('user_guide.html')


# @app.route("/Delete_Books", methods=['POST'])
# def deleteBook():
