import { loadInitialSettings } from "./storage.js";
import { createTimerStore } from "./timer-store.js";

const settings = loadInitialSettings();

if (settings) {
  const store = createTimerStore(settings);
  window.pomodoroApp = {
    settings,
    store,
  };
}