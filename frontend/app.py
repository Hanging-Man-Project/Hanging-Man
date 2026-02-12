import streamlit as st
import requests
import time

# Configuration de la page
st.set_page_config(
    page_title="Jeu du Pendu",
    page_icon="🎮",
    layout="centered"
)

# URL de l'API (utilise le nom du service Docker)
API_URL = "http://proxy:8080"

# Styles CSS personnalisés
st.markdown("""
    <style>
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        text-align: center;
        letter-spacing: 10px;
        color: #1f77b4;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 20px 0;
    }
    .win {
        background-color: #d4edda;
        color: #155724;
    }
    .lose {
        background-color: #f8d7da;
        color: #721c24;
    }
    .in-progress {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .letter-button {
        margin: 5px;
        padding: 10px 20px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Fonction pour dessiner le pendu
def draw_hangman(attempts_left, max_attempts=6):
    stages = [
        """
        ═══════╗
        ║     ║
        ║     O
        ║    /|\\
        ║    / \\
        ║
        """,
        """
        ═══════╗
        ║     ║
        ║     O
        ║    /|\\
        ║    /
        ║
        """,
        """
        ═══════╗
        ║     ║
        ║     O
        ║    /|\\
        ║
        ║
        """,
        """
        ═══════╗
        ║     ║
        ║     O
        ║    /|
        ║
        ║
        """,
        """
        ═══════╗
        ║     ║
        ║     O
        ║     |
        ║
        ║
        """,
        """
        ═══════╗
        ║     ║
        ║     O
        ║
        ║
        ║
        """,
        """
        ═══════╗
        ║     ║
        ║
        ║
        ║
        ║
        """
    ]
    
    stage_index = max_attempts - attempts_left
    if stage_index >= len(stages):
        stage_index = 0
    elif stage_index < 0:
        stage_index = len(stages) - 1
    
    return stages[stage_index]

# Initialisation de la session
if 'game_id' not in st.session_state:
    st.session_state.game_id = None
if 'game_status' not in st.session_state:
    st.session_state.game_status = None

# Titre
st.title("🎮 Jeu du Pendu")
st.markdown("---")

# Sidebar avec instructions
with st.sidebar:
    st.header("📖 Instructions")
    st.write("""
    1. Cliquez sur **Nouvelle Partie** pour commencer
    2. Devinez les lettres en cliquant sur les boutons
    3. Vous avez **6 tentatives**
    4. Bonne chance ! 🍀
    """)
    
    st.markdown("---")
    st.header("📊 Statistiques")
    
    try:
        response = requests.get(f"{API_URL}/games")
        if response.status_code == 200:
            data = response.json()
            st.metric("Parties actives", data["total_games"])
    except:
        st.error("API non disponible")

# Bouton Nouvelle Partie
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎲 Nouvelle Partie", type="primary", use_container_width=True):
        try:
            response = requests.post(f"{API_URL}/start")
            if response.status_code == 200:
                st.session_state.game_status = response.json()
                st.session_state.game_id = st.session_state.game_status['game_id']
                st.rerun()
            else:
                st.error("Erreur lors du démarrage de la partie")
        except Exception as e:
            st.error(f"Impossible de contacter l'API : {e}")

st.markdown("---")

# Affichage du jeu
if st.session_state.game_status:
    game = st.session_state.game_status
    
    # Dessiner le pendu
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.code(draw_hangman(game['attempts_left']), language=None)
    
    with col2:
        # Affichage du mot
        st.markdown(f'<p class="big-font">{game["letters"]}</p>', unsafe_allow_html=True)
        
        # Tentatives restantes
        st.progress(game['attempts_left'] / 6)
        st.write(f"❤️ Tentatives restantes : **{game['attempts_left']}/6**")
        
        # Lettres déjà devinées
        if game['guessed_letters']:
            st.write(f"🔤 Lettres utilisées : **{', '.join(sorted(game['guessed_letters']))}**")
    
    st.markdown("---")
    
    # Statut de la partie
    if game['status'] == 'won':
        st.markdown('<div class="status-box win">🎉 Bravo ! Vous avez gagné ! 🎉</div>', unsafe_allow_html=True)
        st.balloons()
    elif game['status'] == 'lost':
        st.markdown('<div class="status-box lose">😢 Perdu ! Le mot était révélé ci-dessus</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-box in-progress">🎯 Partie en cours...</div>', unsafe_allow_html=True)
        
        # Clavier virtuel
        st.subheader("Choisissez une lettre :")
        
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        guessed = set(game['guessed_letters'])
        
        # Affichage du clavier en 3 rangées
        row1 = alphabet[:9]
        row2 = alphabet[9:18]
        row3 = alphabet[18:]
        
        for row in [row1, row2, row3]:
            cols = st.columns(len(row))
            for idx, letter in enumerate(row):
                with cols[idx]:
                    disabled = letter in guessed
                    if st.button(
                        letter,
                        key=f"btn_{letter}",
                        disabled=disabled,
                        use_container_width=True
                    ):
                        try:
                            response = requests.post(
                                f"{API_URL}/guess",
                                json={
                                    "game_id": st.session_state.game_id,
                                    "letter": letter
                                }
                            )
                            if response.status_code == 200:
                                st.session_state.game_status = response.json()
                                st.rerun()
                            else:
                                st.error(f"Erreur : {response.json().get('detail', 'Erreur inconnue')}")
                        except Exception as e:
                            st.error(f"Erreur : {e}")

else:
    # Écran d'accueil
    st.info("👆 Cliquez sur **Nouvelle Partie** pour commencer à jouer !")
    
    # Affichage du pendu vide
    st.code(draw_hangman(6), language=None)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Made with ❤️ using Streamlit & FastAPI</div>",
    unsafe_allow_html=True
)
