from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        bib = request.form
        print(bib)
        return bib
