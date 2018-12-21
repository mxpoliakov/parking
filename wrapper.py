from model import predict_one
from cropper import read_mapping, crop_predict
from keras.models import load_model

def predict_all(filename):
    model = load_model('model.h5')
    points = read_mapping('mapping.json')
    return crop_predict(points, filename, predict_one, model)

predictions = predict_all('images/2018-07-13 14_44_54.816.jpg')

print(predictions)