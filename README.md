# SysWatch

A simple cross-platform system monitor written in Python using `psutil`.

## Getting Started

### 1) Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2) Install requirements

```bash
pip install -r requirements.txt
```

### 3) Run the monitor

```bash
python monitor.py
```

### 4) Optional flags

- `--interval <seconds>` / `-i`: refresh interval (default `1.0`)
- `--once`: print one snapshot and exit

---

## Notes

- Works on Windows/macOS/Linux.
- Uses `psutil` for CPU, memory, disk, and network stats.
