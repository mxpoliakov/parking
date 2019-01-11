import cv2

from cropper import Cropper

result = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 0, 12: 1, 13: 1, 14: 1, 15: 0, 16: 1, 17: 0, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 0, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 0, 31: 1, 32: 1, 33: 1, 34: 1, 35: 0, 36: 1, 37: 1, 38: 0, 39: 1, 40: 1, 41: 0, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 0, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 0, 55: 1, 56: 1, 57: 1, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 1, 64: 1, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0, 70: 0, 71: 0, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 0, 84: 1, 85: 1, 86: 0, 87: 0, 88: 1, 89: 1, 90: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 1, 96: 0, 97: 1, 98: 1, 99: 1, 100: 1}

points = Cropper('mapping.json', None).points
file = 'images/2018-07-31 15_10_20.626.jpg'
file1 = 'images/2018-07-31 15_10_20.6262.jpg'

image = cv2.imread(file)
for index in range(2):
    for i in range(len(points)):
        if result[i]:
            if index: continue
            color = (0, 0, 255)
        else:
            if not index: continue
            color = (0, 255, 0)

        for j in range(4):
            cv2.line(image, tuple(points[i][j]), tuple(points[i][(j+1)%4]), color, 10)

cv2.imwrite(file1, image)
