# use PowerShell instead of sh:
set shell := ["cmd.exe", "/c"]

list:
    just --list

lint:
    uvx ruff check
    uvx ruff format

run: printup
    uv run python run_oereb_server_waitress_local.py

test env:
    uv run pytest --env={{env}}

test_concurrent env:
    uv run pytest tests\test_concurrent_extracts.py --env={{env}}

printup:
    cd /d C:\Daten\prog\apache-tomcat-11.0.22\bin && startup.bat
    
printdown:
    cd /d C:\Daten\prog\apache-tomcat-11.0.22\bin && shutdown.bat
    