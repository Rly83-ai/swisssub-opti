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

TEXTES = {
    "FR": {
        "titre": "SwissSub Opti",
        "sous_titre": "Votre gardien de portefeuille suisse — Analysez, economisez, resiliez",
        "badge1": "LPD Conforme",
        "badge2": "Conception Suisse",
        "badge3": "100% Local",
        "securite": "Votre PDF est analyse uniquement sur votre ordinateur. Aucune donnee transmise. Conforme nLPD 2023.",
        "deposez": "Deposez votre contrat PDF",
        "upload_label": "Cliquez ou glissez votre PDF ici — Assurance maladie · 3eme pilier · Telecom · Assurance menage",
        "analyse": "Analyse en cours...",
        "resume": "Resume de votre contrat",
        "categorie": "Categorie",
        "detecte": "Detecte automatiquement",
        "prime": "Prime mensuelle",
        "extrait": "Extrait du PDF",
        "date_res": "Date de resiliation",
        "preavis": "Preavis",
        "mois": "mois",
        "score": "Score d Economie",
        "votre_score": "Votre score",
        "alerte_titre": "Alerte — Surcout detecte",
        "alerte_texte": "Vous payez",
        "alerte_mois": "CHF/mois de plus que la moyenne.",
        "alerte_annuel": "Economie annuelle possible",
        "alerte_marche": "Moyenne marche",
        "norme_titre": "Votre prime est dans la norme",
        "norme_texte": "Moyenne du marche suisse",
        "economie_titre": "Votre economie potentielle",
        "economie_sub": "En changeant de prestataire au moment de l echeance",
        "btn_economiser": "Je veux economiser — Voir les meilleures offres",
        "comparer": "Comparer les offres maintenant",
        "affiliation_note": "Lien partenaire — SwissSub Opti peut recevoir une commission si vous souscrivez. Cela ne change pas votre prix.",
        "rdv_titre": "Prendre rendez-vous avec un conseiller",
        "rdv_sub": "Choisissez vos disponibilites — Un conseiller vous contactera",
        "vos_coords": "Vos coordonnees",
        "prenom": "Prenom",
        "nom": "Nom",
        "email": "Email",
        "telephone": "Telephone",
        "disponibilites": "Vos disponibilites — Choisissez jusqu a 3 creneaux",
        "creneau1": "Creneau 1 — Preferentiel",
        "creneau2": "Creneau 2 — Alternatif",
        "creneau3": "Creneau 3 — Si les autres ne conviennent pas",
        "jour": "Jour",
        "mois_label": "Mois",
        "annee": "Annee",
        "heure": "Heure",
        "remarques": "Remarques ou questions (optionnel)",
        "remarques_placeholder": "Ex: Je prefere etre contacte en francais...",
        "btn_confirmer": "Confirmer mes disponibilites",
        "confirmation": "Vos disponibilites ont ete transmises. Un conseiller vous contactera.",
        "recap": "Recapitulatif",
        "coords_manquantes": "Merci de remplir votre prenom, email et telephone.",
        "autres_actions": "Autres actions",
        "btn_rappel": "Me rappeler de resilier",
        "rappel_ok": "Rappel configure pour le",
        "rappel_non": "Date de resiliation non detectee.",
        "btn_lettre": "Generer ma lettre de resiliation",
        "lettre_titre": "Lettre de resiliation",
        "nom_complet": "Votre nom complet",
        "adresse": "Votre adresse",
        "prestataire": "Nom du prestataire",
        "preavis_mois": "Preavis (mois)",
        "btn_generer": "Generer la lettre",
        "btn_telecharger": "Telecharger la lettre (.txt)",
        "voir_texte": "Voir le texte extrait du PDF",
        "texte_brut": "Texte brut",
        "footer": "SwissSub Opti v1.0 · Conforme nLPD · CO · LAMal · Aucune transmission externe · Conception Suisse",
        "jours": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
        "mois_liste": ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"],
        "cat_labels": {
            "assurance_maladie": "Assurance maladie",
            "3eme_pilier": "3eme pilier",
            "telecom": "Telecom",
            "assurance_menage": "Assurance menage",
            "autre": "Autre contrat",
        },
        "lettre_objet": "Resiliation de contrat",
        "lettre_corps1": "Par la presente, je vous informe de ma decision de resilier le contrat",
        "lettre_corps2": "souscrit aupres de vos services, avec effet au",
        "lettre_corps3": "conformement au delai de preavis contractuel de",
        "lettre_corps4": "Je vous prie de bien vouloir confirmer la reception de ce courrier.",
        "lettre_corps5": "Conformement a la nLPD, je vous demande de supprimer mes donnees personnelles.",
        "lettre_salut": "Salutations distinguees,",
        "lettre_envoi": "A envoyer au plus tard le",
        "adresse_placeholder": "Rue de la Paix 10, 1204 Geneve",
    },
    "DE": {
        "titre": "SwissSub Opti",
        "sous_titre": "Ihr Schweizer Vertragsmanager — Analysieren, sparen, kundigen",
        "badge1": "DSG Konform",
        "badge2": "Swiss Made",
        "badge3": "100% Lokal",
        "securite": "Ihre PDF wird nur auf Ihrem Computer analysiert. Keine Daten werden ubertragen. Konform mit nDSG 2023.",
        "deposez": "Laden Sie Ihren Vertrag hoch",
        "upload_label": "PDF hier ablegen — Krankenversicherung · 3. Saule · Telekom · Haushaltsversicherung",
        "analyse": "Analyse lauft...",
        "resume": "Zusammenfassung Ihres Vertrags",
        "categorie": "Kategorie",
        "detecte": "Automatisch erkannt",
        "prime": "Monatliche Pramie",
        "extrait": "Aus PDF extrahiert",
        "date_res": "Kundigungsdatum",
        "preavis": "Kundigungsfrist",
        "mois": "Monate",
        "score": "Sparquote",
        "votre_score": "Ihre Punktzahl",
        "alerte_titre": "Warnung — Mehrkosten erkannt",
        "alerte_texte": "Sie zahlen",
        "alerte_mois": "CHF/Monat mehr als der Marktdurchschnitt.",
        "alerte_annuel": "Mogliche Jahrseinsparung",
        "alerte_marche": "Marktdurchschnitt",
        "norme_titre": "Ihre Pramie ist im normalen Bereich",
        "norme_texte": "Schweizer Marktdurchschnitt",
        "economie_titre": "Ihr mogliches Einsparpotenzial",
        "economie_sub": "Beim Wechsel des Anbieters zum Falligkeitsdatum",
        "btn_economiser": "Ich mochte sparen — Beste Angebote anzeigen",
        "comparer": "Angebote jetzt vergleichen",
        "affiliation_note": "Partnerlink — SwissSub Opti kann eine Provision erhalten. Ihr Preis andert sich nicht.",
        "rdv_titre": "Termin mit einem Berater vereinbaren",
        "rdv_sub": "Wahlen Sie Ihre Verfugbarkeit — Ein Berater wird sich bei Ihnen melden",
        "vos_coords": "Ihre Kontaktdaten",
        "prenom": "Vorname",
        "nom": "Nachname",
        "email": "E-Mail",
        "telephone": "Telefon",
        "disponibilites": "Ihre Verfugbarkeit — Wahlen Sie bis zu 3 Termine",
        "creneau1": "Termin 1 — Bevorzugt",
        "creneau2": "Termin 2 — Alternativ",
        "creneau3": "Termin 3 — Falls andere nicht passen",
        "jour": "Tag",
        "mois_label": "Monat",
        "annee": "Jahr",
        "heure": "Uhrzeit",
        "remarques": "Bemerkungen oder Fragen (optional)",
        "remarques_placeholder": "z.B. Ich bevorzuge Deutsch...",
        "btn_confirmer": "Verfugbarkeit bestatigen",
        "confirmation": "Ihre Verfugbarkeit wurde ubermittelt. Ein Berater wird sich melden.",
        "recap": "Zusammenfassung",
        "coords_manquantes": "Bitte Vorname, E-Mail und Telefon ausfullen.",
        "autres_actions": "Weitere Aktionen",
        "btn_rappel": "Kundigungserinnerung setzen",
        "rappel_ok": "Erinnerung gesetzt fur",
        "rappel_non": "Kundigungsdatum nicht erkannt.",
        "btn_lettre": "Kundigungsschreiben erstellen",
        "lettre_titre": "Kundigungsschreiben",
        "nom_complet": "Vollstandiger Name",
        "adresse": "Adresse",
        "prestataire": "Name des Anbieters",
        "preavis_mois": "Kundigungsfrist (Monate)",
        "btn_generer": "Schreiben erstellen",
        "btn_telecharger": "Schreiben herunterladen (.txt)",
        "voir_texte": "Extrahierten Text anzeigen",
        "texte_brut": "Rohtext",
        "footer": "SwissSub Opti v1.0 · nDSG Konform · OR · KVG · Keine externe Ubertragung · Swiss Made",
        "jours": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
        "mois_liste": ["Januar", "Februar", "Marz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
        "cat_labels": {
            "assurance_maladie": "Krankenversicherung",
            "3eme_pilier": "3. Saule",
            "telecom": "Telekommunikation",
            "assurance_menage": "Haushaltsversicherung",
            "autre": "Anderer Vertrag",
        },
        "lettre_objet": "Kundigung des Vertrags",
        "lettre_corps1": "Hiermit teile ich Ihnen mit, dass ich den Vertrag",
        "lettre_corps2": "bei Ihren Diensten mit Wirkung zum",
        "lettre_corps3": "gemas der vertraglichen Kundigungsfrist von",
        "lettre_corps4": "Ich bitte Sie, den Eingang dieses Schreibens zu bestatigen.",
        "lettre_corps5": "Gemas nDSG bitte ich Sie, meine personlichen Daten zu loschen.",
        "lettre_salut": "Freundliche Grusse,",
        "lettre_envoi": "Spatestens senden bis",
        "adresse_placeholder": "Musterstrasse 10, 8001 Zurich",
    },
    "IT": {
        "titre": "SwissSub Opti",
        "sous_titre": "Il vostro gestore di contratti svizzeri — Analizzate, risparmiate, disdette",
        "badge1": "Conforme LPD",
        "badge2": "Prodotto in Svizzera",
        "badge3": "100% Locale",
        "securite": "Il vostro PDF viene analizzato solo sul vostro computer. Nessun dato trasmesso. Conforme nLPD 2023.",
        "deposez": "Caricate il vostro contratto PDF",
        "upload_label": "Trascinate il PDF qui — Assicurazione malattia · 3° pilastro · Telecom · Assicurazione economia domestica",
        "analyse": "Analisi in corso...",
        "resume": "Riepilogo del vostro contratto",
        "categorie": "Categoria",
        "detecte": "Rilevato automaticamente",
        "prime": "Premio mensile",
        "extrait": "Estratto dal PDF",
        "date_res": "Data di disdetta",
        "preavis": "Preavviso",
        "mois": "mesi",
        "score": "Punteggio di risparmio",
        "votre_score": "Il vostro punteggio",
        "alerte_titre": "Avviso — Costo eccessivo rilevato",
        "alerte_texte": "Pagate",
        "alerte_mois": "CHF/mese in piu della media di mercato.",
        "alerte_annuel": "Risparmio annuale possibile",
        "alerte_marche": "Media di mercato",
        "norme_titre": "Il vostro premio e nella norma",
        "norme_texte": "Media del mercato svizzero",
        "economie_titre": "Il vostro potenziale di risparmio",
        "economie_sub": "Cambiando fornitore alla scadenza del contratto",
        "btn_economiser": "Voglio risparmiare — Vedere le migliori offerte",
        "comparer": "Confronta le offerte ora",
        "affiliation_note": "Link partner — SwissSub Opti puo ricevere una commissione. Il vostro prezzo non cambia.",
        "rdv_titre": "Prendere appuntamento con un consulente",
        "rdv_sub": "Scegliete le vostre disponibilita — Un consulente vi contatterà",
        "vos_coords": "I vostri dati di contatto",
        "prenom": "Nome",
        "nom": "Cognome",
        "email": "E-mail",
        "telephone": "Telefono",
        "disponibilites": "Le vostre disponibilita — Scegliete fino a 3 orari",
        "creneau1": "Orario 1 — Preferito",
        "creneau2": "Orario 2 — Alternativo",
        "creneau3": "Orario 3 — Se gli altri non vanno bene",
        "jour": "Giorno",
        "mois_label": "Mese",
        "annee": "Anno",
        "heure": "Ora",
        "remarques": "Osservazioni o domande (facoltativo)",
        "remarques_placeholder": "Es: Preferisco essere contattato in italiano...",
        "btn_confirmer": "Confermare le disponibilita",
        "confirmation": "Le vostre disponibilita sono state trasmesse. Un consulente vi contatterà.",
        "recap": "Riepilogo",
        "coords_manquantes": "Si prega di compilare nome, e-mail e telefono.",
        "autres_actions": "Altre azioni",
        "btn_rappel": "Ricordami di disdire",
        "rappel_ok": "Promemoria impostato per il",
        "rappel_non": "Data di disdetta non trovata.",
        "btn_lettre": "Generare la lettera di disdetta",
        "lettre_titre": "Lettera di disdetta",
        "nom_complet": "Nome completo",
        "adresse": "Indirizzo",
        "prestataire": "Nome del fornitore",
        "preavis_mois": "Preavviso (mesi)",
        "btn_generer": "Generare la lettera",
        "btn_telecharger": "Scaricare la lettera (.txt)",
        "voir_texte": "Visualizzare il testo estratto dal PDF",
        "texte_brut": "Testo grezzo",
        "footer": "SwissSub Opti v1.0 · Conforme nLPD · CO · LAMal · Nessuna trasmissione esterna · Prodotto in Svizzera",
        "jours": ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato"],
        "mois_liste": ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"],
        "cat_labels": {
            "assurance_maladie": "Assicurazione malattia",
            "3eme_pilier": "3° pilastro",
            "telecom": "Telecomunicazioni",
            "assurance_menage": "Assicurazione economia domestica",
            "autre": "Altro contratto",
        },
        "lettre_objet": "Disdetta del contratto",
        "lettre_corps1": "Con la presente vi informo della mia decisione di disdire il contratto",
        "lettre_corps2": "sottoscritto presso i vostri servizi, con effetto dal",
        "lettre_corps3": "conformemente al termine di preavviso contrattuale di",
        "lettre_corps4": "Vi chiedo di confermare la ricezione della presente lettera.",
        "lettre_corps5": "Conformemente alla nLPD, vi chiedo di cancellare i miei dati personali.",
        "lettre_salut": "Distinti saluti,",
        "lettre_envoi": "Da inviare entro il",
        "adresse_placeholder": "Via della Pace 10, 6900 Lugano",
    },
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(160deg, #f0ede6 0%, #e8f0e8 40%, #dde8dd 100%); min-height: 100vh; }
.hero { background: linear-gradient(135deg, rgba(74,103,65,0.92) 0%, rgba(95,130,80,0.88) 100%); border-radius: 24px; padding: 2.8rem 2rem 2.5rem; text-align: center; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 8px 32px rgba(74,103,65,0.25); position: relative; overflow: hidden; }
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
.affiliation-note { background: rgba(255,255,255,0.6); border: 1px solid rgba(74,103,65,0.15); border-radius: 10px; padding: 0.7rem 1rem; font-size: 0.75rem; color: #7a8f74; margin-top: 0.5rem; text-align: center; }
.letter-box { background: rgba(255,255,255,0.85); border: 1px solid rgba(74,103,65,0.15); border-radius: 14px; padding: 1.8rem; font-size: 0.88rem; line-height: 1.9; color: #2d3a2a; white-space: pre-wrap; }
.footer { text-align: center; color: #7a8f74; font-size: 0.75rem; padding: 2rem 0 1rem; border-top: 1px solid rgba(74,103,65,0.15); margin-top: 2rem; }
.welcome-card { background: rgba(255,255,255,0.6); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(255,255,255,0.5); }
.lang-selector { display: flex; justify-content: flex-end; gap: 8px; margin-bottom: 1rem; }
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
    r'(?:prime|pramie|montant|premio)[^\d]*(\d[\d\s]{0,8}(?:\.\d{2})?)\s*(?:CHF|Fr)',
    r'(\d[\d\s]{0,8}(?:\.\d{2})?)\s*(?:CHF|Fr)\s*(?:/|par|pro|al)\s*(?:mois|Monat|mese|an|Jahr|anno)',
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
    "3eme_pilier": "https://www.comparis.ch/vorsorge",
    "telecom": "https://www.comparis.ch/telecom/mobile",
    "assurance_menage": "https://www.comparis.ch/assurances/rc-menage",
    "autre": "https://www.comparis.ch",
}

MOTS_CLES_CATEGORIE = {
    "assurance_maladie": ["lamal", "assurance-maladie", "krankenversicherung", "css", "helsana", "swica", "visana", "assicurazione malattia"],
    "3eme_pilier": ["3e pilier", "3eme pilier", "prevoyance", "pilier", "3. saule", "terzo pilastro"],
    "telecom": ["swisscom", "salt", "sunrise", "telecom", "mobile", "forfait"],
    "assurance_menage": ["menage", "haushalt", "responsabilite", "economia domestica"],
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
        texte = "Erreur: " + str(e)
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
    mots_cibles = ["prime", "pramie", "premio", "resiliation", "kundigung", "disdetta", "echeance", "CHF", "LAMal", "assurance"]
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
    preavis_match = re.search(r'(\d+)\s*(mois|Monate|mesi)', texte, re.IGNORECASE)
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


def generer_lettre(t, nom, adresse, service, date_res, preavis):
    aujourd_hui = date.today().strftime("%d.%m.%Y")
    date_res_str = date_res.strftime("%d.%m.%Y")
    date_envoi_limite = date_res - timedelta(days=preavis * 30)
    lignes = [
        nom, adresse, "", service, "[" + t["adresse"] + " du prestataire]", "",
        "Lieu, le " + aujourd_hui, "",
        t["lettre_objet"] + " - " + service, "",
        t["lettre_salut"].replace(",", "").strip() + ",", "",
        t["lettre_corps1"],
        t["lettre_corps2"] + " " + date_res_str + ",",
        t["lettre_corps3"] + " " + str(preavis) + " " + t["mois"] + ".", "",
        t["lettre_corps4"], "",
        t["lettre_corps5"], "",
        t["lettre_salut"], "", nom, "",
        t["lettre_envoi"] + " : " + date_envoi_limite.strftime("%d.%m.%Y"),
    ]
    return "\n".join(lignes)


# SELECTEUR DE LANGUE
col_lang = st.columns([4, 1, 1, 1])
with col_lang[1]:
    if st.button("🇫🇷 FR", use_container_width=True):
        st.session_state["langue"] = "FR"
with col_lang[2]:
    if st.button("🇩🇪 DE", use_container_width=True):
        st.session_state["langue"] = "DE"
with col_lang[3]:
    if st.button("🇮🇹 IT", use_container_width=True):
        st.session_state["langue"] = "IT"

if "langue" not in st.session_state:
    st.session_state["langue"] = "FR"

t = TEXTES[st.session_state["langue"]]

# HERO
st.markdown("""
<div class="hero">
    <h1>""" + t["titre"] + """</h1>
    <p>""" + t["sous_titre"] + """</p>
    <div class="badges">
        <span class="badge">🔒 """ + t["badge1"] + """</span>
        <span class="badge">🏔 """ + t["badge2"] + """</span>
        <span class="badge">⚡ """ + t["badge3"] + """</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="security-bar">🌿 &nbsp;' + t["securite"] + '</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📄 ' + t["deposez"] + '</div>', unsafe_allow_html=True)

pdf_file = st.file_uploader(label=t["upload_label"], type=["pdf"])

if pdf_file:
    with st.spinner(t["analyse"]):
        pdf_bytes = pdf_file.read()
        texte = extraire_texte_pdf(pdf_bytes)
        analyse = analyser_contrat(texte)

    st.markdown('<div class="section-title">📊 ' + t["resume"] + '</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-label">' + t["categorie"] + '</div><div class="metric-value" style="font-size:1rem">' + t["cat_labels"].get(analyse["categorie"], "Autre") + '</div><div class="metric-sub">' + t["detecte"] + '</div></div>', unsafe_allow_html=True)
    with col2:
        prime_str = str(analyse["prime_principale"]) + " CHF" if analyse["prime_principale"] else "-"
        st.markdown('<div class="metric-card"><div class="metric-label">' + t["prime"] + '</div><div class="metric-value">' + prime_str + '</div><div class="metric-sub">' + t["extrait"] + '</div></div>', unsafe_allow_html=True)
    with col3:
        date_str = analyse["date_principale"].strftime("%d.%m.%Y") if analyse["date_principale"] else "-"
        st.markdown('<div class="metric-card"><div class="metric-label">' + t["date_res"] + '</div><div class="metric-value" style="font-size:1.2rem">' + date_str + '</div><div class="metric-sub">' + t["preavis"] + ' : ' + str(analyse["preavis_mois"]) + ' ' + t["mois"] + '</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if analyse["prime_principale"]:
        score_data = calculer_score_economie(analyse["prime_principale"], analyse["categorie"])
        st.markdown('<div class="section-title">💰 ' + t["score"] + '</div>', unsafe_allow_html=True)
        col_s, col_d = st.columns([1, 2])
        with col_s:
            st.markdown('<div class="metric-card"><div class="metric-label">' + t["votre_score"] + '</div><div class="metric-value ' + score_data["css"] + '" style="font-size:2.8rem">' + str(score_data["score"]) + '</div><div class="metric-sub">/ 100 — ' + score_data["emoji"] + ' ' + score_data["niveau"] + '</div></div>', unsafe_allow_html=True)
        with col_d:
            if score_data["alerte_prioritaire"]:
                st.markdown('<div class="alert-box"><h4>⚠️ ' + t["alerte_titre"] + '</h4><p>' + t["alerte_texte"] + ' <strong>' + str(abs(score_data["ecart_mensuel"])) + ' ' + t["alerte_mois"] + '</strong><br>' + t["alerte_annuel"] + ' : <strong>' + str(abs(score_data["ecart_annuel"])) + ' CHF</strong><br>' + t["alerte_marche"] + ' : ' + str(score_data["moyenne_marche"]) + ' CHF</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box"><h4>🌿 ' + t["norme_titre"] + '</h4><p>' + t["norme_texte"] + ' : ' + str(score_data["moyenne_marche"]) + ' CHF</p></div>', unsafe_allow_html=True)

        if score_data["alerte_prioritaire"]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="economie-box"><div class="economie-titre">' + t["economie_titre"] + '</div><div class="economie-montant">' + str(abs(score_data["ecart_annuel"])) + ' CHF / an</div><div class="economie-sub">' + t["economie_sub"] + '</div></div>', unsafe_allow_html=True)
            lien = LIENS_AFFILIATION.get(analyse["categorie"], LIENS_AFFILIATION["autre"])
            if st.button("💚 " + t["btn_economiser"], use_container_width=True, type="primary"):
                st.markdown('<a href="' + lien + '" target="_blank" style="display:block;text-align:center;background:linear-gradient(135deg,#4a6741,#5f8250);color:white;padding:12px;border-radius:12px;text-decoration:none;font-weight:600;margin:8px 0">' + t["comparer"] + ' →</a>', unsafe_allow_html=True)
                st.markdown('<div class="affiliation-note">ℹ️ ' + t["affiliation_note"] + '</div>', unsafe_allow_html=True)

    if analyse["mots_cles_trouves"]:
        tags = "".join(['<span class="keyword-tag">' + m + '</span>' for m in analyse["mots_cles_trouves"]])
        st.markdown(tags, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 ' + t["rdv_titre"] + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="dispo-box"><div style="font-family:Lora,serif;font-size:1.1rem;color:#2d3a2a;margin-bottom:1rem;font-weight:600">' + t["rdv_sub"] + '</div>', unsafe_allow_html=True)

    with st.form("form_dispo"):
        st.markdown("**" + t["vos_coords"] + "**")
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            prenom = st.text_input(t["prenom"], placeholder="Jean")
            email = st.text_input(t["email"], placeholder="jean@example.com")
        with col_n2:
            nom_rdv = st.text_input(t["nom"], placeholder="Dupont")
            telephone = st.text_input(t["telephone"], placeholder="+41 79 000 00 00")

        st.markdown("**" + t["disponibilites"] + "**")
        heures = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00"]
        annees = ["2025", "2026", "2027"]

        st.markdown("**" + t["creneau1"] + "**")
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1: jour1 = st.selectbox(t["jour"], t["jours"], key="j1")
        with col_d2: mois1 = st.selectbox(t["mois_label"], t["mois_liste"], key="m1", index=date.today().month-1)
        with col_d3: annee1 = st.selectbox(t["annee"], annees, key="a1", index=1)
        with col_d4: heure1 = st.selectbox(t["heure"], heures, key="h1", index=2)

        st.markdown("**" + t["creneau2"] + "**")
        col_d5, col_d6, col_d7, col_d8 = st.columns(4)
        with col_d5: jour2 = st.selectbox(t["jour"], t["jours"], key="j2", index=1)
        with col_d6: mois2 = st.selectbox(t["mois_label"], t["mois_liste"], key="m2", index=date.today().month-1)
        with col_d7: annee2 = st.selectbox(t["annee"], annees, key="a2", index=1)
        with col_d8: heure2 = st.selectbox(t["heure"], heures, key="h2", index=4)

        st.markdown("**" + t["creneau3"] + "**")
        col_d9, col_d10, col_d11, col_d12 = st.columns(4)
        with col_d9: jour3 = st.selectbox(t["jour"], t["jours"], key="j3", index=3)
        with col_d10: mois3 = st.selectbox(t["mois_label"], t["mois_liste"], key="m3", index=date.today().month-1)
        with col_d11: annee3 = st.selectbox(t["annee"], annees, key="a3", index=1)
        with col_d12: heure3 = st.selectbox(t["heure"], heures, key="h3", index=8)

        notes = st.text_area(t["remarques"], placeholder=t["remarques_placeholder"], height=80)
        submitted_dispo = st.form_submit_button(t["btn_confirmer"], use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted_dispo:
        if prenom and email and telephone:
            st.success("✅ " + prenom + " — " + t["confirmation"])
            st.info(t["recap"] + " :\n- " + t["creneau1"] + " : " + jour1 + " " + mois1 + " " + annee1 + " " + heure1 + "\n- " + t["creneau2"] + " : " + jour2 + " " + mois2 + " " + annee2 + " " + heure2 + "\n- " + t["creneau3"] + " : " + jour3 + " " + mois3 + " " + annee3 + " " + heure3)
        else:
            st.warning(t["coords_manquantes"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📬 ' + t["autres_actions"] + '</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔔 " + t["btn_rappel"], use_container_width=True, type="primary"):
            if analyse["date_principale"]:
                date_rappel = analyse["date_principale"] - timedelta(days=analyse["preavis_mois"] * 30 + 15)
                st.success(t["rappel_ok"] + " " + date_rappel.strftime("%d.%m.%Y"))
            else:
                st.warning(t["rappel_non"])
    with col_b:
        generer = st.button("📝 " + t["btn_lettre"], use_container_width=True)

    if generer:
        st.markdown('<div class="section-title">✉️ ' + t["lettre_titre"] + '</div>', unsafe_allow_html=True)
        with st.form("form_lettre"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                nom_user = st.text_input(t["nom_complet"], "Jean Dupont")
                adresse_user = st.text_input(t["adresse"], t["adresse_placeholder"])
            with col_f2:
                service_name = st.text_input(t["prestataire"], pdf_file.name.replace(".pdf",""))
                preavis_override = st.number_input(t["preavis_mois"], min_value=1, max_value=12, value=analyse["preavis_mois"])
            submitted = st.form_submit_button(t["btn_generer"], use_container_width=True)
        if submitted:
            date_res = analyse["date_principale"] or date(date.today().year+(1 if date.today().month>=10 else 0),12,31)
            lettre = generer_lettre(t, nom_user, adresse_user, service_name, date_res, preavis_override)
            st.markdown('<div class="letter-box">' + lettre.replace("\n","<br>") + '</div>', unsafe_allow_html=True)
            st.download_button(label="⬇️ " + t["btn_telecharger"], data=lettre, file_name="resiliation_" + service_name.replace(" ","_") + ".txt", mime="text/plain", use_container_width=True)

    with st.expander("🔍 " + t["voir_texte"]):
        st.text_area(t["texte_brut"], texte[:3000] + ("..." if len(texte)>3000 else ""), height=200)

    st.markdown('<div class="footer">' + t["footer"] + '</div>', unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="welcome-card"><div style="font-size:2rem">📋</div><div style="font-size:0.7rem;font-weight:600;color:#7a8f74;letter-spacing:1.5px;text-transform:uppercase;margin:0.5rem 0">Etape 1</div><div style="font-size:0.85rem;color:#5a6e55">' + t["deposez"] + '</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="welcome-card"><div style="font-size:2rem">💰</div><div style="font-size:0.7rem;font-weight:600;color:#7a8f74;letter-spacing:1.5px;text-transform:uppercase;margin:0.5rem 0">Etape 2</div><div style="font-size:0.85rem;color:#5a6e55">' + t["score"] + '</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="welcome-card"><div style="font-size:2rem">📅</div><div style="font-size:0.7rem;font-weight:600;color:#7a8f74;letter-spacing:1.5px;text-transform:uppercase;margin:0.5rem 0">Etape 3</div><div style="font-size:0.85rem;color:#5a6e55">' + t["rdv_titre"] + '</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">' + t["footer"] + '</div>', unsafe_allow_html=True)
