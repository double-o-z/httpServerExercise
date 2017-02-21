# httpServerExercise

Run server with python:
python ThreadedHTTTPServer.py

Note: the server will run forever until terminated.

Run example client with PS script:
.\client_upload_file.ps1

Note: The script will upload one file via HTTP Post to the server.
In turn the server will save the file locally, send the file to VirusTotal for inspection, 
create a report and respond to the client via json.

Also note: The inspection in VirusTotal may take a few seconds to a minute, and thus the client may be suspended until a response is given.

The client script will ask the user for input - a file name this is found in the same folder, to check for viruses.
Type on of the EICAR files' names.

Note, VirutsTotal does not flag EICAR files as viruses.

The client then prints the number of infections found by VirutsTotal to the log file and the screen and exits.
