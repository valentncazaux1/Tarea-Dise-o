import streamlit as st
from datetime import time

st.set_page_config(page_title="Cantina Elbio", page_icon="🏫")

if 'tema' not in st.session_state:
    st.session_state.tema = 'claro'

def cambiar_tema():
    st.session_state.tema = 'oscuro' if st.session_state.tema == 'claro' else 'claro'

col_t1, col_t2 = st.columns([0.9, 0.1])
with col_t2:
    icono = "🌙" if st.session_state.tema == 'claro' else "☀️"
    if st.button(icono):
        cambiar_tema()
        st.rerun()

if st.session_state.tema == 'oscuro':
    bg_color = "#0E1117"
    txt_color = "#FFFFFF"
    card_bg = "#262730"
    glow = "0px 0px 15px #f1c40f"
else:
    bg_color = "#FFFFFF"
    txt_color = "#000000"
    card_bg = "#F0F2F6"
    glow = "none"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {txt_color}; }}
    .comida-icon {{
        width: 80px; height: 80px;
        border: 2px solid #004a99; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 35px; background-color: {card_bg}; 
        margin: 0 auto 10px auto; box-shadow: {glow};
    }}
    p, h1, h2, h3, span, label, .stMarkdown {{ color: {txt_color} !important; }}
    .stButton>button {{ border-radius: 20px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

if 'paso' not in st.session_state:
    st.session_state.paso = 'login'

if st.session_state.paso == 'login':
    st.markdown("<h1 style='text-align: center;'>👤</h1>", unsafe_allow_html=True)
    cedula = st.text_input("Cédula", placeholder="12345678")
    email = st.text_input("Email Institucional", placeholder="Correos Institucionales")
    password = st.text_input("Contraseña", type="password")
    if st.button("INGRESAR"):
        if not email.lower().endswith("@elbiofernandez.edu.uy") or password != f"ef{cedula}":
            st.error("Datos incorrectos")
        else:
            st.session_state.paso = 'menu'; st.rerun()

elif st.session_state.paso == 'menu':
    st.subheader("Selecciona tu comida")
    col1, col2 = st.columns(2)
    items = [("🍎", "Saludable"), ("🍔", "Hamburguesa"), ("🍕", "Pizza"), ("🥪", "Sándwich")]
    for i, (icon, name) in enumerate(items):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f'<div class="comida-icon">{icon}</div>', unsafe_allow_html=True)
            if st.button(name):
                st.session_state.comida = name
                st.session_state.paso = 'hora'; st.rerun()

elif st.session_state.paso == 'hora':
    st.subheader(f"Pedido: {st.session_state.comida}")
    hora_sug = time(12, 15)
    st.info(f"Sugerido: {hora_sug.strftime('%H:%M')}")
    if st.radio("¿Confirmas este horario?", ["Sí", "No"]) == "Sí":
        st.session_state.hora_final = hora_sug
        if st.button("SIGUIENTE"): st.session_state.paso = 'pago'; st.rerun()
    else:
        h = st.time_input("Elegir hora (07:30-15:50):", value=time(13,0))
        if st.button("CONFIRMAR HORA"):
            if time(7,30) <= h <= time(15,50):
                st.session_state.hora_final = h
                st.session_state.paso = 'pago'; st.rerun()
            else: st.error("Horario no permitido")

elif st.session_state.paso == 'pago':
    st.subheader("💳 Datos de Pago")
    if st.radio("Método:", ["Tarjeta", "Efectivo"]) == "Tarjeta":
        st.text_input("Nombre Titular")
        st.text_input("Número de Tarjeta", max_chars=16)
        c1, c2 = st.columns(2)
        c1.text_input("MM/AA")
        c2.text_input("CVV", type="password", max_chars=3)
        if st.button("PAGAR"): st.session_state.paso = 'retiro'; st.rerun()
    else:
        st.warning("Pagarás al retirar.")
        if st.button("CONTINUAR"): st.session_state.paso = 'retiro'; st.rerun()

elif st.session_state.paso == 'retiro':
    st.subheader("¿Dónde lo retiras?")
    opcion = st.radio("Selecciona:", ["Mostrador", "Llevar al salón"])
    
    if opcion == "Llevar al salón":
        st.session_state.salon = st.text_input("Ingresa el número de tu salón:", placeholder="Ej: 3ro B")
    
    if st.button("FINALIZAR"):
        st.session_state.entrega = opcion
        if opcion == "Llevar al salón" and not st.session_state.get('salon'):
            st.error("Por favor ingresa el número de salón.")
        else:
            st.session_state.paso = 'final'; st.rerun()

elif st.session_state.paso == 'final':
    st.balloons()
    st.success("¡Pedido enviado con éxito!")
    resumen = f"**Pedido:** {st.session_state.comida} | **Hora:** {st.session_state.hora_final.strftime('%H:%M')}"
    if st.session_state.entrega == "Llevar al salón":
        resumen += f" | **Salón:** {st.session_state.salon}"
    else:
        resumen += " | **Lugar:** Mostrador"
    st.markdown(resumen)
    
    if st.button("Hacer otro pedido"):
        tema_actual = st.session_state.tema
        st.session_state.clear()
        st.session_state.tema = tema_actual
        st.session_state.paso = 'login'
        st.rerun()
    