import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class IAContentAnalyzer:
    def __init__(self):
        self.stop_words_fr = [
            "alors","au","aucuns","aussi","autre","avant","avec","avoir","bon","car",
            "ce","cela","ces","ceux","chaque","ci","comme","comment","dans","des",
            "du","dedans","dehors","depuis","devrait","doit","donc","dos","début",
            "elle","elles","en","encore","essai","est","et","eu","fait","faites",
            "fois","font","hors","ici","il","ils","je","juste","la","le","les",
            "leur","là","ma","maintenant","mais","mes","mine","moins","mon","mot",
            "même","ni","nommés","notre","nous","nouveaux","ou","où","par","parce",
            "parole","pas","personnes","peut","peu","pièce","plupart","pour",
            "pourquoi","quand","que","quel","quelle","quelles","quels","qui",
            "sa","sans","ses","seulement","si","sien","son","sont","sous",
            "soyez","sujet","sur","ta","tandis","tellement","tels","tes","ton",
            "tous","tout","trop","très","tu","valeur","voie","voient","vont",
            "votre","vous","vu","ça","étaient","état","étions","été","être"
        ]

        self.vectorizer = TfidfVectorizer(
            stop_words=self.stop_words_fr,
            ngram_range=(1, 2),
            max_df=0.85,
            min_df=1
        )

    def clean(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def is_valid(self, mot):
        mots_interdits = ["chose","truc","machin","genre","faire","dire"]

        if len(mot) < 4:
            return False

        if any(char.isdigit() for char in mot):
            return False

        if mot in mots_interdits:
            return False

        return True

    def remove_redundant(self, tags):
        final = []

        for t in tags:
            if not any(t in other and t != other for other in tags):
                final.append(t)

        return final

    def generer_tags(self, texte, n=6):
        texte = self.clean(texte)

        try:
            X = self.vectorizer.fit_transform([texte])
        except:
            return []

        mots = self.vectorizer.get_feature_names_out()
        scores = X.toarray()[0]

        pairs = list(zip(mots, scores))
        pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

        tags = []

        for mot, score in pairs:
            if self.is_valid(mot):
                tags.append(mot)

            if len(tags) >= n * 2:
                break

        tags = self.remove_redundant(tags)

        if not tags:
            mots = texte.split()
            freq = Counter(mots)
            tags = [m for m, _ in freq.most_common(n) if self.is_valid(m)]

        return tags[:n]

    def detect_spam(self, texte):
        texte = texte.lower()
        spam_words = ["gratuit","promo","argent","clique","offre"]
        score = sum(1 for w in spam_words if w in texte)
        return score >= 2

    def similarite(self, contenu, contenus):
        textes = [c['contenu'] for c in contenus]

        vect = self.vectorizer.fit_transform(textes)

        index = contenus.index(contenu)
        sims = cosine_similarity(vect[index], vect).flatten()

        result = []
        for i, score in enumerate(sims):
            if i != index:
                result.append((contenus[i], score))

        result = sorted(result, key=lambda x: x[1], reverse=True)

        return [r[0] for r in result[:3]]