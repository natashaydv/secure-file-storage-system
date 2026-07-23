from flask import Flask, request, redirect, send_file, render_template
import boto3

app = Flask(__name__)

BUCKET_NAME = "secure-file-storage-033216807797-ap-south-1-an"

s3 = boto3.client("s3")


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        file = request.files["file"]

        if file.filename != "":
            s3.upload_fileobj(file, BUCKET_NAME, file.filename)

        return redirect("/")

    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)

    files = []

    if "Contents" in objects:
        for obj in objects["Contents"]:
            files.append(obj["Key"])

    return render_template(
        "index.html",
        files=files,
        file_count=len(files)
    )
@app.route("/download/<filename>")
def download(filename):

    file_path = "/tmp/" + filename

    s3.download_file(BUCKET_NAME, filename, file_path)

    return send_file(file_path, as_attachment=True)


@app.route("/delete/<filename>")
def delete(filename):

    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=filename
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
