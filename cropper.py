import json
import glob
import os
import numpy as np
import cv2

def read_mapping(mapping_json):
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

    return points

def extract_parklot(img, parklot, w, h):
    parklot_rect = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

    if np.linalg.norm(parklot[2] - parklot[3]) > np.linalg.norm(parklot[1] - parklot[2]):
        parklot = parklot[[1, 2, 3, 0]]

    matrix = cv2.getPerspectiveTransform(parklot, parklot_rect)

    return cv2.warpPerspective(img, matrix, (w, h))

def crop(points, filename, out=None, w=135, h=235):
    if not os.path.exists(out) :
            os.makedirs(out)

    img = cv2.imread(filename)
    
    for i, parklot in enumerate(points):
        cropped = extract_parklot(img, parklot, w, h)
        base = os.path.splitext(os.path.basename(filename))[0]
        cv2.imwrite(out + '/' + base + '+' + str(i) + '.jpg', cropped)

def crop_predict(points, filename, predict, *args, w=135, h=235):
    img = cv2.imread(filename)
    predictions = {}
    
    for i, parklot in enumerate(points):
        cropped = extract_parklot(img, parklot, w, h)
        predictions[i] = predict(*args, cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    return predictions

if __name__ == '__main__':
    points = read_mapping('mapping.json')
    for filename in glob.glob('images/*'):
        print(filename)
        crop(points, filename, out='parklots_all')

   