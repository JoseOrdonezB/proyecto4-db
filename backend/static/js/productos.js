document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-filtros-productos");
  const exportarCsv = document.getElementById("exportar-csv");
  const exportarPdf = document.getElementById("exportar-pdf");

  // Envío automático del formulario al cambiar un filtro
  if (form) {
    form.addEventListener("change", () => {
      form.submit();
    });
  }

  // Exportar a CSV
  if (exportarCsv) {
    exportarCsv.addEventListener("click", () => {
      exportarTablaCSV("tabla-productos", "reporte_productos.csv");
    });
  }

  // Función auxiliar para exportar tabla a CSV
  function exportarTablaCSV(idTabla, nombreArchivo) {
    const tabla = document.getElementById(idTabla);
    let csv = [];
    for (let fila of tabla.rows) {
      let datos = [];
      for (let celda of fila.cells) {
        datos.push('"' + celda.innerText.replace(/"/g, '""') + '"');
      }
      csv.push(datos.join(","));
    }
    const contenidoCsv = csv.join("\n");
    const blob = new Blob([contenidoCsv], { type: "text/csv" });
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = nombreArchivo;
    enlace.click();
  }
});