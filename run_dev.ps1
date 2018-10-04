.\venv\Scripts\activate.ps1
$env:FLASK_ENV="development"
$env:FLASK_APP="pg-ledger-pyflask-api"
flask run
