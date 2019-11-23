from flair.data import Corpus
from flair.datasets import CSVClassificationCorpus

# this is the folder in which train, test and dev files reside
data_folder = 'data'

# column format indicating which columns hold the text and label(s)
column_name_map = {
    16: "text",
    6: "label_topic"
}
# column_name_map = {4: "text", 1: "label_topic", 2: "label_subtopic"}

# load corpus containing training, test and dev data and if CSV has a header, you can skip it
corpus: Corpus = CSVClassificationCorpus(data_folder,
                                         column_name_map,
                                         skip_header=True,
                                         delimiter='\n',
                                         )

print(corpus)



