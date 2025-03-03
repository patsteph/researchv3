import os
import re
import requests
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Tuple, Optional
import time

class ContentProcessor:
    def __init__(self):
        self.user_agent = UserAgent()
        
    def fetch_content(self, url: str) -> Optional[str]:
        """Fetch website content with improved error handling and anti-blocking measures"""
        # Enhanced headers to appear more like a real browser
        headers = {
            "User-Agent": self.user_agent.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
        # Add a small random delay between requests (0.5 to 2 seconds)
        time.sleep(random.uniform(0.5, 2))
        
        try:
            # First try with regular request
            response = requests.get(url, headers=headers, timeout=10)
            
            # If we get a 403, try again with a different User-Agent
            if response.status_code == 403:
                headers["User-Agent"] = self.user_agent.random
                time.sleep(1)  # Wait a second before retrying
                response = requests.get(url, headers=headers, timeout=10)
            
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.SSLError:
            # Try again without SSL verification if SSL fails
            try:
                response = requests.get(url, headers=headers, timeout=10, verify=False)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"❌ SSL Error fetching {url}: {str(e)}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {url}: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error fetching {url}: {str(e)}")
            return None

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove citations
        text = re.sub(r'\[\d+\]|\[citation needed\]|\(cite:.*?\)|\[\w+\s\d{4}\]', '', text)
        
        # Remove headers/footers and common web elements
        patterns_to_remove = [
            r'(?i)copyright © .*',
            r'(?i)all rights reserved.*',
            r'(?i)terms (of use|of service).*',
            r'(?i)privacy policy.*',
            r'(?i)follow us on.*',
            r'(?i)share this:.*',
            r'(?i)subscribe to our newsletter.*',
            r'[\w\.-]+@[\w\.-]+\.\w+',  # emails
            r'@[\w_]+',  # social media handles
            r'https?://\S+|www\.\S+',  # URLs
            r'(?i)menu|home|about|contact|search|skip to content|back to top'
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        
        return text.strip()

    def extract_text(self, html: str) -> str:
        """Extract relevant text from HTML"""
        soup = BeautifulSoup(html, "lxml")
        
        # Remove unwanted elements
        unwanted_elements = {
            'tags': ["script", "style", "noscript", "iframe", "header", "footer", 
                    "nav", "aside", "advertisement", "form", "button"],
            'classes': ["header", "footer", "nav", "sidebar", "ad", "social", 
                       "comment", "cookie", "popup", "newsletter"],
            'ids': ["header", "footer", "sidebar", "newsletter", "cookie-notice", 
                   "popup", "modal", "advertisement"]
        }
        
        for tag in unwanted_elements['tags']:
            for element in soup.find_all(tag):
                element.decompose()
                
        for class_name in unwanted_elements['classes']:
            for element in soup.find_all(class_=re.compile(class_name, re.I)):
                element.decompose()
                
        for id_name in unwanted_elements['ids']:
            for element in soup.find_all(id=re.compile(id_name, re.I)):
                element.decompose()
        
        # Extract main content
        content_tags = ["article", "main", "div", "section"]
        main_content = ""
        
        for tag in content_tags:
            if content := soup.find(tag):
                main_content = content.get_text(separator=" ")
                break
        
        if not main_content:
            main_content = soup.get_text(separator=" ")
        
        return self.clean_text(main_content)

class DocumentHandler:
    @staticmethod
    def get_output_directory() -> str:
        """Create and return Customer Research directory"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        output_dir = os.path.join(desktop_path, "Customer Research")
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"✅ Created Customer Research folder on Desktop")
            except Exception as e:
                print(f"❌ Error creating directory: {str(e)}")
                return ""
        return output_dir

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Clean filename of invalid characters"""
        return re.sub(r'[<>:"/\\|?*]', '', filename).strip()

    def save_as_docx(self, content: str, output_dir: str, filename: str) -> None:
        """Save content as DOCX file"""
        doc = Document()
        doc.add_paragraph(content)
        output_path = os.path.join(output_dir, f"{filename}.docx")
        doc.save(output_path)

    def save_as_pdf(self, content: str, output_dir: str, filename: str) -> None:
        """Save content as PDF file"""
        output_path = os.path.join(output_dir, f"{filename}.pdf")
        pdf = canvas.Canvas(output_path, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        
        y_position = 750
        max_chars = 90
        
        for paragraph in content.split('\n'):
            words = paragraph.split()
            line = ""
            
            for word in words:
                if len(line) + len(word) + 1 <= max_chars:
                    line += word + " "
                else:
                    pdf.drawString(50, y_position, line.strip())
                    y_position -= 20
                    line = word + " "
                    
                    if y_position < 50:
                        pdf.showPage()
                        pdf.setFont("Helvetica", 12)
                        y_position = 750
            
            if line:
                pdf.drawString(50, y_position, line.strip())
                y_position -= 20
        
        pdf.save()

class ResearchAssistant:
    def __init__(self):
        self.processor = ContentProcessor()
        self.doc_handler = DocumentHandler()

    def get_search_results(self, query: str, max_results: int) -> List[str]:
        """Perform DuckDuckGo search with improved error handling"""
        try:
            urls = []
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                for result in search_results:
                    if isinstance(result, dict):
                        url = result.get('href') or result.get('link') or result.get('url')
                        if url and url.startswith('http'):
                            urls.append(url)
                    if len(urls) >= max_results:
                        break
                        
            if not urls:
                print("⚠️ No valid URLs found in search results")
                return []
                
            return urls
        except Exception as e:
            print(f"🔍 Search error: {str(e)}")
            return []

    def preview_content_length(self, url: str) -> Optional[Dict]:
        """Preview content length without full processing"""
        html_content = self.processor.fetch_content(url)
        if not html_content:
            return None
            
        extracted_text = self.processor.extract_text(html_content)
        if not extracted_text.strip():
            return None
            
        word_count = len(extracted_text.split())
        if word_count < 500:
            rating, length_desc = 1, "Short"
        elif word_count < 2000:
            rating, length_desc = 2, "Medium"
        else:
            rating, length_desc = 3, "Long"
            
        return {
            'url': url,
            'rating': rating,
            'length': length_desc
        }

    def process_url(self, url: str) -> Optional[Dict]:
        """Process single URL and return content only"""
        html_content = self.processor.fetch_content(url)
        if not html_content:
            return None
            
        extracted_text = self.processor.extract_text(html_content)
        if not extracted_text.strip():
            return None
            
        return {
            'url': url,
            'content': extracted_text
        }

    def execute(self):
        """Main execution loop"""
        while True:
            print("\n🔍 Welcome to the Research Assistant!")
            
            query = input("Enter your research topic: ").strip()
            
            while True:
                try:
                    num_urls = int(input("\nHow many URLs would you like to analyze? (1-20): "))
                    if 1 <= num_urls <= 20:
                        break
                    print("Please enter a number between 1 and 20.")
                except ValueError:
                    print("Please enter a valid number.")
            
            print("\n🔎 Searching DuckDuckGo...")
            urls = self.get_search_results(query, num_urls)
            
            if not urls:
                print("❌ No results found.")
                if input("\nWould you like to try another search? (yes/no): ").lower().strip() != 'yes':
                    break
                continue

            print(f"\n✅ Found {len(urls)} URLs. Analyzing content length...")
            
            # Preview content lengths first
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {executor.submit(self.preview_content_length, url): url for url in urls}
                url_previews = []
                
                for i, future in enumerate(future_to_url, 1):
                    url = future_to_url[future]
                    try:
                        result = future.result()
                        if result:
                            url_previews.append(result)
                            print(f"\n🌐 URL {i}: {url}")
                            print(f"📊 Expected Content Length: {result['length']} ({result['rating']}/3)")
                    except Exception as e:
                        print(f"❌ Error analyzing {url}: {str(e)}")

            if not url_previews:
                print("❌ No valid content found.")
                if input("\nWould you like to try another search? (yes/no): ").lower().strip() != 'yes':
                    break
                continue

            print("\nWould you like to proceed with content extraction? (yes/no): ")
            if input().lower().strip() != 'yes':
                if input("\nWould you like to try another search? (yes/no): ").lower().strip() != 'yes':
                    break
                continue

            # Process URLs for content
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {executor.submit(self.process_url, preview['url']): preview['url'] 
                               for preview in url_previews}
                url_contents = []
                
                for i, future in enumerate(future_to_url, 1):
                    url = future_to_url[future]
                    print(f"\n📥 Extracting content from URL {i}/{len(url_previews)}")
                    
                    try:
                        result = future.result()
                        if result:
                            url_contents.append(result)
                    except Exception as e:
                        print(f"❌ Error processing {url}: {str(e)}")

            if not url_contents:
                print("❌ No valid content extracted.")
                if input("\nWould you like to try another search? (yes/no): ").lower().strip() != 'yes':
                    break
                continue

            output_dir = self.doc_handler.get_output_directory()
            if not output_dir:
                if input("\nWould you like to try another search? (yes/no): ").lower().strip() != 'yes':
                    break
                continue

            print("\n💾 Choose file format:")
            print("1. DOCX")
            print("2. PDF")
            
            while True:
                file_choice = input("Enter your choice (1 or 2): ").strip()
                if file_choice in ["1", "2"]:
                    break
                print("Please enter either 1 for DOCX or 2 for PDF.")
            
            filename_base = input("\n✏️ Enter a name for your research file (without extension): ").strip()
            filename_base = self.doc_handler.sanitize_filename(filename_base)
            
            # Format content without URLs and ratings
            all_content = ""
            for i, content_data in enumerate(url_contents, 1):
                all_content += f"\nArticle {i}\n"
                all_content += "=" * 80 + "\n\n"
                all_content += content_data['content'].strip() + "\n\n"
                all_content += "=" * 80 + "\n"
            
            try:
                if file_choice == "1":
                    self.doc_handler.save_as_docx(all_content, output_dir, filename_base)
                else:
                    self.doc_handler.save_as_pdf(all_content, output_dir, filename_base)
                
                print(f"\n📂 Your file has been saved to: {output_dir}")
                print(f"📄 Filename: {filename_base}.{'docx' if file_choice == '1' else 'pdf'}")
                
            except Exception as e:
                print(f"❌ Error saving file: {str(e)}")
                if input("\nWould you like to try another search? (yes/no): ").lower().strip() != 'yes':
                    break
                continue

            print("\n✨ Research compilation complete!")
            
            if input("\nWould you like to perform another search? (yes/no): ").lower().strip() != 'yes':
                break

        print("\nThank you for using the Research Assistant!")

if __name__ == "__main__":
    assistant = ResearchAssistant()
    assistant.execute()   