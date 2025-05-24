import React, { useState, useEffect } from "react";

// Вернёт массив дат текущего месяца
function getMonthDates(year, month) {
  const result = [];
  const date = new Date(year, month, 1);
  while (date.getMonth() === month) {
    result.push(new Date(date));
    date.setDate(date.getDate() + 1);
  }
  return result;
}

export default function Weekends() {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth());
  const [selected, setSelected] = useState(() => {
    const saved = localStorage.getItem("weekends");
    return saved ? JSON.parse(saved) : [];
  });

  const dates = getMonthDates(year, month);

  function toggleDate(dateStr) {
    setSelected(sel => {
      let next;
      if (sel.includes(dateStr)) {
        next = sel.filter(d => d !== dateStr);
      } else {
        next = [...sel, dateStr];
      }
      localStorage.setItem("weekends", JSON.stringify(next));
      return next;
    });
  }

  function prevMonth() {
    setMonth(m => (m === 0 ? 11 : m - 1));
    if (month === 0) setYear(y => y - 1);
  }
  function nextMonth() {
    setMonth(m => (m === 11 ? 0 : m + 1));
    if (month === 11) setYear(y => y + 1);
  }

  return (
    <div style={{ padding: 16, color: "#fff" }}>
      <h3 style={{ marginBottom: 12 }}>Выходные</h3>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <button onClick={prevMonth} style={{ fontSize: 20 }}>◀</button>
        <strong>{today.toLocaleString("ru", { month: "long" })} {year}</strong>
        <button onClick={nextMonth} style={{ fontSize: 20 }}>▶</button>
      </div>
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(7, 1fr)",
        gap: 4,
        marginTop: 16
      }}>
        {["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"].map(d => (
          <div key={d} style={{ textAlign: "center", color: "#aaa" }}>{d}</div>
        ))}
        {dates.map(date => {
          const dateStr = date.toISOString().slice(0, 10);
          const isSelected = selected.includes(dateStr);
          return (
            <button
              key={dateStr}
              onClick={() => toggleDate(dateStr)}
              style={{
                background: isSelected ? "#A259FF" : "#23232D",
                color: isSelected ? "#fff" : "#ccc",
                border: "none",
                borderRadius: 6,
                padding: "8px 0",
                margin: 0,
                cursor: "pointer"
              }}
            >
              {date.getDate()}
            </button>
          );
        })}
      </div>
      <p style={{ marginTop: 16, fontSize: 13, color: "#bbb" }}>
        Отмеченные дни будут выходными. Записи на эти даты будут невозможны.<br />
        Существующие записи не отменяются автоматически.
      </p>
    </div>
  );
}