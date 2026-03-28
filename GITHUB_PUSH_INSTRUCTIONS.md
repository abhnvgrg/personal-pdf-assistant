# 🚀 GitHub Push Instructions

## Step 1: Install Git (if not installed)

Download and install Git from: https://git-scm.com/download/win

**After installation**, restart your terminal/PowerShell.

---

## Step 2: Configure Git

Open PowerShell/Terminal and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `RAG-PDF-Personal-Assistant`
3. Description: `Intelligent PDF Q&A system with comprehensive synthesis using RAG`
4. ✅ Public repository (or Private if you prefer)
5. ❌ **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

**Copy the repository URL** (it will look like):
```
https://github.com/YOUR_USERNAME/RAG-PDF-Personal-Assistant.git
```

---

## Step 4: Initialize and Push

In the project directory, run these commands:

```bash
cd "D:\Code\ML\Personal Assistant(PDF)"

# Initialize Git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete RAG PDF Assistant with comprehensive synthesis"

# Rename branch to main
git branch -M main

# Add remote (REPLACE with your actual repository URL)
git remote add origin https://github.com/YOUR_USERNAME/RAG-PDF-Personal-Assistant.git

# Push to GitHub
git push -u origin main
```

---

## Step 5: Verify

Visit your repository on GitHub:
```
https://github.com/YOUR_USERNAME/RAG-PDF-Personal-Assistant
```

You should see:
✅ README.md displayed nicely
✅ All source files
✅ License file
✅ Project structure

---

## Optional: Add Repository Topics

On GitHub, add these topics to your repository for discoverability:
- `rag`
- `pdf`
- `question-answering`
- `langchain`
- `huggingface`
- `faiss`
- `streamlit`
- `fastapi`
- `nlp`
- `machine-learning`
- `python`
- `retrieval-augmented-generation`

---

## Files Included in Repository

✅ Source code (app.py, main.py, rag_pipeline/, utils/)
✅ README.md (comprehensive documentation)
✅ requirements.txt (all dependencies)
✅ LICENSE (MIT)
✅ .gitignore (excludes data/, vector_store/, venv/)
✅ Configuration templates (.env.example)
✅ Documentation (TESTING_GUIDE.md, etc.)

**Excluded** (via .gitignore):
❌ data/ (uploaded PDFs - user-specific)
❌ vector_store/ (FAISS indexes - generated)
❌ venv/ (virtual environment)
❌ __pycache__/ (Python cache)

---

## Quick Commands Reference

```bash
# Clone your repository (for others)
git clone https://github.com/YOUR_USERNAME/RAG-PDF-Personal-Assistant.git

# Update README
git add README.md
git commit -m "Update README"
git push

# Add new feature
git add .
git commit -m "Add feature: [description]"
git push

# Check status
git status

# View commit history
git log --oneline
```

---

## Troubleshooting

### "fatal: not a git repository"
Run: `git init` in project directory

### "remote origin already exists"
Run: `git remote remove origin` then add again

### "failed to push"
Make sure repository URL is correct:
```bash
git remote -v  # Check current remote
git remote set-url origin https://github.com/YOUR_USERNAME/RAG-PDF-Personal-Assistant.git
```

### Authentication Issues
Use Personal Access Token instead of password:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Use token as password when pushing

---

**Once pushed, share your repository link with others!** 🎉
