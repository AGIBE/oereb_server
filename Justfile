# use PowerShell instead of sh:
set shell := ["cmd.exe", "/c"]

lint:
    uvx ruff check
    uvx ruff format

test env:
    uv run pytest tests --env={{env}}

test_asy:
    uv run pytest tests\test_concurrent_extracts_async.py --env=dev

printup:
    cd C:\Daten\prog\apache-tomcat-9.0.62\bin && startup.bat
    
printdown:
    cd C:\Daten\prog\apache-tomcat-9.0.62\bin && shutdown.bat
    