If the user appends the letters 'sa' after a question mark, provide a short answer no longer than a single sentence.

Entries in DevelopmentLog.md should document steps for reproducibility: commands, versions, and context sufficient for someone to replicate the work from scratch.

When the user asks a purely interpretational, comprehension, or theoretical question about quantum mechanics, append the response to the end of ~/quantum/Q2.md in readable markdown format (proper headings, LaTeX in $$ blocks, etc.).

When writing markdown that will be converted to PDF via pandoc + xelatex with Latin Modern fonts, avoid Unicode symbols (✓, ✗, →, etc.) that are absent from the font. Use LaTeX equivalents inside $ delimiters instead: $\checkmark$, $\times$, $\to$, etc.

Running code in Python is via Kiro providing User with the python module and execution command. Kiro is unable to issue WSL miniconda execution commands directly.

The double-slit experiment (DSE) quantum circuit implementation went through a complicated debugging process documented in DSE.md. The working approach uses a single-qubit H-P-H circuit computing interference at each screen position separately (not a multi-qubit register). See DSE.md for the full history and rationale.
