import streamlit as st
import pandas as pd
from itertools import combinations

from db.connection import get_connection
from matching.score import compatibility_score

conn = get_connection()

st.title("🌸 Perfume Layering Finder")

perfumes_df = pd.read_sql("SELECT id, name, brand FROM perfumes ORDER BY brand, name", conn)
perfumes_df["label"] = perfumes_df["brand"] + " — " + perfumes_df["name"]

selected = st.multiselect("Escolha os perfumes que você tem:", perfumes_df["label"])

if selected:
    selected_ids = perfumes_df[perfumes_df["label"].isin(selected)]["id"].tolist()

    accords_query = """
        SELECT p.id, a.name, pa.strength
        FROM perfume_accords pa
        JOIN perfumes p ON p.id = pa.perfume_id
        JOIN accords a ON a.id = pa.accord_id
        WHERE p.id = ANY(%(ids)s)
    """
    accords_df = pd.read_sql(accords_query, conn, params={"ids": selected_ids})

    perfume_accords = {
        pid: dict(zip(group["name"], group["strength"]))
        for pid, group in accords_df.groupby("id")
    }

    st.subheader("Sugestões de pares")
    for a, b in combinations(selected_ids, 2):
        score = compatibility_score(perfume_accords.get(a, {}), perfume_accords.get(b, {}))
        name_a = perfumes_df.loc[perfumes_df.id == a, "label"].values[0]
        name_b = perfumes_df.loc[perfumes_df.id == b, "label"].values[0]
        st.write(f"**{name_a}** + **{name_b}** → compatibilidade: `{score:.0%}`")