import streamlit as st
import google.generativeai as genai
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# Configuración de la página
st.set_page_config(
    page_title="TechFix Honduras | Asistencia Técnica Inteligente",
    page_icon="💻",
    layout="wide"
)

# Cargar API Key automáticamente desde st.secrets o variable de entorno
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if API_KEY:
    genai.configure(api_key=API_KEY)

# Estilos CSS
st.markdown("""
    <style>
    .main-title { color: #2e7d32; text-align: center; font-weight: bold; }
    .sub-title { text-align: center; color: #666; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>💻 TechFix Honduras</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Diagnóstico de Cómputo con Inteligencia Artificial y Geolocalización GPS</p>", unsafe_allow_html=True)
st.divider()

# Función para consultar a la IA
def obtener_solucion_ia(categoria, problema_seleccionado, detalle_adicional=""):
    if not API_KEY:
        return "⚠️ Error de configuración: La clave de la API de Gemini no ha sido configurada en el servidor."
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Actúa como un técnico experto en soporte informático de hardware y software.
        El usuario presenta un problema en la categoría: {categoria}.
        Problema seleccionado: {problema_seleccionado}.
        Detalles adicionales del usuario: {detalle_adicional if detalle_adicional else 'Ninguno'}.

        Proporciona una respuesta estructurada y clara en español:
        1. 🔍 **Causas Probables**: 2-3 motivos de la falla.
        2. 🛠️ **Soluciones Paso a Paso**: Instrucciones claras de solución.
        3. ⚠️ **Recomendación de Seguridad**: Si debe acudir a un taller especializado.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al conectar con la IA: {str(e)}"

# Pestañas de la aplicación
tab1, tab2, tab3 = st.tabs(["🛠️ Diagnóstico con IA", "🗺️ Tiendas Cerca de Mí (GPS)", "🏢 Directorio Nacional"])

# ==========================================
# SECCIÓN 1: DIAGNÓSTICO CON IA
# ==========================================
with tab1:
    st.header("Selecciona la falla que presenta tu equipo")
    col_hw, col_sw, col_rec = st.columns(3)

    with col_hw:
        st.subheader("🔧 Hardware")
        opciones_hw = [
            "Seleccionar una opción...",
            "El equipo enciende pero la pantalla se queda negra",
            "La computadora se apaga sola a los pocos minutos de encender",
            "Hace un ruido fuerte o sobrecalentamiento excesivo",
            "No reconoce la memoria RAM o emite pitidos al arrancar",
            "El disco duro hace ruidos raros (clicks) o no detecta almacenamiento",
            "Otro problema de Hardware..."
        ]
        seleccion_hw = st.selectbox("Problemas de Hardware:", opciones_hw, key="hw_select")
        detalle_hw = st.text_input("Detalle adicional:", placeholder="Ej: Ocurrió tras un bajón de luz", key="hw_det")
        btn_hw = st.button("Diagnosticar Hardware", type="primary", key="btn_hw")

    with col_sw:
        st.subheader("💻 Software")
        opciones_sw = [
            "Seleccionar una opción...",
            "Pantalla azul de la muerte (BSOD) en Windows",
            "El sistema está extremadamente lento / Disco al 100%",
            "Infección por virus, malware o publicidad molesta (pop-ups)",
            "El equipo no inicia el sistema operativo (Bucle de reinicios)",
            "Error al actualizar drivers o controladores de video",
            "Otro problema de Software..."
        ]
        seleccion_sw = st.selectbox("Problemas de Software:", opciones_sw, key="sw_select")
        detalle_sw = st.text_input("Detalle adicional:", placeholder="Ej: Código 0x80070002", key="sw_det")
        btn_sw = st.button("Diagnosticar Software", type="primary", key="btn_sw")

    with col_rec:
        st.subheader("🛡️ Recuperación de Datos")
        opciones_rec = [
            "Seleccionar una opción...",
            "Formateé el disco duro o borré archivos por accidente",
            "La memoria USB o tarjeta SD pide formatear para poder usarse",
            "El disco duro externo no aparece en 'Mi Equipo'",
            "Archivos o carpetas dañadas / no se pueden abrir",
            "Otro problema de Datos..."
        ]
        seleccion_rec = st.selectbox("Problemas de Datos:", opciones_rec, key="rec_select")
        detalle_rec = st.text_input("Detalle adicional:", placeholder="Ej: Memoria USB Kingston de 32GB", key="rec_det")
        btn_rec = st.button("Diagnosticar Datos", type="primary", key="btn_rec")

    st.divider()

    if btn_hw and seleccion_hw != "Seleccionar una opción...":
        with st.spinner("Analizando falla de Hardware..."):
            st.markdown(obtener_solucion_ia("Mantenimiento de Hardware", seleccion_hw, detalle_hw))

    elif btn_sw and seleccion_sw != "Seleccionar una opción...":
        with st.spinner("Analizando falla de Software..."):
            st.markdown(obtener_solucion_ia("Soporte de Software", seleccion_sw, detalle_sw))

    elif btn_rec and seleccion_rec != "Seleccionar una opción...":
        with st.spinner("Analizando caso de Datos..."):
            st.markdown(obtener_solucion_ia("Recuperación de Datos", seleccion_rec, detalle_rec))

# ==========================================
# SECCIÓN 2: MAPA GPS Y TIENDAS CERCANAS
# ==========================================
with tab2:
    st.header("Localización GPS y Tiendas Cercanas")
    st.write("Visualiza en el mapa interactivo los centros de soporte técnico más cercanos.")

    loc = get_geolocation()

    lat_def = 14.0723
    lon_def = -87.1921

    if loc and 'coords' in loc:
        lat_user = loc['coords']['latitude']
        lon_user = loc['coords']['longitude']
        st.success(f"📍 Ubicación GPS obtenida: **Latitud {lat_user:.4f}, Longitud {lon_user:.4f}**")
    else:
        lat_user = lat_def
        lon_user = lon_def
        st.info("ℹ️ Mostrando ubicación de referencia en el mapa.")

    m = folium.Map(location=[lat_user, lon_user], zoom_start=14)

    folium.Marker(
        [lat_user, lon_user],
        popup="Tu ubicación actual",
        tooltip="Estás aquí",
        icon=folium.Icon(color="red", icon="user", prefix="fa")
    ).add_to(m)

    tiendas_cercanas = [
        {
            "nombre": "Computadoras PCI Honduras • City Mall TGU",
            "lat": 14.0682,
            "lon": -87.2171,
            "tel": "+504 3322-7677",
            "direccion": "City Mall Tegucigalpa, Entrada Principal, Sótano 1"
        },
        {
            "nombre": "AVACO - Reparación Computadoras Mac y PC",
            "lat": 14.0850,
            "lon": -87.1710,
            "tel": "+504 9976-7735",
            "direccion": "Residencial Guaymuras, Tegucigalpa"
        },
        {
            "nombre": "Bortech84",
            "lat": 14.0750,
            "lon": -87.2050,
            "tel": "+504 8785-3527",
            "direccion": "Comayagüela, Francisco Morazán"
        },
        {
            "nombre": "Multisistemas",
            "lat": 14.0710,
            "lon": -87.1950,
            "tel": "+504 2280-2939",
            "direccion": "Tegucigalpa, Francisco Morazán"
        },
        {
            "nombre": "WNET",
            "lat": 14.0730,
            "lon": -87.1980,
            "tel": "+504 3143-5296",
            "direccion": "Tegucigalpa, Francisco Morazán"
        }
    ]

    for t in tiendas_cercanas:
        folium.Marker(
            [t["lat"], t["lon"]],
            popup=f"<b>{t['nombre']}</b><br>Tel: {t['tel']}<br>{t['direccion']}",
            tooltip=t["nombre"],
            icon=folium.Icon(color="green", icon="wrench", prefix="fa")
        ).add_to(m)

    st_folium(m, width=1100, height=500)

    st.subheader("Talleres y Centros de Servicio Recomendados")
    cols = st.columns(2)
    for index, tienda in enumerate(tiendas_cercanas):
        with cols[index % 2]:
            st.markdown(f"""
            ### 🏬 [{tienda['nombre']}](https://maps.google.com/?q={tienda['lat']},{tienda['lon']})
            * 📍 **Dirección:** {tienda['direccion']}
            * 📞 **Teléfono:** `{tienda['tel']}`
            """)

# ==========================================
# SECCIÓN 3: DIRECTORIO NACIONAL
# ==========================================
with tab3:
    st.header("Directorio de Cadenas Principales en Honduras")
    c1, c2 = st.columns(2)
    with c1:
        st.info("### Jetstereo\n* **Tel:** +504 2276-0000\n* **Cobertura:** Tegucigalpa, SPS, La Ceiba\n* **Especialidad:** Garantías y repuestos de laptops.")
        st.info("### SYCOM\n* **Tel:** +504 2232-1111\n* **Cobertura:** Tegucigalpa\n* **Especialidad:** Componentes de PC, fuentes y tarjetas de video.")
    with c2:
        st.info("### Diunsa\n* **Tel:** +504 2516-2000\n* **Cobertura:** San Pedro Sula, Tegucigalpa\n* **Especialidad:** Mantenimiento preventivo y repuestos.")
        st.info("### RadioShack\n* **Tel:** +504 2280-3000\n* **Cobertura:** Nivel Nacional\n* **Especialidad:** Cables, adaptadores y discos externos.")
