from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle the image upload."""
    if 'file' not in request.files:
        return 'No file part in the request'
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Save the file to the uploads folder
        return f'File uploaded successfully! File saved at: {file_path}'
    else:
        return 'Invalid file type. Please upload an image.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
