import os

from flair.data import Corpus
from flair.datasets import CSVClassificationCorpus
from flair.embeddings import FlairEmbeddings, WordEmbeddings, DocumentPoolEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer

if __name__ == '__main__':

    # this is the folder in which train, test and dev files reside
    data_directory = 'data'

    experiment_name = 'test2'
    tagger_output_directory = os.path.join(data_directory, 'tagger_%s' % experiment_name)
    try:
        os.makedirs(tagger_output_directory)
    except FileExistsError:
        pass

    # column format indicating which columns hold the text and label(s)
    column_name_map = {
        2: "text",
        0: "label_topic"
    }

    # load corpus containing training, test and dev data and if CSV has a header, you can skip it
    corpus: Corpus = CSVClassificationCorpus(data_directory,
                                             column_name_map,
                                             delimiter=',',
                                             )

    print(corpus.obtain_statistics())

    label_dictionary = corpus.make_label_dictionary()
    print(label_dictionary.item2idx)

    # specify word embeddings you want to use
    word_embeddings = [
        WordEmbeddings('glove'),
        FlairEmbeddings('news-forward-fast'),
        FlairEmbeddings('news-backward-fast')
    ]

    # specify document embeddings that are created from word embeddings
    document_embeddings = DocumentPoolEmbeddings(
        word_embeddings,
        pooling='mean',
        fine_tune_mode='nonlinear',
    )

    # choose classifier type
    tagger: TextClassifier = TextClassifier(document_embeddings=document_embeddings,
                                            label_dictionary=label_dictionary,
                                            multi_label=False
                                            )
    # define model
    trainer = ModelTrainer(tagger, corpus)

    # train model
    trainer.train(
        'data/tagger',
        learning_rate=0.7,
        mini_batch_size=64,  # decrease to prevent graphic card memory errors. Increase to improve learning speed
        monitor_test=True,
        monitor_train=True,
        patience=3,  # after how many unsuccessful epochs should we start annealing the learning rate
        anneal_factor=0.5,
        embeddings_storage_mode='cpu',  # warning: if this leads to memory errors set to 'none'
        max_epochs=3,
        # use_amp=True,
    )


