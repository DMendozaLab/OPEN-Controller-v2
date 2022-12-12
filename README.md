# OPEN Controller V2.0.0
Open-Source controlling software for the OPEN Root Phenotyping System at the David Mendoza labs. The system is designed to run on Armx86 operating systems, mainly Raspberry Pi. 

# Contact Information
## Developer and Maintainer: _Landon Swartz_
Email: lgsm2n@umsystem.edu
Adviser: David Mendoza, Associate Professor, University of Missouri and Kannappan Palaniappan, Professor, University of Missouri

# How to install and run
1. Download and extract the project from this repository to a desired folder location. We recommended the Desktop for user-specific use or the /opt/ folder for system use.
2. Navigate using the terminal (Ctrl+Alt+T) to the project folder location. Navigate to the OPEN_Controller Folder and not the /src/ folder.
3. Use the 'ls /dev/ttyACM*' command to see the relavant serial port locations for the Arduinos
4. Run the program using the command format 'python3 src/main.py --GRBL {GRBL Arduino Location} --lights {Lights Arduino Location}'
Use 'python3 src/main.py -h' for more explanation if needed

# Requirements
- Please install GRBL onto one arduino and plug it into the Raspberry Pi. Install the GitPeriphrealControllerV6.ino on the other arduino and plug into the Arduino. 
- Install the requirements.txt using 'pip -r install requirements.txt'
