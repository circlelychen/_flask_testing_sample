
from flask import current_app
from flask import abort
from flask import jsonify
from flask import request
from flask import Blueprint
from werkzeug import secure_filename

from models import db
from models.FileInfo import FileInfo
from .utils import allowed_file

restful = Blueprint('restful', __name__)

@restful.route('/files',methods=['GET'])
def list_files():
    files = db.session.query(FileInfo).order_by().all()
    result = []
    for file in files:
        result.append({"name": file.file_name, "create_datetime": file.create_datetime})
    return jsonify(code=200, status="SUCCESS", result=result)

@restful.route('/file',methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        abort(400)
    filename = secure_filename(file.filename)

    # avoid duplicated filename
    count = db.session.query(FileInfo).filter(FileInfo.file_name == filename).count()
    if count > 0:
        abort(403)
    from .connector import s3_api
    content = file.read()
    current_app.logger.info(content)
    file_storage = s3_api(filename,content)
    try:
        file_storage.save()
    except Exception as e:
        current_app.logger.info(e)
    return jsonify(code=200, status="SUCCESS", result={"filename": filename})
