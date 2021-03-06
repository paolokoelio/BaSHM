## BaSHM

This is a project for a Master Thesis in Computer Engineering about TRIAGE methods application
in Digital Forensics.

Based on pytsk, BaSHM stands for Bahs Saree Lel Ashyaa Mohema in Arabic "Fast Search For Important Things". 
The aim is to develop a Python program to speed up and automate parts of procedures
for forensic data acquisition and searching for clues (artifacts to-be evidence).

You can check and disable Windows automount feature for new drives.
Then you can connect a drive and check its information together with its SMART health indicators.
You have thus created a folder for a case where you will save the timelines of a drive.
Also information on logical structure is available, you should check that before extracting timelines.

Then you're free to choose whether generating a super-timeline of events with log2timeline tool.
Or sticking with TSK tools to compute smaller file system timelines, using both 4.5 binaries or custom version 3 Python wrapper pytsk.
Now you can to analyze the generated body-format and CSV files with grep, text editor or through the HTML interface.
Such interface provides means to rapidly assess the presence of abnormal event activity with non linear displacement and colors.

INSTALLATION
- clone this source and install python 2.7
- clone or install pytsk package (it comes with sleuthkit source)
- setup and build pytsk by following instructions on pytsk readme (if compiling pay attention to Visual C++ 2008-10 part)
- install smartmontools for Windows (https://www.smartmontools.org/)
- clone or install pySMART python package (https://github.com/freenas/py-SMART/tree/master/pySMART)
- download Windows version of plaso (1.5.1) and TSK (4.5) and put their "root folders" in the root of BaSHM
- rename the plaso and TSK folders to "plaso151" and "sleuthkit45" or accordingly to the config/config.cfg file
- to run BaSHM execute with python2.7 the bashm/bashm.py script and you're done

We skip the original pytsk README to this link: https://github.com/py4n6/pytsk

If downloaded pytsk using git you'll have to first run:

python setup.py update

To build the bindings just use the standard Python distutils method:

python setup.py build
python setup.py install

The same is valid for pySMART.
