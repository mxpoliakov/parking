import json
import numpy as np
import cv2


class Cropper(object):

    def __init__(self, points_file, model, w=135, h=235):
        self.model = model
        self.w = w
        self.h = h
        self.read_map(points_file)

    def read_map(self, mapping_json):
        mapping = json.loads(open(mapping_json).read())[0]['annotations']
        points = []

        for parklot in mapping:
            x = map(float, parklot['xn'].split(';'))
            y = map(float, parklot['yn'].split(';'))
            coords = np.array(list(zip(x, y))).astype(np.float32)
            reorder = np.zeros((4, 2), dtype=np.float32)
            reorder[0] = coords[np.argmin(coords.sum(axis=1))]
            reorder[1] = coords[np.argmin(np.diff(coords, axis=1))]
            reorder[2] = coords[np.argmax(coords.sum(axis=1))]
            reorder[3] = coords[np.argmax(np.diff(coords, axis=1))]
            points.append(reorder)

        self.points = points
        return self

    @staticmethod
    def extract_parklot(img, parklot, w, h):
        parklot_rect = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

        if np.linalg.norm(parklot[2] - parklot[3]) > np.linalg.norm(parklot[1] - parklot[2]):
            parklot = parklot[[1, 2, 3, 0]]

        matrix = cv2.getPerspectiveTransform(parklot, parklot_rect)

        return cv2.warpPerspective(img, matrix, (w, h))

    def predict(self, filename):
        img = cv2.imread(filename)
        predictions = {}

        for i, parklot in enumerate(self.points):
            cropped = Cropper.extract_parklot(img, parklot, self.w, self.h)
            predictions[i] = self.model.predict(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        return predictions
