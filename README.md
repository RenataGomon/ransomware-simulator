#Ransomware Simulator (Educational Project)

Educational ransomware simulation written in Python.
This project demonstrates how ransomware-like behavior works in a safe sandbox environment, without encrypting or damaging real user data.

#Important
This is a safe educational simulation.
No real encryption is performed.
Original files are NOT modified.
The program operates only inside the sandbox/ directory.
A safety marker (.SANDBOX_MARKER) is required.

**How to Run**

Make sure you are in the project root folder.
Run simulation
python main.py simulate
This will:
scan sandbox/
create .locked placeholder files
generate README_RESTORE.txt
log the event
Restore simulation results
python main.py restore
Removes .locked files and ransom note.

**Defense Commands**

Create backup
python main.py backup
Copies allowed files to sandbox_backup/.
Recover from backup
python main.py recover
Restores files from backup.
Detect suspicious files
python main.py detect
Scans for .locked files.
Integrity Monitoring
Create baseline:
python main.py baseline
Check for changes:
python main.py check

**How It Works**
Discovery Module
Recursively scans sandbox for allowed file types.
Impact Module
Creates .locked placeholder files (no encryption).
Note Module
Generates README_RESTORE.txt with session info.
Logger Module
Saves events in attack_log.json.
Defense Modules
Provide backup, detection, and integrity monitoring.

**Learning Objectives**
This project demonstrates:
How ransomware selects and targets files
How attack artifacts are created
Why backups are critical
How detection systems identify suspicious activity
How integrity monitoring works

**Safety Mechanisms**
Hard sandbox restriction
Marker file validation
No access outside project directory
No real encryption
File size and extension filtering

**Requirements**
Python 3.9+
No external dependencies required
