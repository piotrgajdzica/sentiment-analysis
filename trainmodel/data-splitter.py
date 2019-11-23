import random

# data sets ratio
train = 80
test = 10
dev = 10

with open("data/Sentiment.csv") as fr:
    with open("data/train.csv", "w+") as f1, open("data/test.csv", "w+") as f2, open("data/dev.csv", "w+") as f3:
        for line in fr.readlines():
            rd = random.randint(1, train + test + dev)
            if rd < train:
                f = f1
            elif rd < train + test:
                f = f2
            else:
                f = f3
            f.write(line)
