If the user appends the letters 'sa' after a question mark, provide a short answer no longer than a single sentence.

Entries in DevelopmentLog.md should document steps for reproducibility: commands, versions, and context sufficient for someone to replicate the work from scratch.

When the user asks a purely interpretational, comprehension, or theoretical question about quantum mechanics, append the response to the end of ~/quantum/Q2.md in readable markdown format (proper headings, LaTeX in $$ blocks, etc.).

When writing markdown that will be converted to PDF via pandoc + xelatex with Latin Modern fonts, never use bare Unicode Greek letters, math symbols, or special characters (α, β, γ, δ, η, θ, φ, ν, π, ∼, ⟩, ✓, ✗, →, etc.) outside of math delimiters. All such characters must appear inside $...$ or $$...$$ so LaTeX renders them natively. Use LaTeX equivalents:
- Greek: $\alpha$, $\beta$, $\gamma$, $\delta$, $\eta$, $\theta$, $\varphi$, $\nu$, $\pi$
- Symbols: $\sim$, $\rangle$, $\checkmark$, $\times$, $\to$
- Ket notation outside math: use $|0\rangle$, $|1\rangle$ (never bare |0⟩)

Additional rule for $\sim$ (the tilde/approximately symbol): never place $\sim$ as a standalone math block adjacent to text (e.g. $\sim$5 GHz). This causes pandoc to emit a bare ∼ into text mode. Instead, include the number inside the same math block: $\sim 5$ GHz. Same applies in table cells.

The canonical pandoc command for converting any Q*.md file to PDF is:
pandoc <file>.md -o <file>.pdf --pdf-engine=xelatex -V mainfont="Latin Modern Roman" -V mathfont="Latin Modern Math"
No header.tex or fallback fonts are needed when the markdown follows the rules above.

Running code in Python is via Kiro providing User with the python module and execution command. Kiro is unable to issue WSL miniconda execution commands directly. Do not include extraneous commands such as `conda activate` — assume the user's environment is already configured.

The double-slit experiment (DSE) quantum circuit implementation went through a complicated debugging process now documented in DevelopmentLog.md. The working approach uses a single-qubit H-P-H circuit computing interference at each screen position separately (not a multi-qubit register). See DevelopmentLog.md for the full history and rationale.

Slide decks use marp (markdown presentation ecosystem). Use `---` as slide separators.

When the user asks about estimating payload volume or context window usage, point them to the circle icon in the chat window — hovering over it shows how much of the context window is in use for the current session.

NEVER read, cat, or display the contents of ~/.aws/credentials, ~/.aws/config, any .env file, any API key file, or any file likely to contain secrets. If the user asks about credential configuration, describe the procedure without reading the actual file. Reference keys by profile name or last 4 characters only, never the full value.

Before providing any execution command that submits jobs to paid quantum hardware (IBM Pay-As-You-Go, AWS Braket QPU, Azure Quantum hardware, etc.), always perform a cost estimate first. State: "I estimate the spend for [brief description of what will run] will be $X. Do you want me to go ahead and provide the execution command?" Wait for user confirmation before providing the command.
