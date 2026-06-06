# Loan Approval Prediction

This project contains:
- a Streamlit app (`app (1).py`) to interactively predict loan approval
- a FastAPI endpoint (`api.py`) for programmatic predictions
- pretrained artifacts: `loan_model.pkl` and `scaler_top5.pkl`

---

## Quick start (local)

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run Streamlit UI:

```bash
python -m streamlit run "app (1).py"
```

3. Run FastAPI (optional):

```bash
uvicorn api:app --reload
```

---

## Deploying the Streamlit app to Streamlit Cloud (formerly Streamlit Sharing)

Follow these steps to publish the Streamlit app publicly:

1. Initialize a Git repository in the project folder (if you haven't already):

```bash
git init
git add .
git commit -m "Initial commit: Streamlit + FastAPI + model" 
```

2. Create a new GitHub repository and push the code there. Replace `<your-repo-url>` with the URL GitHub gives you:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

3. On Streamlit Cloud (https://share.streamlit.io/) sign in with your GitHub account and click **New app** → choose your repo and branch (`main`) and set the main file to `app (1).py`.

4. Click **Deploy**. Streamlit Cloud will install dependencies from `requirements.txt` and start the app. Model artifacts (`loan_model.pkl` and `scaler_top5.pkl`) must be committed to the repo so the app can load them at runtime.

Notes & tips for smooth deployment:
- Ensure `requirements.txt` lists all dependencies (already included). If a package needs a specific version, pin it (e.g., `streamlit==1.58.0`).
- Keep repository size reasonable: large pickle/model files may exceed Streamlit Cloud repo limits. If files are large, use an external storage (S3, Git LFS) and load them at runtime.
- The app uses relative paths to load `loan_model.pkl` and `scaler_top5.pkl`; do not change those paths unless you update the repo structure.
- If you face import errors during deploy, open the app logs in Streamlit Cloud, pin problematic package versions in `requirements.txt`, then re-deploy.

---

## Files of interest
- `app (1).py` — Streamlit frontend
- `api.py` — FastAPI backend with `/predict` endpoint
- `loan_model.pkl`, `scaler_top5.pkl` — model artifacts
- `requirements.txt` — dependency list used by Streamlit Cloud

If you'd like, I can:
- create a small `deploy.sh` script to automate git push steps,
- add Git LFS instructions if model files are large,
- or test the Streamlit app locally in this environment.

---


