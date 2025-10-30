# 🧭 Contributing Guide

Thank you for contributing to **Software Engineering Course project**!
This guide explains how to safely make contributions, test your changes, and keep our Git history clean and consistent.

---

### 🚀 Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork:

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
3. **Add the main repo as a remote**:

   ```bash
   git remote add upstream https://github.com/<org-or-owner>/<repo-name>.git
   ```

---

### 🌱 Creating a New Branch

Always create a separate branch for your work:

```bash
git checkout -b feature/add-new-endpoint
```

#### ✅ Branch Naming Convention

| Type              | Prefix     | Example                   |
| ----------------- | ---------- | ------------------------- |
| New feature       | `feature/` | `feature/add-auth-api`    |
| Bug fix           | `fix/`     | `fix/vue-login-redirect`  |
| Chore or refactor | `chore/`   | `chore/update-deps`       |
| Test-related      | `test/`    | `test/api-user-endpoints` |

> ⚠️ Never work directly on the `main` or `develop` branch.

---

### 💻 Making Code Changes

* Write **clear, small commits** for each logical change.
* Follow consistent code style:

  * **Backend:** use `black` and `isort`
  * **Frontend:** follow ESLint + Prettier conventions
* Run linters before committing:

  ```bash
  # Backend
  black app tests && isort app tests

  # Frontend
  npm run lint
  ```
* Commit with meaningful messages:

  ```bash
  git commit -m "feat(api): add JWT authentication to user login"
  ```

---

### 🧪 Writing and Running Tests

#### 🐍 Backend (FastAPI + pytest)

* Place tests inside the `tests/` directory.
* File naming: `test_<module>.py`
* Run backend tests:

  ```bash
  pytest --maxfail=1 --disable-warnings -q
  ```
* To test specific files:

  ```bash
  pytest tests/test_users.py
  ```

#### ⚡ Frontend (Vue + Vitest)

* Place component tests in the same folder or under `src/tests/`.
* File naming: `<Component>.spec.ts` or `<Component>.spec.js`
* Run frontend tests:

  ```bash
  npm run test
  ```
* Run a specific test file:

  ```bash
  npx vitest run src/components/MyComponent.spec.ts
  ```

> ✅ All tests (both backend and frontend) **must pass before submitting a PR.**

---

### 🔄 Keeping Your Branch Updated (Rebasing)

Before opening a pull request, always **rebase** to stay in sync with `main`:

```bash
git fetch upstream
git rebase upstream/main
```

If you hit merge conflicts:

```bash
git status   # see conflicted files
# fix conflicts manually
git add .
git rebase --continue
```

Then force-push your rebased branch:

```bash
git push origin feature/your-branch-name --force
```

> 💡 Rebase keeps the Git history clean and linear — **avoid merging main into your branch** unless necessary.

---

### 🔍 Submitting a Pull Request

1. Push your branch to your fork:

   ```bash
   git push origin feature/your-branch-name
   ```
2. On GitHub, open a **Pull Request**:

   * **Base branch:** `main` (or `develop`, if used)
   * **Compare branch:** your feature branch
3. Fill in:

   * A descriptive **title**
   * A short **summary** of your changes
   * Reference any related issues (e.g., `Closes #42`)
   * Mention reviewers or tag teammates

---

### 🧹 After Merge: Cleaning Up

Once your PR is merged:

```bash
# Delete local branch
git branch -d feature/your-branch-name

# Delete remote branch
git push origin --delete feature/your-branch-name

# Update local main
git checkout main
git pull upstream main
```

---

### 🧭 Quick Reference

| Action               | Command                                          | Notes             |
| -------------------- | ------------------------------------------------ | ----------------- |
| Create branch        | `git checkout -b feature/xyz`                    | Start new work    |
| Sync with main       | `git fetch upstream && git rebase upstream/main` | Stay updated      |
| Run backend tests    | `pytest`                                         | FastAPI backend   |
| Run frontend tests   | `npm run test`                                   | Vue frontend      |
| Push branch          | `git push origin feature/xyz`                    | Push to your fork |
| Delete merged branch | `git branch -d feature/xyz`                      | After merge       |

---

### 💡 Tips for Safe Contributions

* Always run **both back-end and front-end tests** before opening a PR.
* Keep PRs focused — one feature or fix per PR.
* Avoid large formatting-only changes.
* Communicate early if your work might overlap with someone else’s.
* Keep a clean commit history — use **rebase** and **squash** when needed.

---
