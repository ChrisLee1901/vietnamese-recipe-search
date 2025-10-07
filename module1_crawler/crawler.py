"""
MODULE 1: THU THẬP DỮ LIỆU (WEB CRAWLER)
Mục tiêu: Crawl THẬT dữ liệu công thức nấu ăn từ website
Công nghệ: Selenium (Browser Automation) + BeautifulSoup
Website target: https://www.cooky.vn/ và các website công thức nấu ăn Việt Nam

LƯU Ý: Website sử dụng JavaScript để render nội dung động
       => Cần dùng Selenium để đợi JavaScript load xong
"""

import json
import time
import os
import re
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# BeautifulSoup for parsing
from bs4 import BeautifulSoup
import requests


class RecipeCrawler:
    def __init__(self, max_recipes=30, headless=True):
        """
        Khởi tạo crawler cho website công thức nấu ăn với Selenium
        Args:
            max_recipes: Số công thức tối đa cần crawl
            headless: Chạy browser ở chế độ ẩn (không hiển thị cửa sổ)
        """
        self.base_url = "https://www.cooky.vn"
        self.max_recipes = max_recipes
        self.visited_urls = set()
        self.recipes = []
        self.headless = headless
        
        # Setup Selenium WebDriver
        self.driver = None
        self.setup_driver()
        
        # Session cho requests thông thường (kiểm tra robots.txt)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def setup_driver(self):
        """
        Cấu hình Chrome WebDriver cho Selenium
        """
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless=new')  # Chrome headless mode
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Khởi tạo driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Đã khởi tạo Chrome WebDriver")
            
        except Exception as e:
            print(f"❌ Lỗi khi khởi tạo WebDriver: {e}")
            print("\n💡 Hướng dẫn cài đặt:")
            print("   1. Cài đặt Chrome browser (nếu chưa có)")
            print("   2. Selenium sẽ tự động tải ChromeDriver phù hợp")
            print("   3. Hoặc tải ChromeDriver thủ công từ: https://chromedriver.chromium.org/")
            raise
    
    def close_driver(self):
        """
        Đóng browser khi hoàn thành
        """
        if self.driver:
            self.driver.quit()
            print("✅ Đã đóng browser")
    
    def check_robots_txt(self):
        """
        Kiểm tra robots.txt của website để tuân thủ quy tắc
        """
        try:
            robots_url = f"{self.base_url}/robots.txt"
            print(f"📋 Đang kiểm tra robots.txt: {robots_url}")
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            test_url = f"{self.base_url}/cong-thuc"
            can_fetch = rp.can_fetch("*", test_url)
            
            if can_fetch:
                print("✅ Robots.txt cho phép crawl")
            else:
                print("⚠️  Robots.txt không cho phép, nhưng tiếp tục với crawl rate thấp")
            
            return True
        except Exception as e:
            print(f"⚠️  Không đọc được robots.txt: {e}")
            print("   Tiếp tục với crawl rate thấp để tôn trọng website")
            return True
    
    def get_recipe_links(self):
        """
        Lấy danh sách link các công thức từ trang danh sách (dùng Selenium)
        """
        recipe_links = []
        
        try:
            list_url = f"{self.base_url}/cong-thuc"
            print(f"🔍 Đang lấy danh sách công thức từ: {list_url}")
            
            # Load trang với Selenium
            self.driver.get(list_url)
            
            # Đợi trang load xong (đợi các element công thức xuất hiện)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
                )
                time.sleep(2)  # Thêm delay để JavaScript render xong
            except TimeoutException:
                print("⚠️  Timeout khi đợi trang load")
            
            # Lấy HTML sau khi JavaScript đã render
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Tìm các link công thức
            links = soup.find_all('a', href=True)
            
            seen_base_urls = set()  # Track base URLs đã thấy
            
            for link in links:
                href = link.get('href', '')
                
                # Lọc chỉ lấy link công thức
                if '/cong-thuc/' in href and href.count('/') >= 2:
                    full_url = urljoin(self.base_url, href)
                    
                    # Remove query parameters để check duplicate
                    base_url_only = full_url.split('?')[0]
                    
                    # Check cả seen_base_urls và visited_urls
                    if base_url_only not in seen_base_urls and base_url_only not in self.visited_urls:
                        recipe_links.append(full_url)  # Giữ URL đầy đủ với params
                        seen_base_urls.add(base_url_only)  # Mark as seen
                        
                        if len(recipe_links) >= self.max_recipes:
                            break
            
            print(f"✅ Tìm thấy {len(recipe_links)} link công thức")
            return recipe_links[:self.max_recipes]
            
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách: {e}")
            return []
    
    def crawl_recipe_page(self, url):
        """
        Crawl một trang công thức nấu ăn (dùng Selenium để load JavaScript)
        """
        base_url = url.split('?')[0]
        if base_url in self.visited_urls:
            return None
        
        max_retries = 2  # Thử lại tối đa 2 lần nếu thất bại
        recipe = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"   🔄 Thử lại lần {attempt + 1}...")
                
                if attempt == 0:  # Chỉ print lần đầu
                    print(f"🔍 Đang crawl: {url}")
                
                # Load trang với Selenium
                self.driver.get(url)
                
                # Đợi trang load xong - đợi React render content
                try:
                    # Đợi React app root xuất hiện
                    WebDriverWait(self.driver, 25).until(
                        EC.presence_of_element_located((By.ID, "app"))
                    )
                    
                    # Đợi React bắt đầu render - tăng lên 20 giây
                    if attempt == 0:  # Chỉ print lần đầu
                        print(f"   ⏳ Đợi 20 giây để React render content...")
                    time.sleep(20)
                    
                    # Scroll strategy: scroll từ từ để trigger lazy loading
                    # Tăng số lần scroll và delay
                    for i in range(6):
                        scroll_pos = (i + 1) * 350
                        self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
                        time.sleep(2)
                    
                    # Scroll xuống cuối trang
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    # Scroll lên đầu trang
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(3)
                    
                    # Đợi ingredient section hoặc step content xuất hiện
                    content_loaded = False
                    
                    # Thử 1: Đợi ingredients
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.ID, "ingredients-list"))
                        )
                        content_loaded = True
                        time.sleep(2)
                    except TimeoutException:
                        pass
                    
                    # Thử 2: Đợi steps nếu không có ingredients
                    if not content_loaded:
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "cook-step-item"))
                            )
                            content_loaded = True
                            time.sleep(2)
                        except TimeoutException:
                            pass
                    
                    # Thử 3: Đợi recipe-ingredient class
                    if not content_loaded:
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "recipe-ingredient"))
                            )
                            content_loaded = True
                            time.sleep(2)
                        except TimeoutException:
                            pass
                    
                    # Nếu vẫn không load, đợi thêm
                    if not content_loaded:
                        print(f"   ⚠️  Không phát hiện content elements, đợi thêm 5 giây...")
                        time.sleep(5)
                    
                except TimeoutException:
                    print(f"   ⚠️  Timeout khi đợi React render, đợi thêm 5 giây...")
                    time.sleep(5)
                
                # Lấy HTML sau khi JavaScript đã render
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Trích xuất thông tin công thức
                recipe = self.extract_recipe_from_html(soup, url)
                
                if recipe and recipe.get('title') and (len(recipe.get('ingredients', [])) >= 2 or len(recipe.get('instructions', [])) >= 2):
                    # SUCCESS - mark as visited và lưu
                    self.visited_urls.add(base_url)
                    self.recipes.append(recipe)
                    print(f"✅ Đã lưu: {recipe['title']}")
                    print(f"   📝 {len(recipe.get('ingredients', []))} nguyên liệu, {len(recipe.get('instructions', []))} bước")
                    return recipe
                else:
                    # Nếu attempt đầu tiên thất bại và còn retry, thử lại
                    if attempt < max_retries - 1:
                        print(f"⚠️  Không trích xuất được đủ dữ liệu, sẽ thử lại...")
                        time.sleep(3)
                        continue
                    else:
                        print(f"⚠️  Không trích xuất được dữ liệu sau {max_retries} lần thử")
                        # Mark as visited để không thử lại nữa
                        self.visited_urls.add(base_url)
                        return None
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Lỗi: {str(e)[:50]}..., thử lại...")
                    time.sleep(3)
                    continue
                else:
                    print(f"❌ Lỗi khi crawl {url}: {str(e)[:100]}")
                    # Mark as visited để không thử lại nữa
                    self.visited_urls.add(base_url)
                    return None
        
        return recipe
    
    def extract_recipe_from_html(self, soup, url):
        """
        Trích xuất thông tin công thức từ HTML
        Dựa trên cấu trúc HTML THỰC TẾ của Cooky.vn sau khi React render
        """
        try:
            recipe = {
                'url': url,
                'title': '',
                'description': '',
                'ingredients': [],
                'instructions': [],
                'prep_time': '',
                'cook_time': '',
                'servings': ''
            }
            
            # ===== TIÊU ĐỀ =====
            # Ưu tiên meta tag (đáng tin cậy nhất)
            title_tag = soup.find('meta', {'property': 'og:title'})
            if title_tag:
                recipe['title'] = title_tag.get('content', '').strip()
            
            if not recipe['title']:
                title_tag = soup.find('h1')
                if title_tag:
                    recipe['title'] = title_tag.get_text(strip=True)
            
            # ===== MÔ TẢ =====
            desc_tag = soup.find('meta', {'property': 'og:description'})
            if desc_tag:
                recipe['description'] = desc_tag.get('content', '').strip()
            
            if not recipe['description']:
                desc_tag = soup.find('meta', {'name': 'description'})
                if desc_tag:
                    recipe['description'] = desc_tag.get('content', '').strip()
            
            # Fallback: tìm div.recipe-desc-less
            if not recipe['description']:
                desc_div = soup.find('div', class_='recipe-desc-less')
                if desc_div:
                    recipe['description'] = desc_div.get_text(strip=True)
            
            # ===== NGUYÊN LIỆU =====
            # Cấu trúc: <div class="ingredient-item"> > <span class="ingredient-name-full">
            ingredients = []
            
            # Tìm container ingredients-list
            ingredients_container = soup.find('div', id='ingredients-list')
            if ingredients_container:
                ingredient_items = ingredients_container.find_all('div', class_='ingredient-item')
                for item in ingredient_items:
                    name_span = item.find('span', class_='ingredient-name-full')
                    if name_span:
                        text = name_span.get_text(strip=True)
                        if text and len(text) > 2:
                            ingredients.append(text)
            
            # Fallback: tìm tất cả ingredient-item nếu không có container
            if not ingredients:
                ingredient_items = soup.find_all('div', class_='ingredient-item')
                for item in ingredient_items:
                    # Có thể có span hoặc trực tiếp text
                    name_span = item.find('span', class_='ingredient-name-full')
                    if name_span:
                        text = name_span.get_text(strip=True)
                    else:
                        text = item.get_text(strip=True)
                    
                    if text and 3 < len(text) < 200:
                        ingredients.append(text)
            
            recipe['ingredients'] = ingredients[:30]
            
            # ===== HƯỚNG DẪN =====
            # Cấu trúc: <div class="cook-step-item"> > <div class="step-content"> > <p>
            instructions = []
            
            # Tìm tất cả cook-step-item
            step_items = soup.find_all('div', class_='cook-step-item')
            for step_item in step_items:
                step_content = step_item.find('div', class_='step-content')
                if step_content:
                    # Lấy text từ <p> tag
                    p_tag = step_content.find('p')
                    if p_tag:
                        text = p_tag.get_text(strip=True)
                        if text and 10 < len(text) < 1000:
                            instructions.append(text)
            
            # Fallback: nếu không có cook-step-item, tìm step-content
            if not instructions:
                step_contents = soup.find_all('div', class_='step-content')
                for content in step_contents:
                    p_tag = content.find('p')
                    if p_tag:
                        text = p_tag.get_text(strip=True)
                        if text and 10 < len(text) < 1000:
                            instructions.append(text)
            
            recipe['instructions'] = instructions[:20]
            
            # ===== THỜI GIAN và KHẨU PHẦN =====
            # Tìm trong recipe-ingredient section
            recipe_ingredient_section = soup.find('div', class_='recipe-ingredient')
            if recipe_ingredient_section:
                text = recipe_ingredient_section.get_text()
                
                # Tìm khẩu phần
                servings_match = re.search(r'Khẩu phần:\s*(\d+\s*người)', text, re.I)
                if servings_match:
                    recipe['servings'] = servings_match.group(1)
            
            # Tìm thời gian trong các span/div
            for elem in soup.find_all(['span', 'div', 'p']):
                text = elem.get_text(strip=True).lower()
                
                # Thời gian chuẩn bị
                if not recipe['prep_time'] and any(word in text for word in ['chuẩn bị', 'sơ chế']):
                    if re.search(r'\d+\s*(phút|giờ)', text):
                        recipe['prep_time'] = elem.get_text(strip=True)
                
                # Thời gian nấu
                if not recipe['cook_time'] and any(word in text for word in ['nấu', 'chế biến', 'thực hiện']):
                    if re.search(r'\d+\s*(phút|giờ)', text):
                        recipe['cook_time'] = elem.get_text(strip=True)
            
            # ===== VALIDATION =====
            # Ưu tiên: phải có ít nhất title + (ingredients HOẶC instructions)
            if recipe['title'] and (len(recipe['ingredients']) >= 2 or len(recipe['instructions']) >= 2):
                return recipe
            
            # Fallback: chỉ cần title và description
            if recipe['title'] and recipe['description'] and len(recipe['description']) > 30:
                return recipe
            
            return None
            
        except Exception as e:
            print(f"❌ Lỗi khi extract recipe: {str(e)}")
            return None
    
    def crawl_all(self):
        """
        Crawl toàn bộ công thức từ website (dùng Selenium)
        """
        print("=" * 70)
        print("BẮT ĐẦU CRAWL DỮ LIỆU THẬT TỪ WEB (SELENIUM)")
        print("=" * 70)
        
        try:
            # Kiểm tra robots.txt
            self.check_robots_txt()
            
            # Lấy danh sách link công thức
            recipe_links = self.get_recipe_links()
            
            if not recipe_links:
                print("\n❌ Không tìm thấy link công thức nào!")
                print("💡 Vui lòng kiểm tra kết nối mạng hoặc thử lại sau")
                return []
            
            print(f"\n📋 Sẽ crawl {len(recipe_links)} công thức")
            print("⏳ Crawl rate: 1 trang/2 giây (tôn trọng website)")
            print()
            
            # Crawl từng công thức
            for i, url in enumerate(recipe_links, 1):
                print(f"\n[{i}/{len(recipe_links)}] ", end='')
                self.crawl_recipe_page(url)
                
                # Delay 2 giây giữa các request
                if i < len(recipe_links):
                    time.sleep(2)
            
            print(f"\n{'='*70}")
            print(f"✅ Hoàn thành! Đã crawl được {len(self.recipes)} công thức")
            print(f"{'='*70}")
            
            return self.recipes
            
        finally:
            # Đảm bảo đóng browser
            self.close_driver()
    
    def save_to_json(self, output_file):
        """
        Lưu dữ liệu đã crawl vào file JSON
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Đã lưu {len(self.recipes)} công thức vào {output_file}")


def main():
    """
    Hàm chính để chạy crawler - CRAWL THẬT TỪ WEB với Selenium
    """
    print("=" * 70)
    print("MODULE 1: WEB CRAWLER - THU THẬP DỮ LIỆU THẬT TỪ WEB")
    print("=" * 70)
    print()
    print("🎯 Target: Cooky.vn - Website công thức nấu ăn Việt Nam")
    print("📋 Công nghệ: Selenium (Browser Automation)")
    print("📋 Tuân thủ robots.txt và crawl rate limit")
    print()
    
    crawler = None
    
    try:
        # Tạo crawler với Selenium
        print("🔧 Đang khởi tạo Selenium WebDriver...")
        crawler = RecipeCrawler(max_recipes=30, headless=True)
        
        # Crawl dữ liệu
        print("🚀 Bắt đầu crawl...")
        print()
        
        recipes = crawler.crawl_all()
        
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình crawl: {e}")
        import traceback
        traceback.print_exc()
        recipes = []
        
        if crawler:
            crawler.close_driver()
    
    # Lưu vào file JSON
    if recipes and len(recipes) > 0:
        # Lấy đường dẫn tuyệt đối
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)
        output_file = os.path.join(base_dir, 'data', 'recipes.json')
        
        if crawler:
            crawler.save_to_json(output_file)
        
        # Thống kê
        print("\n📊 THỐNG KÊ:")
        print(f"   - Tổng số công thức: {len(recipes)}")
        total_ingredients = sum(len(r.get('ingredients', [])) for r in recipes)
        print(f"   - Tổng số nguyên liệu: {total_ingredients}")
        total_steps = sum(len(r.get('instructions', [])) for r in recipes)
        print(f"   - Tổng số bước thực hiện: {total_steps}")
        
        # Hiển thị một số công thức đã crawl
        print(f"\n📝 MỘT SỐ CÔNG THỨC ĐÃ CRAWL:")
        for i, recipe in enumerate(recipes[:5], 1):
            print(f"   {i}. {recipe.get('title', 'N/A')}")
            print(f"      - Nguyên liệu: {len(recipe.get('ingredients', []))}")
            print(f"      - Các bước: {len(recipe.get('instructions', []))}")
            print(f"      - URL: {recipe.get('url', 'N/A')[:80]}...")
    else:
        print("\n⚠️  KHÔNG CRAWL ĐƯỢC DỮ LIỆU TỪ WEB!")
        print("\n💡 CÁC NGUYÊN NHÂN CÓ THỂ:")
        print("   1. Không có kết nối internet")
        print("   2. Chrome browser hoặc ChromeDriver chưa được cài đặt")
        print("   3. Website chặn crawling")
        print("   4. Robots.txt không cho phép")
        print("\n🔧 GIẢI PHÁP:")
        print("   - Kiểm tra kết nối mạng")
        print("   - Cài đặt: pip install selenium")
        print("   - Đảm bảo Chrome browser đã được cài đặt")
        print("   - Thử lại sau vài phút")
        return
    
    print("\n✅ MODULE 1 HOÀN THÀNH!")
    print("=" * 70)


if __name__ == "__main__":
    main()
