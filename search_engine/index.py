import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sent2vec


def get_raw_facts(filename):
    file = open(filename, 'r')
    results = []
    for line in file.readlines():
        results.append("".join(line.split(".")[1:]).strip())
    return results


def to_vectors(facts, model):
    sent_vecs = []
    for fact in facts:
        sent_vecs.append(model.embed_sentence(fact))
    return sent_vecs


class SearchEngine:
    model = sent2vec.Sent2vecModel()

    @staticmethod
    def load_model(model_name='wiki_unigrams.bin'):
        print("Loading model")
        SearchEngine.model.load_model(model_name)
        print("Model has been loaded")

    def __init__(self, raw_facts):
        self.raw_facts = raw_facts
        print("Transforming sentences to vectors")
        self.sent_vecs = to_vectors(self.raw_facts, SearchEngine.model)

    def find(self, sentence):
        emb = SearchEngine.model.embed_sentence(sentence).reshape((1, -1))
        similarity = cosine_similarity(emb, self.sent_vecs)[0]
        return self.raw_facts[np.argmax(similarity)], max(similarity)

