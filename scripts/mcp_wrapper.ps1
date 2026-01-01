# DaVinci Resolve MCP Server - PowerShell Wrapper for WSL stdio
# Uses async event handlers for non-blocking IO

param(
    [string]$ProjectPath = "C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp",
    [string]$ApiPath = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting",
    [string]$LibPath = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
)

# Set environment variables
$env:PYTHONPATH = $ProjectPath
$env:RESOLVE_SCRIPT_API = $ApiPath
$env:RESOLVE_SCRIPT_LIB = $LibPath

# Setup process
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "$ProjectPath\venv\Scripts\python.exe"
$pinfo.Arguments = "`"$ProjectPath\src\main.py`""
$pinfo.RedirectStandardInput = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $pinfo

# Event handlers for async output - write directly to console
$outAction = {
    if (-not [String]::IsNullOrEmpty($EventArgs.Data)) {
        [Console]::Out.WriteLine($EventArgs.Data)
        [Console]::Out.Flush()
    }
}

$errAction = {
    if (-not [String]::IsNullOrEmpty($EventArgs.Data)) {
        [Console]::Error.WriteLine($EventArgs.Data)
    }
}

# Register event handlers
Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action $outAction | Out-Null
Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action $errAction | Out-Null

# Start process and begin async reading
$process.Start() | Out-Null
$process.BeginOutputReadLine()
$process.BeginErrorReadLine()

# Read stdin and forward to process
while (-not $process.HasExited) {
    $line = [Console]::In.ReadLine()
    if ($null -eq $line) {
        break
    }
    $process.StandardInput.WriteLine($line)
    $process.StandardInput.Flush()
}

# Close stdin and wait
$process.StandardInput.Close()
$process.WaitForExit(10000) | Out-Null

# Cleanup
Get-EventSubscriber | Unregister-Event -Force

exit $process.ExitCode
