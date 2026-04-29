from collections import Counter

def calculer_stats(contenus):
    total_vues = sum(c['vues'] for c in contenus)
    total_likes = sum(c['likes'] for c in contenus)

    return {
        'total_contenus': len(contenus),
        'total_vues': total_vues,
        'total_likes': total_likes,
        'engagement': (total_likes / total_vues * 100) if total_vues else 0
    }


def top_contenus(contenus):
    return sorted(contenus, key=lambda c: c['likes'] + c['vues'], reverse=True)[:5]
from collections import Counter

def calculer_stats(contenus):
    total_vues = sum(c['vues'] for c in contenus)
    total_likes = sum(c['likes'] for c in contenus)
    total_contenus = len(contenus)

    return {
        'total_contenus': total_contenus,
        'total_vues': total_vues,
        'total_likes': total_likes,
        'moyenne_vues': (total_vues / total_contenus) if total_contenus else 0,  # ✅ ajouté
        'taux_engagement': (total_likes / total_vues * 100) if total_vues else 0  # ✅ renommé
    }


def top_contenus(contenus):
    return sorted(contenus, key=lambda c: c['likes'] + c['vues'], reverse=True)[:5]


def tags_populaires(contenus):
    all_words = []
    for c in contenus:
        all_words.extend(c['contenu'].split())

    return Counter(all_words).most_common(5)

def tags_populaires(contenus):
    all_words = []
    for c in contenus:
        all_words.extend(c['contenu'].split())

    return Counter(all_words).most_common(5)