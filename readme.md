# 🔍 Research Assistant

A powerful Python tool that automates web research by searching, extracting, and compiling content from multiple sources into neatly formatted documents.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

## ✨ Features

- 🌐 Searches the web using DuckDuckGo to find relevant information
- 📊 Smart content preview to evaluate sources before full extraction
- 🧹 Advanced text extraction with noise removal (ads, navigation, etc.)
- 📑 Compiles multiple sources into a single organized document
- 📁 Saves research in DOCX or PDF format to your Desktop
- 🛡️ Built-in anti-blocking measures and robust error handling
- 🧵 Multi-threaded processing for faster results

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- Pip package manager

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/research-assistant.git
   cd research-assistant
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Dependencies

- requests: For fetching web content
- bs4 (Beautiful Soup): For HTML parsing
- fake_useragent: For rotating user agents
- python-docx: For creating DOCX files
- reportlab: For generating PDF files
- duckduckgo_search: For web searching
- lxml: For HTML parsing

## 🎮 Usage

1. Run the script:
   ```
   python researchv3.py
   ```

2. Follow the interactive prompts:
   - Enter your research topic
   - Specify how many URLs to analyze (1-20)
   - Review content preview information
   - Choose to proceed with extraction
   - Select output format (DOCX or PDF)
   - Name your research file

3. Find your compiled research in the "Customer Research" folder on your Desktop

## 📋 Example Session

```
🔍 Welcome to the Research Assistant!

Enter your research topic: climate change solutions

How many URLs would you like to analyze? (1-20): 5

🔎 Searching DuckDuckGo...

✅ Found 5 URLs. Analyzing content length...

🌐 URL 1: https://www.example.com/climate-solutions
📊 Expected Content Length: Long (3/3)

[...additional URLs...]

Would you like to proceed with content extraction? (yes/no): 
yes

📥 Extracting content from URL 1/5
[...extraction progress...]

💾 Choose file format:
1. DOCX
2. PDF
Enter your choice (1 or 2): 1

✏️ Enter a name for your research file (without extension): Climate_Solutions_Research

📂 Your file has been saved to: /Users/username/Desktop/Customer Research
📄 Filename: Climate_Solutions_Research.docx

✨ Research compilation complete!

Would you like to perform another search? (yes/no): no

Thank you for using the Research Assistant!
```

## 🔧 How It Works

1. **Search**: Queries DuckDuckGo for your topic and collects relevant URLs
2. **Preview**: Analyzes content length and quality before full extraction
3. **Extract**: Uses BeautifulSoup to retrieve meaningful content while filtering out ads, navigation, etc.
4. **Clean**: Removes citations, boilerplate text, and fixes formatting
5. **Compile**: Organizes all extracted content into a single document
6. **Save**: Creates a DOCX or PDF file on your Desktop

## 🛠️ Customization

The script includes several classes that can be extended or modified:

- `ContentProcessor`: Handles web content fetching and cleaning
- `DocumentHandler`: Manages file output and formatting
- `ResearchAssistant`: Orchestrates the research process

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [DuckDuckGo](https://duckduckgo.com/) for their search API
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- All the other amazing libraries that make this project possible
