# Second Brain Assistant

An AI-powered personal knowledge management system that organizes notes, links ideas, and visualizes a knowledge graph. It supports natural language search, semantic tagging, and GPT-driven summaries.

[![CI](https://github.com/ashikbro/second-brain-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/ashikbro/second-brain-assistant/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

## Features

- 📝 **Note Management**: Create, organize, and link notes seamlessly
- 🔍 **Semantic Search**: Find related notes using natural language queries
- 🌐 **Knowledge Graph**: Visualize connections between your ideas
- 🏷️ **Smart Tagging**: Automatically tag and categorize your notes
- 🤖 **AI-Powered Summaries**: Generate summaries using GPT models
- 🔗 **Bi-directional Links**: Connect related concepts effortlessly

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ashikbro/second-brain-assistant.git
cd second-brain-assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

4. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

## Quick Start

### Command Line Interface

```bash
# Start the CLI
second-brain

# Or run directly with Python
python -m second_brain.cli
```

### Python API

```python
from second_brain import KnowledgeGraph, Note, SemanticSearch

# Create a knowledge graph
kg = KnowledgeGraph()

# Add notes
note1 = Note(
    title="Machine Learning Basics",
    content="Introduction to ML concepts",
    tags=["ai", "ml"]
)
note2 = Note(
    title="Deep Learning",
    content="Advanced ML with neural networks",
    tags=["ai", "deep-learning"]
)
note_id_1 = kg.add_note(note1)
note_id_2 = kg.add_note(note2)

# Search for notes
search = SemanticSearch(kg)
results = search.search("machine learning", top_k=5)

# Link related notes
kg.link_notes(note_id_1, note_id_2)
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/second_brain --cov-report=html

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code with black
black src tests

# Lint with flake8
flake8 src tests

# Type check with mypy
mypy src
```

## Project Structure

```
second-brain-assistant/
├── src/
│   └── second_brain/         # Main package
│       ├── __init__.py
│       ├── core.py           # Core data structures
│       ├── search.py         # Search functionality
│       └── cli.py            # Command-line interface
├── tests/                    # Test suite
├── docs/                     # Documentation
├── examples/                 # Example usage
├── .github/                  # GitHub workflows and templates
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── pyproject.toml           # Build configuration
└── README.md                # This file
```

## Roadmap

- [ ] Web interface for managing notes
- [ ] Integration with popular note-taking apps
- [ ] Advanced NLP for automatic tagging
- [ ] Knowledge graph visualization
- [ ] Export/import functionality
- [ ] Mobile app support
- [ ] Collaborative features

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ for knowledge management enthusiasts
- Inspired by tools like Obsidian, Roam Research, and Notion

## Support

- 📫 Issues: [GitHub Issues](https://github.com/ashikbro/second-brain-assistant/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ashikbro/second-brain-assistant/discussions)

---

**Status**: 🚧 This project is in early development (v0.1.0). APIs may change.
