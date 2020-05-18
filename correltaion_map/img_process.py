import math

import cv2
import numpy as np
from matplotlib import pyplot as plt


def find_theta(img1, img2, lines=0):
    """
    Return the angle of rotation of the img2 relative to img1
    """
    # Use descriptor for detecting the img2 in img1
    orb = cv2.ORB_create()
    kpt1, des1 = orb.detectAndCompute(img1, None)
    kpt2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    # Show both images with the result work of descriptor
    if not lines:
        lines = 0
    elif lines > len(matches):
        lines = matches
    img3 = 0
    img3 = cv2.drawMatches(img1, kpt1, img2, kpt2, matches[:lines], img3, flags=2)
    # Calculation angle
    src_pts = np.float32([kpt1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kpt2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    theta = - math.atan2(matrix[0, 1], matrix[0, 0]) * 180 / math.pi
    return theta, img3


def rotate_img(image, theta: float):
    """
    Rotate the image by theta degrees relative to the center of image
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    matrix = cv2.getRotationMatrix2D(center, theta, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h))
    return rotated


def pixel_intensity_x_y(img, x: int, y: int) -> float:
    """Returns the pixel intensity, having pixel coordinates and image"""
    return (img[x][y][0] / 255 * 0.299 +
            img[x][y][1] / 255 * 0.587 +
            img[x][y][2] / 255 * 0.114)


def pixel_intensity(pixel) -> float:
    """Returns the pixel intensity on a gray scale"""
    return (pixel[0] / 255 * 0.299 +
            pixel[1] / 255 * 0.587 +
            pixel[2] / 255 * 0.114)


def mean_intensity(img) -> float:
    """Return average intensity of image"""
    m_int = 0
    for line in img:
        for pxl in line:
            m_int += pixel_intensity(pxl)
    return m_int / img.size


def view_image(name, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig = plt.figure()
    a = fig.add_subplot()
    plt.imshow(img)
    a.set_title(name)
    plt.show()


def show_images(images, titles):
    for n, (image, title) in enumerate(zip(images, titles)):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        fig = plt.figure()
        a = fig.add_subplot()
        a.set_title(title)
        plt.imshow(image)
        plt.show()


def select_region(image_path, top_left, bottom_right):
    image = cv2.imread(image_path)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    return image


def get_image_zone(image, top_left, bottom_right):
    x1, y1 = top_left
    x2, y2 = bottom_right
    return image[x1:x2, y1:y2]


def img_to_matrix(img):
    """Returns the image matrix of which was converted on a gray scale of intensity"""
    height, width, _ = img.shape
    matrix = np.zeros((height, width))
    for i, column in enumerate(img):
        for j, pixel in enumerate(column):
            intensity = pixel_intensity(pixel)
            matrix[i][j] = intensity
    return matrix
