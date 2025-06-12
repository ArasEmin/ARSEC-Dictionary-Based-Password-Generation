# ARSEC - Dictionary Based Password Generation Tool

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)](https://docs.python.org/3/library/tkinter.html)

ARSEC is an advanced password generation tool that creates potential password combinations based on dictionary words and various transformation rules. This tool is designed for security professionals to test password strength and for educational purposes only.

## Features

- **Keyword-based password generation** - Input multiple keywords to generate password variations
- **Multiple transformation rules**:
  - Leet speak transformations (e.g., a→@, e→3)
  - Number appending (e.g., 123, 2023, etc.)
  - Special character additions (e.g., !, @, #)
  - Case variation combinations
- **Combination modes**:
  - Individual word processing
  - Multi-word combinations (optional)
- **Export capability** - Save generated passwords to a text file
- **User-friendly GUI** - Built with Tkinter for easy interaction

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ArasEmin/ARSEC-Dictionary-Based-Password-Generation.git
   cd ARSEC-Dictionary-Based-Password-Generation

2. Ensure you have Python 3.8+ installed

3. Run the application:
bash
python main.py

## Usage
Enter your keywords separated by commas (e.g., "name,surname,pet")
Select your desired transformation options
Choose whether to combine keywords
Select an output file location
Click "Generate Passwords" button
Wait for the process to complete (progress bar will show status)
Find your generated passwords in the output file

## Example Output
With input keywords: "ali,kutay,metin" and all options enabled:

text
ali
ALi
ALI
ali123
ali!
@ali@
4l1
al1
kutay
KUTAY
kutay007
kutay#
$kutay$
k7tay
metin
METIN
metin2023
metin!
met1n
alikutay
kutaymetin
metinali
ALIKUTAY
alikutay123
... (and hundreds more)

## Ethical Considerations
⚠️ Important: This tool is intended for:

Security professionals testing their own systems

Educational purposes in cybersecurity training

Password strength evaluation

🚫 Do not use this tool for any unauthorized testing or illegal activities. Always obtain proper authorization before testing any systems.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.
