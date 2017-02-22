# Create the log file function and file
$Logfile = "loggers\client.log"
Function LogWrite
{
   Param ([string]$logstring)

   Add-content $Logfile -value "$logstring  -  From Client 127.0.0.1"
}

# Create the WebClient that makes the post request
$WebClient = new-object System.Net.WebClient

# Ask user to check highest cpu process executable, or input a file
$ReportType = Read-Host -Prompt 'Scan High CPU Process Executable or a specific file? 0 for Process, 1 for file: '
if ($ReportType -eq 0){
    $ProcessPathObject = Get-Process | Sort CPU -descending | Select -first 1 | Select-Object Path
    $FilePath = $ProcessPathObject.Path
    Write-Host "Scanning executable: $FilePath"
    LogWrite "Scanning executable: $FilePath"
} elseif ($ReportType -eq 1){
    $FileName = Read-Host -Prompt 'Input file name: '
    $FilePath = $PSScriptRoot + "\" + $FileName
    Write-Host "Scanning input file: $FilePath"
    LogWrite "Scanning input file: $FilePath"
} else {
    Write-Host "Unknown option, terminating..."
    exit
}

# Prepare the paramaters for the post request
$Uri = "http://localhost:8080/"
# $fileName = Read-Host -Prompt 'Input file name: '

# Prepare full path ofthe input file
# $scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
# $filePath = $scriptPath + "\" + $fileName

# Print to console file name and server address
LogWrite "Uploading $FilePath to $Uri"

# Send the post request and save response
$Response = $WebClient.UploadFile($Uri,$FilePath)

# Save Json response
$JsonResponse = [System.Text.Encoding]::ASCII.GetString($Response) | ConvertFrom-Json
$PositiveInfections = $JsonResponse.positives
$ScanID = $JsonResponse.scan_id

LogWrite "Scan ID: $ScanID"
Write-Host "Scan ID: $ScanID"
LogWrite "Number of infections found by VirusTotal: $PositiveInfections"
Write-Host "Number of infections found by VirusTotal: $PositiveInfections"

Write-Host "Client terminates."