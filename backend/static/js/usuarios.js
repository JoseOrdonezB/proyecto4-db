document.addEventListener("DOMContentLoaded", function () {
  const exportarCsv = document.getElementById("exportar-csv");
  const form = document.querySelector("form[method='get']"); // busca el form de filtros

  // Envío automático del formulario de filtros
  if (form) {
    form.addEventListener("change", () => {
      form.submit();
    });
  }

  // Exportar a CSV
  if (exportarCsv) {
    exportarCsv.addEventListener("click", () => {
      exportarTablaCSV("tabla-usuarios", "reporte_usuarios.csv");
    });
  }

  function exportarTablaCSV(idTabla, nombreArchivo) {
    const tabla = document.getElementById(idTabla);
    if (!tabla) {
      alert("No hay tabla para exportar.");
      return;
    }

    let csv = [];
    for (let fila of tabla.rows) {
      let filaCsv = [];
      for (let celda of fila.cells) {
        let texto = celda.innerText.replace(/"/g, '""'); // escapar comillas
        filaCsv.push(`"${texto}"`);
      }
      csv.push(filaCsv.join(","));
    }

    const contenido = csv.join("\n");
    const blob = new Blob([contenido], { type: "text/csv;charset=utf-8;" });
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = nombreArchivo;
    enlace.style.display = "none";
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
  }
});