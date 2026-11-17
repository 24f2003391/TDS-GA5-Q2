# TDS GA5 – Q2

Follow the instructions for your operating system. You do not need to edit the Python code.

## Windows

1. Install [Git](https://git-scm.com/downloads), [Python 3](https://www.python.org/downloads/), and [Ollama](https://ollama.com/download/windows). During Python installation, enable **Add Python to PATH** if shown.

2. Open **PowerShell** and run:

```powershell
mkdir GA5
cd GA5
git clone https://github.com/24f2003391/TDS-GA5-Q2.git
cd TDS-GA5-Q2
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

   If PowerShell blocks environment activation, run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

3. Open Ollama and keep it running. In PowerShell, download the models:

```powershell
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

4. Download **dataset.json** from your GA5 assignment page. Replace the repository's `dataset.json` with your downloaded file (or paste its contents into that file). Save it with the exact name `dataset.json` in the `TDS-GA5-Q2` folder.

5. In PowerShell, from the `TDS-GA5-Q2` folder with `.venv` activated, run:

```powershell
python solve.py
```

6. Open the generated `answer.json` in the same folder. Copy its complete contents, paste them into the GA5 answer box, and submit.

## Linux

1. Install Git, Python, and Ollama. On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
```

   Install Ollama using the instructions at https://ollama.com/download.

2. Open a terminal and run:

```bash
mkdir -p ~/GA5
cd ~/GA5
git clone https://github.com/24f2003391/TDS-GA5-Q2.git
cd TDS-GA5-Q2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Make sure the Ollama service is running, then download both models:

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

4. Download **dataset.json** from your GA5 assignment page. Replace the repository's `dataset.json` with your downloaded file (or paste its contents into that file). Save it with the exact name `dataset.json` in the `TDS-GA5-Q2` folder.

5. From the `TDS-GA5-Q2` folder with `.venv` activated, run:

```bash
python solve.py
```

6. Open the generated `answer.json` in the same folder. Copy its complete contents, paste them into the GA5 answer box, and submit.

## macOS

1. Install [Git](https://git-scm.com/downloads), [Python 3](https://www.python.org/downloads/macos/), and [Ollama](https://ollama.com/download).

2. Open Terminal and run:

```bash
mkdir -p ~/GA5
cd ~/GA5
git clone https://github.com/24f2003391/TDS-GA5-Q2.git
cd TDS-GA5-Q2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Open Ollama and keep it running. In Terminal, download both models:

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

4. Download **dataset.json** from your GA5 assignment page. Replace the repository's `dataset.json` with your downloaded file (or paste its contents into that file). Save it with the exact name `dataset.json` in the `TDS-GA5-Q2` folder.

5. From the `TDS-GA5-Q2` folder with `.venv` activated, run:

```bash
python solve.py
```

6. Open the generated `answer.json` in the same folder. Copy its complete contents, paste them into the GA5 answer box, and submit.

## If something goes wrong

- **Ollama connection error:** Open/start Ollama and keep it running while the script runs.
- **Model not found:** Run the two `ollama pull` commands again.
- **Python package missing:** Activate `.venv` and run `pip install -r requirements.txt`.
- **Dataset not found:** Make sure `dataset.json` is in the same folder as `solve.py`.
- **Cannot find the result:** Look for `answer.json` in the `TDS-GA5-Q2` folder.

**Submit the contents of `answer.json`, not `dataset.json`.**
