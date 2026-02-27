# Project Monolith v5.5 "Immortal" Upgrade Plan

This plan outlines the steps to upgrade Project Monolith from v4.5/v5.0 to v5.5 "Immortal". The upgrade focuses on transitioning agents from purely advisory roles to active execution, implementing critical system hygiene, and hardening the master orchestrator.

## Proposed Changes

### 🛡️ System Hygiene Layer

Implementing a dedicated agent to manage system health and disk longevity, essential for long-term "Immortal" status.

#### [NEW] [system_hygiene.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/system_hygiene.py)

* **Purpose**: Log rotation, temporary file cleanup, and disk space monitoring.
* **Logic**:
  * Rotate logs in `Logs/` directory every 7 days or if size > 10MB.
  * Clear `System/Sentinels/*.done` files older than 48 hours.
  * Monitor disk usage and alert if < 10% remains.

---

### 💰 Active Revenue Engines

Transforming advisory scripts into active execution agents.

#### [MODIFY] [bounty_arbitrageur.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/bounty_arbitrageur.py)

* **Change**: Add active RSS/API scraping for current bounties.
* **Integration**: Add `fetch_gitcoin_bounties()` and `fetch_hackerone_rss()` to provide real-time opportunities instead of static links.

#### [MODIFY] [creative_engine.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/Creators/creative_engine.py)

* **Change**: Add a `generate_assets()` method that simulates (or uses tools for) real asset creation.
* **Action**: Use `generate_image` (simulated in my context) to create art assets based on generated specs.

#### [MODIFY] [first_dollar_tracker.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/first_dollar_tracker.py)

* **Change**: Implement real platform check logic (mocked but structurally correctly for API integration).

---

### 🧠 Orchestration & Hardening

#### [MODIFY] [master_assistant.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/master_assistant.py)

* **Change**: Resolve `# TODO: Hook into Director Schedule`.
* **Addition**: Integrate `system_hygiene` into the maintenance cycle.
* **Improvement**: Update Pillar definitions to include the new hygiene agent.

#### [MODIFY] [monolith_omega.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/monolith_omega.py)

* **Change**: Update version to v5.5 and add the hygiene check to the boot sequence.

---

## Verification Plan

### Automated Tests

1. **Hygiene Test**: Run `python System/Agents/system_hygiene.py` and verify it creates log archives and cleans old sentinel files.
2. **Orchestrator Cycle**: Run `python System/Agents/master_assistant.py` and verify all 5 Pillars (plus Growth/Creative/Scanner) execute without crashing.
3. **Kernel Boot**: Run `python monolith_omega.py` and enter `status` to verify all systems report "GREEN".

### Manual Verification

1. **Check Sentinel Outputs**: Verify `System/Sentinels/system_hygiene.done` exists and reports success.
2. **Review Creative Queue**: Verify `System/Sentinels/creative_engine.done` contains freshly generated specs.
3. **Check Logs**: Ensure `Logs/Treasury/first_dollar.json` is correctly updated after running the tracker.
