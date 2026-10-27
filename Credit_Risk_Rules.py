
# these initiate the program by making sure that taken data can be randomized, that the program can count the data, and that the program can read the csv files.
import random
from collections import Counter
import pandas as pd


# this tells the program to read the csv files and store them in a variable called df and test_df. df has the training data and test_df holds data to be tested.
df = pd.read_csv("training_data.csv")
test_df = pd.read_csv("test_data.csv")