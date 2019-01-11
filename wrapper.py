from model import Model
from cropper import Cropper


predict_model = Model('model.h5')
cropper = Cropper('mapping.json', predict_model)
predictions = cropper.predict('images/2018-07-16 10_06_58.325.jpg')

print(predictions)
