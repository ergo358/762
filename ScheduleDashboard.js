import React, { useState } from "react";

export default function ScheduleDashboard() {
  const [activeTab, setActiveTab] = useState("schedules");

  return (
    <div style={{ minHeight: "100vh", background: "#18181F" }}>
      {/* Верхняя панель */}
      <div style={{ display: "flex", alignItems: "center", padding: "16px 16px 0 16px" }}>
        <span style={{ fontWeight: "bold", fontSize: 24, color: "#fff", letterSpacing: 1 }}>Zavtra.</span>
        <span style={{ color: "#A259FF", fontWeight: "bold", marginLeft: 2, fontSize: 24 }}>live</span>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center" }}>
          <button style={{
            background: "none", border: "none", color: "#fff", marginRight: 8, fontSize: 18, cursor: "pointer"
          }}>🌙</button>
          <select style={{
            background: "#23232D", color: "#fff", border: "none", borderRadius: 4, padding: "2px 8px"
          }}>
            <option>Русский</option>
          </select>
        </div>
      </div>

      {/* Заголовок */}
      <div style={{ padding: "24px 16px 0 16px" }}>
        <h2 style={{ color: "#fff", margin: 0, fontSize: 22 }}>Рабочий кабинет</h2>
      </div>

      {/* Вкладки */}
      <div style={{ display: "flex", gap: 8, padding: "24px 16px 0 16px" }}>
        <button
          onClick={() => setActiveTab("schedules")}
          style={{
            flex: 1,
            background: activeTab === "schedules" ? "#23232D" : "transparent",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontWeight: activeTab === "schedules" ? "bold" : "normal",
            padding: "8px 0",
            fontSize: 16,
            transition: "background .15s"
          }}
        >
          Расписания
        </button>
        <button
          onClick={() => setActiveTab("weekends")}
          style={{
            flex: 1,
            background: activeTab === "weekends" ? "#23232D" : "transparent",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontWeight: activeTab === "weekends" ? "bold" : "normal",
            padding: "8px 0",
            fontSize: 16,
            transition: "background .15s"
          }}
        >
          Выходные
        </button>
      </div>

      {/* Кнопка */}
      {activeTab === "schedules" && (
        <div style={{ padding: "32px 16px 0 16px" }}>
          <button
            style={{
              width: "100%",
              background: "#A259FF",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              padding: "16px 0",
              fontWeight: "bold",
              fontSize: 16,
              cursor: "pointer",
              boxShadow: "0 2px 8px #0002"
            }}
            onClick={() => alert("Создать новое расписание (логика добавления впереди!)")}
          >
            Создать новое расписание
          </button>
        </div>
      )}

      {/* Нижняя навигация */}
      <div style={{
        position: "fixed",
        left: 0,
        right: 0,
        bottom: 0,
        background: "#23232D",
        display: "flex",
        justifyContent: "space-around",
        padding: "8px 0",
        borderTop: "1px solid #312f41",
        zIndex: 100
      }}>
        <NavItem icon="📋" label="Заявки" active={false} />
        <NavItem icon="📅" label="Расписания" active={true} />
        <NavItem icon="👤" label="Профиль" active={false} />
      </div>
    </div>
  );
}

function NavItem({ icon, label, active }) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      color: active ? "#A259FF" : "#fff",
      fontWeight: active ? "bold" : "normal",
      fontSize: 13,
      cursor: "pointer"
    }}>
      <span style={{ fontSize: 20 }}>{icon}</span>
      <span>{label}</span>
    </div>
  );
}