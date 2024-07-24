from datetime import timedelta
from django.utils import timezone
from os import path

import string
import random
import cv2

def datetime_format(dt):
    now = timezone.now()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return f"{int(diff.total_seconds())} seconds ago"
    elif diff < timedelta(hours=1):
        return f"{int(diff.total_seconds() // 60)} minutes ago"
    elif diff < timedelta(days=1):
        return f"{int(diff.total_seconds() // 3600)} hours ago"
    elif diff < timedelta(days=2):
        return "Yesterday"
    elif diff < timedelta(days=7):
        return f"{diff.days} days ago"
    elif diff < timedelta(days=365):
        return dt.strftime("%b %d")
    else:
        return dt.strftime("%b %d, %Y")
    
def resize_img(main_path, new_path, x2, y2):
    img = cv2.imread(main_path)
    y1, x1, _ = img.shape

    if x1/y1 == x2/y2:
        img = cv2.resize(img, (x2, y2))
        background = img

    else:
        if x1/y1 > x2/y2:
            img = cv2.resize(img, (x2, int(x2 * img.shape[0] / img.shape[1])))
            # img = cv2.resize(img, (int(x2 * img.shape[1] / img.shape[0]), y2))

        elif x1/y1 < x2/y2:
            img = cv2.resize(img, (int(y2 * img.shape[1] / img.shape[0]), y2))

        background = cv2.resize(img, (x2, y2))
        background = cv2.blur(background, (10, 10)) 

        # Calculate the position to place your image in the middle
        x_offset = (background.shape[1] - img.shape[1]) // 2
        y_offset = (background.shape[0] - img.shape[0]) // 2

        background[y_offset:y_offset + img.shape[0],
                    x_offset:x_offset + img.shape[1]] = img
    
    cv2.imwrite(new_path, background)

def check_image_size(main_path, x, y):
    img = cv2.imread(main_path)
    y1, x1, _ = img.shape

    return x == x1 and y == y1

def get_random_image_name(old_path):
    path_list = path.split(old_path)
    old_name = path_list[-1]
    ext = old_name.split(".")[-1]

    return "\\".join(list(path_list[:-1]) + [f"{get_random_sid()}.{ext}"])

def get_random_sid(length=12):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_random_slug_suffix():
    return get_random_sid(2)

