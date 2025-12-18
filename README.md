# LinkedIn Outreach Automation

This script automates LinkedIn outreach by sending connection requests with a note, checking for acceptance, and sending a follow-up message once the connection is accepted. It uses a one-time manual login and reuses stored cookies for future runs.

## Supported Actions

- **Connect with note** when a Connect option is available.
- **Connect via More actions** for profiles where Connect is not shown directly.
- **Follow-first profiles** are supported; the script locates Connect when it appears in alternate UI layouts.

## How to Run

1. Install dependencies: `pip install -r requirements.txt`  
2. Create `people.csv` with columns `name,profile_url,status`  
3. Run the script: `python automate.py`  
4. On first run, log in manually and press Enter; future runs are automatic
