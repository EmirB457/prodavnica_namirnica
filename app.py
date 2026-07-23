import streamlit as st
import pandas as pd
import plotly.express as px

from database import init_db, add_product, get_products, delete_product, get_low_stock

st.set_page_config(page_title="Prodavnica namirnica", layout="wide")

init_db()

st.title("Sistem za upravljanje zalihama u prodavnici namirnica")
st.write("Aplikacija za evidenciju proizvoda, praćenje zaliha i upozorenje na nizak lager.")

menu = st.sidebar.radio(
    "Navigacija",
    ["Dodavanje proizvoda", "Pregled proizvoda", "Nizak lager", "Statistika"]
)

if menu == "Dodavanje proizvoda":
    st.subheader("Dodavanje novog proizvoda")

    with st.form("product_form"):
        name = st.text_input("Naziv proizvoda")
        category = st.selectbox(
            "Kategorija",
            ["Voće i povrće", "Mliječni proizvodi", "Piće", "Pekarski proizvodi", "Slatkiši", "Ostalo"]
        )
        price = st.number_input("Cijena", min_value=0.0, step=0.1)
        quantity = st.number_input("Količina", min_value=0, step=1)
        expiry_date = st.date_input("Rok trajanja")
        supplier = st.text_input("Dobavljač")
        min_stock = st.number_input("Minimalni lager", min_value=0, step=1)

        submitted = st.form_submit_button("Sačuvaj proizvod")

        if submitted:
            if name.strip() == "":
                st.warning("Naziv proizvoda je obavezan.")
            else:
                add_product(
                    name,
                    category,
                    price,
                    quantity,
                    str(expiry_date),
                    supplier,
                    min_stock
                )
                st.success("Proizvod je uspješno dodat.")

elif menu == "Pregled proizvoda":
    st.subheader("Pregled svih proizvoda")

    df = get_products()

    if df.empty:
        st.info("Nema unesenih proizvoda.")
    else:
        st.dataframe(df, use_container_width=True)

        st.markdown("### Brisanje proizvoda")
        product_id = st.number_input("Unesite ID proizvoda za brisanje", min_value=1, step=1)
        if st.button("Obriši proizvod"):
            delete_product(product_id)
            st.success("Proizvod je obrisan. Osvježite prikaz ako je potrebno.")

elif menu == "Nizak lager":
    st.subheader("Proizvodi sa niskim lagerom")

    low_stock_df = get_low_stock()

    if low_stock_df.empty:
        st.success("Trenutno nema proizvoda sa niskim lagerom.")
    else:
        st.warning("Prikaz proizvoda koje treba dopuniti.")
        st.dataframe(low_stock_df, use_container_width=True)

elif menu == "Statistika":
    st.subheader("Statistički prikaz zaliha")

    df = get_products()

    if df.empty:
        st.info("Nema podataka za prikaz statistike.")
    else:
        category_summary = df.groupby("category")["quantity"].sum().reset_index()

        fig = px.bar(
            category_summary,
            x="category",
            y="quantity",
            color="category",
            title="Ukupna količina proizvoda po kategoriji"
        )
        st.plotly_chart(fig, use_container_width=True)

        price_fig = px.pie(
            df,
            names="category",
            values="price",
            title="Udio cijena po kategorijama"
        )
        st.plotly_chart(price_fig, use_container_width=True)