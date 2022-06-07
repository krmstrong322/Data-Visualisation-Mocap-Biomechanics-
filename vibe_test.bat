@echo off
title VIBE batch run
CD /D C:\Users\KaiArmstrongMSKPhD\Desktop\VIBE-master
echo Prepare large batch of VIBE
call E:\miniconda\Scripts\activate.bat venv_vibe
for /f %%a IN ('dir /b /s "E:\Videos\pt*\*.mkv"') do call python C:\Users\KaiArmstrongMSKPhD\Desktop\VIBE-master\demo_alter.py --vid_file %%a --output_folder E:\Videos\output\ --detector maskrcnn --save_obj
pause
