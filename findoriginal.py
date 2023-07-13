import pandas as pd
import json

# Read the CSV file into a dataframe
df = pd.read_csv('/Users/odysseasdrosis/Desktop/mimic_pmc_kaggle/mtsamples.csv')
#
# # Display the dataframe
KAGGLE_matrix =[]
for i in range(len(df)):
    if (type(df['transcription'][i]) == str):
        KAGGLE_matrix.append(df['transcription'][i])


pmc = []
# Open the JSON file
data_files = [
    '/Users/odysseasdrosis/Desktop/mimic_pmc_kaggle/PMC-Patients_dev.json',
    '/Users/odysseasdrosis/Desktop/mimic_pmc_kaggle/PMC-Patients_train.json',
    '/Users/odysseasdrosis/Desktop/mimic_pmc_kaggle/PMC-Patients_test.json'
]
pmc = []
for file_path in data_files:
    with open(file_path) as file:
        data = json.load(file)
        for i in range(len(data)):
            pmc.append(data[i]['patient'])

PMC_matrix = pmc[:10000]

# Read the JSONL file into a pandas dataframe
df1 = pd.read_json('/Users/odysseasdrosis/Desktop/mimic_pmc_kaggle/clinical-notes-live.jsonl', lines=True)

# Extract the "note" column as a matrix
notes_matrix = []

for i in range(len(df1)):
    notes_matrix.append(df1['note'][i])


# Display the matrix
print("1")
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.matrix = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, matrix):
        node = self.root
        for char in word:
            node = node.children[char]
        node.matrix = matrix

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.matrix

def build_trie(matrix, texts):
    trie = Trie()
    for text in texts:
        trie.insert(text, matrix)
    return trie

# Assuming you have the PMC, KAGGLE, and notes matrices

# Build Trie structures for PMC and KAGGLE matrices
trie_pmc = build_trie('PMC', PMC_matrix)  # Replace PMC_matrix with the actual PMC matrix
trie_kaggle = build_trie('KAGGLE', KAGGLE_matrix)  # Replace KAGGLE_matrix with the actual KAGGLE matrix

# Find the matrix for each entry in the notes matrix
result = []
for note in notes_matrix:
    matrix_label = None
    if trie_pmc.search(note) is not None:
        matrix_label = 'PMC'
    elif trie_kaggle.search(note) is not None:
        matrix_label = 'KAGGLE'
    result.append(matrix_label)

# Print the matrix labels for each note
for i, note in enumerate(notes_matrix):
    matrix_label = result[i]
    print(f"The note '{i}' exists in matrix {matrix_label}")
