from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGRetriever:
    def __init__(self, document_path):
        self.document_path = Path(document_path)
        text = self.document_path.read_text(encoding='utf-8')
        self.chunks = [re.sub(r'\s+', ' ', x).strip() for x in re.split(r'\n\s*\n', text) if x.strip()]
        if not self.chunks:
            raise ValueError('La base de conocimiento está vacía.')
        self.vectorizer = TfidfVectorizer(lowercase=True, strip_accents='unicode', ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform(self.chunks)

    def retrieve(self, question, top_k=3):
        q = self.vectorizer.transform([question])
        scores = cosine_similarity(q, self.matrix)[0]
        ranked = scores.argsort()[::-1][:top_k]
        return [{'text': self.chunks[i], 'score': float(scores[i])} for i in ranked if scores[i] > 0]
