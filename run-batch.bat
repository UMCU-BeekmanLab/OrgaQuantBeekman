call env\Scripts\activate
for /d %%i in (data\*) do (
    echo %%i
    call python scripts/batchDetection.py "%%i" > "%%i/output.log"
    ) 
PAUSE