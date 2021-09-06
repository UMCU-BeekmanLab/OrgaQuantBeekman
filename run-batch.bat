call env\Scripts\activate.bat
for /d %%i in (data\) do (
    python scripts/batchDetection.py "%%i" > "%%ioutput.log"
    ) 
PAUSE