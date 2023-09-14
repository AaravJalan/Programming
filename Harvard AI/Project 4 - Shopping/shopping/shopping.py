import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # A dictionary mapping the month (string) to its equivalent integer value.
    months = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
              "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}

    evidence = []
    labels = []

    # Opening the csv file.
    with open(filename, mode='r') as file:
        # Storing data in a dictionary to access evidences more easily.
        data = csv.DictReader(file)

        for user in data:
            # Appending a list of individual user values to evidence list.
            evidence.append([
                # Values arranged in same order as 'shopping.csv'.
                # Typecasting from string to required data type.
                int(user["Administrative"]),
                float(user["Administrative_Duration"]),
                int(user["Informational"]),
                float(user["Informational_Duration"]),
                int(user["ProductRelated"]),
                float(user["ProductRelated_Duration"]),
                float(user["BounceRates"]),
                float(user["ExitRates"]),
                float(user["PageValues"]),
                float(user["SpecialDay"]),

                # Selecting the respective month integer from dictionary.
                months[user["Month"]],

                int(user["OperatingSystems"]),
                int(user["Browser"]),
                int(user["Region"]),
                int(user["TrafficType"]),

                # Returns 1 if condition is met, else 0.
                int(user["VisitorType"] == "Returning_Visitor"),
                int(user["Weekend"] == "TRUE")
            ])

            # Adding whether revenue is true or not to 'labels' list.
            labels.append(int(user["Revenue"] == "TRUE"))

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # The model is a k-nearest-neighbors classification, where k = 1.
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Number of accurate identifications of positives or negatives.
    true_positives = 0
    true_negatives = 0

    # Total number of actual positives or negatives.
    positive_count = 0
    negative_count = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            # If actual is positive, increment total positive.
            positive_count += 1
            # If predicted correctly, increment true_positives.
            if predicted == actual:
                true_positives += 1
        else:
            # If actual is negative, increment total negative.
            negative_count += 1
            # If predicted correctly, increment true_negatives.
            if predicted == actual:
                true_negatives += 1

    sensitivity = true_positives / positive_count
    specificity = true_negatives / negative_count

    return sensitivity, specificity


if __name__ == "__main__":
    main()
