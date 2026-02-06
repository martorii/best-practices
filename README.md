# 🐍 best-practices

A modern Python repository template showcasing the 2026 "Gold Standard" for development. This project leverages **uv** for blistering fast package management, **Ruff** for linting, **Mypy** for strict typing, and **Pytest** for robust testing.

---

## 🛠 Tech Stack

| Tool | Purpose | Key Benefit |
| :--- | :--- | :--- |
| **[uv](https://github.com/astral-sh/uv)** | Package & Project Manager | Extremely fast, replaces `pip`, `poetry`, and `venv`. |
| **[Ruff](https://github.com/astral-sh/ruff)** | Linter & Formatter | Rust-based; replaces Black, Isort, and Flake8. |
| **[Mypy](https://mypy-lang.org/)** | Static Type Checker | Catches logic errors before code ever runs. |
| **[Pytest](https://pytest.org/)** | Testing Framework | Simple syntax with powerful features like parameterization. |
| **[Pre-commit](https://pre-commit.com/)** | Git Hooks | Automates code quality checks before every commit. |

---

## 📂 Project Structure

This repository uses the **src-layout**, a best practice that forces tests to run against the installed package to catch packaging issues early.

```text
best-practices/
├── .github/workflows/ci.yml  # Automated GitHub Actions
├── src/
│   └── best_practices/       # Main package source
│       ├── __init__.py
│       └── utils.py
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_utils.py
├── .pre-commit-config.yaml   # Pre-commit hook definitions
├── pyproject.toml            # Unified tool configuration
└── README.md
```

---

## 🚀 Quick Start Guide

Get your development environment running in seconds.

### 1. Initialize the Project
If you don't have `uv` installed yet, grab it first. Then, set up the repo:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and enter the repo (or initialize a new one)
mkdir best-practices && cd best-practices
uv init --lib
```

### 2. Install Dependencies & Hooks
`uv` handles the virtual environment and all dependencies automatically.

```bash
# Sync environment and install dev tools
uv sync

# Setup git hooks
uv run pre-commit install
```

---

## 🛠 Development Commands

Stay within the `uv` ecosystem for a consistent experience across different machines.

### Testing & Quality
* **Run Tests:** `uv run pytest`
* **Type Checking:** `uv run mypy src`
* **Linting:** `uv run ruff check .`
* **Auto-Formatting:** `uv run ruff format .`

### Continuous Integration
This repo includes a GitHub Actions workflow (`.github/workflows/ci.yml`). Every push or pull request automatically triggers:
1. **Environment Syncing** via `uv`.
2. **Linting & Formatting** checks via `Ruff`.
3. **Type validation** via `Mypy`.
4. **Unit tests** via `Pytest`.

---

## 💡 Coding Philosophy

> **"Explicit is better than implicit."**
> This repository enforces strict typing and linting to ensure the code remains readable, maintainable, and bug-free.

* **Type Everything:** Use Python type hints for all function signatures.
* **Pure Functions:** Aim for logic that returns values rather than modifying global states.
* **Fail Fast:** Let the CI/CD pipeline catch errors so your main branch stays "green" and deployable at all times.
