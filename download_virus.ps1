$url = "http://www.eicar.org/download/eicar.com.txt"

$output = "$PSScriptRoot\eicar.com.txt"

Invoke-WebRequest -Uri $url -OutFile $output