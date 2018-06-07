# -*- coding: utf-8 -*-

import MySQLdb
import sys
import os

import yaml
from tqdm import tqdm

conn = MySQLdb.connect(user="root", passwd="FlhbfyjD", db="avito_train")
cur = conn.cursor()

id_from = str(sys.argv[1])
id_to = str(sys.argv[2])

sql = "SELECT item_id, image FROM train_image_classes WHERE image != '' AND width IS NULL AND id>" + id_from + " AND id<=" + id_to + " LIMIT 100"

geometry_ind = 4

red_mean_ind = 19
red_std_ind = 20

green_mean_ind = 26
green_std_ind = 27

blue_mean_ind = 33
blue_std_ind = 34

image_stat_mean_ind = 41
image_stat_std_ind = 42

while True:
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        break

    for row in tqdm(rows):
        image = row[1] + '.jpg'
        image_info = os.popen("identify -verbose /home/adrianoff/Temp/train_jpg/" + image).read()
        image_info_arr = image_info.split("\n")

        img_dict = {}
        for i, item in enumerate(image_info_arr):
            img_dict[i] = item

        geometry_str = img_dict[4]
        width = geometry_str[(geometry_str.index('Geometry: ')+len('Geometry: ')):geometry_str.index('x')]
        height = geometry_str[(geometry_str.index('x')+len('x')):geometry_str.index('+0')]

        try:
            red_mean = img_dict[red_mean_ind].strip().split(' ')[1]
        except:
            red_mean = 0.0

        try:
            red_std = img_dict[red_std_ind].strip().split(' ')[2]
        except:
            red_std = 0.0

        try:
            green_mean = img_dict[green_mean_ind].strip().split(' ')[1]
        except:
            green_mean = 0.0

        try:
            green_std = img_dict[green_std_ind].strip().split(' ')[2]
        except:
            green_std = 0.0

        try:
            blue_mean = img_dict[blue_mean_ind].strip().split(' ')[1]
        except:
            blue_mean = 0.0

        try:
            blue_std = img_dict[blue_std_ind].strip().split(' ')[2]
        except:
            blue_std = 0.0

        try:
            image_stat_mean = img_dict[image_stat_mean_ind].strip().split(' ')[1]
        except:
            image_stat_mean = 0.0

        try:
            image_stat_std = img_dict[image_stat_std_ind].strip().split(' ')[2]
        except:
            image_stat_std = 0.0

        try:
            image_info = {
                'width': float(width),
                'height': float(height),

                'red_mean': float(red_mean),
                'red_std': float(red_std),

                'green_mean': float(green_mean),
                'green_std': float(green_std),

                'blue_mean': float(blue_mean),
                'blue_std': float(blue_std),

                'image_stat_mean': float(image_stat_mean),
                'image_stat_std': float(image_stat_std),
            }
        except:
            image_info = {
                'width': float(width),
                'height': float(height),

                'red_mean': 0.0,
                'red_std': 0.0,

                'green_mean': 0.0,
                'green_std': 0.0,

                'blue_mean': 0.0,
                'blue_std': 0.0,

                'image_stat_mean': 0.0,
                'image_stat_std': 0.0,
            }

        cur.execute(
            "UPDATE train_image_classes SET width=" + str(image_info['width']) + ", height=" + str(image_info['height']) +
            ", red_mean='" + str(image_info['red_mean']) + "', red_std='" + str(image_info['red_std']) +
            "', green_mean='" + str(image_info['green_mean']) + "', green_std='" + str(image_info['green_std']) +
            "', blue_mean='" + str(image_info['blue_mean']) + "', blue_std='" + str(image_info['blue_std']) +
            "', image_stat_mean='" + str(image_info['image_stat_mean']) + "', image_stat_std='" + str(image_info['image_stat_std']) +
            "' WHERE item_id='" + row[0] + "'"
        )

    conn.commit()


cur.close()
conn.close()
