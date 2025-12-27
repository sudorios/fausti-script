(async () => {
  const files = [
    { id: "7707", name: "00_SILABO" },
    { id: "7708", name: "00_NORMAS_APA_7a_ed" },
    { id: "7709", name: "00_REGLAMENTO_GRADOS_TITULOS" },
    { id: "8131", name: "T01_PPT_Planteamiento_Problema" },
    { id: "8133", name: "T02_PPT_Antecedentes" },
    { id: "7703", name: "T03_PPT_Bases_Teoricas" },
    { id: "8654", name: "T04_PPT_Hipotesis" },
    { id: "9183", name: "T05_PPT_Matriz_Operacionalizacion" },
    { id: "9528", name: "T06_PPT_Metodologia" },
    { id: "10006", name: "T07_PPT_Resultados" },
    { id: "10460", name: "T08_PPT_Contrastacion_Hipotesis" },
    { id: "10929", name: "T09_PPT_Discusion" },
    { id: "11450", name: "T10_PPT_Conclusiones_Recomendaciones" },
    { id: "11828", name: "T11_PPT_Referencias" },
    { id: "12116", name: "T12_PPT_Informe_Tesis" },
    { id: "12529", name: "T13_PPT_Antiplagio" },
    { id: "12747", name: "T14_PPT_Articulo_Cientifico" },
    { id: "12978", name: "T15_PPT_Sustentacion_Tesis" },
  ];

  console.log(
    `%c📂 Iniciando descarga de blobs para ${files.length} archivos...`,
    "color: #00ff00; font-weight: bold; font-size: 14px;"
  );

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const url = `https://aulafiisi.unjfsc.edu.pe/mod/resource/view.php?id=${file.id}&redirect=1`;
    console.log(`⬇️ Obteniendo blob (${i + 1}/${files.length}): ${file.name}`);
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = blobUrl;
      a.download = `${file.name}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(blobUrl);
      document.body.removeChild(a);
      await new Promise((r) => setTimeout(r, 1000));
    } catch (e) {
      console.error(`❌ Error descargando ${file.name}:`, e);
    }
  }
  console.log("%c✅ Proceso terminado.", "color: #00ff00; font-weight: bold;");
})();
