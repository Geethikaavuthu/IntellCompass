Purpose
-------
This project includes two requirements manifests so you can keep installs small:

- `requirements-minimal.txt` — the minimal runtime dependencies for the app (recommended for most uses).
- `requirements-optional.txt` — optional heavy dependencies (AI features). Install only when you need them.

Quick install (recommended)
---------------------------
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
# or .\.venv\Scripts\activate    # cmd
```

2. Install minimal requirements without caching (saves disk space):

```powershell
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements-minimal.txt
```

3. Only install optional AI dependencies when needed:

```powershell
python -m pip install --no-cache-dir -r requirements-optional.txt
```

Space-saving tips
-----------------
- Use `--no-cache-dir` to avoid pip saving wheel caches.
- Use a lightweight Python installation (Miniconda or system Python) — avoid full Anaconda if you want minimal disk use.
- If you installed optional packages before and want to free space, uninstall them:

```powershell
python -m pip uninstall -y google-generativeai grpcio protobuf google-api-core google-api-python-client
```

- Use a shared Redis or external services for caches in production to avoid local disk overhead.

If you want, I can:
- Create a `setup_dev.ps1` script to create the venv and install minimal requirements (fast, minimal).
- Add CI instructions that use the minimal requirements file.

Tell me which automation you want and I will add it. 