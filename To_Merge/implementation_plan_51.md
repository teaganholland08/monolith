# Global Agent Expansion Plan

## Goal Description

Implement the "Global Expansion" and "Revenue & Market Dominance" agent departments for Project Monolith. This involves creating a Central Registry for agent communication and a suite of specialized agents to target global markets, maximize revenue, and ensure system integrity.

## Proposed Changes

### Central Registry (The Backbone)

#### [NEW] [central_registry.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/central_registry.py)

- **Role:** The "Phone Book" and "Event Bus" for the system.
- **Functionality:**
  - Allows agents to register their capabilities.
  - Enables message passing between agents.
  - Implements a "Kill Switch" for the Revenue department.

### Global Expansion Department

#### [NEW] [trend_scout.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/trend_scout.py)

- **Role:** Finds where the people are and what they are buying.
- **Functionality:** Scrapes social signals (simulated or real APIs) to identify high-value keywords and trends.

#### [NEW] [cultural_localizer.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/cultural_localizer.py)

- **Role:** Adapts messaging and offers for local markets.
- **Functionality:** Translates and adapts content based on target region data.

#### [NEW] [geo_arbitrageur.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/geo_arbitrageur.py)

- **Role:** Exploits price differences across regions.
- **Functionality:** Monitors currency and service costs to optimize profitability.

### Revenue & Market Dominance Department

#### [NEW] [funnel_architect.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/funnel_architect.py)

- **Role:** Builds entry points for the Monolith ecosystem.
- **Functionality:** Generates landing page concepts and "hooks".

#### [NEW] [portfolio_manager.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/portfolio_manager.py)

- **Role:** Reinvests assets.
- **Functionality:** Manages the portfolio of generated assets and re-allocates capital.

### Immune System & Operations

#### [NEW] [compliance_guardian.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/compliance_guardian.py)

#### [NEW] [rate_limit_captain.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/rate_limit_captain.py)

#### [NEW] [infrastructure_scout.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/infrastructure_scout.py)

#### [NEW] [refactor_bot.py](file:///c:/Users/Teagan%20Holland/Desktop/Monolith_v4.5_Immortal/System/Agents/refactor_bot.py)

## Verification Plan

### Automated Tests

- Create a test script `System/Agents/tests/test_global_agents.py` to verify:
  - Registry registration and message passing.
  - Agent instantiation and basic `run()` execution without errors.
  - Sentinel file creation (`.done` files).

### Manual Verification

- Run each agent individually and check the `System/Sentinels` directory for output files.
- Verify the content of the sentinel files matches the expected JSON structure.
