# TDS GA5 – Q2: Dual Embedding Alignment

This repository contains a Python solution for the **Dual Embedding Alignment: Ollama, FAISS, and Rank Correlation** assignment.

It uses two local Ollama embedding models:

- \`nomic-embed-text\`
- \`mxbai-embed-large\`

The script builds separate FAISS indexes, finds the top three documents for each query, calculates Spearman's rank correlation across all documents, and saves the result as JSON.

## Files

| File | Purpose |
|---|---|
| \`dataset.json\` | Input dataset |
| \`solve.py\` | Main solution |
| \`requirements.txt\` | Python packages to install |
| \`answer.json\` | Generated result after running the solution |

## 1. Download and replace dataset.json

**This is the only dataset step you need to do.**

1. Open your GA5 assignment page and download your \`dataset.json\` file.
2. Open the downloaded \`dataset.json\` in a text editor (Notepad or VS Code).
3. Press **Ctrl + A**, then **Ctrl + C** to copy everything.
4. Open the \`dataset.json\` file from this GitHub repository folder.
5. Press **Ctrl + A**, then **Ctrl + V** to replace its contents with the downloaded data.
6. Save the file.

That is it. Keep the filename exactly as \`dataset.json\` and keep it in the same folder as \`solve.py\`. **Do not change \`solve.py\`.**

## 2. Install Ollama and download the models

Install Ollama from <https://ollama.com/> and make sure it is running.

Open a terminal and run:

\`\`\`bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
\`\`\`

## 3. Install Python dependencies

Open PowerShell or a terminal in the repository folder.

### Windows PowerShell

\`\`\`powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
\`\`\`

### Linux / macOS / WSL

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
\`\`\`

## 4. Run the solution

With Ollama running and your downloaded data saved as \`dataset.json\`, execute:

\`\`\`bash
python solve.py
\`\`\`

The script will calculate the results, print the JSON matrix, and save it in **\`answer.json\`**.

## 5. Submit the result

Open \`answer.json\` and copy its contents into the assignment submission box.

Each row has this format:

\`\`\`json
[idx_a1, idx_a2, idx_a3, idx_b1, idx_b2, idx_b3, rho]
\`\`\`

- First three numbers: top-three document indices from \`nomic-embed-text\`.
- Next three numbers: top-three document indices from \`mxbai-embed-large\`.
- Last number: Spearman's rank correlation across the full document rankings.

## Troubleshooting

- **Connection refused:** Make sure Ollama is running.
- **Model not found:** Run the two \`ollama pull\` commands again.
- **Missing Python package:** Activate your virtual environment and run \`pip install -r requirements.txt\`.
- **Input file error:** Make sure the downloaded content was saved in the repository's \`dataset.json\` file.

