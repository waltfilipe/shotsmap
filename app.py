import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")

st.title("Shot Map Interativo com Vídeo")

# ================================
# DADOS DOS CHUTES
# ================================

data = {
    "x": [105, 102, 98, 110, 95, 108],
    "y": [40, 30, 50, 45, 35, 42],
    "xg": [0.30, 0.12, 0.05, 0.45, 0.08, 0.20],
    "resultado": ["Gol", "Fora", "Bloqueado", "Gol", "Fora", "No Alvo"],
    "video": [
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/movie.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/movie.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/movie.mp4"
    ]
}

df = pd.DataFrame(data)

# ================================
# CRIAR CAMPO DE FUTEBOL
# ================================

fig = go.Figure()

# Campo (retângulo)
fig.add_shape(type="rect",
              x0=80, y0=0, x1=120, y1=80,
              line=dict(color="white"),
              fillcolor="#1c1c1c")

# Área
fig.add_shape(type="rect",
              x0=102, y0=18,
              x1=120, y1=62,
              line=dict(color="white"))

# Pequena área
fig.add_shape(type="rect",
              x0=114, y0=30,
              x1=120, y1=50,
              line=dict(color="white"))

# Gol
fig.add_shape(type="rect",
              x0=120, y0=36,
              x1=122, y1=44,
              line=dict(color="white"))

# ================================
# CORES POR RESULTADO
# ================================

color_map = {
    "Gol": "#EF476F",
    "No Alvo": "#06D6A0",
    "Fora": "#FFD166",
    "Bloqueado": "#118AB2"
}

# ================================
# PLOTAR CHUTES
# ================================

for i, row in df.iterrows():
    
    fig.add_trace(go.Scatter(
        x=[row["x"]],
        y=[row["y"]],
        mode="markers",
        marker=dict(
            size=row["xg"] * 60 + 10,
            color=color_map[row["resultado"]],
            line=dict(width=1,color="black")
        ),
        name=row["resultado"],
        customdata=[row["video"]],
        hovertemplate=f"xG: {row['xg']}"
    ))

# ================================
# LAYOUT
# ================================

fig.update_layout(
    xaxis=dict(range=[80,122],visible=False),
    yaxis=dict(range=[0,80],visible=False),
    plot_bgcolor="#1c1c1c",
    paper_bgcolor="#1c1c1c",
    height=600,
    showlegend=False
)

# ================================
# CAPTURAR CLIQUE
# ================================

selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False
)

# ================================
# MOSTRAR VIDEO
# ================================

if selected_points:

    point_index = selected_points[0]["pointIndex"]

    video_url = df.iloc[point_index]["video"]

    st.subheader("Vídeo da Finalização")

    st.video(video_url)
