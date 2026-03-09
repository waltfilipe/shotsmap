import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

st.title("Shot Map")

data = {
    "x": [105, 102, 98, 110, 95, 108, 100],
    "y": [40, 30, 50, 45, 35, 42, 38],
    "xg": [0.30, 0.12, 0.05, 0.45, 0.08, 0.20, 0.15],
    "resultado": ["Gol", "Fora", "Bloqueado", "Gol", "Fora", "No Alvo", "Bloqueado"]
}

df_shots = pd.DataFrame(data)

shots_goal = df_shots[df_shots["resultado"] == "Gol"]
shots_on_target = df_shots[df_shots["resultado"] == "No Alvo"]
shots_off_target = df_shots[df_shots["resultado"] == "Fora"]
shots_blocked = df_shots[df_shots["resultado"] == "Bloqueado"]

pitch = VerticalPitch(
    half=True,
    pitch_type='statsbomb',
    pitch_color='#1c1c1c',
    line_color='white'
)

fig, ax = pitch.draw(figsize=(10,7))

pitch.scatter(shots_goal.x, shots_goal.y,
              s=(shots_goal.xg*2000)+100,
              marker='*',
              c='#EF476F',
              ax=ax,
              label='Gol')

pitch.scatter(shots_on_target.x, shots_on_target.y,
              s=(shots_on_target.xg*1800)+100,
              marker='h',
              c='#06D6A0',
              ax=ax,
              label='No alvo')

pitch.scatter(shots_off_target.x, shots_off_target.y,
              s=(shots_off_target.xg*1800)+100,
              marker='o',
              c='#FFD166',
              ax=ax,
              label='Fora')

pitch.scatter(shots_blocked.x, shots_blocked.y,
              s=(shots_blocked.xg*1800)+100,
              marker='s',
              c='#118AB2',
              ax=ax,
              label='Bloqueado')

ax.legend()

st.pyplot(fig)
