"""
LEGAL SENTINEL - Project Monolith v7.0
Purpose: Regional Compliance, ID Acquisition, and Bureaucracy Navigation.
Strategy: Monitor ID Status -> Generate Forms -> Track Submissions.
"""
import json
import io
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class LegalSentinel:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.sentinel_dir = self.root / "Sentinels"
        self.data_dir = self.root.parent / "Data"
        self.sentinel_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def audit_identity_status(self):
        """Checks the status of Critical ID documents."""
        print("[LEGAL] ⚖️ Auditing Identity Stack...")
        
        # Determine status based on tracker (or default to MISSING if no tracker)
        tracker_file = self.data_dir / "subsidy_tracker.json"
        phn_status = "UNKNOWN"
        bcid_status = "UNKNOWN"
        
        if tracker_file.exists():
            try:
                data = json.loads(tracker_file.read_text())
                for item in data:
                    if item["name"] == "BC Personal Health Number (PHN)":
                        phn_status = item["status"]
                    if item["name"] == "BC ID Supplement":
                        bcid_status = item["status"]
            except:
                pass

        print(f"   -> BCID Status: {bcid_status}")
        print(f"   -> PHN Status: {phn_status}")
        
        return {
            "BCID": bcid_status,
            "PHN": phn_status
        }

    def generate_form_claims(self, status):
        """Generates markdown claim files if status is QUALIFIED or PENDING."""
        if status["BCID"] in ["QUALIFIED", "APPLY_NOW"]:
            claim_file = self.root.parent / "Documents" / "IDENTITY_SUPPLEMENT_REQUEST.md"
            if not claim_file.exists():
                claim_file.parent.mkdir(exist_ok=True)
                content = """# REQUEST FOR IDENTIFICATION SUPPLEMENT
To: Ministry of Social Development and Poverty Reduction (MSDPR)
Re: Teagan Holland - Date of Birth: [DOB]

I am requesting the Identification Supplement to cover the costs of obtaining my BC Services Card (Photo ID). 

Confirmed Eligibility:
- Receiving Assistance / Person with Persistent Multiple Barriers
- No current valid photo ID
- Required for banking and housing security.

Please issue the supplement voucher immediately.
"""
                claim_file.write_text(content)
                print("[LEGAL] 📝 Generated 'IDENTITY_SUPPLEMENT_REQUEST.md'.")

    def run(self):
        print("\n--- [LEGAL SENTINEL] 🏛️ COMPLIANCE SCAN ---")
        id_status = self.audit_identity_status()
        self.generate_form_claims(id_status)
        
        report = {
            "agent": "legal_sentinel",
            "timestamp": datetime.now().isoformat(),
            "id_status": id_status,
            "compliance": "GREEN" # Assuming no active lawsuits
        }

        with open(self.sentinel_dir / "legal_sentinel.done", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print("--- [LEGAL SENTINEL] SCAN COMPLETE --- \n")

if __name__ == "__main__":
    LegalSentinel().run()
