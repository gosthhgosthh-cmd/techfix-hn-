import streamlit as st


st.set_page_config(
    page_title="TechFix Honduras | Asistencia Técnica",
    page_icon="💻",
    layout="wide"
)


st.markdown("""
    <style>
    .main-title {
        color: #2e7d32;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #555;
    }
    .stCard {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='main-title'>💻 TechFix Honduras</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Plataforma de Diagnóstico Técnico de Cómputo y Directorio de Soporte</p>", unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3 = st.tabs(["🛠️ Servicios", "🔍 Diagnóstico Interactivo", "🏬 Tiendas en Honduras"])


with tab1:
    st.header("Nuestros Servicios de Soporte Técnico")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔧 Mantenimiento Hardware")
        st.write("Limpieza profunda, cambio de pasta térmica, reparación de componentes y actualizaciones de RAM o SSD.")

    with col2:
        st.subheader("💻 Soporte de Software")
        st.write("Eliminación de virus/malware, formateo, optimización del sistema operativo e instalación de programas.")

    with col3:
        st.subheader("🛡️ Recuperación de Datos")
        st.write("Diagnóstico y rescate de información en discos duros dañados, SSDs o unidades USB con fallas lógicas.")


with tab2:
    st.header("Diagnóstico de Averías en Tiempo Real")
    st.write("Selecciona una categoría o escribe los síntomas que presenta tu equipo para obtener posibles causas y soluciones.")


    base_datos_problemas = [
        {
            "categoria": "Hardware",
            "titulo": "Equipo enciende pero no da video (Pantalla negra)",
            "sintomas": "pantalla negra no da video luces encienden pitidos",
            "causas": ["Falso contacto o suciedad en los módulos RAM.", "Falla en la tarjeta gráfica o GPU integrada.", "Cable HDMI/DisplayPort defectuoso."],
            "soluciones": ["Limpiar los contactos de la RAM con una goma de borrar suave.", "Probar con otro cable o puerto de video.", "Verificar secuencias de pitidos al encender."]
        },
        {
            "categoria": "Hardware",
            "titulo": "Computadora extremadamente lenta o disco al 100%",
            "sintomas": "lenta disco 100% congelada tarda en cargar",
            "causas": ["Disco duro mecánico (HDD) envejecido o degradado.", "Falta de memoria RAM suficiente.", "Sobrecalentamiento por acumulación de polvo."],
            "soluciones": ["Actualizar la unidad de almacenamiento a un SSD.", "Realizar mantenimiento físico y cambio de pasta térmica.", "Aumentar la memoria RAM del equipo."]
        },
        {
            "categoria": "Software",
            "titulo": "Pantallazo Azul de la Muerte (BSOD) en Windows",
            "sintomas": "pantalla azul bsod reinicios inesperados error",
            "causas": ["Controladores (drivers) desactualizados o corruptos.", "Archivos dañados del sistema operativo.", "Incompatibilidad tras una actualización."],
            "soluciones": ["Iniciar en Modo Seguro y actualizar drivers de video.", "Ejecutar en la terminal de administrador: sfc /scannow", "Desinstalar las últimas actualizaciones de Windows."]
        },
        {
            "categoria": "Software",
            "titulo": "Infección por Malware / Ventanas emergentes",
            "sintomas": "virus malware publicidad ventanas emergentes lentitud",
            "causas": ["Descarga de programas de fuentes no oficiales.", "Extensiones maliciosas instaladas en el navegador."],
            "soluciones": ["Ejecutar un escaneo profundo con Windows Defender o Malwarebytes.", "Revisar y eliminar extensiones desconocidas en el navegador.", "Restablecer la configuración predeterminada del navegador."]
        }
    ]

  
    col_busqueda, col_filtro = st.columns([3, 1])
    with col_busqueda:
        busqueda = st.text_input("🔍 Escribe el problema o síntoma:", placeholder="Ej: pantalla azul, lenta, virus...")
    with col_filtro:
        filtro_cat = st.selectbox("Categoría:", ["Todas", "Hardware", "Software"])

    resultados = []
    for item in base_datos_problemas:
        cumple_cat = (filtro_cat == "Todas") or (item["categoria"] == filtro_cat)
        coincide_texto = (busqueda.lower() in item["titulo"].lower()) or (busqueda.lower() in item["sintomas"].lower())
        
        if cumple_cat and coincide_texto:
            resultados.append(item)

    st.subheader(f"Resultados encontrados ({len(resultados)})")
    if resultados:
        for res in resultados:
            with st.container():
                st.markdown(f"### ⚠️ {res['titulo']}")
                st.caption(f"Categoría: **{res['categoria']}**")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**Causas probables:**")
                    for causa in res["causas"]:
                        st.write(f"- {causa}")
                with c2:
                    st.write("**Soluciones recomendadas:**")
                    for solucion in res["soluciones"]:
                        st.write(f"- {solucion}")
                st.divider()
    else:
        st.warning("No se encontraron coincidencias para tu búsqueda. Intenta con términos como 'lenta', 'RAM' o 'virus'.")


with tab3:
    st.header("Centros de Servicio y Tiendas de Cómputo en Honduras")
    st.write("Directorio de contacto con tiendas y talleres de soporte especializado.")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.info("""
        ### Jetstereo (Soporte Técnico)
        * **Ubicaciones:** Tegucigalpa, San Pedro Sula y principales ciudades.
        * **Teléfono:** +504 2276-0000
        * **Servicios:** Garantías, repuestos originales, diagnóstico de laptops y equipos multimarca.
        """)

        st.info("""
        ### SYCOM (Sistemas y Computadoras)
        * **Ubicación:** Tegucigalpa, M.D.C.
        * **Teléfono:** +504 2232-1111
        * **Servicios:** Ensamblaje de PC, venta de componentes internos, tarjetas madre y almacenamiento.
        """)

    with col_t2:
        st.info("""
        ### Diunsa (Servicio y Garantías)
        * **Ubicaciones:** San Pedro Sula, Tegucigalpa, La Ceiba.
        * **Teléfono:** +504 2516-2000
        * **Servicios:** Soporte de garantías, mantenimiento preventivo de laptops y accesorios.
        """)

        st.info("""
        ### RadioShack Honduras
        * **Ubicación:** Cobertura a nivel nacional.
        * **Teléfono:** +504 2280-3000
        * **Servicios:** Accesorios de conectividad, fuentes de poder, adaptadores y componentes generales.
        """)
