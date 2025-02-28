from flask import Flask, request, render_template
from google.cloud import storage
import os

# Initialize Flask app
app = Flask(__name__)

# Set Google Cloud credentials and bucket name
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/key.json"
BUCKET_NAME = "wildlens_upload"

def upload_to_gcloud(file, filename):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client.from_service_account_json("/etc/secrets/key.json")
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"


@app.route("/", methods=["GET", "POST"])
def upload_images():
    if request.method == "POST":
        if "images" not in request.files:
            return "No file part", 400

        files = request.files.getlist("images")
        if not files:
            return "No files selected", 400

        uploaded_files = []
        for file in files:
            if file.filename:
                public_url = upload_to_gcloud(file, file.filename)
                uploaded_files.append(public_url)

        return f"Files uploaded successfully: <br>" + "<br>".join(
            [f"<a href='{url}'>{url}</a>" for url in uploaded_files]
        )

    return render_template("templates/index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
