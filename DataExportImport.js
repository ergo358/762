import React, { useRef } from "react";

// Получить все данные из localStorage
function collectData() {
  return {
    profile: JSON.parse(localStorage.getItem("profile") || "{}"),
    weekends: JSON.parse(localStorage.getItem("weekends") || "[]"),
    schedules: JSON.parse(localStorage.getItem("schedules") || "[]"),
  };
}

// Сохранить все данные в localStorage
function restoreData(data) {
  if (data.profile) localStorage.setItem("profile", JSON.stringify(data.profile));
  if (data.weekends) localStorage.setItem("weekends", JSON.stringify(data.weekends));
  if (data.schedules) localStorage.setItem("schedules", JSON.stringify(data.schedules));
}

export default function DataExportImport({ onImport }) {
  const fileRef = useRef();

  const handleExport = () => {
    const data = collectData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data_export.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      try {
        const data = JSON.parse(ev.target.result);
        restoreData(data);
        if (onImport) onImport();
        alert("Данные успешно импортированы!");
      } catch {
        alert("Ошибка при импорте данных.");
      }
    };
    reader.readAsText(file);
  };

  return (
    <div style={{ margin: "24px 0", background: "#23232D", padding: 16, borderRadius: 8 }}>
      <h4 style={{ color: "#fff" }}>Экспорт / Импорт данных</h4>
      <button onClick={handleExport} style={{ marginRight: 10, background: "#A259FF", color: "#fff", border: "none", borderRadius: 6, padding: "8px 16px", cursor: "pointer" }}>
        Экспорт (скачать data_export.json)
      </button>
      <input
        ref={fileRef}
        type="file"
        accept="application/json"
        style={{ display: "none" }}
        onChange={handleImport}
      />
      <button
        onClick={() => fileRef.current && fileRef.current.click()}
        style={{ background: "#444", color: "#fff", border: "none", borderRadius: 6, padding: "8px 16px", cursor: "pointer" }}
      >
        Импорт (загрузить data_export.json)
      </button>
      <p style={{ color: "#bbb", marginTop: 12, fontSize: 13 }}>
        Экспортируй данные перед переходом на другой ПК или аккаунт.<br />
        Импортируй файл, чтобы восстановить все расписания, выходные и профиль.
      </p>
    </div>
  );
}