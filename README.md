# Wordcloud Generator

Generate beautiful wordclouds from your codebase or project files. This tool analyzes text files in directories and creates visual wordclouds based on word frequencies, code-only analysis, or programming language distribution.

## Features

- **Full Text Analysis** - Generate wordclouds from all text and code files
- **Code-Only Analysis** - Focus only on source code files, excluding documentation
- **Language Distribution** - Visualize programming languages used in your project
- **Smart Filtering** - Exclude patterns via `exclude.txt` file
- **Stopword Filtering** - Automatically filters common English words and programming keywords using NLTK

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync
```

### Dependencies

- `wordcloud>=1.9.6` - Generate wordcloud images
- `matplotlib>=3.10.8` - Plot and save visualizations
- `nltk>=3.9.2` - Natural language processing for stopword filtering

## Usage

### 1. Generate Wordcloud from All Text Files

Analyzes all text files including code, markdown, JSON, YAML, etc.

```bash
python wordcloud_generator.py
```

**Supported file types:**
- Code: `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.java`, `.go`, `.cs`, `.cpp`, `.c`, `.h`, `.rs`, `.rb`, `.php`, `.scala`, `.kt`
- Markup: `.md`, `.txt`, `.html`, `.css`
- Config: `.json`, `.yaml`, `.yml`, `.sh`

**Output:** `images/wordcloud.png`

### 2. Generate Wordcloud from Code Files Only

Analyzes only source code files, excluding documentation and config files.

```bash
python wordcloud_code_only.py
```

**Supported code extensions:**
`.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.java`, `.go`, `.cs`, `.cpp`, `.c`, `.h`, `.hpp`, `.rs`, `.rb`, `.php`, `.scala`, `.kt`, `.swift`, `.m`, `.sh`, `.bash`, `.pl`, `.r`

**Output:** `images/wordcloud_code_only.png`

### 3. Generate Language Distribution Wordcloud

Visualizes programming languages used based on file extensions.

```bash
python wordcloud_languages.py
```

Shows:
- Number of files per language
- Percentage distribution
- Visual wordcloud representation

**Output:** `images/wordcloud_languages.png`

## Configuration

### Exclude Patterns

Create or edit `exclude.txt` to specify patterns for files/directories to exclude:

```
# Exclude patterns (one per line)
node_modules
.git
*.min.js
__pycache__
.venv
dist
build
```

The tool uses glob-style patterns and checks against:
- Directory names
- File names
- Path components

### Customization

Each script can be customized by editing the following parameters in the source:

**Wordcloud parameters:**
- `width` / `height` - Image dimensions
- `background_color` - Background color
- `max_words` - Maximum number of words to display
- `colormap` - Color scheme (e.g., 'viridis', 'plasma', 'Set1')
- `relative_scaling` - Font size scaling
- `min_font_size` - Minimum font size

## Project Structure

```
wordcloud-generator/
├── wordcloud_generator.py      # Full text analysis
├── wordcloud_code_only.py      # Code-only analysis
├── wordcloud_languages.py      # Language distribution
├── exclude.txt                 # Exclusion patterns
├── images/                     # Generated wordclouds
├── pyproject.toml             # Project dependencies
└── README.md                  # This file
```

## How It Works

1. **File Collection** - Walks through the parent directory, filtering files based on extensions and exclude patterns
2. **Word Extraction** - Extracts words using regex (alphanumeric sequences, 2+ characters)
3. **Stopword Filtering** - Removes common English words and programming keywords
4. **Frequency Analysis** - Counts word occurrences
5. **Visualization** - Generates wordcloud with frequency-based sizing

## Output

All wordclouds are saved to the `images/` directory as 1600x1600 square images at 150 DPI.

## Notes

- The scripts analyze the **parent directory** of the wordcloud-generator folder
- First run will download NLTK stopwords data automatically
- Words are converted to lowercase for consistency
- Minimum word length is 2 characters

## License

MIT
