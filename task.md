# Task: The Omega Dashboard (Single Pane of Glass)

## 0. PREPARATION

- [x] Analyze User Request ("Make it all one" / "Split as needed")
- [x] Design Modular Architecture (Command / Library / Agents / Terminal)

## 1. CORE ARCHITECTURE

- [ ] Refactor `monolith_ui.py` to use a Main Dispatcher pattern.
- [ ] Implement Sidebar Mode Selector (HUD / OS / ADMIN / EXECUTION).
- [ ] Ensure Global Stats (Battery/Net/Crypto) persist across ALL modes.

## 2. MODULE IMPLEMENTATION

- [ ] **COMMAND MODULE (The HUD)**: Port existing Hardware/Tactical dashboard.
- [ ] **LIBRARY MODULE (The Personal OS)**: Implement Markdown Reader for Manual/Blueprint.
- [ ] **AGENTS MODULE (The Execution Dashboard)**: Visual cards for Scout/Writer/Sentinel.
- [ ] **TERMINAL MODULE (The Admin Console)**: Interactive CLI shell simulation.

## 3. VERIFICATION

- [ ] Verify Mobile Responsiveness (Shield Mode) works in all modules.
- [ ] Test "Ghost Mode" & "Kill Switch" persistent accessibility.
- [ ] Validate Read/Write access to artifacts.
