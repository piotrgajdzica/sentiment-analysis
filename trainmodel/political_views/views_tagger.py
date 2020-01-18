import os
from typing import List

from flair.data import Sentence, Label
from flair.models import TextClassifier


class ViewsTagger:
    def __init__(self):

        classifier_path = os.path.join(*os.path.split(__file__)[:-1], 'data/tagger_political_views/best-model.pt')
        self.classifier: TextClassifier = TextClassifier.load(classifier_path)

    def predict(self, tweet_text_list: List[str]) -> List[Label]:
        sentences = [Sentence(t) for t in tweet_text_list]

        self.classifier.predict(sentences)
        return [sentence.labels[0] for sentence in sentences]
