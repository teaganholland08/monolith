# Implementation Plan - Phase 0 Deployment

Deploy the "Zero-Capital Bootstrap" code provided by the user.

## Proposed Changes

### Directory Structure

* `c:\Users\Teagan Holland\Desktop\Master Architecture\Monolith_Profit\`

### Files

1. **`.env`**: Copied from `autonomous_profit_system/.env` to ensure API keys are available.
2. **`requirements.txt`**:

    ```text
    crewai
    langchain-google-genai
    python-dotenv
    pyyaml
    ```

3. **`treasury.py`**: The logic class provided by the user.
4. **`main.py`**: The execution script.
    * *Modification*: Import `load_dotenv` and call it to load the API key from the local `.env` file.

### Execution

1. Install dependencies: `pip install -r requirements.txt`
2. Run system: `python main.py`

## Verification

* Check terminal output for "MONOLITH SYSTEM: ONLINE" and "ASSET GENERATED BELOW".
