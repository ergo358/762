export function saveProfile(profile) {
  localStorage.setItem("profile", JSON.stringify(profile));
}

export function loadProfile() {
  try {
    return JSON.parse(localStorage.getItem("profile"));
  } catch {
    return null;
  }
}