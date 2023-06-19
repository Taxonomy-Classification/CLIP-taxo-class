import json
from collections import Counter

# Read JSON data from file line by line
data = []
count = 0
with open("./data/textaug_train_full_capaug_compressed.json", "r") as file:
    for line in file:
        if len(json.loads(line)["captions"]) == 8 and count < 0:
            count += 1
            print(line, "\n")
        data.append(json.loads(line))

# Count the number of captions for each entry
caption_counts = [len(entry["captions"]) for entry in data]

# Calculate the frequency of each caption count
caption_count_freq = Counter(caption_counts)

# Print the count and frequency as text
caption_count_list = sorted(caption_count_freq.keys())
freq_list = [caption_count_freq[count] for count in caption_count_list]

print("Caption count:")
for count, freq in zip(caption_count_list, freq_list):
    print(f"{count}: {freq}")
