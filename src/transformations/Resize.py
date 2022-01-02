import cv2
import numpy as np


class Resize:
    """Resizes image and polygons to given size relative to longest side of image"""

    def __init__(self, size_range=(400, 600)):
        self.size_range = size_range

    def __call__(self, sample, size):
        image, card_polygon, label_polygons = sample['image'].copy(), sample['card_polygon'], sample['label_polygons']
        aug_image, matrix = self.resize_image(image, size)
        aug_label_polygons = [self.rotate_polygon(polygon, matrix) for polygon in label_polygons]
        aug_card_polygon = self.rotate_polygon(card_polygon, matrix)
        return {'image': aug_image, "card_polygon": aug_card_polygon, 'label_polygons': aug_label_polygons}

    def get_random_size(self):
        return np.random.randint(*self.size_range)

    def resize_image(self, image, size):
        height, width = image.shape[:2]
        if height >= width:
            scaling_factor = size / height
            new_width = int(scaling_factor * width)
            matrix = np.float32([[scaling_factor, 0, 0],
                                 [0, scaling_factor, 0]])
            t = np.float32(matrix)
            aug_image = cv2.warpAffine(image, t, (new_width, size))
        else:
            scaling_factor = size / width
            new_height = int(scaling_factor * height)
            matrix = np.float32([[scaling_factor, 0, 0],
                                 [0, scaling_factor, 0]])
            t = np.float32(matrix)
            aug_image = cv2.warpAffine(image, t, (size, new_height))
        t = np.vstack((t, np.asarray([[0, 0, 1]])))
        return aug_image, t

    def rotate_polygon(self, pts, M):

        """Transforms a list of points, `pts`,
        using the affine transform `A`."""
        src = np.zeros((len(pts), 1, 2))
        src[:, 0] = pts
        dst = np.squeeze(cv2.perspectiveTransform(src, M))
        return self.numpy_to_list(dst)

    @staticmethod
    def numpy_to_list(array):
        lst2 = []
        for i in array:
            lst = []
            for k in i:
                lst.append(float(k))
            lst2.append(lst)
        return lst2