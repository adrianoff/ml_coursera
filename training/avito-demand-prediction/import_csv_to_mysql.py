import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='FlhbfyjD',
    db='avito_train')
cursor = mydb.cursor()

csv_data = csv.reader(open('./data/df_to_mysql_test.csv', 'rb'))
i = 0
for row in csv_data:
    i += 1
    if i == 1:
        continue
    cursor.execute(
        "INSERT INTO test_image_classes (item_id, image, image_class_1, image_class_2, image_class_3, image_class_4, image_class_5) \
        VALUES('" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] + "', '" + row[5] + "', '" + row[6] + "', '" + row[7] + "')"
    )
    mydb.commit()

cursor.close()
print("Done")
