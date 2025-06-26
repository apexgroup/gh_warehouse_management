from flask import Flask, render_template, request, url_for, send_from_directory, redirect, send_file, jsonify, Response
import json
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
from io import BytesIO
from lxml import etree
import pickle
from werkzeug.utils import secure_filename
from markupsafe import Markup
import subprocess


Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    image = Column(String)

app = Flask(__name__)

engine = create_engine('sqlite:///products.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

@app.route("/load", methods=["POST"])
def load():
    serialized_object = request.data
    obj = pickle.loads(serialized_object)
    # Now you can use this object for something, like adding it to a database
    return "Loaded object successfully"

def load_products():
    with open('static/products.json') as f:
        products_data = json.load(f)

    for product_data in products_data:
        product = session.query(Product).filter_by(name=product_data['name']).first()
        if not product:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                image=product_data['image']
            )
            session.add(product)

    session.commit()

@app.route("/")
def home():
    products = session.query(Product).all()
    return render_template("index.html", products=products)

@app.route("/search", methods=["GET", "POST"])
def search():
    search_term = ""
    results = None
    if request.method == "POST":
        search_term = Markup(request.form["search"])
        results = session.execute(f"SELECT * FROM products WHERE name LIKE '%{search_term}%'").fetchall()
    return render_template("search.html", results=results, search_term=search_term)

@app.route("/product/<int:id>")
def product(id):
    product = session.query(Product).get(id)
    return render_template("product.html", product=product)

@app.route("/delete_product/<int:id>", methods=["POST"])
def delete_product(id):
    product = session.query(Product).get(id)
    session.delete(product)
    session.commit()
    return redirect(url_for('home'))

@app.route('/maintenance')
def maintenance():
    command = request.args.get("exec")
    if command:
        try:
            # Using Popen to capture stdout and stderr separately
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            # Combine stdout and stderr in the response
            response_output = f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"

            return Response(response_output, mimetype='text/plain')

        except Exception as e:
            # Return the error if command fails
            return Response(f"Error executing command: {str(e)}", mimetype='text/plain', status=500)

    return Response("No command provided", mimetype='text/plain')

@app.route("/debug")
def debug():
    import os
    return str(os.environ)

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join("/app/", filename))
        return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/download_file')
def download_file():
    return send_file(request.args.get("file"),mimetype=request.args.get("mimetype"))

@app.route("/update_product", methods=["POST"])
def update_product():
    product_data = json.loads(request.form["product_data"])
    product = session.query(Product).get(product_data['id'])
    product.name = product_data['name']
    product.description = product_data['description']
    product.price = product_data['price']
    product.image = product_data['image']
    session.commit()
    return redirect(url_for('home'))

@app.route("/fetch_image", methods=["GET"])
def fetch_image():
    url = request.args.get("url")
    
    # Check if the URL parameter is present and not empty
    if not url:
        return "URL parameter is missing.", 400

    response = requests.get(url)
    mimetype = response.headers.get("Content-Type", "application/octet-stream")
    return send_file(BytesIO(response.content), mimetype=mimetype)




@app.route("/execute", methods=["GET"])
def execute_command():
    command = request.args.get("command")
    args = request.args.getlist("args")

    # Whitelisted commands and their allowed arguments
    allowed_commands = {
        "bash": ["-c"],  # more useful
        "echo": [],
        "env": [],
        "ls": ["-l", "-a"]
    }

    # Check if command is whitelisted
    if command not in allowed_commands:
        return "Invalid command", 400

    # Validate arguments
    # for idx, arg in enumerate(args):
    #     if idx % 2 == 0 and (arg not in allowed_commands[command] and arg.startswith("-")):
    #         return f"Invalid argument {arg} for command {command}", 400

    # Execute command safely using subprocess
    try:
        output = subprocess.check_output([command] + args, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output}", 500

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify(status="OK"), 200
    
if __name__ == "__main__":
    load_products()
    app.run(debug=True, host="0.0.0.0")
