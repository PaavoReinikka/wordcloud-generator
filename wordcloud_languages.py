#!/usr/bin/env python3
"""
Generate a wordcloud based on programming languages used (file extensions).
Each file extension is mapped to its language name and counted.
"""

import os
from collections import Counter
from pathlib import Path
from fnmatch import fnmatch


# Map file extensions to language names
LANGUAGE_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript',
    '.jsx': 'JavaScript',
    '.java': 'Java',
    '.go': 'Go',
    '.rs': 'Rust',
    '.c': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.cxx': 'C++',
    '.h': 'C',
    '.hpp': 'C++',
    '.cs': 'C#',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.r': 'R',
    '.m': 'Objective-C',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.pl': 'Perl',
    '.lua': 'Lua',
    '.vim': 'VimScript',
    '.el': 'Emacs-Lisp',
    '.clj': 'Clojure',
    '.ex': 'Elixir',
    '.erl': 'Erlang',
    '.hs': 'Haskell',
    '.ml': 'OCaml',
    '.sql': 'SQL',
    '.dockerfile': 'Docker',
    '.tf': 'Terraform',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.json': 'JSON',
    '.xml': 'XML',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'Less',
    '.md': 'Markdown',
    '.rst': 'reStructuredText',
    '.tex': 'LaTeX',
}


def load_exclude_patterns(exclude_file='exclude.txt'):
    """Load exclusion patterns from file."""
    patterns = []
    if os.path.exists(exclude_file):
        with open(exclude_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns


def should_exclude(path, exclude_patterns):
    """Check if path matches any exclusion pattern."""
    path_parts = Path(path).parts
    for pattern in exclude_patterns:
        for part in path_parts:
            if fnmatch(part, pattern):
                return True
        if fnmatch(os.path.basename(path), pattern):
            return True
    return False


def collect_languages(base_dir, exclude_patterns):
    """Collect language frequencies based on file extensions."""
    language_counts = Counter()
    files_by_language = {}
    
    files_processed = 0
    files_skipped = 0
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), exclude_patterns)]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            if should_exclude(filepath, exclude_patterns):
                files_skipped += 1
                continue
            
            # Get file extension
            ext = os.path.splitext(file)[1].lower()
            
            # Check if it's a known language
            if ext in LANGUAGE_MAP:
                language = LANGUAGE_MAP[ext]
                language_counts[language] += 1
                
                if language not in files_by_language:
                    files_by_language[language] = []
                files_by_language[language].append(filepath)
                
                files_processed += 1
    
    print(f"Files processed: {files_processed}")
    print(f"Files skipped: {files_skipped}")
    return language_counts, files_by_language


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    print(f"Base directory: {base_dir}")
    print(f"Loading exclusion patterns...")
    
    exclude_patterns = load_exclude_patterns(os.path.join(script_dir, 'exclude.txt'))
    print(f"Loaded {len(exclude_patterns)} exclusion patterns\n")
    
    print("Analyzing programming languages used...")
    language_counts, files_by_language = collect_languages(base_dir, exclude_patterns)
    
    print(f"\nTotal files analyzed: {sum(language_counts.values())}")
    print(f"Languages found: {len(language_counts)}\n")
    
    print("Language distribution:")
    for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / sum(language_counts.values())) * 100
        print(f"  {lang:20s}: {count:5d} files ({percentage:5.1f}%)")
    
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        
        # Create wordcloud from language frequencies
        wordcloud = WordCloud(
            width=1600, 
            height=800, 
            background_color='white',
            colormap='Set1',
            relative_scaling=0.5,
            min_font_size=12,
            max_words=50
        ).generate_from_frequencies(language_counts)
        
        output_file = os.path.join(script_dir, 'images', 'wordcloud_languages.png')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.figure(figsize=(20, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Language Distribution', fontsize=24, pad=20)
        plt.tight_layout(pad=0)
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Language wordcloud saved to {output_file}")
        
    except ImportError:
        print("\n⚠ wordcloud library not installed.")


if __name__ == '__main__':
    main()
