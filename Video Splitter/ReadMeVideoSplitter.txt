Read Me For Video Splitter

---Requirements---
Python 3.0+
OpenCV
Numpy
pip (optional)

---How to run---
Once above requirements are met it can be run with any python ide

---Making an executable---
I used pyInstaller for more information on installation visit https://www.pyinstaller.org/
FOR WINDOWS
1. in terminal enter "pip install pyinstaller" to install pyinstaller
2. Download VideoSplitter.py and icon.ico(optional)
3. in the terminal cd to the location of VideoSplitter.py
4. enter the following:
	pyinstaller -F -w --icon=icon.ico ^
	--add-data "INSERT LOCATION OF opencv_ffmpeg341_64.dll; FILE./" ^
	VideoSplitter.py 
For a break down of the commands:
First statement "pyinstaller -F -w --icon=icon.ico ^"
-F means one file if you would like a system of files (i.e. a directory that contains all revelvent files this shouldnt be included)
-w means windowed or no consle when it i run u will not get a terminal screen because the program is GUI based
--icon is to add an icon. This is completely optional but I think the choosen icon is cute and it gives our program charachter.
If you dont apprectiate or like the cute icon dont include this part but jokes are on you
FYI the "^" just means more stuff will be added to the statement.

Second statement "--add-data "INSERT LOCATION OF opencv_ffmpeg341_64.dll; FILE./" ^"
When I was compiling the program it was not including opencv in the bundle and therefore my program wasnt running.
Because of this issue u have to manually tell pyinstaller u want to include opencv.
You have to find the location of where your computer has installed opencv_ffmpeg*.dll (the exact name of the file varies by version)
Mine was at "C:\Users\IEUser\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\opencv_ffmpeg341_64.dll"
Therefore my second line was "--add-data "C:\Users\IEUser\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\opencv_ffmpeg341_64.dll;./" ^" 

Third statement
Literally just the file name of what u wanna compile "VideoSplitter.py"

5. After this is done a folder "dist" will be made. Inside you will find VideoSplitter.exe which you should be able to run.

FOR LINUX
1. Steps 1-3 are identical to windows
2. Enter in the following:
	pyinstaller --onefile --windowed --icon=icon.ico 
	--add-data "INSERT LOCATION OF opencv_ffmpeg341_64.dll; FILE./" ^
	VideoSplitter.py 
3. Very similar documentation to Windows
4. You should be greeted with a "dist" folder with the executable inside

FOR MAC
I literally have no idea but I assume its similar to above ^^^

---Using the program---
ANNOTAION FILE
Formmating is "00:00:00 00:00:00 Action\n"
Where it is "starttime endtime nameOfAction"
Has to be a .txt
VIDEO FILE
The output is supported to to be either avi or mp4 
Other inputs probably work but do at your own risk
FPS
If you dont know use 30, its probably 30 but also try to figure it out
ONCE YOU RUN
Youll get a progress bar, itll take a while and it will vet for a lot of issues but not everything
It will create a "Video Sets" file in your home dir. In that dir a file for each action is made with all the video segments
Videos are broken up into 10 second segments.
If there was an issue after the process is complete a warnings/errors screen will pop up.  
 