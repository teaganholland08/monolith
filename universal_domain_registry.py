"""
UNIVERSAL DOMAIN REGISTRY - Project Monolith v5.5
The master registry of all domains and agent specializations.
"""

DOMAINS = {
    "finance": ["trading", "arbitrage", "defi", "tax_optimization", "portfolio", "forex", "crypto"],
    "content": ["blog_writing", "seo", "social_media", "video_script", "email_marketing", "copywriting"],
    "tech": ["web_dev", "api_integration", "automation", "security", "cloud_infra", "data_pipeline"],
    "commerce": ["dropshipping", "lead_gen", "affiliate", "saas", "digital_products", "consulting"],
    "operations": ["monitoring", "scheduling", "reporting", "alerting", "backup", "optimization"],
    "research": ["market_analysis", "competitor_intel", "trend_detection", "news_aggregation", "patent_search"],
    "health": ["biometrics", "nutrition", "sleep_optimization", "fitness", "mental_clarity"],
    "legal": ["contract_review", "compliance", "ip_protection", "tax_law", "entity_structure"],
}

SENTINEL_TYPES = ["watchdog", "auditor", "recovery", "health_check"]


def get_all_agent_names() -> list:
    """Returns a flat list of all agent names."""
    names = []
    for domain, specs in DOMAINS.items():
        for spec in specs:
            names.append(f"{domain}_{spec}_agent")
    return names


def get_domain_count() -> dict:
    """Returns statistical summary of the registry."""
    total_agents = sum(len(v) for v in DOMAINS.values())
    total_sentinels = len(DOMAINS) * len(SENTINEL_TYPES)
    return {
        "domains": len(DOMAINS),
        "specializations": total_agents,
        "potential_agents": total_agents,
        "potential_sentinels": total_sentinels,
    }


if __name__ == "__main__":
    stats = get_domain_count()
    print(f"[REGISTRY] Domains: {stats['domains']}")
    print(f"[REGISTRY] Potential Agents: {stats['potential_agents']}")
    print(f"[REGISTRY] Potential Sentinels: {stats['potential_sentinels']}")
