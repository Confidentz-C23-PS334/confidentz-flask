import os
import time

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from flask import Flask, request
from werkzeug.utils import secure_filename

# Model init
print('compiling')
model = tf.keras.saving.load_model('./confidentz_model.h5', custom_objects={ 'KerasLayer': hub.KerasLayer }, compile=True)

# Flask init
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/detect", methods=['POST'])
def detect():
    file = request.files['file']
    filename = str(time.time()) + '-' + secure_filename(file.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filePath)
    
    img = tf.keras.utils.load_img(filePath, target_size=(160, 160))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    images = np.vstack([img_array])
    print(img_array.shape)

    prediction = model.predict(images, batch_size=10)
    print(prediction[0])

    class_names = ['No Caries', 'Caries']
    score = tf.nn.softmax(prediction[0])
    print(
        "{} detected with a {:.2f} percent confidence.\n"
        .format(class_names[np.argmax(score)], 100 * np.max(score))+
        "{} detected with a {:.2f} percent confidence."
        .format(class_names[np.argmin(score)], 100 * np.min(score))
    )

    os.remove(filePath)

    results = {}
    results[class_names[np.argmax(score)]] = 100 * np.max(score)
    results[class_names[np.argmin(score)]] = 100 * np.min(score)
    return results
