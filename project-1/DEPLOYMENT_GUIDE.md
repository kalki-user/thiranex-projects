# Deployment & Hosting Guide: Project Thiranex
## Step-by-Step Roadmap to Launching your Intelligence Suite

This guide explains how to upload your project to GitHub and host it live on the web using **Streamlit Cloud**.

---

## Phase 1: Preparing for Version Control

Before uploading, we need to ensure we don't upload "junk" files (like temporary Python caches). 

### 1. Create a `.gitignore` file
In your project root (`e:\Thiranex\`), create a file named `.gitignore` and add these lines:
```text
__pycache__/
.pytest_cache/
.streamlit/
*.pyc
.env
data/raw/*.csv
```
> [!NOTE]
> We typically exclude large CSV files from GitHub. If your data file is under 25MB, you can include it. If it is larger, you should upload it to a Google Drive or S3 bucket and link it, or use **Git LFS**.

### 2. Verify `requirements.txt`
Ensure your `requirements.txt` contains all the necessary libraries:
```text
pandas
numpy
plotly
streamlit
```

---

## Phase 2: Uploading to GitHub

1. **Initialize Git**:
   Open your terminal in the project folder and run:
   ```bash
   git init
   ```
2. **Add Files**:
   ```bash
   git add .
   ```
3. **Commit**:
   ```bash
   git commit -m "Initial Release: Intelligence Briefing v4.2"
   ```
4. **Push to GitHub**:
   - Create a new "Public" repository on [GitHub.com](https://github.com) named `Thiranex-Analytics`.
   - Run the commands provided by GitHub to link your local folder:
     ```bash
     git remote add origin https://github.com/YOUR_USERNAME/Thiranex-Analytics.git
     git branch -M main
     git push -u origin main
     ```

---

## Phase 3: Hosting on Streamlit Cloud

Streamlit Cloud is free and connects directly to your GitHub repository.

1. **Sign Up**: Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. **New App**: Click **"New app"**.
3. **Configure**:
   - **Repository**: Select `YOUR_USERNAME/Thiranex-Analytics`.
   - **Branch**: `main`.
   - **Main file path**: `app.py`.
4. **Deploy**: Click **"Deploy!"**.

### 🚀 What happens next?
Streamlit will "spin up" a server, install the libraries from your `requirements.txt`, and launch your dashboard at a public URL (e.g., `https://thiranex-analytics.streamlit.app`).

---

## Phase 4: Managing Large Datasets in Production

If your `online_retail_real.csv` is too large for GitHub (over 100MB), follow this "Pro Tip":

1. Upload the CSV to a **GitHub Release** or **Dropbox**.
2. Update your `IntelligenceEngine` in `main.py` to download the file if it's not found locally:
   ```python
   def load_data(self):
       if not os.path.exists(self.file_path):
           url = "https://your-direct-link-to-data.csv"
           self.df = pd.read_csv(url)
       else:
           self.df = pd.read_csv(self.file_path)
   ```

---

## Summary for your Portfolio
Hosting your app demonstrates that you understand the **Full-Stack Data Science Lifecycle**:
1. Data Engineering (Python/Pandas).
2. Advanced Analytics (RFM/Cohorts).
3. Visualization (Plotly).
4. Deployment (Git/GitHub/Cloud).
