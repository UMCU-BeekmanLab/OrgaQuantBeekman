call env\Scripts\activate
PAUSE
set /p data=<data.conf
PAUSE
echo %data%
PAUSE
for /d %%i in (%data%) do (
    echo %%i
    call python batchDetection.py "%%i" > "%%i/output.log"
    ) 
PAUSE