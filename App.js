import React, { useState } from "react";
import Schedules from "./components/Schedules";
import Weekends from "./components/Weekends";
import Profile from "./components/Profile";

export default function App() {
  const [tab, setTab] = useState("schedules");

  return (
    <div style={{ minHeight: "100vh", background: "#18181F" }}>
      {/* Верхняя панель */}
      <div style={{ display: "flex", alignItems: "center", padding: "16px 16px 0 16px" }}>
        <span style={{ fontWeight: "bold", fontSize: 24, color: "#fff", letterSpacing: 1 }}>Zavtra.</span>
        <span style={{ color: "#A259FF", fontWeight: "bold", marginLeft: 2, fontSize: 24 }}>live</span>
      </div>
      <div style={{ padding: "24px 16px 0 16px" }}>
        <h2 style={{ color: "#fff", margin: 0, fontSize: 22 }}>Рабочий кабинет</h2>
      </div>

      {/* Вкладки */}
      <div style={{ display: "flex", gap: 8, padding: "24px 16px 0 16px" }}>
        <button
          onClick={() => setTab("schedules")}
          style={{
            flex: 1,
            background: tab === "schedules" ? "#23232D" : "transparent",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontWeight: tab === "schedules" ? "bold" : "normal",
            padding: "8px 0",
            fontSize: 16,
            transition: "background .15s"
          }}
        >
          Расписания
        </button>
        <button
          onClick={() => setTab("weekends")}
          style={{
            flex: 1,
            background: tab === "weekends" ? "#23232D" : "transparent",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontWeight: tab === "weekends" ? "bold" : "normal",
            padding: "8px 0",
            fontSize: 16,
            transition: "background .15s"
          }}
        >
          Выходные
        </button>
        <button
          onClick={() => setTab("profile")}
          style={{
            flex: 1,
            background: tab === "profile" ? "#23232D" : "transparent",
            color: "#fff",
            border: "none",
            borderRadius: 5,
            fontWeight: tab === "profile" ? "bold" : "normal",
            padding: "8px 0",
            fontSize: 16,
            transition: "background .15s"
          }}
        >
          Профиль
        </button>
      </div>

      {/* Содержимое вкладки */}
      <div style={{ minHeight: 400 }}>
        {tab === "schedules" && <Schedules />}
        {tab === "weekends" && <Weekends />}
        {tab === "profile" && <Profile />}
      </div>

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
        <NavItem icon="📅" label="Расписания" active={tab === "schedules"} onClick={() => setTab("schedules")} />
        <NavItem icon="🛌" label="Выходные" active={tab === "weekends"} onClick={() => setTab("weekends")} />
        <NavItem icon="👤" label="Профиль" active={tab === "profile"} onClick={() => setTab("profile")} />
      </div>
    </div>
  );
}

function NavItem({ icon, label, active, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
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