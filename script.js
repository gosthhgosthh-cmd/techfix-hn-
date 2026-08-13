// Banco de datos local para diagnósticos de Hardware y Software
const baseDatosProblemas = [
  {
    id: 1,
    categoria: "hardware",
    titulo: "Equipo enciende pero no da video (Pantalla negra)",
    sintomas: ["no da video", "pantalla negra", "luces encienden", "pitidos"],
    causas: [
      "Falso contacto o suciedad en los módulos RAM.",
      "Falla en la tarjeta gráfica o chip de video integrado.",
      "Cable de video (HDMI/DisplayPort) defectuoso o desconectado."
    ],
    soluciones: [
      "Limpiar los contactos de la memoria RAM con una goma de borrar suave.",
      "Probar conectando el monitor a otro puerto o probar con otro cable.",
      "Verificar si el equipo emite una secuencia de pitidos al encender."
    ]
  },
  {
    id: 2,
    categoria: "hardware",
    titulo: "Computadora extremadamente lenta o disco al 100%",
    sintomas: ["lenta", "disco al 100%", "tarda en cargar", "congelada"],
    causas: [
      "Disco duro mecánico (HDD) envejecido o con sectores defectuosos.",
      "Falta de memoria RAM para las aplicaciones ejecutadas.",
      "Sobrecalentamiento por acumulación de polvo en el disipador."
    ],
    soluciones: [
      "Reemplazar el disco HDD tradicional por una unidad SSD de estado sólido.",
      "Realizar limpieza física interna y cambio de pasta térmica al procesador.",
      "Expandir la memoria RAM del equipo."
    ]
  },
  {
    id: 3,
    categoria: "software",
    titulo: "Pantallazo Azul de la Muerte (BSOD) en Windows",
    sintomas: ["pantalla azul", "bsod", "reinicios inesperados", "error de codigo"],
    causas: [
      "Controladores (drivers) desactualizados o incompatibles.",
      "Archivos del sistema dañados por apagados repentinos.",
      "Incompatibilidad de una actualización reciente de Windows."
    ],
    soluciones: [
      "Iniciar en Modo Seguro y actualizar/revertir controladores de video y chipsets.",
      "Abrir CMD como Administrador y ejecutar el comando: sfc /scannow",
      "Desinstalar las últimas actualizaciones de Windows instaladas."
    ]
  },
  {
    id: 4,
    categoria: "software",
    titulo: "Infección por Malware / Ventanas emergentes (Pop-ups)",
    sintomas: ["virus", "malware", "publicidad", "ventanas emergentes", "redirecciones"],
    causas: [
      "Instalación de programas de fuentes no confiables.",
      "Extensiones del navegador maliciosas instaladas sin autorización."
    ],
    soluciones: [
      "Ejecutar un escaneo completo con Microsoft Defender o Malwarebytes.",
      "Revisar y eliminar extensiones desconocidas en Google Chrome o Edge.",
      "Restablecer los valores predeterminados del navegador."
    ]
  },
  {
    id: 5,
    categoria: "hardware",
    titulo: "El equipo se apaga repentinamente a los pocos minutos",
    sintomas: ["se apaga solo", "sobrecalentamiento", "ventilador muy ruidoso", "calor"],
    causas: [
      "Protección térmica activada por exceso de calor en el procesador.",
      "Ventilador (cooler) detenido o obstruido por suciedad.",
      "Falla en la fuente de poder (Power Supply)."
    ],
    soluciones: [
      "Verificar que los ventiladores estén girando correctamente.",
      "Limpiar el polvo acumulado y aplicar nueva pasta térmica de alta calidad.",
      "Probar con una fuente de poder de repuesto para descartar variaciones de voltaje."
    ]
  }
];

// Elementos del DOM
const resultsContainer = document.getElementById("resultsContainer");
const searchInput = document.getElementById("searchInput");
const btnSearch = document.getElementById("btnSearch");
const filterButtons = document.querySelectorAll(".btn-filter");

let filtroActual = "all";

// Función para renderizar tarjetas de diagnóstico
function renderizarDiagnosticos(lista) {
  resultsContainer.innerHTML = "";

  if (lista.length === 0) {
    resultsContainer.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 2rem;">
        <p style="color: var(--text-muted); font-size: 1.1rem;">No se encontraron resultados para tu búsqueda.</p>
        <p style="font-size: 0.9rem;">Prueba buscando palabras como "RAM", "pantalla", "virus" o "lenta".</p>
      </div>
    `;
    return;
  }

  lista.forEach(item => {
    const card = document.createElement("div");
    card.className = "diag-card";

    const causasHTML = item.causas.map(c => `<li>${c}</li>`).join("");
    const solucionesHTML = item.soluciones.map(s => `<li>${s}</li>`).join("");

    card.innerHTML = `
      <span class="badge ${item.categoria}">${item.categoria}</span>
      <h4>${item.titulo}</h4>
      <p><strong>Causas probables:</strong></p>
      <ul>${causasHTML}</ul>
      <p style="margin-top: 0.8rem;"><strong>Soluciones recomendadas:</strong></p>
      <ul>${solucionesHTML}</ul>
    `;

    resultsContainer.appendChild(card);
  });
}

// Función de filtrado por texto y categoría
function filtrarResultados() {
  const textoBusqueda = searchInput.value.toLowerCase().trim();

  const resultadosFiltrados = baseDatosProblemas.filter(item => {
    const coincideCategoria = (filtroActual === "all") || (item.categoria === filtroActual);
    
    const coincideTexto = 
      item.titulo.toLowerCase().includes(textoBusqueda) ||
      item.sintomas.some(sintoma => sintoma.toLowerCase().includes(textoBusqueda));

    return coincideCategoria && coincideTexto;
  });

  renderizarDiagnosticos(resultadosFiltrados);
}

// Event Listeners
btnSearch.addEventListener("click", filtrarResultados);
searchInput.addEventListener("keyup", (e) => {
  if (e.key === "Enter") filtrarResultados();
});

filterButtons.forEach(btn => {
  btn.addEventListener("click", (e) => {
    filterButtons.forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    filtroActual = e.target.dataset.filter;
    filtrarResultados();
  });
});

// Carga inicial
document.addEventListener("DOMContentLoaded", () => {
  renderizarDiagnosticos(baseDatosProblemas);
});