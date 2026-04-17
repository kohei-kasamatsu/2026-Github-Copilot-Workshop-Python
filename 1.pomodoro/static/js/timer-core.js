export function createInitialTimerState(settings) {
  return {
    mode: "work",
    durationMinutes: settings.workDurationMinutes,
  };
}