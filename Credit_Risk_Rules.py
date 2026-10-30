
# these initiate the program by making sure that taken data can be randomized, that the program can count the data, and that the program can read the csv files.
import random
from collections import Counter
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# this tells the program to read the csv files and store them in a variable called df and test_df. df has the training data and test_df holds data to be tested.
df = pd.read_csv("training_data.csv")
test_df = pd.read_csv("test_data.csv")

# this counts all of the good and bad values in the Risk column
print(df["Risk"].value_counts())


# this takes the data from the housing, purpose, loan length, checking and savings accounts columns in the .csv files and holds them as facts
def row_to_facts(row):
    facts = set()
    facts.add(f"checking={row['Checking account']}")
    facts.add(f"savings={row['Saving accounts']}")
    facts.add(f"housing={row['Housing']}")
    facts.add(f"purpose={row['Purpose']}")

# loans of 12 months or less are short, anything longer is long
    facts.add("loan=short" if row['Duration'] <=12 else "loan=long")

    if row['Credit amount'] > 8000:
        facts.add("credit=high")
    if row['Age'] < 25:
        facts.add("age=young")

    return facts

new
credit_risk_rules = [

    # this gives a label of "checking/savings=low" to checking or savings accounts that have a value of little, or moderate.
    ({"checking=little"}, "checking=low"),
    ({"checking=moderate"}, "checking=low"),
    ({"savings=little"}, "savings=low"),
    ({"savings=moderate"}, "savings=low"),
    ({"checking=low", "savings=low"}, "money=low"),

    # this gives a label of "exposure=high" to loans that are long with a high credit amount
    ({"loan=long", "credit=high"}, "exposure=high"),

    # these purposes had higher bad rates in the training data, so they're labelled risky
    ({"purpose=education"}, "purpose_type=risky"),
    ({"purpose=repairs"},  "purpose_type=risky"),
    ({"purpose=vacation/others"}, "purpose_type=risky"),

    #tries to organise people if they are bad risk
    ({"money=low", "loan=long"}, "risk=bad"),
    ({"money=low", "purpose_type=risky"}, "risk=bad"),
    ({"age=young", "checking=low"}, "risk=bad"),
    ({"exposure=high"}, "risk=bad"),
    ({"checking=little", "loan=long"}, "risk=bad"),


    # in the training data people who rent or are free for housing were more likely to be bad risk
    ({"money=low","housing=rent"}, "risk=bad"),
    ({"money=low","housing=free"}, "risk=bad"),
]


# uses forward chaining to help the program decide if risk is good or bad
def forward_chain(facts, rules):
    known = set(facts)
    changed = True
    while changed:
        changed = False
        for conditions, conclusion in rules:
            if conditions <= known and conclusion not in known:
                known.add(conclusion)
                changed = True
    return known

# uses forward chaining to decide good or bad risk, people are good unless risk=bad
def classify(row):
    known = forward_chain(row_to_facts(row), credit_risk_rules)
    return "bad" if "risk=bad" in known else "good"


# converts the table into a list of rows
rows = df.to_dict("records")

# splits training data 70%/30% to design rules (70%) then tests them (30%)
random.seed(42)
shuffled = rows[:]
random.shuffle(shuffled)
cut = int(.7 * len(shuffled))
train, test = shuffled[:cut], shuffled[cut:]


# guesses the most common answer and provides a baseline my rules need to beat
majority = Counter(r["Risk"] for r in train).most_common(1)[0][0]
baseline = sum(r["Risk"] == majority for r in test) / len(test)
print(f"Always predict {majority!r}: {baseline:.2f}")


# compares the programs choices with the answers in test
y_true = [r["Risk"] for r in test]
y_pred = [classify(r) for r in test]
print(f"\nAccuracy: {accuracy_score(y_true, y_pred):.2f}")
print (classification_report(y_true, y_pred, zero_division=0))
print(confusion_matrix(y_true, y_pred, labels=sorted (set(y_true))))


# predicts how many people in the test_data.csv will be good or bad
predictions = [classify(r) for r in test_df.to_dict("records")]
print("\nPredictions for the test data:", Counter(predictions))