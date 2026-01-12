# Form Automation Helper (MV3)

This Chrome extension streamlines internal repair forms by filling:
- System Hours and Oxygen Purity prompts with Confirm
- Accumulator popup values (if present)
- Diagnostic Analysis, Parts Used, and Ending Values/Notes text areas
- Ending Test Results panel: Flow @ 2 LPM, O2 Purity @ 2 LPM, Flow @ 5 LPM, O2 Purity @ 5 LPM, PSI, Hours Out, Alarm Test (Pass/Fail), Install Test Filters
- Parts table: clicks Yes for parts that match your list and checks the confirmation box

## Setup
1. Chrome → Extensions → Enable Developer mode
2. Load unpacked → select this `Work_Automation_V2` folder
3. Pin the extension for quick access

## Use
1. Open target form
2. Click the extension icon to open the popup
3. Enter your values
4. Optional: enable Dry Run to preview actions without clicking submits
5. Click Run Automation

## Notes
- Keyword matching is resilient to minor wording differences
- Per-page “Submit Results” is only clicked if Auto-submit is enabled
- You can re-run after editing values; the script avoids refilling already-handled sections

## Privacy
All values are stored locally via `chrome.storage.sync`.