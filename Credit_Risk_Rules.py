
# these initiate the program by making sure that taken data can be randomized, that the program can count the data, and that the program can read the csv files.
import random
from collections import Counter
import pandas as pd


# this tells the program to read the csv files and store them in a variable called df and test_df. df has the training data and test_df holds data to be tested.
df = pd.read_csv("training_data.csv")
test_df = pd.read_csv("test_data.csv")


# this tells the program to fill in any missing data in the Saving account and Checking account columns with "none" in both the training and testing CSV files.
for column in ["Saving account", "Checking account"]:
    df[column] = df[column].fillna("none")
    test_df[column] = test_df[column].fillna("none")


# this counts all of the good and bad values in the Risk column
print(df["Risk"].value_counts())


# this takes the data from the housing, purpose, loan length, checking and savings accounts columns in the .csv files and holds them as facts
def row_to_facts(row):
    facts = set()
    facts.add(f"checking={row['Checking account']}")
    facts.add(f"savings={row['Saving account']}")
    facts.add(f"housing={row['Housing']}")
    facts.add(f"purpose={row['Purpose']}")

# check to see if these valuse have a corilation  that changes with specific values instead of just a general division.
    facts.add("loan=short" if row['Duration'] <=12 else "loan=long")

    if row['Credit amount'] > 5000:
        facts.add("credit=high")
    if row['Age'] < 30:
        facts.add("age=young")

    return facts


# based on code format from session 3 resources 
credit_risk_rules = [

# this gives a label of "checking/savings=low" to checking or savings accounts that have a value of none, little, or moderate.
# check if none in the checking or savings account columns was actually a negative in the data, not just unfilled info.
    ({"checking=none"}, "checking=low"),
    ({"checking=little"}, "checking=low"),
    ({"checking=moderate"}, "checking=low"),
    ({"savings=none"}, "savings=low"),
    ({"savings=little"}, "savings=low"),
    ({"savings=moderate"}, "savings=low"),

    ({"checking=low", "savings=low"}, "money=low"),

# this gives a label of "exposure=high" to loans that are long with a high credit amount and a label of "history=thin" to young people who rent
    ({"loan=long", "credit=high"}, "exposure=high"),
    ({"age=young", "housing=rent"}, "history=thin"),


# These are placeholders, look in to whether different purposes had different correlations with being bad vs good
    ({"purpose=education"}, "purpose_type=risky"),
    ({"purpose=repairs"},  "purpose_type=risky"),
    ({"purpose=business"}, "purpose_type=risky"),
    ({"purpose=vacation/others"}, "purpose_type=risky"),
    ({"purpose=car"}, "purpose_type=risky"),
    ({"purpose=radio/TV"},  "purpose_type=risky"),
    ({"purpose=furniture/equipment"}, "purpose_type=risky"),
    ({"purpose=domestic appliances"}, "purpose_type=risky"),

#tries to organise people if they are bad risk
    ({"money=low", "loan=long"}, "risk=bad"),
    ({"money=low", "purpose_type=risky"}, "risk=bad"),
    ({"money=low", "history=thin"}, "risk=bad"),

# in the training data people who rent or are free for housing were more likely to be bad risk
    ({"money=low","housing=rent"}, "risk=bad"),
    ({"money=low","housing=free"}, "risk=bad"),
    ({"exposure=high"}, "risk=bad"),
    ({"checking=little", "loan=long"}, "risk=bad"),
]

# from session 3 resources
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

# from session 3 resources
# uses backward chaining to help the program decide if someone is a bad risk by looking at the risk and if the data proves it 
def backward_chain(goal, facts, rules):
    if goal in facts:
        return True
    for conditions, conclusion in rules:
        if conclusion == goal:
            if all(backward_chain(c, facts, rules) for c in sorted(conditions)):
                return True
    return False


