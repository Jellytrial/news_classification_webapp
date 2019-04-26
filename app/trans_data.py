import sys
from collections import Counter


def trans_data(categoryfile, datafile, outfile):

    category = []
    fp = open(categoryfile)
    for line in fp:
        line = line.rstrip()
        category.append(line.split()[0])
    fp.close()
    # print(len(category))

    line_num = []
    fp = open(datafile)
    for line in fp:
        line = line.strip()
        # print(len(line))
        line_num.append(line.split())
    num = len(line_num)

    train_data = []
    for i in range(num):
        train_data.append([])

    lineCount = 0
    fp = open(datafile)
    for line in fp:
        lineCount += 1
        line = line.strip()
        itemList = line.split(',')
        counter = Counter(itemList)
        for word, cnt in counter.most_common():
            train_data[lineCount - 1].append("%s:%d" % (word, cnt))
    fp.close()

    fp = open(outfile, "w")
    for i in range(num):
        fp.write("%s %s\n" % (category[i], " ".join(train_data[i])))
    fp.close()

if __name__ == "__main__":
    # transform to trans_word.csv
    trans_data("category.csv", "word.csv", "trans_word.csv")
