#!/usr/bin/env python3
"""
Generate a wordcloud from all text files in specified directories.
Supports exclusion patterns via exclude.txt file.
"""

import os
import re
import sys
from collections import Counter
from pathlib import Path
from fnmatch import fnmatch


def load_exclude_patterns(exclude_file="exclude.txt"):
    """Load exclusion patterns from file."""
    patterns = []
    if os.path.exists(exclude_file):
        with open(exclude_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


def should_exclude(path, exclude_patterns):
    """Check if path matches any exclusion pattern."""
    path_parts = Path(path).parts
    for pattern in exclude_patterns:
        # Check if any part of the path matches the pattern
        for part in path_parts:
            if fnmatch(part, pattern):
                return True
        # Also check the full filename
        if fnmatch(os.path.basename(path), pattern):
            return True
    return False


def collect_words(base_dir, exclude_patterns):
    """Collect all words from text files."""
    words = []
    text_extensions = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".go",
        ".cs",
        ".cpp",
        ".c",
        ".h",
        ".md",
        ".txt",
        ".html",
        ".css",
        ".json",
        ".yaml",
        ".yml",
        ".sh",
        ".rs",
        ".rb",
        ".php",
        ".scala",
        ".kt",
    }

    files_processed = 0
    files_skipped = 0

    for root, dirs, files in os.walk(base_dir):
        # Filter out excluded directories in-place
        dirs[:] = [
            d
            for d in dirs
            if not should_exclude(os.path.join(root, d), exclude_patterns)
        ]

        for file in files:
            filepath = os.path.join(root, file)

            # Skip if matches exclusion pattern
            if should_exclude(filepath, exclude_patterns):
                files_skipped += 1
                continue

            # Skip if not a text file
            if not any(file.endswith(ext) for ext in text_extensions):
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    # Extract words (alphanumeric sequences, 2+ chars)
                    file_words = re.findall(r"\b[a-zA-Z]{2,}\b", content.lower())
                    words.extend(file_words)
                    files_processed += 1
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)

    print(f"Files processed: {files_processed}")
    print(f"Files skipped: {files_skipped}")
    return words


def filter_stopwords(word_counts):
    """Remove common stopwords and programming keywords using NLTK."""
    try:
        from nltk.corpus import stopwords
        import nltk

        # Try to use stopwords, download if not available
        try:
            english_stopwords = set(stopwords.words("english"))
        except LookupError:
            print("Downloading NLTK stopwords data...")
            nltk.download("stopwords", quiet=True)
            english_stopwords = set(stopwords.words("english"))
    except Exception as e:
        print(f"Warning: Could not load NLTK stopwords: {e}")
        english_stopwords = set()

    # Additional programming keywords
    programming_keywords = {
        "var",
        "let",
        "const",
        "def",
        "class",
        "return",
        "import",
        "function",
        "if",
        "else",
        "elif",
        "then",
        "end",
        "do",
        "while",
        "for",
        "try",
        "catch",
        "finally",
        "throw",
        "new",
        "this",
        "self",
        "super",
        "true",
        "false",
        "none",
        "null",
        "undefined",
        "void",
        "public",
        "private",
        "protected",
        "static",
        "final",
        "abstract",
        "interface",
        "extends",
        "implements",
        "package",
        "namespace",
        "using",
        "include",
        "define",
        "ifdef",
        "endif",
        "extern",
        "typeof",
        "instanceof",
        "async",
        "await",
        "yield",
        "lambda",
        "del",
        "pass",
        "break",
        "continue",
        "raise",
        "except",
        "assert",
        "switch",
        "case",
        "default",
        "goto",
        "struct",
        "enum",
        "union",
        "typedef",
        "sizeof",
        "const",
        "volatile",
        "inline",
        "virtual",
    }

    all_stopwords = english_stopwords  # | programming_keywords
    return {
        word: count for word, count in word_counts.items() if word not in all_stopwords
    }


def main():
    # Determine base directory (parent of wordcloud directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    print(f"Base directory: {base_dir}")
    print(f"Loading exclusion patterns...")

    exclude_patterns = load_exclude_patterns(os.path.join(script_dir, "exclude.txt"))
    print(f"Loaded {len(exclude_patterns)} exclusion patterns\n")

    print("Collecting words from files...")
    words = collect_words(base_dir, exclude_patterns)

    print(f"\nTotal words found: {len(words)}")
    word_counts = Counter(words)
    print(f"Unique words: {len(word_counts)}")

    # Filter stopwords
    filtered_counts = filter_stopwords(word_counts)
    print(f"After filtering stopwords: {len(filtered_counts)} unique words\n")

    # Show top words
    print("Top 50 most common words:")
    for word, count in sorted(
        filtered_counts.items(), key=lambda x: x[1], reverse=True
    )[:50]:
        print(f"  {word}: {count}")

    # Generate wordcloud
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        wordcloud = WordCloud(
            width=1600,
            height=1600,
            background_color="white",
            max_words=200,
            colormap="viridis",
            relative_scaling=0.5,
            min_font_size=10,
        ).generate_from_frequencies(filtered_counts)

        output_file = os.path.join(script_dir, "images", "wordcloud.png")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.figure(figsize=(16, 16))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        print(f"\n✓ Wordcloud saved to {output_file}")

    except ImportError:
        print("\n⚠ wordcloud library not installed.")
        print("Install dependencies with: uv pip install wordcloud matplotlib")


if __name__ == "__main__":
    main()
