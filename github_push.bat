@echo off

:: Enable delayed expansion
setlocal enabledelayedexpansion

set current_path=%cd%
for %%i in ("%current_path%") do (
    set current_folder=%%~nxi
)
set repo_name=%current_folder%

:: Enter Git Credentials after "=" without space
::Example
::set user_name=your_github_username
::set user_email=your_email@example.com
set user_name=Supradeep-007
set user_email=supradeept.07@gmail.com

:: Enter Repo name
:: Enter Repo name if it is different from current folder name

:ask_condition

set /p condition="Is the github repo same as foldername(y or n): "

if /i "%condition%"=="n" (
    set /p repo_name="Enter Repo name: "
    goto :end
) else if /i "%condition%"=="y" (
    echo The repository name is set to: %repo_name%
    goto :end
) else (
    echo Invalid command
    goto :ask_condition
)
:end

:: Git login
git config --global user.name "%user_name%"
git config --global user.email "%user_email%"

:: Initialize a Git repository
git init

:: Add all files to the repository
git add .

:: Commit the changes
set /p commit_message="Enter your commit message: "
git commit -m "%commit_message%"

:: Remove existing remote origin if it exists
git remote remove origin 2>nul

:: Add the remote repository
git remote add origin https://github.com/%user_name%/%repo_name%.git

:: Set the branch to main
git branch -M main

:: Push the commits to the remote repository
git push -u origin main