import React, { useState, useEffect } from "react";

function getInitial(name) {
  return name && name.trim().length > 0 ? name.trim()[0].toUpperCase() : "C";
}

export default function Profile() {
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [desc, setDesc] = useState("");

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem("profile") || "{}");
    setName(data.name || "");
    setRole(data.role || "");
    setDesc(data.desc || "");
  }, []);

  const handleSave = () => {
    localStorage.setItem(
      "profile",
      JSON.stringify({ name, role, desc })
    );
    alert("Профиль сохранён!");
  };

  return (
    <div style={{
      maxWidth: 400, margin: "0 auto", padding: 24, background: "#18181F", borderRadius: 10, color: "#fff"
    }}>
      <h2>Профиль специалиста</h2>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: 16 }}>
        <div style={{
          width: 64, height: 64, borderRadius: "50%", background: "#444", color: "#fff",
          display: "flex", alignItems: "center", justifyContent: "center", fontSize: 32, fontWeight: "bold"
        }}>
          {getInitial(name)}
        </div>
      </div>
      <div>
        <label>Имя</label>
        <input
          style={{ width: "100%", marginBottom: 10 }}
          placeholder="Ваше имя"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <small style={{ color: "#aaa" }}>Ваше имя будет видно клиентам</small>
      </div>
      <div>
        <label>Должность</label>
        <input
          style={{ width: "100%", marginBottom: 10 }}
          placeholder="Кто вы? (например, 'Лучший барбер в Москве')"
          value={role}
          onChange={e => setRole(e.target.value)}
        />
        <small style={{ color: "#aaa" }}>Например: 'Мастер маникюра', 'Стилист', и т.д.</small>
      </div>
      <div>
        <label>Описание</label>
        <textarea
          style={{ width: "100%", marginBottom: 10 }}
          placeholder="Пишите здесь всё, что угодно: о себе, услугах, контактах…"
          rows={4}
          value={desc}
          onChange={e => setDesc(e.target.value)}
        />
        <small style={{ color: "#aaa" }}>Это описание увидят клиенты на странице бронирования</small>
      </div>
      <button
        style={{
          width: "100%", padding: 10, background: "#a259ff", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer"
        }}
        onClick={handleSave}
      >
        Сохранить
      </button>
    </div>
  );
}