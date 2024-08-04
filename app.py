from flask import Flask, redirect, request, render_template, url_for
from docx import Document
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', method = 'POST')
def handle_upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.docx'):
        file_path =os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        #process the uploaded word document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return '<pre>{}</pre>'.format(text)  # Display the document content
    return 'Invalid file format. Please upload a Word document.'
    
if __name__ == '__main__':
    app.run(debug=True)



