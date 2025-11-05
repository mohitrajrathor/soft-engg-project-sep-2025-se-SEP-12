# Backend — AURA

This README explains how to set up, run, and contribute to the backend service for the AURA project (FastAPI + SQLAlchemy).

## Quick start (development)

1. Create & activate a Python environment (recommended: conda or venv)

Using conda:

```fish
conda create -n aura python=3.11 -y
conda activate aura
```

Using venv:

```fish
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```fish
# Make sure you're in the repository root and in the 'backend' directory
cd backend
pip install --upgrade pip
pip install -r requirements.txt
# Install Argon2 support (we use Argon2 as the password hasher)
pip install --no-cache-dir argon2-cffi
# Optional: ensure passlib Argon2 support is present
pip install --no-cache-dir 'passlib[argon2]'
```

3. Initialize / recreate the SQLite DB (dev only)

The app uses `sqlite:///./app.db` by default (file `app.db` in the `backend` directory).
On first run the app creates tables automatically via SQLAlchemy `Base.metadata.create_all(...)`.
If you want a fresh DB, delete `app.db` before starting:

```fish
rm -f app.db
```

4. Run the development server

```fish
# from backend/
uvicorn main:app --reload
```

By default the server runs on `http://127.0.0.1:8000`.

5. Test the signup route

```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'
```

The app prints some logs and will create the `users` table on startup.


## Common issues & troubleshooting

- "no such table: users"
  - Make sure the app ran and created tables on startup. If you previously started the app before `Base.metadata.create_all` was wired, delete `app.db` and restart the server so tables are recreated:

  ```fish
  rm -f app.db
  uvicorn main:app --reload
  ```

- `ValueError: password cannot be longer than 72 bytes`
  - The project code uses Argon2 for password hashing to avoid the bcrypt 72-byte limit. Make sure `argon2-cffi` is installed (see install step above). If you intentionally want bcrypt, pin a compatible `bcrypt` version and ensure passlib picks a working backend.

- `AttributeError: module 'bcrypt' has no attribute '__about__'` or other bcrypt/backend warnings
  - This usually indicates a broken bcrypt wheel or incompatible package. Solutions:
    - Uninstall/reinstall bcrypt: `pip uninstall -y bcrypt` then `pip install bcrypt`
    - Or prefer Argon2 (recommended) and uninstall bcrypt if not needed: `pip uninstall -y bcrypt`

- Pydantic V2 warning about `orm_mode`
  - Some internal schemas may still use `orm_mode` which was renamed to `from_attributes` in Pydantic V2. The warning is harmless but indicates you may want to update Pydantic schema definitions later.


## Configuration

- Database URL: currently hard-coded in `backend/core/db.py` as `sqlite:///./app.db`.
  - For production or testing you can modify `DATABASE_URL` in `backend/core/db.py` or set up environment-based config.

- CORS: configured in `main.py` with dev origins for Vite (`http://localhost:5173`) and common port `http://localhost:3000`.


## Development notes

- Tables are created at application startup using SQLAlchemy `Base.metadata.create_all(bind=engine)` in the app lifespan. This is convenient for local development but you should use proper migrations (Alembic/other tool) for production.

- Password hashing
  - The code currently uses Argon2 via `passlib`. Ensure `argon2-cffi` is installed in your environment.


## Tests & linting

- There are currently no backend tests configured in the repository. If you add tests, prefer `pytest` and add a `backend/tests/` folder.

- Linting / formatting: use `ruff`/`black`/`isort` as preferred. Add config files to the repo if you want automated checks.


## Contributing guide (backend)

1. Create a feature branch from `main` or the relevant branch:

```fish
git checkout -b feat/some-feature
```

2. Keep commits small and focused. Use conventional commit messages if possible.

3. Add tests for new features or bug fixes.

4. Run the app and make sure basic flows (signup/login) work.

5. Open a Pull Request and include:
   - What you changed
   - Why you changed it
   - How to test it locally (commands/data)

6. Maintain code style. If the project adds a pre-commit config later, follow it.


## Recommended additions

- Add `argon2-cffi` to `requirements.txt` to avoid forgetting the package.
- Add a migration tool (Alembic) for schema changes.
- Add unit/integration tests for auth flows.


## Contact / maintainers

If you run into environment-specific issues (WSL, Mac M1, Windows), paste the server logs and the request you executed (mask passwords) and open an issue / PR with reproduction steps.

---

If you want, I can:
- Add `argon2-cffi` to `requirements.txt` now.
- Add a small `backend/health` endpoint that checks DB connectivity and returns 200 if tables exist.
- Add a short test that signs up a user using the test DB.

Tell me which of these you'd like next.
