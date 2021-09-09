call env\Scripts\activate
set /p data=<data.conf
echo %data%
for /d %%i in (%data%*) do (
    echo %%i
    call python scripts/batchDetection.py %%i > %%i/output.log
    ) 
PAUSE