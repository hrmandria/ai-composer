import numpy as np
import pandas as pd
import glob

csv_path = '/*.csv'
csv_files = glob.glob(csv_path)

sequences = []

colonne_notes = 'notes'

for file in csv_files :
    df = pd.read_csv(file)
    sequence = df[colonne_notes].apply(lambda x: [int(note) for note in x.split(',')]).tolist()
    sequences.extend(sequence)

all_notes = set(note for sequence in sequences for note in sequence)
note_to_index = {note: index for index, note in enumerate(all_notes)}
index_to_note = {index: note for note, index in note_to_index.items()}


sequences_indices = [[note_to_index[note] for note in sequence] for sequence in sequences]


num_notes = len(all_notes)
matrix_transition = np.zeros((num_notes, num_notes))

for sequence in sequences_indices:
    for i in range(len(sequence) - 1):
        current_note = sequence[i]
        next_note = sequence[i + 1]
        matrix_transition[current_note, next_note] += 1

matrix_transition /= matrix_transition.sum(axis=1, keepdims=True)

sequence_length = 10
current_note = np.random.choice(num_notes)
generated_sequence = [current_note]

for _ in range(sequence_length - 1):
    next_note = np.random.choice(num_notes, p=matrix_transition[current_note])
    generated_sequence.append(next_note)
    current_note = next_note

generated_sequence = [index_to_note[index] for index in generated_sequence]

print("Séquence générée :", generated_sequence);
