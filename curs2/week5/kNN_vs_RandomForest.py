import numpy as np
from sklearn import datasets as dss
from sklearn.ensemble import RandomForestClassifier

digits_dataset = dss.load_digits()
X = digits_dataset.data
y = digits_dataset.target
train_count = int((1.-0.25)*len(y))

X_train = X[:train_count]
y_train = y[:train_count]
X_test = X[train_count:]
y_test = y[train_count:]

target_names = digits_dataset.target_names

train_pairs = zip(X_train, y_train)
test_pairs = zip(X_test, y_test)


def euclidean_distance(x1, x2):
    return sum(map(lambda (el1, el2): float(el1-el2)**2., zip(x1, x2)))


def predict(train_data, item, labels, k):
    item_vector, expected_label = item
    distances = map(lambda(train_vector, train_label):
                    (euclidean_distance(train_vector, item_vector), train_label),
                    train_data)

    neighbours = sorted(distances, key=lambda(dist, label): dist)[:k]

    counts = np.zeros(len(labels), dtype=int)

    for (_, label) in neighbours:
        idx = np.where(labels == label)[0][0]
        counts[idx] = counts[idx] + 1

    return (labels[np.argmax(counts)], expected_label)


predictions = map(lambda pair: predict(train_pairs, pair, target_names, 1), test_pairs)

false_count = np.sum(map(lambda (predicted, expected): predicted != expected, predictions))
answer1 = float(false_count)/float(len(test_pairs))


def write_answer_kfold(fileName, answer):
    with open("1nnVsRandomForest_" + fileName + ".txt", "w") as fout:
        fout.write(str(answer))
write_answer_kfold("1", answer1)
print answer1


forest_classifier = RandomForestClassifier(n_estimators=1000).fit(X_train, y_train)
forest_predictions = map(lambda (vector, expected_label):
                         (forest_classifier.predict(vector.reshape(1,-1))[0], expected_label),
                         test_pairs)
false_count = np.sum(map(lambda (predicted, expected): predicted != expected, forest_predictions))
answer2 = float(false_count)/float(len(test_pairs))
write_answer_kfold("2", answer2)
print answer2


