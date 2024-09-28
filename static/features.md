##### Changelog:
###### 2024/09/28 - First major release!
After it turned into abandonware, I've taken it on to overhaul OpenEFT to make it function better. I'm no developer, but I know enough to ~~break~~ fix a few things.
Let's talk about some major changes

- Reworked image handling for New EFT creation
- Simplified trainstop logic
	- Step 3: Reason limited to "ATF", Date will now auto-populate, "None" is now auto-populated for missing fingerprints
	- Step 4: "No Middle Name" is a checkbox now to avoid concatenation errors
		- **Important**! SSN is now a protected field. Use the "Validate SSN" button to ensure that your SSNs match and are the correct length before proceeding
	- Step 5: "Race" now matches OPM's list, simplified "Eye Color," simplified "Hair Color," removed incorrect "Sex" entries and added _Non-Binary_ as a selection
- Fixed EFT generation logic, added error-catching logic to prevent some concatenation errors
- Reworked EFT download page
	- Added logic to delete EFT directly from the download page to protect sensitive data
- Changed port to more standard TCP/8080
- Bound Django to 0.0.0.0 so it can be accessible from other hosts on local network
- Cleaned up trainstop form appearance
- Corrected timezone to avoid "time traveling" issues on eForms
- Added a new button on the home page to quickly start a new EFT
- Added an acknowledgement regarding an2ktool (a NBIS binary) restricting functionality of the EFT Viewer
	- Added a link to NIST Viewer as an alternative
- Added information about ATF requirements for EFT generation specifics
- Tested generated EFT with both Form 1 and Form 4
- Reworked loading images
- Moved NBIS to local repo
- Lots of javascript logic added
- Aligned Linux build script with Windows build script
- Branding! There's a new fun logo.

Behind the scenes:
- Markdown engine updated to markdown-it v12.3.2
- Python updated to 

Separtely, I have begun working on a 10-print version of the app which records all 10 rolls, 2 slaps, and 2 thumbs. The logic is working but does not format to ATF/EBTS specifications correctly. Do not use that branch, as it will not validate.