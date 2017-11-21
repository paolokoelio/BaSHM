This is a project for a Master Thesis in Computer Engineering about TRIAGE methods application
in Digital Forensics.

Based on pytsk, BaSHM stands for [...]. The aim is to develop a Python program to speed up and automate parts of procedures
for forensic data acquisition and searching for clues (artifacts to-be evidence).

You can check and disable Windows automount feature for new drives.
Then you can connect a drive and check its information together with its SMART health indicators.
You have thus created a folder for a case where you will save the timelines of a drive.
Also information on logical structure is available, you should check that before extracting timelines.
Then you're free to choose whether generating a super-timeline of events with log2timeline tool.
Or sticking with TSK tools to compute smaller file system timelines, using both 4.5 binaries or custom version 3 Python wrapper pytsk.
Then you're free to analyze the generated body-format and CSV files with grep, text editor or through the web interface.
Such interface should provide means to rapidly assess the presence of abnormal event activity with non linear displacement and colors.

INSTALLATION
- Clone the source and install python 2.7
- clone or install pytsk that comes with sleuthkit source
- setup and build pytsk by following instructions on pytsk readme (pay attention to Visual C++ 2008-10 part)
- download Windows version of plaso 1.5.1 and TSK 4.5 and put the "root folders" in the root of BaSHM
- to run BaSHM execute python bashm.py in bashm folder and you're done
