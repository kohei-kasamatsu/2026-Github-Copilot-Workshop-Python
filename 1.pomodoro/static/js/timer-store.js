import { createInitialTimerState } from "./timer-core.js";

export function createTimerStore(settings) {
  return {
    getState() {
      return createInitialTimerState(settings);
    },
  };
}