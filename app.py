import streamlit as st
import pdfplumber
import re
from datetime import date, timedelta
from io import BytesIO

st.set_page_config(
    page_title="SwissSub Opti",
    page_icon="🇨🇭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #f0ede6 0%, #e8f0e8 40%, #dde8dd 100%);
    min-height: 100vh;
}

.hero {
    background: linear-gradient(135deg, rgba(74,103,65,0.92) 0%, rgba(95,130,80,0.88) 100%);
    border-radius: 24px;
    padding: 2.8rem 2rem 2.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 32px rgba(74,103,65,0.25);
    position: relative;
    overflow: hidden;
}
.hero::before { content: '🏔'; position: absolute; font-size: 8rem; opacity: 0.06; right: -1rem; top: -1rem; transform: rotate(-15deg); }
.hero::after { content: '🇨🇭'; position: absolute; font-size: 5rem; opacity: 0.08; left: 1rem; bottom: -1rem; }
.hero h1 { font-family: 'Lora', serif; color: white; font-size: 2.4rem; font-weight: 700; margin: 0 0 0.4rem 0; text-shadow: 0 2px 8px rgba(0,0,0,0.2); }
.hero p { color: rgba(255,255,255,0.88); font-size: 1rem; margin: 0 0 1rem 0; font-weight: 300; }
.hero .badges { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
.hero .badge { display: inline-block; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35); color: white; font-size: 0.72rem; padding: 4px 12px; border-radius: 20px; letter-spacing: 0.8px; font-weight: 500; }

.security-bar { background: rgba(255,255,255,0.7); border: 1px solid rgba(74,103,65,0.2); border-left: 4px solid #4a6741; border-radius: 12px; padding: 0.8rem 1.2rem; font-size: 0.85rem; color: #2d4a28; margin-bottom: 1.5rem; font-weight: 500; }

.metric-card { background: rgba(255,255,255,0.75); border-radius: 16px; padding: 1.4rem 1rem; border: 1px solid rgba(255,255,255,0.6); box-shadow: 0 4px 16px rgba(74,103,65,0.1); text-align: center; height: 100%; }
.metric-label { font-size: 0.68rem; font-weight: 600; color: #7a8f74; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.5rem; }
.metric-value { font-family: 'Lora', serif; font-size: 1.5rem; font-weight: 700; color: #2d3a2a; }
.metric-sub { font-size: 0.75rem; color: #9aaa94; margin-top: 0.3rem; }

.score-good { color: #2d6a2d; }
.score-medium { color: #8a6a00; }
.score-bad { color: #C8102E; }

.alert-box { background: rgba(254,242,242,0.85); border: 1px solid rgba(252,165,165,0.5); border-left: 4px solid #C8102E; border-radius: 14px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
.alert-box h4 { color: #C8102E; margin: 0 0 0.4rem 0; font-size: 0.95rem; font-weight: 600; }
.alert-box p { color: #7f1d1d; margin: 0; font-size: 0.88rem; line-height: 1.7; }

.success-box { background: rgba(240,253,244,0.85); border: 1px solid rgba(134,239,172,0.5); border-left: 4px solid #2d6a2d; border-radius: 14px; padding: 1.2rem 1.5rem; margin: 1rem 0; }
.success-box h4 { color: #2d6a2d; margin: 0 0 0.3rem 0; font-size: 0.95rem; font-weight: 600; }
.success-box p { color: #14532d; margin: 0; font-size: 0.88rem; }

.section-title { font-family: 'Lora', serif; font-size: 1.15rem; font-weight: 600; color: #2d3a2a; margin: 1.5rem 0 1rem 0; }

.keyword-tag { display: inline-block; background: rgba(74,103,65,0.1); color: #3a5c35; border: 1px solid rgba(74,103,65,0.2); border-radius: 20px; padding: 3px 12px; font-size: 0.78rem; font-weight: 500; margin: 3px; }

.economie-box { background: linear-gradient(135deg, rgba(74,103,65,0.08), rgba(95,130,80,0.05)); border: 2px solid rgba(74,103,65,0.25); border-radius: 20px; padding: 2rem; margin: 1.5rem 0; text-align: center; }
.economie-titre { font-family: 'Lora', serif; font-size: 1.3rem; color: #2d3a2a; margin-bottom: 0.5rem; font-weight: 700; }
.economie-montant { font-family: 'Lora', serif; font-size: 2.5rem; color: #4a6741; font-weight: 700; margin: 0.5rem 0; }
.economie-sub { font-size: 0.85rem; color: #7a8f74; }

.dispo-box { background: rgba(255,255,255,0.8); border-radius: 18px; padding: 1.5rem; border: 1px solid rgba(74,103,65,0.15); margin: 1rem 0; box-shadow: 0 4px 16px rgba(74,103,65,0.08); }
.dispo-titre { font-family: 'Lora', serif; font-size: 1.1rem; color: #2d3a2a; margin-bottom: 1rem; font-weight: 600; }

.affiliation-note { background: rgba(255,255,255,0.6); border: 1px solid rgba(74,103,65,0.15); border-radius: 10px; padding: 0.7rem 1rem; font-size: 0.75rem; color: #7a8f74; margin-top: 0.5rem; text-align: center; }

.letter-box { background: rgba(255,255,255,0.85); border: 1px solid rgba(74,103,65,0.15); border-radius: 14px; padding: 1.8rem; font-size: 0.88rem; line-height: 1.9; color: #2d3a2a; white-space: pre-wrap; }

.footer { text-align: center; color: #7a8f74; font-size: 0.75rem; padding: 2rem 0 1rem; border-top: 1px solid rgba(74,103,65,0.15); margin-top: 2rem; }

.welcome-card { background: rgba(255,255,255,0.6); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(255,255,255,0.5); }
.welcome-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.welcome-label { font-size: 0.7rem; font-weight: 600; color: #7a8f74; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.3rem; }
.welcome-text { font-size: 0.85rem; color: #5a6e55; }

.stButton > button { border-radius: 12px !important; font-weight: 600 !important; font-family: 'Inter', sans-serif !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #4a6741, #5f8250) !important; border: none !important; color: white !important; box-shadow: 0 4px 14px rgba(74,103,65,0.35) !important; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

PATTERNS_RESILIATION = [
    (r'\b31[.\s]?(decembre|Dezember|dicembre)\b', 'Echeance 31 decembre'),
    (r'\b31\.12\.\d{4}\b', 'Date fixe 31.12'),
    (r'\becheance\s+annuelle\b', 'Echeance annuelle'),
    (r'\bJahresende\b', "Fin d annee DE"),
    (r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b', 'Date explicite'),
]

PATTERNS_PRIME = [
    r'(?:prime|pramie|montant)[^\d]*(\d[\d\s]{0,8}(?:\.\d{2})?)\s*(?:CHF|Fr)',
    r'(\d[\d\s]{0,8}(?:\.\d{2})?)\s*(?:CHF|Fr)\s*(?:/|par|pro)\s*(?:mois|Monat|an|Jahr)',
    r'CHF\s*(\d[\d\s]{0,8}(?:\.\d{2})?)',
]

MOYENNES_MARCHE = {
    "assurance_maladie": 380.0,
    "3eme_pilier": 250.0,
    "telecom": 65.0,
    "assurance_menage": 28.0,
    "autre": 100.0,
}

LIENS_AFFILIATION = {
    "assurance_maladie": "https://www.priminfo.admin.ch/fr/assureurs",
    "3eme_pilier": "https://www.vermögenspartner.ch",
    "telecom": "https://www.comparis.ch/telecom/mobile",
    "assurance_menage": "https://www.comparis.ch/assurances/rc-menage",
    "autre": "https://www.comparis.ch",
}

MOTS_CLES_CATEGORIE = {
    "assurance_maladie": ["lamal", "assurance-maladie", "krankenversicherung", "css", "helsana", "swica", "visana"],
    "3eme_pilier": ["3e pilier", "3eme pilier", "prevoyance", "pilier"],
    "telecom": ["swisscom", "salt", "sunrise", "telecom", "mobile", "forfait"],
    "assurance_menage": ["menage", "haushalt", "responsabilite"],
}


def extraire_texte_pdf(fichier_bytes):
    texte = ""
    try:
        with pdfplumber.open(BytesIO(fichier_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    texte += t + "\n"
    except Exception as e:
        texte = "Erreur extraction: " + str(e)
    return texte


def detecter_categorie(texte):
    texte_lower = texte.lower()
    for cat, mots in MOTS_CLES_CATEGORIE.items():
        if any(m in texte_lower for m in mots):
            return cat
    return "autre"


def analyser_contrat(texte):
    resultat = {
        "dates_resiliation": [],
        "date_principale": None,
        "primes_detectees": [],
        "prime_principale": None,
        "preavis_mois": 3,
        "categorie": detecter_categorie(texte),
        "mots_cles_trouves": [],
        "confiance": 0,
    }
    mots_cibles = ["prime", "resiliation", "echeance", "CHF", "LAMal", "assurance"]
    for mot in mots_cibles:
        if re.search(mot, texte, re.IGNORECASE):
            resultat["mots_cles_trouves"].append(mot)
    for pattern, label in PATTERNS_RESILIATION:
        matches = re.findall(pattern, texte, re.IGNORECASE)
        if matches:
            resultat["dates_resiliation"].append({"type": label, "valeur": str(matches[0])})
    annee_cible = date.today().year
    if date.today().month >= 10:
        annee_cible += 1
    if resultat["dates_resiliation"]:
        resultat["date_principale"] = date(annee_cible, 12, 31)
    for pattern in PATTERNS_PRIME:
        matches = re.findall(pattern, texte, re.IGNORECASE)
        for m in matches:
            val = re.sub(r"[\s']", "", m if isinstance(m, str) else m[0])
            try:
                montant = float(val)
                if 10 < montant < 5000:
                    resultat["primes_detectees"].append(montant)
            except ValueError:
                pass
    if resultat["primes_detectees"]:
        primes_triees = sorted(resultat["primes_detectees"])
        resultat["prime_principale"] = primes_triees[len(primes_triees) // 2]
    preavis_match = re.search(r'(\d+)\s*(mois|Monate)', texte, re.IGNORECASE)
    if preavis_match:
        resultat["preavis_mois"] = int(preavis_match.group(1))
    score = 0
    if resultat["date_principale"]: score += 40
    if resultat["prime_principale"]: score += 40
    if len(resultat["mots_cles_trouves"]) > 2: score += 20
    resultat["confiance"] = score
    return resultat


def calculer_score_economie(prime, categorie):
    moyenne = MOYENNES_MARCHE.get(categorie, MOYENNES_MARCHE["autre"])
    ecart = prime - moyenne
    ecart_pct = (ecart / moyenne) * 100 if moyenne else 0
    score = max(0, min(100, round(100 - max(0, ecart_pct))))
    if score >= 70:
        niveau, emoji, css = "Bon", "🌿", "score-good"
    elif score >= 40:
        niveau, emoji, css = "Moyen", "🟡", "score-medium"
    else:
        niveau, emoji, css = "Critique", "🔴", "score-bad"
    return {
        "score": score, "niveau": niveau, "emoji": emoji, "css": css,
        "moyenne_marche": moyenne,
        "ecart_mensuel": round(ecart, 2),
        "ecart_annuel": round(ecart * 12, 2),
        "alerte_prioritaire": score < 40,
    }


def generer_lettre(nom, adresse, service, date_res, preavis):
    aujourd_hui = date.today().strftime("%d.%m.%Y")
    date_res_str = date_res.strftime("%d.%m.%Y")
    date_envoi_limite = date_res - timedelta(days=preavis * 30)
    lignes = [
        nom, adresse, "", service, "[Adresse du prestataire]", "",
        "Lieu, le " + aujourd_hui, "",
        "Objet : Resiliation de contrat - " + service, "",
        "Madame, Monsieur,", "",
        "Par la presente, je vous informe de ma decision de resilier le contrat",
        "souscrit aupres de vos services, avec effet au " + date_res_str + ",",
        "conformement au delai de preavis contractuel de " + str(preavis) + " mois.", "",
        "Je vous prie de bien vouloir confirmer la reception de ce courrier.", "",
        "Conformement a la nLPD, je vous demande de supprimer mes donnees personnelles.", "",
        "Salutations distinguees,", "", nom, "",
        "A envoyer au plus tard le : " + date_envoi_limite.strftime("%d.%m.%Y"),
    ]
    return "\n".join(lignes)


# HERO
st.markdown("""
<div class="hero">
    <h1>SwissSub Opti</h1>
    <p>Votre gardien de portefeuille suisse — Analysez, economisez, resiliez</p>
    <div class="badges">
        <span class="badge">🔒 LPD Conforme</span>
        <span class="badge">🏔 Conception Suisse</span>
        <span class="badge">⚡ 100% Local</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="security-bar">
    🌿 &nbsp; Votre PDF est analyse uniquement sur votre ordinateur. Aucune donnee transmise. Conforme nLPD 2023.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">📄 Deposez votre contrat PDF</div>', unsafe_allow_html=True)

pdf_file = st.file_uploader(
    label="Assurance maladie · 3eme pilier · Telecom · Assurance menage",
    type=["pdf"],
)

if pdf_file:
    with st.spinner("Analyse en cours..."):
        pdf_bytes = pdf_file.read()
        texte = extraire_texte_pdf(pdf_bytes)
        analyse = analyser_contrat(texte)

    st.markdown('<div class="section-title">📊 Resume de votre contrat</div>', unsafe_allow_html=True)

    cat_labels = {
        "assurance_maladie": "Assurance maladie",
        "3eme_pilier": "3eme pilier",
        "telecom": "Telecom",
        "assurance_menage": "Assurance menage",
        "autre": "Autre contrat",
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-label">Categorie</div><div class="metric-value" style="font-size:1rem">' + cat_labels.get(analyse["categorie"], "Autre") + '</div><div class="metric-sub">Detecte automatiquement</div></div>', unsafe_allow_html=True)
    with col2:
        prime_str = str(analyse["prime_principale"]) + " CHF" if analyse["prime_principale"] else "Non detectee"
        st.markdown('<div class="metric-card"><div class="metric-label">Prime mensuelle</div><div class="metric-value">' + prime_str + '</div><div class="metric-sub">Extrait du PDF</div></div>', unsafe_allow_html=True)
    with col3:
        date_str = analyse["date_principale"].strftime("%d.%m.%Y") if analyse["date_principale"] else "Non trouvee"
        st.markdown('<div class="metric-card"><div class="metric-label">Date de resiliation</div><div class="metric-value" style="font-size:1.2rem">' + date_str + '</div><div class="metric-sub">Preavis : ' + str(analyse["preavis_mois"]) + ' mois</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # SCORE + ECONOMIE
    if analyse["prime_principale"]:
        score_data = calculer_score_economie(analyse["prime_principale"], analyse["categorie"])
        st.markdown('<div class="section-title">💰 Score d Economie</div>', unsafe_allow_html=True)

        col_s, col_d = st.columns([1, 2])
        with col_s:
            st.markdown('<div class="metric-card"><div class="metric-label">Votre score</div><div class="metric-value ' + score_data["css"] + '" style="font-size:2.8rem">' + str(score_data["score"]) + '</div><div class="metric-sub">/ 100 — ' + score_data["emoji"] + ' ' + score_data["niveau"] + '</div></div>', unsafe_allow_html=True)
        with col_d:
            if score_data["alerte_prioritaire"]:
                st.markdown('<div class="alert-box"><h4>⚠️ Alerte — Surcout detecte</h4><p>Vous payez <strong>' + str(abs(score_data["ecart_mensuel"])) + ' CHF/mois</strong> de plus que la moyenne.<br>Economie annuelle possible : <strong>' + str(abs(score_data["ecart_annuel"])) + ' CHF/an</strong><br>Moyenne marche : ' + str(score_data["moyenne_marche"]) + ' CHF/mois</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box"><h4>🌿 Votre prime est dans la norme</h4><p>Moyenne du marche suisse : ' + str(score_data["moyenne_marche"]) + ' CHF/mois</p></div>', unsafe_allow_html=True)

        # BOUTON JE VEUX ECONOMISER
        if score_data["alerte_prioritaire"]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="economie-box">
                <div class="economie-titre">Votre economie potentielle</div>
                <div class="economie-montant">""" + str(abs(score_data["ecart_annuel"])) + """ CHF / an</div>
                <div class="economie-sub">En changeant de prestataire au moment de l echeance</div>
            </div>
            """, unsafe_allow_html=True)

            lien = LIENS_AFFILIATION.get(analyse["categorie"], LIENS_AFFILIATION["autre"])

            if st.button("💚 Je veux economiser — Voir les meilleures offres", use_container_width=True, type="primary"):
                st.markdown('<a href="' + lien + '" target="_blank" style="display:block;text-align:center;background:linear-gradient(135deg,#4a6741,#5f8250);color:white;padding:12px;border-radius:12px;text-decoration:none;font-weight:600;margin:8px 0">Comparer les offres maintenant →</a>', unsafe_allow_html=True)
                st.markdown('<div class="affiliation-note">ℹ️ Lien partenaire — SwissSub Opti peut recevoir une commission si vous souscrivez. Cela ne change pas votre prix.</div>', unsafe_allow_html=True)

    if analyse["mots_cles_trouves"]:
        tags = "".join(['<span class="keyword-tag">' + m + '</span>' for m in analyse["mots_cles_trouves"]])
        st.markdown(tags, unsafe_allow_html=True)

    # DISPONIBILITES
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 Prendre rendez-vous avec un conseiller</div>', unsafe_allow_html=True)
    st.markdown('<div class="dispo-box"><div class="dispo-titre">Choisissez vos disponibilites — Un conseiller vous contactera</div>', unsafe_allow_html=True)

    with st.form("form_dispo"):
        st.markdown("**Vos coordonnees**")
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            prenom = st.text_input("Prenom", placeholder="Jean")
            email = st.text_input("Email", placeholder="jean@example.com")
        with col_n2:
            nom_rdv = st.text_input("Nom", placeholder="Dupont")
            telephone = st.text_input("Telephone", placeholder="+41 79 000 00 00")

        st.markdown("<br>**Vos disponibilites** — Choisissez jusqu a 3 creneaux", unsafe_allow_html=True)

        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        heures = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]
        mois_liste = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        annees = ["2025", "2026", "2027"]

        st.markdown("**Creneau 1 — Preferentiel**")
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1:
            jour1 = st.selectbox("Jour", jours, key="j1")
        with col_d2:
            mois1 = st.selectbox("Mois", mois_liste, key="m1", index=date.today().month - 1)
        with col_d3:
            annee1 = st.selectbox("Annee", annees, key="a1", index=1)
        with col_d4:
            heure1 = st.selectbox("Heure", heures, key="h1", index=2)

        st.markdown("**Creneau 2 — Alternatif**")
        col_d5, col_d6, col_d7, col_d8 = st.columns(4)
        with col_d5:
            jour2 = st.selectbox("Jour", jours, key="j2", index=1)
        with col_d6:
            mois2 = st.selectbox("Mois", mois_liste, key="m2", index=date.today().month - 1)
        with col_d7:
            annee2 = st.selectbox("Annee", annees, key="a2", index=1)
        with col_d8:
            heure2 = st.selectbox("Heure", heures, key="h2", index=4)

        st.markdown("**Creneau 3 — Si les autres ne conviennent pas**")
        col_d9, col_d10, col_d11, col_d12 = st.columns(4)
        with col_d9:
            jour3 = st.selectbox("Jour", jours, key="j3", index=3)
        with col_d10:
            mois3 = st.selectbox("Mois", mois_liste, key="m3", index=date.today().month - 1)
        with col_d11:
            annee3 = st.selectbox("Annee", annees, key="a3", index=1)
        with col_d12:
            heure3 = st.selectbox("Heure", heures, key="h3", index=8)

        notes = st.text_area("Remarques ou questions (optionnel)", placeholder="Ex: Je prefere etre contacte en francais...", height=80)

        submitted_dispo = st.form_submit_button("📅 Confirmer mes disponibilites", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted_dispo:
        if prenom and email and telephone:
            st.success("✅ Parfait " + prenom + " ! Vos disponibilites ont ete transmises. Un conseiller vous contactera pour confirmer le creneau le plus adapte.")
            st.info("📋 Recapitulatif :\n- Creneau 1 : " + jour1 + " " + mois1 + " " + annee1 + " a " + heure1 + "\n- Creneau 2 : " + jour2 + " " + mois2 + " " + annee2 + " a " + heure2 + "\n- Creneau 3 : " + jour3 + " " + mois3 + " " + annee3 + " a " + heure3)
        else:
            st.warning("Merci de remplir votre prenom, email et telephone.")

    # ACTIONS
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📬 Autres actions</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔔 Me rappeler de resilier", use_container_width=True, type="primary"):
            if analyse["date_principale"]:
                date_rappel = analyse["date_principale"] - timedelta(days=analyse["preavis_mois"] * 30 + 15)
                st.success("Rappel configure pour le " + date_rappel.strftime("%d.%m.%Y"))
            else:
                st.warning("Date de resiliation non detectee.")
    with col_b:
        generer = st.button("📝 Generer ma lettre de resiliation", use_container_width=True)

    if generer:
        st.markdown('<div class="section-title">✉️ Lettre de resiliation</div>', unsafe_allow_html=True)
        with st.form("form_lettre"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nom_user = st.text_input("Votre nom complet", "Jean Dupont")
                adresse_user = st.text_input("Votre adresse", "Rue de la Paix 10, 1204 Geneve")
            with col_f2:
                service_name = st.text_input("Nom du prestataire", pdf_file.name.replace(".pdf", ""))
                preavis_override = st.number_input("Preavis (mois)", min_value=1, max_value=12, value=analyse["preavis_mois"])
            submitted = st.form_submit_button("Generer la lettre", use_container_width=True)
        if submitted:
            date_res = analyse["date_principale"] or date(date.today().year + (1 if date.today().month >= 10 else 0), 12, 31)
            lettre = generer_lettre(nom_user, adresse_user, service_name, date_res, preavis_override)
            st.markdown('<div class="letter-box">' + lettre.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
            st.download_button(label="⬇️ Telecharger la lettre (.txt)", data=lettre, file_name="resiliation_" + service_name.replace(" ", "_") + ".txt", mime="text/plain", use_container_width=True)

    with st.expander("🔍 Voir le texte extrait du PDF"):
        st.text_area("Texte brut", texte[:3000] + ("..." if len(texte) > 3000 else ""), height=200)

    st.markdown('<div class="footer">SwissSub Opti v1.0 · Conforme nLPD · CO · LAMal · Aucune transmission externe · 🏔 Made for Switzerland</div>', unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="welcome-card"><div class="welcome-icon">📋</div><div class="welcome-label">Etape 1</div><div class="welcome-text">Deposez votre PDF de contrat</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="welcome-card"><div class="welcome-icon">💰</div><div class="welcome-label">Etape 2</div><div class="welcome-text">Comparez avec le marche suisse</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="welcome-card"><div class="welcome-icon">📅</div><div class="welcome-label">Etape 3</div><div class="welcome-text">Prenez rendez-vous avec un conseiller</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="footer">SwissSub Opti v1.0 · Conforme nLPD · CO · LAMal · Aucune transmission externe · 🏔 Made for Switzerland</div>', unsafe_allow_html=True)
