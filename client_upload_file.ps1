# Create the log file function and file
$Logfile = "logs\client.log"
Function LogWrite
{
   Param ([string]$logstring)

   Add-content $Logfile -value "$logstring  -  From Client 127.0.0.1"
}

# Create the WebClient that makes the post request
$WebClient = new-object System.Net.WebClient

# Prepare the paramaters for the post request
$Uri = "http://localhost:8080/"
$fileName = Read-Host -Prompt 'Input file name: '

# Prepare full path ofthe input file
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
$filePath = $scriptPath + "\" + $fileName

# Print to console file name and server address
LogWrite "Uploading $fileName to $Uri"

# Send the post request and save response
$Response = $WebClient.UploadFile($Uri,$filePath)

# Print response to console
[System.Text.Encoding]::ASCII.GetString($Response) | LogWrite