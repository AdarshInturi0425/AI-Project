# Git Workflow: How to Push Changes to Master Branch

## 🎯 Quick Summary

```
Local Changes → Stage → Commit → Push → Remote Master
```

---

## ✅ Step 1: Check Current Status

```bash
# See what files have changed
git status

# Expected output:
# On branch feature/semantic-layer-pyspark-sql-tests
# Untracked files:
#   PROJECT_OVERVIEW.md
#   LEARNING_PATH.md
#   INPUT_OUTPUT_GUIDE.md
#   quick_start.sh
#   GIT_WORKFLOW.md
#   ... (all new files)
```

---

## 🚀 Step 2: Option A - Push to Feature Branch First (RECOMMENDED)

This is the safest approach. Keep your feature branch updated:

```bash
# 1. Add all new files
git add .

# 2. Commit with descriptive message
git commit -m "[DOCS] Add comprehensive learning & setup guides

- PROJECT_OVERVIEW.md: Complete project explanation
- LEARNING_PATH.md: 8-module structured learning
- INPUT_OUTPUT_GUIDE.md: Input/output guide
- GIT_WORKFLOW.md: Git workflow guide
- quick_start.sh: Automated setup (macOS/Linux)
- quick_start.ps1: Automated setup (Windows)
- summary_stats.py: Summary statistics script
- data_validation.py: Data quality checks
- EXAMPLE_QUERIES.md: 10+ SQL query examples
- colab_duckdb.ipynb: DuckDB Colab notebook
- CONTRIBUTING.md: Contribution guidelines
- Enhanced README.md with badges & resources"

# 3. Verify commit
git log --oneline -3

# 4. Push to your feature branch
git push origin feature/semantic-layer-pyspark-sql-tests

# Output:
# Enumerating objects: 25, done.
# Counting objects: 100% (25/25), done.
# ... (upload process)
# To https://github.com/AdarshInturi0425/AI-Project.git
#    abc1234..def5678  feature/semantic-layer-pyspark-sql-tests -> feature/semantic-layer-pyspark-sql-tests
```

---

## 🔀 Step 3: Create Pull Request (RECOMMENDED)

Go to GitHub and create a PR to merge feature branch → main/master:

```
1. Go to https://github.com/AdarshInturi0425/AI-Project
2. Click "Compare & pull request" (yellow banner)
3. Set:
   - Base: main (or master)
   - Compare: feature/semantic-layer-pyspark-sql-tests
4. Fill PR template:
   - Title: "[DOCS] Add comprehensive documentation & automation"
   - Description: (your commit message)
5. Click "Create pull request"
6. Wait for checks to pass
7. Click "Merge pull request"
```

---

## 🎯 Step 4: Option B - Push Directly to Master (IF SOLO)

Only if you're working alone and want direct push:

```bash
# 1. Make sure you're on master
git checkout master

# 2. Pull latest changes from remote
git pull origin master

# 3. Add your new files
git add .

# 4. Commit
git commit -m "[DOCS] Add comprehensive learning & setup guides"

# 5. Push to master
git push origin master

# Verify
git log --oneline -5
```

---

## 📊 What Gets Pushed

Your commit will include:

**New Files (12 files):**
```
✓ PROJECT_OVERVIEW.md
✓ LEARNING_PATH.md
✓ INPUT_OUTPUT_GUIDE.md
✓ GIT_WORKFLOW.md
✓ quick_start.sh
✓ quick_start.ps1
✓ SemanticLayer/scripts/summary_stats.py
✓ SemanticLayer/scripts/data_validation.py
✓ SemanticLayer/EXAMPLE_QUERIES.md
✓ SemanticLayer/notebooks/colab_duckdb.ipynb
✓ CONTRIBUTING.md
✓ README.md (updated)
```

**Git will track:**
- File additions
- Commits with messages
- Push history

---

## ✅ Verification After Push

### Check GitHub

```bash
# 1. Go to: https://github.com/AdarshInturi0425/AI-Project
# 2. Click "Commits"
# 3. Verify your commit appears at top
# 4. Click on commit to see changed files

# Or via command line:
git log --oneline -5
git show --name-status

# Output should show:
# commit abc1234567890 (HEAD -> master)
# Author: Your Name <your@email.com>
# Date: ...
# 
#     [DOCS] Add comprehensive learning & setup guides
#
# A  PROJECT_OVERVIEW.md
# A  LEARNING_PATH.md
# ...
```

### Verify Remote State

```bash
# Check that remote matches local
git log --oneline origin/master -5

# Should show your commit at top
```

---

## 🔄 If You Made a Mistake

### Undo Last Commit (not pushed yet)

```bash
# Undo last commit, keep files
git reset --soft HEAD~1

# Or undo commit and files
git reset --hard HEAD~1
```

### Undo Last Push (already pushed)

```bash
# Force push previous commit (careful!)
git revert HEAD
git push origin master

# Or reset (harder)
git reset --hard HEAD~1
git push -f origin master  # Warning: dangerous!
```

---

## 📋 Git Commands Reference

| Command | What it does |
|---------|-------------|
| `git status` | Show changed files |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Create commit |
| `git push origin branch` | Push to remote |
| `git log --oneline` | Show commit history |
| `git diff` | Show file changes |
| `git branch` | List branches |
| `git checkout -b feature/name` | Create & switch to branch |
| `git pull origin master` | Get latest from remote |

---

## 🎯 Recommended Workflow

**For team projects:**

1. ✅ Create feature branch
   ```bash
   git checkout -b feature/semantic-layer-improvements
   ```

2. ✅ Make changes locally
   ```bash
   # Edit files
   # Test changes
   ```

3. ✅ Commit regularly
   ```bash
   git add .
   git commit -m "[FEATURE] Add X"
   ```

4. ✅ Push to feature branch
   ```bash
   git push origin feature/semantic-layer-improvements
   ```

5. ✅ Create Pull Request on GitHub

6. ✅ Get code review

7. ✅ Merge to master

**For solo projects:**

1. ✅ Make changes on master
2. ✅ Test thoroughly
3. ✅ `git add .`
4. ✅ `git commit -m "msg"`
5. ✅ `git push origin master`

---

## 🚨 Important Git Best Practices

### ✓ DO:
- Write clear commit messages
- Commit related changes together
- Test before pushing
- Pull before pushing (avoid conflicts)
- Use branches for features

### ✗ DON'T:
- Push broken code
- Use generic messages ("fixed stuff")
- Force push to main branch
- Commit large binaries (use .gitignore)
- Ignore merge conflicts

---

## 📝 Example .gitignore

Create `~/.gitignore` to exclude files:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/

# Data files (large)
*.csv
data/raw/*
data/silver/*
data/gold/*

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## 🆘 Common Git Issues

### Issue: "Updates were rejected"

**Cause:** Remote has changes you don't have locally

**Solution:**
```bash
git pull origin master
# Resolve any conflicts
git push origin master
```

### Issue: "Permission denied"

**Cause:** SSH keys not set up

**Solution:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your@email.com"

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key

# Test
ssh -T git@github.com
```

### Issue: "Nothing to commit"

**Cause:** Files not staged

**Solution:**
```bash
git add .  # Stage all files
git commit -m "message"
git push origin master
```

---

## ✅ Pre-Push Checklist

Before pushing to master:

- [ ] Code is tested and working
- [ ] No sensitive data (passwords, keys) in commits
- [ ] .gitignore includes large/sensitive files
- [ ] Commit messages are clear
- [ ] All tests pass: `pytest -q`
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] `git pull` latest changes first

---

## 🎓 Next Steps After Push

1. ✅ Verify commit on GitHub
2. ✅ Verify CI/CD runs tests
3. ✅ Update CHANGELOG.md
4. ✅ Tag release (if applicable)
5. ✅ Announce to team

---

## 📚 Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [Atlassian Git Guide](https://www.atlassian.com/git)
- [GitHub Desktop GUI](https://desktop.github.com/) (if you prefer UI)

---

**Ready to push? Let's do it! 🚀**
