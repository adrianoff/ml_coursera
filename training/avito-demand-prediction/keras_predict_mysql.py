# -*- coding: utf-8 -*-

import MySQLdb
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from tqdm import tqdm
import sys
# load the model
model = VGG16()

conn = MySQLdb.connect(user="root", passwd="FlhbfyjD", db="avito_train")
cur = conn.cursor()

id_from = str(sys.argv[1])
id_to = str(sys.argv[2])

# id_from = str(0)
# id_to = str(250000)

def predict(image):
    image_name = '/home/adrianoff/Temp/test_jpg/' + image + '.jpg'
    image = load_img(image_name, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model.predict(image)
    label = decode_predictions(yhat)

    return [label[0][0][1], label[0][1][1], label[0][2][1], label[0][3][1], label[0][4][1]]


sql = "SELECT item_id, image FROM test_image_classes WHERE image != '' AND image_class_1 = 'None' AND id>" + id_from + \
      " AND id<=" + id_to + " LIMIT 100"

while True:
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        break
    for row in tqdm(rows):
        try:
            labels = predict(row[1])
            labels[0] = labels[0].replace("'", '')
            labels[1] = labels[1].replace("'", '')
            labels[2] = labels[2].replace("'", '')
            labels[3] = labels[3].replace("'", '')
            labels[4] = labels[4].replace("'", '')
        except Exception as e:
            print(e)
            continue

        cur.execute(
            "UPDATE test_image_classes SET image_class_1='" + labels[0] + "', image_class_2='" + labels[1] + "', image_class_3='" + labels[2] + "', image_class_4='" + labels[3] + "', image_class_5='" + labels[4] + "' WHERE item_id='" + row[0] + "'"
        )
    conn.commit()

cur.close()
conn.close()
