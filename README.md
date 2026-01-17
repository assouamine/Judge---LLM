# 🎓 UPF AI Assistant - LLM-as-a-Judge RAG Evaluation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

**Assistant IA intelligent spécialisé pour l'Université Privée de Fès (UPF), Maroc**

Ce projet implémente un système d'évaluation automatique comparant les réponses **RAG (Retrieval-Augmented Generation)** vs **Non-RAG** en utilisant un **LLM-as-a-Judge**. Spécialisé pour répondre aux questions sur l'UPF avec précision et sources vérifiables.

---

## ✨ Fonctionnalités Principales

- 🤖 **Génération Non-RAG** : Réponses directes du LLM sans contexte
- 📚 **Génération RAG** : Réponses basées sur 77+ KB de documents officiels UPF
- ⚖️ **LLM-as-a-Judge** : Évaluation automatique sur 5 critères (Exactitude, Complétude, Pertinence, Clarté, Ancrage)
- 🌐 **Interface Web Moderne** : Design responsive et élégant en français
- 💻 **Interface CLI** : Alternative en ligne de commande avec formatage riche
- 📊 **Comparaison Visuelle** : Tableau de scores et déclaration du gagnant
- 🎯 **Spécialisé UPF** : Base de connaissances complète sur l'université

---

## 🏛️ Base de Connaissances UPF

### 📄 Documents Inclus (77.6 KB)

1. **Informations Générales** (18.6 KB)
   - Présentation de l'UPF (création 2006, reconnaissance État 2018)
   - 11 structures et facultés
   - 50+ programmes académiques
   - Frais de scolarité détaillés en DH
   - Procédures d'admission
   - Bourses et partenariats internationaux

2. **Détails des Départements** (27.6 KB)
   - Faculté des Sciences de l'Ingénieur (FSI)
   - Fès Business School (FBS)
   - Médecine Dentaire
   - Sciences Paramédicales
   - Architecture
   - American International Institute (AII)

3. **Scénarios Étudiants** (31.4 KB)
   - Processus d'admission détaillé
   - Solutions financières (bourses, crédits)
   - Gestion académique
   - Logement à Fès
   - Recherche de stages

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8 ou supérieur
- Clé API OpenRouter ([obtenir ici](https://openrouter.ai/))

### Installation en 5 Minutes

```bash
# 1. Naviguer vers le projet
cd c:\Users\moham\Desktop\1111

# 2. Activer l'environnement virtuel
.venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install flask openai python-dotenv

# 4. Configurer la clé API
# Éditer .env et ajouter :
# OPENROUTER_API_KEY=votre_clé_api

# 5. Lancer l'application
python app.py

# 6. Ouvrir le navigateur
# http://localhost:5000
```

### 🖥️ Interface CLI (Alternative)

```bash
# Installer les dépendances supplémentaires
pip install rich

# Lancer l'interface terminal
python main.py
```

---

## 📁 Structure du Projet

```
1111/
├── 📄 app.py                      # Serveur Flask (interface web)
├── 📄 main.py                     # Interface CLI
├── 📄 requirements.txt            # Dépendances
├── 🔐 .env                        # Configuration API
│
├── 📂 src/modules/
│   ├── llm_client.py             # Client LLM (OpenRouter)
│   ├── rag_engine.py             # Moteur RAG
│   └── judge.py                  # Évaluateur automatique
│
├── 📂 data/documents/            # Base de connaissances UPF (77.6 KB)
│   ├── university_knowledge_base.txt
│   ├── university_departments_detailed.txt
│   └── university_student_scenarios.txt
│
├── 📂 templates/
│   └── index.html                # Interface web
│
├── 📂 static/
│   ├── style.css                 # Styles
│   └── script.js                 # Logique frontend
│
└── 📂 Documentation/
    ├── README.md                 # Ce fichier
    ├── PROJECT_DESCRIPTION.md    # Description complète
    ├── WEB_INTERFACE_GUIDE.md    # Guide interface web
    ├── PROJECT_GUIDE.md          # Documentation technique
    ├── QUICKSTART.md             # Tutoriel démarrage
    └── EXAMPLE_RESULTS.md        # Exemples de résultats
```

---

## 💡 Exemples d'Utilisation

### Questions Supportées

**Admission et Programmes :**
- "Quels sont les frais de scolarité pour le Génie Informatique ?"
- "Comment s'inscrire à la Faculté de Médecine Dentaire ?"
- "Quelles sont les conditions d'admission pour le Master en IA ?"

**Vie Étudiante :**
- "Où trouver un logement étudiant à Fès ?"
- "Quelles bourses sont disponibles à l'UPF ?"
- "Comment chercher un stage au Maroc ?"

**Informations Pratiques :**
- "Où se trouve l'Université Privée de Fès ?"
- "Quel est le numéro de téléphone de l'UPF ?"
- "L'UPF est-elle reconnue par l'État ?"

### Exemple de Résultat

**Question :** "Combien coûte le Master en Intelligence Artificielle ?"

**Réponse RAG :**
> "Le Master en Intelligence Artificielle et Data Science (IADS) à l'UPF coûte 50 000 DH par an. Ce programme de 2 ans est proposé par la Faculté des Sciences de l'Ingénieur..."

**Évaluation :**
- Exactitude : 10/10
- Complétude : 9/10
- Pertinence : 10/10
- Clarté : 9/10
- Ancrage : 10/10
- **Moyenne : 9.6/10** ✅

---

## 🔧 Configuration

### Fichier `.env`

```env
# Clé API OpenRouter (obligatoire)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# Modèle LLM (optionnel, par défaut : llama-3.1-8b)
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Paramètres de génération
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### Personnalisation

**Modifier le nombre de documents récupérés :**
```python
# Dans src/modules/rag_engine.py, ligne 28
def retrieve(self, query, k=2):  # Changer k=2 à k=3 ou plus
```

**Changer le modèle LLM :**
```python
# Dans src/modules/llm_client.py
self.model = "meta-llama/llama-3.1-70b-instruct"  # Modèle plus puissant
```

---

## 📊 Architecture Technique

### Stack Technologique

**Backend :**
- Python 3.8+
- Flask (serveur web)
- OpenAI SDK (via OpenRouter)
- python-dotenv (configuration)

**Frontend :**
- HTML5 / CSS3
- JavaScript (Vanilla)
- Fetch API

**IA / ML :**
- LLM : Meta Llama 3.1 (via OpenRouter)
- RAG : Recherche par mots-clés (extensible à embeddings vectoriels)
- Évaluation : LLM-as-a-Judge

### Flux de Données

```
Question Utilisateur
    ↓
┌─────────────────────┬─────────────────────┐
│   Non-RAG Path      │     RAG Path        │
│                     │                     │
│  LLM Direct         │  1. Retrieve Docs   │
│  Response           │  2. Format Context  │
│                     │  3. LLM + Context   │
└─────────────────────┴─────────────────────┘
    ↓                       ↓
    └───────────┬───────────┘
                ↓
         LLM-as-a-Judge
         (Évaluation)
                ↓
         Résultats Comparés
         (Interface Web)
```

---

## 🧪 Tests et Validation

### Tests Recommandés

```bash
# Tester l'interface web
python app.py
# Puis ouvrir http://localhost:5000

# Tester l'interface CLI
python main.py

# Exécuter la suite de tests (si disponible)
python test_suite.py
```

### Questions de Test

1. ✅ "Quels sont les frais de scolarité en Génie Civil ?"
2. ✅ "Comment obtenir une bourse à l'UPF ?"
3. ✅ "Où se trouve l'université ?"
4. ✅ "Quels programmes sont en anglais ?"
5. ❌ "Quelle est la capitale de la France ?" (hors contexte)

---

## 📈 Améliorations Futures

### Court Terme
- [ ] Ajouter plus de documents UPF (règlements, calendriers)
- [ ] Implémenter embeddings vectoriels (meilleure recherche)
- [ ] Système de cache pour questions fréquentes
- [ ] Support multilingue (arabe, anglais)

### Moyen Terme
- [ ] Base de données vectorielle (Chroma, FAISS)
- [ ] Dashboard analytics
- [ ] Historique des conversations
- [ ] Authentification utilisateur

### Long Terme
- [ ] Chatbot conversationnel avec mémoire
- [ ] Application mobile
- [ ] Interface vocale
- [ ] Déploiement production (serveur UPF)

---

## 📖 Documentation Complète

| Document | Description |
|----------|-------------|
| **PROJECT_DESCRIPTION.md** | Description complète du projet (architecture, cas d'usage, détails techniques) |
| **WEB_INTERFACE_GUIDE.md** | Guide d'utilisation de l'interface web |
| **PROJECT_GUIDE.md** | Documentation technique approfondie |
| **QUICKSTART.md** | Tutoriel de démarrage rapide |
| **EXAMPLE_RESULTS.md** | Exemples de résultats d'évaluation |

---

## 🤝 Contribution

Ce projet est développé à des fins éducatives et de recherche.

**Pour contribuer :**
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📞 Contact

**Développeur :** Mohammed Azzouzi  
**Institution :** Université Privée de Fès (UPF)  
**Email :** [Votre email]  
**GitHub :** [Votre profil GitHub]  

**Informations Officielles UPF :**
- 🌐 Site Web : [www.upf.ac.ma](https://www.upf.ac.ma)
- 📧 Email : info@upf.ac.ma
- 📞 Téléphone : +212 535 610 320
- 📍 Adresse : Lotissement Quaraouiyine, Route Ain Chkef, Fès 30000, Maroc

---

## 📄 Licence

Ce projet est développé à des fins **éducatives et de recherche**.  
Les informations sur l'UPF sont basées sur des sources publiques.

**Usage :**
- ✅ Démonstration académique
- ✅ Recherche sur le RAG
- ✅ Prototype pour l'UPF
- ❌ Production sans validation officielle UPF

---

## 🙏 Remerciements

- **OpenRouter** : Accès aux modèles LLM
- **Meta AI** : Modèle Llama 3.1
- **UPF** : Informations publiques
- **Communauté Open Source** : Outils et bibliothèques

---

## 🎯 Statut du Projet

✅ **Fonctionnel et Testé**  
📅 **Dernière mise à jour :** 27 Décembre 2024  
🔢 **Version :** 1.0  
🚀 **Prêt pour démonstration**

---

**⭐ Si ce projet vous est utile, n'hésitez pas à le mettre en favoris !**

