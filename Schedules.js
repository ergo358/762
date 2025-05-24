import React, { useState, useEffect } from "react";

export default function Schedules() {
  const [items, setItems] = useState(() => {
    const saved = localStorage.getItem("schedules");
    return saved ? JSON.parse(saved) : [];
  });
  const [showForm, setShowForm] = useState(false);
  const [date, setDate] = useState("");
  const [desc, setDesc] = useState("");

  function addSchedule(e) {
    e.preventDefault();
    if (!date) return;
    const newItems = [...items, { date, desc }];
    setItems(newItems);
    localStorage.setItem("schedules", JSON.stringify(newItems));
    setDate("");
    setDesc("");
    setShowForm(false);
  }

  return (
    <div style={{ padding: 16, color: "#fff" }}>
      <h3>Расписания</h3>
      <button
        style={{
          background: "#A259FF",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          padding: "12px 0",
          width: "100%",
          fontWeight: "bold",
          fontSize: 16,
          marginBottom: 16,
          cursor: "pointer"
        }}
        onClick={() => setShowForm(v => !v)}
      >
        {showForm ? "Отмена" : "Создать новое расписание"}
      </button>
      {showForm && (
        <form onSubmit={addSchedule} style={{ marginBottom: 16 }}>
          <input
            type="date"
            value={date}
            onChange={e => setDate(e.target.value)}
            required
            style={{ width: "100%", marginBottom: 8, padding: 8, borderRadius: 6, border: "1px solid #ccc" }}
          />
          <textarea
            value={desc}
            onChange={e => setDesc(e.target.value)}
            placeholder="Описание (например, смена, рабочие часы и т.д.)"
            rows={2}
            style={{ width: "100%", marginBottom: 8, padding: 8, borderRadius: 6, border: "1px solid #ccc" }}
          />
          <button
            type="submit"
            style={{
              width: "100%", background: "#A259FF", color: "#fff", border: "none",
              borderRadius: 6, padding: 10, fontWeight: "bold", cursor: "pointer"
            }}
          >
            Добавить
          </button>
        </form>
      )}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {items.length === 0 && <li style={{ color: "#aaa" }}>Нет расписаний</li>}
        {items.map((item, i) => (
          <li key={i} style={{
            background: "#23232D", borderRadius: 8, padding: 12, marginBottom: 8
          }}>
            <div><b>Дата:</b> {item.date}</div>
            <div><b>Описание:</b> {item.desc}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}