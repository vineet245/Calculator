# Simple Calculator

Addition and subtraction using FastAPI, a separate pure-Python Decimal engine,
and a vanilla HTML/CSS/JavaScript frontend. Hindi interface. No database,
authentication, Node.js, React, or frontend arithmetic. No catalogue is needed
for this calculator; future configurators can add JSON data separately.

## Run locally (Python 3.12)

From this folder:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m pytest -q
.venv/Scripts/python main.py
```

Open http://127.0.0.1:8000. API documentation: /docs.
Stop the server with Ctrl+C.

## API

POST /api/calculate

```json
{"first":"0.1","second":"0.2","operation":"add"}
```

```json
{"result":"0.3","expression":"0.1 + 0.2"}
```

Use `subtract` for subtraction. Send numbers as decimal strings for exact
arithmetic. Each input allows up to 30 digits and 12 decimal places.
Invalid data returns HTTP 422. GET /health returns {"status":"ok"}.

## GitHub and Railway (one-time setup)

1. Create a GitHub repository named `simple-python-calculator` (private is fine).
2. Push the contents of this folder to its `main` branch. Include dotfiles and
   `.github/workflows/tests.yml`. Do not include your local virtual environment.
3. In Railway: New Project -> Deploy from GitHub repo -> select that repository.
4. Use Railpack. Dependencies install from requirements.txt. Root directory: `/`.
5. Set Start Command to `python main.py`. It reads Railway's PORT automatically
   and listens on 0.0.0.0. No secrets or variables need to be added for this app.
6. Set Healthcheck Path to `/health`.
7. Enable GitHub Autodeploy and Wait for CI, connected to `main`. The supplied
   workflow runs on pushes to main and pull requests. Ensure required tests run
   and pass; do not bypass them with skipped/cancelled workflows.
8. Under Settings -> Networking -> Public Networking, select Generate Domain.
9. Open the generated HTTPS address. Check 0.1 + 0.2 = 0.3 and 2 - 3 = -1.

Railway may require billing/trial eligibility before running the service.
Review the account's displayed charges when enabling hosting.

## Updates

Make changes on a branch -> run tests -> open a pull request -> merge to main.
GitHub runs the test workflow; with Wait for CI, Railway waits for it before
deploying. Railway activates the deployment after its healthcheck succeeds.
Set required checks on main where your GitHub plan supports branch protection.
For an urgent faulty release, restore the previous Railway deployment and
revert the faulty GitHub commit so subsequent deploys stay corrected.

## Deployment status

This source tree is deploy-ready. A live deployment is only confirmed once a
Railway service reports success and provides a working public URL.
