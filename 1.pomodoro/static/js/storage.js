export function loadInitialSettings() {
  const settingsElement = document.getElementById("initial-settings");

  if (!settingsElement) {
    return null;
  }

  return JSON.parse(settingsElement.textContent || "null");
}