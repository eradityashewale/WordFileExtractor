from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from docx import Document
from docx.oxml.ns import qn
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'custom_upload_folder'
app.config['IMAGES_FOLDER'] = 'custom_upload_folder/images'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['IMAGES_FOLDER']):
    os.makedirs(app.config['IMAGES_FOLDER'])

def extract_images(doc, folder):
    images = []
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            img = rel.target_part
            img_filename = os.path.join(folder, rel.target_part.partname.split('/')[-1])
            with open(img_filename, 'wb') as img_file:
                img_file.write(img.blob)
            images.append(img_filename)
    return images

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.docx'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Process the uploaded Word document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        
        # Extract and save images
        images = extract_images(doc, app.config['IMAGES_FOLDER'])
        
        # Generate HTML to display text and images
        images_html = ''.join([f'<img src="{url_for("uploaded_file", filename=os.path.basename(img))}" />' for img in images])
        return f'<pre>{text}</pre><br>{images_html}'
    
    return 'Invalid file format. Please upload a Word document.'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
