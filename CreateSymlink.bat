@echo off
:: Check if a link path was provided
if "%~1"=="" (
  echo Usage: %~nx0 [link_directory_path]
  goto :EOF
)

set "LINK=%~1"
set "TARGET=D:\Projekt\wow-api-libraries\API"

echo Creating symlink...
mklink /J "%LINK%" "%TARGET%"

if errorlevel 1 (
  echo Failed to create symlink.
) else (
  echo Symlink created successfully.
)
pause
