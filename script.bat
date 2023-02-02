@echo off

setlocal enabledelayedexpansion

rem Set the maximum number of times to try executing the script
set max_tries=500

rem Initialize the counter
set counter=1

:loop

rem Execute the script
python main.py -m scrape_companies 

rem Check the exit code of the script
if %errorlevel% == 0 (
    rem Set the flag to True if the script executes successfully
    set success=true
) else (
    rem Increment the counter if the script fails
    set /a counter=counter+1
    if !counter! leq %max_tries% (
        goto loop
    )
)

rem Check if the script was successful
if defined success (
    echo The script was executed successfully.
) else (
    echo The script failed after %max_tries% tries.
)
