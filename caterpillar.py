from flask import Flask, request, render_template, session, redirect ,url_for, send_from_directory
import random
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/test/'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)
app.secret_key = "IamTheMasterSecret"



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/profile')
def profile():
	return render_template('profile.html')


@app.route('/profile2')
def profile2():
	return render_template('profile2.html')

@app.route('/profile3')
def profile3():
	return render_template('profile3.html')


@app.route('/science')
def science():
	return render_template('science.html')

@app.route('/compare')
def compare():
	return render_template('compare.html')

app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/process_money', methods=["POST"])
def process():
	if 'gold' and 'activities' in session:
		session['gold'] = session['gold']
		if request.form['action'] == 'farm':
			session['farm'] = random.randrange(10,20)
			session['gold'] = session['gold'] + session['farm'] 
			session['activities'].append('Earned '+str(session['farm'])+' from Farm' +str(datetime.now()))
		if request.form['action'] == 'cave':
			session['cave'] = random.randrange(5,10)
			session['gold'] = session['gold'] + session['cave'] 
			session['activities'].append('Earned '+str(session['cave'])+' from Cave' +str(datetime.now()))
		if request.form['action'] == 'house':
			session['house'] = random.randrange(2,5)
			session['gold'] =  session['gold'] + session['house']
			session['activities'].append('Earned '+str(session['house'])+' from House   ' +str(datetime.now()))
		if request.form['action'] == 'casino':
			session['casino'] = random.randrange(0,50)
			session['gold'] =  session['gold'] - session['casino']
			session['activities'].append('Entered a casino and lost '+str(session['casino'])+' OUCH!   ' +str(datetime.now()))
	else:
		session['gold']=0
		session['activities'] = []

	if 'activities' in session:
		session['activities'] = session['activities']

	return redirect('/')




app.run(debug=True)