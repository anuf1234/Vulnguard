@echo off
color 0A
echo.
echo  ========================================================
echo    🛡️  VulnGuard Security Platform v2.0
echo    Complete Vulnerability Management Suite
echo  ========================================================
echo.
echo  Choose your action:
echo.
echo  [1] 🚀 Install Complete Platform
echo  [2] 🔍 Run Security Agent Scan  
echo  [3] 💻 Launch Desktop Application
echo  [4] ⚙️  Command Line Tools Help
echo  [5] 📚 View Documentation
echo  [6] ❌ Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting VulnGuard Platform Installer...
    echo This will install the complete platform with web UI
    echo.
    call vulnguard-installer.bat
) else if "%choice%"=="2" (
    echo.
    echo 🔍 Running Security Agent Scan...
    echo This will scan the local system for vulnerabilities
    echo.
    call vulnguard-agent.bat --no-upload --verbose
) else if "%choice%"=="3" (
    echo.
    echo 💻 Launching Desktop Application...
    start "VulnGuard Desktop" vulnguard-desktop.bat
) else if "%choice%"=="4" (
    echo.
    echo ⚙️  VulnGuard CLI Tools:
    echo.
    call vulnguard-cli.bat --help
    echo.
    echo For more commands try:
    echo   vulnguard-cli.bat assets --help
    echo   vulnguard-cli.bat scan --help
    echo   vulnguard-cli.bat findings --help
) else if "%choice%"=="5" (
    echo.
    echo 📚 Opening documentation...
    if exist README.md (
        notepad README.md
    ) else (
        echo README.md not found in current directory
    )
) else if "%choice%"=="6" (
    echo.
    echo Thank you for using VulnGuard! 👋
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please try again.
    timeout /t 3 >nul
    goto :eof
)

echo.
echo ✅ Operation completed!
pause
