# TDS GA5 – Q2: Dual Embedding Alignment

A beginner-friendly guide to running the solution for **Dual Embedding Alignment: Ollama, FAISS, and Rank Correlation**.

You do not need to write or edit any Python code. Follow the instructions for your operating system, replace the sample dataset with the file from your assignment page, run the program, and submit the generated JSON.

## What this program does

The program:

1. Reads the 50 corpus sentences and 10 evaluation queries from `dataset.json`.
2. Uses two local Ollama embedding models: `nomic-embed-text` and `mxbai-embed-large`.
3. Builds separate FAISS indexes using normalized embeddings.
4. Finds the top three matching documents for each query.
5. Calculates Spearman's rank correlation across the full document rankings.
6. Saves the final 10-row JSON answer in `answer.json`.

## Before you begin

You will need:

- An internet connection for downloading the repository, Python packages, and Ollama models.
- **Git**, to download this repository.
- **Python 3**, to run the solution.
- **Ollama**, to run the embedding models locally.
- A text editor, such as Notepad (Windows), TextEdit (Mac), or VS Code, to replace the dataset file.

If Git or Python is not installed, install them first:

- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/

During Python installation on Windows, select **Add Python to PATH** if the installer shows that option.

---

# Part A – Windows instructions

Use **Windows PowerShell** for the commands in this section.

## Step 1 – Create a working folder

1. Open the Start menu.
2. Search for **PowerShell** and open it.
3. Run these commands one at a time:

```powershell
mkdir GA5
cd GA5
```

This creates a folder named `GA5` and moves your terminal into it. You can use a different folder name if you want.

## Step 2 – Download this GitHub repository

Run:

```powershell
git clone https://github.com/24f2003391/TDS-GA5-Q2.git
cd TDS-GA5-Q2
```

The repository has now been downloaded. You should be inside the `TDS-GA5-Q2` folder.

## Step 3 – Create and activate a Python virtual environment

A virtual environment keeps this project's Python packages separate from other Python projects.

Run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

After activation, your PowerShell prompt should show `(.venv)`.

**If PowerShell says that script execution is disabled**, run this command once in the same PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Step 4 – Install the required Python packages

Make sure the virtual environment is activated. Then run:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Wait for the installation to finish.

## Step 5 – Install Ollama and download both embedding models

1. Visit https://ollama.com/download/windows
2. Download and install Ollama for Windows.
3. Open Ollama. Keep it running while you use this solution.
4. Return to PowerShell and run these commands:

```powershell
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

The models are fairly large downloads, so this step may take a little while. You only need to download them once.

## Step 6 – Download your assignment dataset and replace the repository's dataset

**This step is important. Use the dataset downloaded from your own GA5 assignment page.**

1. Open your GA5 assignment page in your browser.
2. Download the file named `dataset.json`.
3. Open your Downloads folder.
4. Right-click the downloaded `dataset.json` and open it with Notepad or VS Code.
5. Press **Ctrl + A** to select everything.
6. Press **Ctrl + C** to copy everything.
7. Now open the `TDS-GA5-Q2` folder that you cloned from GitHub.
8. Find and open the `dataset.json` file already present in that folder.
9. Press **Ctrl + A** to select its existing contents.
10. Press **Ctrl + V** to paste the dataset you copied.
11. Save the file using **Ctrl + S**.

You are replacing the repository's existing `dataset.json` with the one from your assignment page. Keep the filename exactly as `dataset.json`, and do not move it out of the repository folder.

## Step 7 – Run the solution

Return to PowerShell. Check that you are still inside the `TDS-GA5-Q2` folder and that the virtual environment is active.

Run:

```powershell
python solve.py
```

Wait for the program to finish. It will display the result and create a file named **`answer.json`** in the same folder.

## Step 8 – Submit your answer

1. Open the `TDS-GA5-Q2` folder.
2. Open the generated `answer.json` file using Notepad or VS Code.
3. Press **Ctrl + A**, then **Ctrl + C** to copy the complete contents.
4. Open the GA5 assignment submission page.
5. Paste the copied JSON into the answer box and submit it.

**Submit the contents of `answer.json`, not the contents of `dataset.json`.**

---

# Part B – Linux and macOS instructions

Open a Terminal window. The commands below work in a typical Linux or macOS terminal. On Ubuntu/Debian, the optional installation commands below can help install the required system tools.

## Step 1 – Install Git and Python, if needed

### Ubuntu / Debian Linux

Run:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
```

### macOS

Install Git and Python if they are not already installed:

- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/macos/

You can check whether they are available by running:

```bash
git --version
python3 --version
```

## Step 2 – Create a working folder

Run:

```bash
mkdir -p ~/GA5
cd ~/GA5
```

This creates a folder named `GA5` in your home directory and moves the terminal into it. You can choose another location if you prefer.

## Step 3 – Download this GitHub repository

Run:

```bash
git clone https://github.com/24f2003391/TDS-GA5-Q2.git
cd TDS-GA5-Q2
```

You are now inside the downloaded repository folder.

## Step 4 – Create and activate a Python virtual environment

Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, your terminal prompt should show `(.venv)`.

## Step 5 – Install the required Python packages

With the virtual environment activated, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Wait for the installation to finish.

## Step 6 – Install Ollama and download both embedding models

1. Visit https://ollama.com/download
2. Follow the installation instructions for your Linux distribution or macOS.
3. Start Ollama and keep it running while you use this solution.
4. Open a terminal and run:

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

The models are fairly large downloads, so this step may take a little while. You only need to download them once.

## Step 7 – Download your assignment dataset and replace the repository's dataset

**Use the `dataset.json` downloaded from your own GA5 assignment page.**

1. Open your GA5 assignment page in your browser.
2. Download the file named `dataset.json`.
3. Open your Downloads folder and open the downloaded file in a text editor, such as TextEdit (Mac) or VS Code.
4. Select all the text (**Ctrl + A** on Linux, **Command + A** on Mac).
5. Copy the selected text (**Ctrl + C** on Linux, **Command + C** on Mac).
6. Open the `TDS-GA5-Q2` folder you cloned from GitHub.
7. Open the `dataset.json` file already present in that folder.
8. Select all its existing text (**Ctrl + A** on Linux, **Command + A** on Mac).
9. Paste the copied dataset (**Ctrl + V** on Linux, **Command + V** on Mac).
10. Save the file (**Ctrl + S** on Linux, **Command + S** on Mac).

You are replacing the repository's existing `dataset.json` with the one from your assignment page. Keep the filename exactly as `dataset.json`, and do not move it out of the repository folder.

## Step 8 – Run the solution

Return to your terminal. Make sure you are inside the `TDS-GA5-Q2` folder and that the virtual environment is active.

Run:

```bash
python solve.py
```

Wait for the program to finish. It will display the result and create a file named **`answer.json`** in the same folder.

## Step 9 – Submit your answer

1. Open the `TDS-GA5-Q2` folder in your file manager.
2. Open the generated `answer.json` file in a text editor.
3. Select and copy the complete contents (**Ctrl + A**, **Ctrl + C** on Linux; **Command + A**, **Command + C** on Mac).
4. Open the GA5 assignment submission page.
5. Paste the copied JSON into the answer box and submit it.

**Submit the contents of `answer.json`, not the contents of `dataset.json`.**

---

# What should the answer look like?

The program generates **10 rows**, one for each evaluation query. Each row contains seven values. The generated `answer.json` is written as **one compact line**, with no extra spaces or line breaks:

```json
[[idx_a1,idx_a2,idx_a3,idx_b1,idx_b2,idx_b3,rho],[idx_a1,idx_a2,idx_a3,idx_b1,idx_b2,idx_b3,rho]]
```

- Values 1–3: the top three document indices returned by `nomic-embed-text`.
- Values 4–6: the top three document indices returned by `mxbai-embed-large`.
- Value 7 (`rho`): Spearman's rank correlation between the two models' rankings across all documents.

Your actual `answer.json` will contain numeric values, not the labels shown in this example. Copy the entire JSON array from that file into the assignment submission box.

# Troubleshooting

| Problem | What to do |
|---|---|
| `git` is not recognized / command not found | Install Git, reopen your terminal, and try again. |
| `python` or `python3` is not found | Install Python 3 and reopen your terminal. On Windows, try `py -3`. |
| Virtual environment activation fails on Windows | Follow the PowerShell execution-policy instruction in Step 3. |
| `ollama` is not recognized / command not found | Install Ollama, then close and reopen your terminal. |
| Connection refused / cannot connect to Ollama | Start Ollama and leave it running while the script executes. |
| Model not found | Run both `ollama pull` commands again and wait for them to finish. |
| A Python package is missing | Activate `.venv` and run `pip install -r requirements.txt` again. |
| Dataset file cannot be found | Confirm that `dataset.json` is in the same folder as `solve.py`. |
| The program has finished but you cannot find the answer | Look for `answer.json` in the same `TDS-GA5-Q2` folder. |

## Important reminders

- Replace the repository's `dataset.json` with the file downloaded from your own assignment page.
- Do not rename `dataset.json`.
- Do not edit `solve.py`.
- Keep Ollama running while executing the program.
- The file you submit is **`answer.json`**.
