from flask import Flask, request, jsonify
import cv2
import base64
import pickle
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder   

app = Flask(__name__)
model = tf.keras.models.load_model('model_1.h5')
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)


def decode_base64(image_base64):
    img_bytes = base64.b64decode(image_base64)
    img_np_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_np_array, cv2.IMREAD_GRAYSCALE)
    img=cv2.resize(img,(28,28))
    record = img.flatten()
    record = record.reshape(1, 784)
    return record

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    record = decode_base64(data['image'])
    predicted_labels = model.predict(record)
    predicted_class = np.argmax(predicted_labels, axis=1)
    decoded_prediction = label_encoder.inverse_transform(predicted_class)
    predicted_class_probability = predicted_labels[0][predicted_class[0]]
    response = {
        'letter': decoded_prediction[0],
        'probability': int(predicted_class_probability)*100
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
