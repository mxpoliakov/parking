from model import predict_one
from cropper import read_mapping, crop
from keras.models import load_model
from matplotlib import pyplot as PLT


def wrapper(filename):
    predictions = {}
    model = load_model('model.h5')
    points = read_mapping('mapping.json')
    ret = crop(points, filename)
    for i, parklot in enumerate(ret):
        PLT.imshow(parklot)
        PLT.show()
        predictions[i] = predict_one(model, parklot)
    return predictions


wrapper('images/photo5251373246744472076.jpg')