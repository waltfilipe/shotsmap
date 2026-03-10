import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from streamlit_image_coordinates import streamlit_image_coordinates
from io import BytesIO
from PIL import Image
import numpy as np

st.set_page_config(layout="wide")

st.title("Shot Map com Vídeos")

# ==========================
# DADOS DOS CHUTES
# ==========================

data = {
    "x": [105, 102, 98, 110, 95, 108, 100],
    "y": [40, 30, 50, 45, 35, 42, 38],
    "xg": [0.30, 0.12, 0.05, 0.45, 0.08, 0.20, 0.15],
    "resultado": ["Gol", "Fora", "Bloqueado", "Gol", "Fora", "No Alvo", "Bloqueado"],
    "video": [
        "videos/Sebas - Shot 1.mp4",   # seu vídeo local
        "videos/Sebas - Shot 2.mp4",
        None,
        None,
        None,
        None,
        None
    ]
}


df_shots = pd.DataFrame(data)

shots_goal = df_shots[df_shots["resultado"] == "Gol"]
shots_on_target = df_shots[df_shots["resultado"] == "No Alvo"]
shots_off_target = df_shots[df_shots["resultado"] == "Fora"]
shots_blocked = df_shots[df_shots["resultado"] == "Bloqueado"]

# ==========================
# CRIAR CAMPO
# ==========================

pitch = VerticalPitch(
    half=True,
    pitch_type="statsbomb",
    pitch_color="#1c1c1c",
    line_color="white"
)

fig, ax = pitch.draw(figsize=(6,4))

# ==========================
# TAMANHO DOS CHUTES (REDUZIDO)
# ==========================

pitch.scatter(
    shots_goal.x,
    shots_goal.y,
    s=(shots_goal.xg * 900) + 40,
    marker="*",
    c="#EF476F",
    edgecolors="#383838",
    linewidth=1,
    ax=ax,
    label="Gol"
)

pitch.scatter(
    shots_on_target.x,
    shots_on_target.y,
    s=(shots_on_target.xg * 850) + 40,
    marker="h",
    c="#06D6A0",
    edgecolors="#383838",
    linewidth=1,
    ax=ax,
    label="Chute no alvo"
)

pitch.scatter(
    shots_off_target.x,
    shots_off_target.y,
    s=(shots_off_target.xg * 850) + 40,
    marker="o",
    c="#FFD166",
    edgecolors="#383838",
    linewidth=1,
    ax=ax,
    label="Chute para fora"
)

pitch.scatter(
    shots_blocked.x,
    shots_blocked.y,
    s=(shots_blocked.xg * 850) + 40,
    marker="s",
    c="#118AB2",
    edgecolors="#383838",
    linewidth=1,
    ax=ax,
    label="Chute bloqueado"
)

# ==========================
# LEGENDA (AJUSTADA)
# ==========================

legend = ax.legend(
    loc="lower right",
    frameon=True,
    borderpad=0.8,
    fontsize=9,
    labelspacing=0.6,
    handletextpad=0.6
)

legend.get_frame().set_facecolor("#f5f5f5")
legend.get_frame().set_edgecolor("black")
legend.get_frame().set_linewidth(1.2)

# ==========================
# CONVERTER FIGURA PARA IMAGEM
# ==========================

buf = BytesIO()
fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
buf.seek(0)

img = Image.open(buf)

# ==========================
# IMAGEM CLICÁVEL
# ==========================

coords = streamlit_image_coordinates(img)

# ==========================
# DETECTAR CHUTE CLICADO
# ==========================

if coords:

    click_x = coords["x"]
    click_y = coords["y"]

    width, height = img.size

    pitch_x = 120 - (click_y / height * 60)
    pitch_y = click_x / width * 80

    distances = np.sqrt(
        (df_shots["x"] - pitch_x)**2 +
        (df_shots["y"] - pitch_y)**2
    )

    shot_index = distances.idxmin()

    st.subheader("Vídeo da finalização")

    st.video(df_shots.loc[shot_index, "video"])
