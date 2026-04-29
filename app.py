from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import data_manager
import ia_engine as ia
import dashboard

app = Flask(__name__)

dm = data_manager.DataManager()
ia_analyzer = ia.IAContentAnalyzer()


def generer_id():
    contenus = dm.lire_tous()
    if not contenus:
        return 1
    return max(c['id'] for c in contenus) + 1


@app.route('/')
def accueil():
    contenus = dm.lire_tous()
    return render_template('accueil.html', contenus=contenus)


@app.route('/contenu/<int:id>')
def voir_contenu(id):
    contenu = dm.trouver_par_id(id)
    if not contenu:
        return "Not found", 404

    contenu['vues'] += 1
    dm.mettre_a_jour(id, contenu)

    tags = ia_analyzer.generer_tags(contenu['contenu'])
    similaires = ia_analyzer.similarite(contenu, dm.lire_tous())

    return render_template(
        'analyse.html',
        contenu=contenu,
        tags=tags,
        similaires=similaires
    )


@app.route('/contenu/nouveau', methods=['GET', 'POST'])
def nouveau_contenu():
    if request.method == 'POST':
        texte = request.form['contenu']

        if ia_analyzer.detect_spam(texte):
            return "Spam détecté"

        nouveau = {
            'id': generer_id(),
            'titre': request.form['titre'],
            'contenu': texte,
            'categorie': request.form['categorie'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'vues': 0,
            'likes': 0
        }

        dm.ajouter(nouveau)
        return redirect(url_for('voir_contenu', id=nouveau['id']))

    return render_template('formulaire.html')


@app.route('/contenu/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_contenu(id):
    contenu = dm.trouver_par_id(id)

    if request.method == 'POST':
        contenu['titre'] = request.form['titre']
        contenu['contenu'] = request.form['contenu']
        contenu['categorie'] = request.form['categorie']
        dm.mettre_a_jour(id, contenu)

        return redirect(url_for('voir_contenu', id=id))

    return render_template('formulaire.html', contenu=contenu)


@app.route('/contenu/supprimer/<int:id>', methods=['POST'])
def supprimer_contenu(id):
    dm.supprimer(id)
    return redirect(url_for('accueil'))


@app.route('/dashboard')
def dashboard_view():
    contenus = dm.lire_tous()

    stats = dashboard.calculer_stats(contenus)
    top = dashboard.top_contenus(contenus)
    tags = dashboard.tags_populaires(contenus)

    return render_template(
        'dashboard.html',
        stats=stats,
        top=top,
        tags=tags
    )


@app.route('/contenu/like/<int:id>', methods=['POST'])
def liker_contenu(id):
    contenu = dm.trouver_par_id(id)
    contenu['likes'] += 1
    dm.mettre_a_jour(id, contenu)

    return redirect(url_for('voir_contenu', id=id))


if __name__ == '__main__':
    app.run(debug=True)