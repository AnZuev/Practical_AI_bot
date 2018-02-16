import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sent2vec


def to_vectors(rows, model):
    sent_vecs = []
    for facts in rows:
        res = []
        for fact in facts:
            res.append(model.embed_sentence(fact))
        sent_vecs.append(np.array(res))
    return np.array(sent_vecs).T


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
        emb = np.array([self.model.embed_sentence(sentence)])
        similarity = []
        for inst in self.sent_vecs:
            t = cosine_similarity(emb, inst)
            similarity.append(max(t[0]))
        return self.raw_facts[np.argmax(np.array(similarity))][0], max(similarity)

