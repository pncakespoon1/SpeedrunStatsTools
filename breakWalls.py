import cv2
import os
rows = 0
columns = 0
instances = 0

def get_image_wall(rows1, columns1, instances1, img1, num1):
    column_size = 1920/columns1
    row_size = 1080/rows1
    count = 0
    for row in range(rows1):
        for column in range(columns1()):
            if count < instances1:
                count += 1
                new_img = img1[(row * row_size):((row+1) * row_size), (column * column_size):((column+1) * column_size)]
                cv2.imwrite("D:/ResetEfficiency/nn_images/unsorted_images/" + "image" + str(num1) + "-" + str(count).zfill(2), new_img)


wall_images = os.listdir(("D:/ResetEfficiency/nn_images/unsorted_images"))
for i in range(len(wall_images)):
    img = cv2.imread(wall_images[i])
    get_image_wall(rows, columns, instances, img, i)


