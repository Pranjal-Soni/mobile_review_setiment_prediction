import sys
import os,io
import pytreebank

out_path = os.path.join('../inputs/', 'sst_{}.txt')
dataset = pytreebank.load_sst('../inputs')

# Store train, dev and test in separate files
for category in ['train', 'test', 'dev']:
    with open(out_path.format(category), 'w') as outfile:
        for item in dataset[category]:
            outfile.write("{}\t{}\n".format(
                item.to_labeled_lines()[0][0],
                item.to_labeled_lines()[0][1]
            ))