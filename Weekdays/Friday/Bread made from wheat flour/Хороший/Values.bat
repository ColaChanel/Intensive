@echo off
setlocal EnableDelayedExpansion

set num=100
for /F "delims=" %%i in ('dir /B *.jpg') do (
   set /A num+=1
   ren "%%i" "!num:~1!.jpg"
)