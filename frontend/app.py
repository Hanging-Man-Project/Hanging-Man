import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# Page configuration
st.set_page_config(
    page_title="Hanging Man Game",
    page_icon="🎮",
    layout="wide"
)

API_URL = "http://proxy:8080"

# Apple CSS Styles 2026 - Optimized Layout
st.markdown("""
    <style>
    /* Fond général */
    .main {
        background-color: #FBFBFD;
    }
    
    /* Typographie moderne pour le mot - Épuré */
    .word-display {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
        font-size: 36px;
        font-weight: 300;
        text-align: center;
        letter-spacing: 16px;
        color: #1D1D1F;
        margin: 12px 0;
        padding: 20px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        white-space: nowrap;
        overflow-x: auto;
    }
    
    /* Scrollbar minimaliste pour le mot */
    .word-display::-webkit-scrollbar {
        height: 4px;
    }
    .word-display::-webkit-scrollbar-track {
        background: transparent;
    }
    .word-display::-webkit-scrollbar-thumb {
        background: #E5E5EA;
        border-radius: 2px;
    }
    
    /* Cartes Bento */
    .bento-card {
        background: white;
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        margin-bottom: 10px;
    }
    
    /* Status boxes minimalistes */
    .status-box {
        padding: 14px;
        border-radius: 16px;
        text-align: center;
        font-size: 15px;
        font-weight: 500;
        margin: 12px 0;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .win {
        background-color: rgba(94, 92, 230, 0.08);
        color: #5E5CE6;
        border: 1px solid rgba(94, 92, 230, 0.2);
    }
    .lose {
        background-color: rgba(255, 59, 48, 0.08);
        color: #FF3B30;
        border: 1px solid rgba(255, 59, 48, 0.2);
    }
    .in-progress {
        background-color: rgba(94, 92, 230, 0.05);
        color: #5E5CE6;
        border: 1px solid rgba(94, 92, 230, 0.15);
    }
    
    /* Boutons Streamlit personnalisés */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #E5E5EA;
        background-color: white;
        color: #1D1D1F;
        font-weight: 500;
        transition: all 0.2s;
        padding: 6px 10px;
        font-size: 13px;
        min-height: 34px;
    }
    .stButton > button:hover {
        background-color: #5E5CE6;
        color: white;
        border-color: #5E5CE6;
        box-shadow: 0 2px 8px rgba(94, 92, 230, 0.2);
    }
    .stButton > button[disabled] {
        background-color: #F5F5F7;
        color: #C7C7CC;
        border-color: #E5E5EA;
    }
    
    /* Espacement général optimal */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1100px;
    }
    
    /* Progress bar indigo */
    .stProgress > div > div > div {
        background-color: #5E5CE6;
    }
    
    /* Réduction espaces entre éléments */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Function to draw hangman in minimalist SVG
def draw_hangman_svg(attempts_left, max_attempts=6):
    stages_errors = max_attempts - attempts_left
    
    html_content = '''
    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <svg width="180" height="220" viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg">
            <style>
                .hangman-line { stroke: #5E5CE6; stroke-width: 2; stroke-linecap: round; fill: none; }
                .hangman-circle { stroke: #5E5CE6; stroke-width: 2; fill: none; }
            </style>
            
            <!-- Base -->
            <line x1="20" y1="230" x2="100" y2="230" class="hangman-line"/>
            <!-- Poteau vertical -->
            <line x1="60" y1="230" x2="60" y2="20" class="hangman-line"/>
            <!-- Poteau horizontal -->
            <line x1="60" y1="20" x2="140" y2="20" class="hangman-line"/>
            <!-- Corde -->
            <line x1="140" y1="20" x2="140" y2="50" class="hangman-line"/>
    '''
    
    if stages_errors >= 1:
        # Head
        html_content += '<circle cx="140" cy="70" r="20" class="hangman-circle"/>'
    if stages_errors >= 2:
        # Body
        html_content += '<line x1="140" y1="90" x2="140" y2="150" class="hangman-line"/>'
    if stages_errors >= 3:
        # Left arm
        html_content += '<line x1="140" y1="110" x2="110" y2="130" class="hangman-line"/>'
    if stages_errors >= 4:
        # Right arm
        html_content += '<line x1="140" y1="110" x2="170" y2="130" class="hangman-line"/>'
    if stages_errors >= 5:
        # Left leg
        html_content += '<line x1="140" y1="150" x2="120" y2="190" class="hangman-line"/>'
    if stages_errors >= 6:
        # Right leg
        html_content += '<line x1="140" y1="150" x2="160" y2="190" class="hangman-line"/>'
    
    html_content += '</svg></div>'
    return html_content

# Session initialization
if 'game_id' not in st.session_state:
    st.session_state.game_id = None
if 'game_status' not in st.session_state:
    st.session_state.game_status = None

# Title centered
st.markdown('<h1 style="text-align: center; color: #1D1D1F; font-weight: 600; font-size: 28px; margin-bottom: 12px; margin-top: 0;">Jeu du Pendu</h1>', unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.markdown('<div style="padding: 12px;">', unsafe_allow_html=True)
    st.header("Instructions")
    st.write("""
    Cliquez sur **Nouvelle Partie** pour commencer
    
    Devinez les lettres en cliquant sur les boutons
    
    Vous avez **6 tentatives**
    """)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    st.header("Statistiques")
    
    try:
        response = requests.get(f"{API_URL}/games")
        if response.status_code == 200:
            data = response.json()
            st.metric("Parties actives", data["total_games"])
    except:
        st.error("API non disponible")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Bouton Nouvelle Partie
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Nouvelle Partie", type="primary", use_container_width=True):
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

st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

# Affichage du jeu
if st.session_state.game_status:
    game = st.session_state.game_status
    
    # Layout en deux colonnes : Pendu + Clavier (gauche) et Mot (droite)
    col_left, col_right = st.columns([1, 1.5], gap="large")
    
    # ========== COLONNE DE GAUCHE : Pendu + Tentatives ==========
    with col_left:
        # Dessin du Pendu (sans conteneur blanc)
        components.html(draw_hangman_svg(game['attempts_left']), height=240)
        
        # Tentatives en dessous du pendu
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        st.progress(game['attempts_left'] / 6)
        st.markdown(f'<p style="text-align: center; margin-top: 8px; font-size: 13px; color: #86868B;">Tentatives restantes: <span style="color: #5E5CE6; font-weight: 600;">{game["attempts_left"]}/6</span></p>', unsafe_allow_html=True)
    
    # ========== COLONNE DE DROITE : Mot + Clavier ==========
    with col_right:
        # Mot à deviner (sans conteneur blanc)
        st.markdown(f'<div class="word-display">{game["letters"]}</div>', unsafe_allow_html=True)
        
        # Lettres déjà devinées
        if game['guessed_letters']:
            st.markdown(f'<p style="text-align: center; color: #86868B; font-size: 12px; margin-top: 10px;">Lettres utilisées: {", ".join(sorted(game["guessed_letters"]))}</p>', unsafe_allow_html=True)
        
        # Clavier virtuel (uniquement si partie en cours)
        if game['status'] == 'in_progress':
            st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #86868B; font-size: 12px; margin-bottom: 10px;">Choisissez une lettre</p>', unsafe_allow_html=True)
            
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
    
    # ========== STATUT EN DESSOUS DES DEUX COLONNES ==========
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    col1, col_center, col3 = st.columns([1, 2, 1])
    with col_center:
        if game['status'] == 'won':
            st.markdown('<div class="status-box win">Bravo ! Vous avez gagné</div>', unsafe_allow_html=True)
            st.balloons()
        elif game['status'] == 'lost':
            st.markdown('<div class="status-box lose">Perdu !</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box in-progress">Partie en cours</div>', unsafe_allow_html=True)

else:
    # Écran d'accueil minimaliste
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="bento-card" style="text-align: center;">', unsafe_allow_html=True)
        components.html(draw_hangman_svg(6), height=240)
        st.markdown('<p style="color: #86868B; margin-top: 12px; font-size: 13px;">Cliquez sur <strong>Nouvelle Partie</strong> pour commencer</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer minimaliste
st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #86868B; font-size: 11px;'>Streamlit & FastAPI</div>",
    unsafe_allow_html=True
)
