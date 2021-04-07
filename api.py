'''
Author : 
Date : 2021/01/30
Version : v1.0

Ref
1. https://ithelp.ithome.com.tw/articles/10209404
2. https://stackoverflow.com/questions/48107708/how-do-i-load-image-in-python-flask
3. https://medium.com/@charming_rust_oyster_221/flask-%E6%AA%94%E6%A1%88%E4%B8%8A%E5%82%B3%E5%88%B0%E4%BC%BA%E6%9C%8D%E5%99%A8%E7%9A%84%E6%96%B9%E6%B3%95-1-c11097c23137
4. https://blog.csdn.net/qq_25730711/article/details/53643758 [**]
5. https://josh199483.gitbooks.io/flask_tutorial/content/3flaskxia-zai-dang-an.html [**]
6. https://medium.com/@charming_rust_oyster_221/flask-%E6%AA%94%E6%A1%88%E4%B8%8A%E5%82%B3%E5%88%B0%E4%BC%BA%E6%9C%8D%E5%99%A8%E7%9A%84%E6%96%B9%E6%B3%95-1-c11097c23137 [**]
'''

#!/usr/bin/python3

import os, time
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, jsonify
import shutil

app = Flask(__name__)


## Flask Configuration
### Set up the upload path
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False
### Limit upload size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
### Limit upload file type
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG'])
### Others
basedir = os.path.abspath(os.path.dirname(__file__))  # Getting current abs. path

# For a test web page to upload image with form type
@app.route('/')
def upload_test():
    return render_template('Multiple.html')

@app.route("/download/<filename>")
def download(filename):
    dirpath = os.path.join(app.root_path, 'upload')      # build-in function 'send_from_directory()'
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True >> Optional
    # as_attachment = True >> Browser will DOWNLOAD the file
    # as_attachment = False >> Browser will DISPLAY the file

@app.route("/download/all")
def download_all():
    shutil.make_archive("download", "zip", "upload/RAW")
    dirpath = os.path.join(app.root_path)      # build-in function 'send_from_directory()'
    return send_from_directory(dirpath, "download.zip" , as_attachment=True)  # as_attachment=True >> Optional
#    return send_from_directory(basedir, "download.zip" , as_attachment=True)  # as_attachment=True >> Optional
    
    
# Check file type 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#web upload
@app.route('/api/upload/web', methods=['POST'], strict_slashes=False)
def api_upload_web():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'],'ANALYZED')  # Merge dest. to abs. path
    if not os.path.exists(file_dir): # Check if folder is create or not
        os.makedirs(file_dir) # if no target folder then 'mkdir' a new folder with terminal command
        
    ff = request.files.getlist('myfile') # 'myFile' is the object ID from index.html for the upload file
    i=0
    d=0
    a=[]
    picJSON={"errno": 0, "errmsg": "Upload Successful"}
    for f in ff:
        if f and allowed_file(f.filename):  # Check file type
            i=i+1
            fname = f.filename
            ext = fname.rsplit('.', 1)[1]  # Get file extension
            temp_dict = {fname.rsplit('.', 1)[0] : "Successful"} # Put back ai result JSON
            picJSON.update(temp_dict)
            unix_time = int(time.time())+i*0.1
            new_filename = str(unix_time)+'.'+ext   # Modify file name
            f.save(os.path.join(file_dir, fname))  #Save to folder
        else:
            d=d+1
            a.extend(f.filename)
    if d==0:
        return jsonify(picJSON)
    else:
        return jsonify({"errno": 1001, "wrong":{}, "errmsg": "Upload Error"}).format(a)


@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'],'RAW')  # Merge dest. to abs. path
    if not os.path.exists(file_dir): # Check if folder is create or not
        os.makedirs(file_dir) # if no target folder then 'mkdir' a new folder with terminal command
    ff = request.files.getlist('myfile') # 'myFile' is the object ID from index.html for the upload file
    d=0
    a=[]
    picJSON={}
    for f in ff:
        if f and allowed_file(f.filename):  # Check file type
            fname = f.filename
            ext = fname.rsplit('.', 1)[1]  # Get file extension
            temp_dict = {fname.rsplit('.', 1)[0] : "Successful"} # Put back ai result JSON
            picJSON.update(temp_dict)
            new_filename = request.args.get('user')+"_"+request.args.get('name')+"_"+request.args.get('mark')+"_"+request.args.get('time')+'.'+ext
            f.save(os.path.join(file_dir, new_filename))  #Save to folder
        else:
            d=d+1
            a.extend(f.filename)
    if d==0:
#         return jsonify({"errno": 0, "errmsg": "Upload Successful"})
        return jsonify(picJSON)
    else:
        return jsonify({"errno": 0, "wrong":{}, "errmsg": "Upload Error"}).format(a)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
