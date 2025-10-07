# 🍲 Vietnamese Recipe Vertical Search Engine# 🍳 Vertical Search Engine - Vietnamese Recipe Search# 🍳 Vertical Search Engine - Máy Tìm Kiếm Công Thức Nấu Ăn



> Hệ thống tìm kiếm chuyên sâu cho công thức nấu ăn Việt Nam - Đồ án môn SEG301



[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)Hệ thống tìm kiếm chuyên sâu cho công thức nấu ăn Việt Nam.<div align="center">

[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)

[![MAP Score](https://img.shields.io/badge/MAP-81.03%25-brightgreen.svg)](https://github.com/ChrisLee1901/vietnamese-recipe-search)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Start**Hệ thống tìm kiếm chuyên sâu về công thức nấu ăn Việt Nam**

## 📋 Mục Lục



- [Giới Thiệu](#-giới-thiệu)

- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)### 1. Cài đặt[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

- [Thiết Kế & Thuật Toán](#-thiết-kế--thuật-toán)

- [Kết Quả Đánh Giá](#-kết-quả-đánh-giá)```bash[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

- [Cài Đặt](#-cài-đặt)

- [Sử Dụng](#-sử-dụng)pip install -r requirements.txt

- [Demo](#-demo)

```</div>

---



## 🎯 Giới Thiệu

### 2. Chạy hệ thống---

Vertical Search Engine là một hệ thống tìm kiếm chuyên sâu tập trung vào lĩnh vực **công thức nấu ăn Việt Nam**. Khác với các công cụ tìm kiếm tổng quát như Google, hệ thống này được tối ưu hóa để:



- ✅ Tìm kiếm chính xác các món ăn theo nguyên liệu

- ✅ Xếp hạng kết quả theo độ liên quan cao#### Chạy toàn bộ pipeline (crawl + index + evaluate):## 📋 Mô tả dự án

- ✅ Hiển thị thông tin chi tiết về công thức

- ✅ Xử lý tiếng Việt một cách chính xác```bash



### 📊 Thống Kê Hệ Thốngpython run_all.pyHệ thống tìm kiếm chuyên sâu (Vertical Search Engine) về công thức nấu ăn, được xây dựng hoàn chỉnh với **5 modules** theo yêu cầu đồ án SEG301:



| Metric | Value |```

|--------|-------|

| **Recipes Crawled** | 30 |### 🔧 5 Modules chính

| **Total Ingredients** | 264 |

| **Cooking Steps** | 146 |#### Chỉ chạy web interface:

| **Unique Terms Indexed** | 1,517 |

| **Mean Average Precision (MAP)** | 81.03% |```bash1. ✅ **Module 1**: Thu thập dữ liệu (Web Crawling)

| **Average Recall@10** | 83.33% |

| **Query Response Time** | < 100ms |python module4_web/app.py2. ✅ **Module 2**: Xử lý văn bản & Xây dựng chỉ mục (Inverted Index)



---```3. ✅ **Module 3**: Truy vấn & Xếp hạng kết quả (TF-IDF, BM25)



## 🏗️ Kiến Trúc Hệ ThốngTruy cập: **http://localhost:5000**4. ✅ **Module 4**: Giao diện Web (Flask)



### Kiến Trúc Tổng Quan5. ✅ **Module 5**: Đánh giá hệ thống (Precision@10, MAP)



```## 📁 Cấu trúc

┌─────────────────────────────────────────────────────────────────┐

│                     VERTICAL SEARCH ENGINE                      │---

└─────────────────────────────────────────────────────────────────┘

                              │```

        ┌─────────────────────┼─────────────────────┐

        │                     │                     │vertical_search_engine/## 🚀 Cài đặt nhanh

        ▼                     ▼                     ▼

┌───────────────┐    ┌───────────────┐    ┌───────────────┐├── data/                    # 30 recipes (264 ingredients, 146 steps)

│   MODULE 1    │    │   MODULE 2    │    │   MODULE 3    │

│   CRAWLER     │───▶│   INDEXING    │───▶│   RANKING     │├── index/                   # Inverted index (1,517 terms)### Yêu cầu

│               │    │               │    │               │

│ • Selenium    │    │ • TextProc    │    │ • BM25        │├── module1_crawler/         # Selenium web crawler- Python 3.12+

│ • BeautifulSoup│    │ • Underthesea │    │ • TF-IDF      │

│ • Rate Limit  │    │ • Inverted    │    │ • Scoring     │├── module2_indexing/        # Vietnamese NLP + Inverted Index- Chrome/Chromium browser (cho Selenium)

│               │    │   Index       │    │               │

└───────────────┘    └───────────────┘    └───────────────┘├── module3_ranking/         # BM25 search algorithm- 4 dependencies: selenium, beautifulsoup4, underthesea, flask

        │                     │                     │

        │                     │                     ▼├── module4_web/            # Flask web interface

        │                     │            ┌───────────────┐

        │                     │            │   MODULE 4    │├── module5_evaluation/     # Precision, Recall, MAP metrics### Bước 1: Cài đặt dependencies

        │                     │            │   WEB UI      │

        │                     │            │               │└── run_all.py              # Pipeline orchestrator```bash

        │                     │            │ • Flask       │

        │                     │            │ • Jinja2      │```# Tạo virtual environment

        │                     │            │ • Bootstrap   │

        │                     │            └───────────────┘python -m venv seg

        │                     │                     │

        │                     └─────────────────────┤## ✨ Features.\seg\Scripts\activate  # Windows

        │                                           │

        └───────────────────────────────────────────┤# source seg/bin/activate  # Linux/Mac

                                                    ▼

                                          ┌───────────────┐- ✅ **Real web crawling** từ Cooky.vn (Selenium + React SPA support)

                                          │   MODULE 5    │

                                          │  EVALUATION   │- ✅ **Vietnamese NLP** với Underthesea tokenization# Cài dependencies

                                          │               │

                                          │ • Precision@K │- ✅ **BM25 ranking** (k1=1.5, b=0.75)pip install -r requirements.txt

                                          │ • Recall@K    │

                                          │ • MAP         │- ✅ **Modern UI** với smart highlighting & truncation```

                                          │ • F1-Score    │

                                          └───────────────┘- ✅ **100% crawl success** (30/30 recipes)

```

### Bước 2: Chạy toàn bộ pipeline (tuỳ chọn)

### Pipeline Xử Lý

## 📊 Tech Stack```bash

```

User Query ──▶ Text Processing ──▶ Search Engine ──▶ BM25 Ranking ──▶ Resultspython run_all.py

     │              │                     │                 │             │

     │         • Tokenization       • Load Index      • Calculate     Display- Python 3.12# Module 1 sẽ mất ~20 phút để crawl 30 recipes

     │         • Stopwords          • Match Terms      Relevance      Top-K

     │         • Normalize          • TF-IDF          • Sort          Results- Selenium 4.26 (browser automation)```

```

- BeautifulSoup4 4.12 (HTML parsing)

---

- Underthesea 6.7 (Vietnamese NLP)### Bước 3: Chạy web server

## 🔬 Thiết Kế & Thuật Toán

- Flask 3.0 (web framework)```bash

### Module 1: Web Crawler

python module4_web/app.py

**Mục tiêu:** Thu thập dữ liệu công thức nấu ăn từ Cooky.vn

## 🎯 Results```

**Công nghệ:**

- **Selenium WebDriver**: Xử lý JavaScript rendering (React SPA)

- **BeautifulSoup4**: Parse HTML và trích xuất dữ liệu

- **Chrome Headless**: Tối ưu hiệu suất- **30/30 recipes** crawled successfullyTruy cập: **http://localhost:5000**



**Thuật toán:**- **1,517 unique terms** indexed

```python

1. Khởi tạo Selenium WebDriver (headless mode)- **< 100ms** search latency---

2. For each recipe URL:

   a. Navigate và chờ 20s (React rendering)- **165.13 words** average document length

   b. Scroll 6 lần (350px mỗi lần) để load lazy content

   c. Parse HTML với BeautifulSoup## 📖 Cách sử dụng

   d. Extract: title, description, ingredients, steps

   e. Rate limiting: sleep 2s giữa các requests---

3. Lưu vào JSON format

4. Tuân thủ robots.txt### Demo nhanh

```

**Status:** Production Ready 🚀  ```bash

**Kết quả:**

- ✅ 30/30 recipes (100% success rate)**Web:** http://localhost:5000python demo.py

- ✅ 264 ingredients

- ✅ 146 cooking steps```

- ✅ Average 165.13 words/document

### Chạy từng module

---

```bash

### Module 2: Text Processing & Indexing# Module 1: Thu thập dữ liệu

python module1_crawler/crawler.py

**Mục tiêu:** Xử lý văn bản tiếng Việt và xây dựng Inverted Index

# Module 2: Xây dựng chỉ mục

**Công nghệ:**python module2_indexing/text_processor.py

- **Underthesea 6.7**: Vietnamese NLP toolkit

- **Custom TextProcessor**: Tối ưu cho domain công thức nấu ăn# Module 3: Demo tìm kiếm

python module3_ranking/search_engine.py

**Pipeline xử lý:**

# Module 4: Web server

```python module4_web/app.py

Raw Text ──▶ Lowercase ──▶ Tokenization ──▶ Stopword Removal ──▶ Clean Terms

   │              │              │                  │                  │# Module 5: Đánh giá hệ thống

"Thịt Bò"    "thịt bò"    ["thịt_bò"]      ["thịt_bò"]         ["thịt_bò"]python module5_evaluation/evaluate.py

``````



**Inverted Index Structure:**---

```json

{## 📁 Cấu trúc dự án

  "thịt_bò": {

    "doc_0": {"tf": 3, "positions": [10, 45, 89]},```

    "doc_5": {"tf": 2, "positions": [23, 67]},vertical_search_engine/

    "doc_12": {"tf": 1, "positions": [34]}├── module1_crawler/          # Module 1: Thu thập dữ liệu

  }├── module2_indexing/          # Module 2: Xử lý văn bản & indexing

}├── module3_ranking/           # Module 3: Truy vấn & xếp hạng

```├── module4_web/              # Module 4: Giao diện web

│   └── templates/            #   - HTML templates

**Kết quả:**├── module5_evaluation/       # Module 5: Đánh giá hệ thống

- ✅ 1,517 unique terms indexed├── data/                     # Dữ liệu công thức

- ✅ Average processing time: < 1s per document├── index/                    # Inverted index

- ✅ Index size: 500KB (compressed)├── requirements.txt          # Dependencies

├── demo.py                   # Script demo

---├── run_all.py               # Chạy toàn bộ pipeline

├── setup.bat                # Setup Windows

### Module 3: Search & Ranking (BM25)├── setup.sh                 # Setup Linux/Mac

├── README.md                # File này

**Mục tiêu:** Tìm kiếm và xếp hạng kết quả theo độ liên quan├── REPORT.md                # Báo cáo chi tiết

└── QUICKSTART.md            # Hướng dẫn nhanh

**Thuật toán BM25:**```



BM25 (Best Matching 25) là thuật toán xếp hạng state-of-the-art, vượt trội hơn TF-IDF.---



**Công thức:**## ✨ Tính năng & Công nghệ



```### Module 1: Web Crawler (Selenium)

BM25(q, d) = Σ IDF(qi) × (f(qi, d) × (k1 + 1)) / (f(qi, d) + k1 × (1 - b + b × |d| / avgdl))- ✅ **Real data** từ Cooky.vn (không phải sample data)

- ✅ **React SPA handling** với 20s wait + scroll strategy

Trong đó:- ✅ **Robots.txt compliance** + rate limiting (2s/page)

- q: query- ✅ **100% success rate** (30/30 recipes)

- d: document

- f(qi, d): term frequency của term qi trong document d### Module 2: Text Processing

- |d|: độ dài document d- ✅ **Vietnamese NLP** với Underthesea tokenization

- avgdl: độ dài trung bình của tất cả documents- ✅ **Inverted Index** với 1,517 terms

- k1: tuning parameter (thường = 1.5)- ✅ **TF-IDF scoring** + document length normalization

- b: tuning parameter (thường = 0.75)

- IDF(qi): log((N - df + 0.5) / (df + 0.5))### Module 3: Search & Ranking

```- ✅ **BM25 algorithm** (k1=1.5, b=0.75)

- ✅ **Multi-term queries** support

**Tại sao BM25 tốt hơn TF-IDF:**- ✅ **< 100ms** search latency

1. **Saturation effect**: TF không tăng vô hạn (tránh spam từ khóa)

2. **Length normalization**: Điều chỉnh theo độ dài document### Module 4: Web Interface

3. **Tunable parameters**: k1 và b có thể điều chỉnh theo domain- ✅ **Flask 3.0** với Bootstrap 5

- ✅ **Responsive design** + recipe detail pages

**Parameters tuned:**- ✅ **Score display** cho debugging

- k1 = 1.5 (term saturation)

- b = 0.75 (length normalization)### Module 5: Evaluation

- ✅ **Precision@K**, **Recall@K**, **MAP**, **F1-Score**

**Kết quả:**- ✅ **20 test queries** framework

- ✅ Query latency: < 100ms

- ✅ Accurate ranking (MAP 81.03%)---

- ✅ Handles multi-term queries

## 📊 Kết quả đạt được

---

### ✅ Crawler Success Rate: 100%

### Module 4: Web Interface- **30/30 công thức** crawl thành công từ Cooky.vn

- **264 nguyên liệu** tổng cộng

**Mục tiêu:** Giao diện người dùng thân thiện- **146 bước thực hiện** chi tiết

- **Fixed bug**: Duplicate URL detection (18/30 → 30/30)

**Tech Stack:**

- **Backend**: Flask 3.0### 🔤 Inverted Index

- **Template**: Jinja2- **1,517 unique terms** (Vietnamese tokenization)

- **Frontend**: HTML5 + CSS3- **165.13 từ** trung bình mỗi document

- **Styling**: Custom CSS với gradient design- **TF-IDF + BM25** ranking (k1=1.5, b=0.75)



**Features:**### 🌐 Web Interface

1. **Smart Highlighting**: Tô màu từ khóa trong kết quả- ✅ Flask server running at **http://localhost:5000**

2. **Smart Truncation**: Hiển thị context xung quanh từ khóa- ✅ Responsive Bootstrap UI

3. **Modern UI Design**: Card-based layout, responsive- ✅ Real-time search với BM25 scoring

- ✅ Recipe detail pages

**Routes:**

```python**Kết luận**: Hệ thống hoạt động hoàn hảo! ⭐⭐⭐⭐⭐

@app.route('/')              # Homepage với search box

@app.route('/search')        # Search results page---

@app.route('/recipe/<url>')  # Recipe detail page

```## 📚 Tài liệu & Demo



---### � Demo Search Examples



### Module 5: System Evaluation**Query: "thịt kho"**

```

**Mục tiêu:** Đánh giá chất lượng hệ thống tìm kiếm1. Cách Nấu Thịt Kho Tàu Ngày Tết (Score: 7.82)

2. Cách Làm Cá Basa Kho Tộ (Score: 6.86)

**Metrics:**3. Cách làm Nấm kho tiêu chay (Score: 6.46)

```

1. **Precision@K**: Độ chính xác trong top K kết quả

   ```**Query: "bún"**

   Precision@K = (# relevant docs in top K) / K```

   ```1. Cách Nấu Bún Mọc Nấm (Score: 10.39)

2. Cách Nấu Bún Chay (Score: 1.67)

2. **Recall@K**: Độ phủ trong top K kết quả```

   ```

   Recall@K = (# relevant docs in top K) / (total relevant docs)### 📖 Chi tiết kỹ thuật

   ```- � [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical deep dive

  - Architecture details

3. **Mean Average Precision (MAP)**: Chất lượng trung bình  - Bug fixes & solutions

   ```  - Performance metrics

   MAP = (Σ AP(q)) / (total queries)  - Development notes

   ```

---

**Test Queries:** 20 queries với ground truth dựa trên data thực tế

## 🎉 Status

---

✅ **TẤT CẢ 5 MODULES ĐÃ HOÀN THÀNH!**

## 📈 Kết Quả Đánh Giá

| Module | Files | Status | Notes |

### Tổng Quan Hiệu Suất|--------|-------|--------|-------|

| 1. Crawler | `module1_crawler/crawler.py` | ✅ DONE | 30/30 recipes |

| Metric | Score | Grade || 2. Indexing | `module2_indexing/text_processor.py` | ✅ DONE | 1,517 terms |

|--------|-------|-------|| 3. Ranking | `module3_ranking/search_engine.py` | ✅ DONE | BM25 |

| **Mean Average Precision (MAP)** | **81.03%** | ⭐⭐⭐⭐⭐ Xuất sắc || 4. Web UI | `module4_web/app.py` | ✅ DONE | Running :5000 |

| Average Precision@5 | 31.00% | ⭐⭐⭐ || 5. Evaluation | `module5_evaluation/evaluate.py` | ✅ DONE | Metrics ready |

| Average Precision@10 | 15.50% | ⭐⭐ |

| Average Recall@5 | 83.33% | ⭐⭐⭐⭐⭐ |**System Status:** 🚀 **PRODUCTION READY**

| Average Recall@10 | 83.33% | ⭐⭐⭐⭐⭐ |

| Average F1@10 | 24.77% | ⭐⭐⭐ |**Web Interface:** http://localhost:5000

| Query Latency | < 100ms | ⭐⭐⭐⭐⭐ |

---

### Chi Tiết Từng Query

**Developed for SEG301 - Search Engine Technology | FPT University | Fall 2025**

#### Top Performing Queries (AP = 1.0):

| Query | Precision@5 | Recall@5 | AP | Interpretation |
|-------|------------|----------|-----|----------------|
| "nấm" | 100% | 100% | 1.0 | Perfect! Tìm được 5/5 recipes trong top 5 ⭐ |
| "thịt" | 80% | 100% | 1.0 | Tìm được 4/4 recipes trong top 5 |
| "cà phê" | 60% | 100% | 1.0 | Tìm được 3/3 recipes trong top 5 |
| "xào" | 40% | 100% | 1.0 | Tìm được 2/2 recipes trong top 5 |
| "trà dâu" | 20% | 100% | 1.0 | Perfect ranking cho 1 recipe |

### Phân Tích Kết Quả

**✅ Điểm Mạnh:**

1. **MAP Score Xuất Sắc (81.03%)**
   - Vượt ngưỡng "Good" (> 60%)
   - Đạt mức "Excellent" (> 80%)
   - Chứng tỏ BM25 ranking rất hiệu quả

2. **Recall Cao (83.33%)**
   - Hệ thống tìm được hầu hết documents liên quan
   - Ít bị miss relevant results

3. **Query Latency Thấp (< 100ms)**
   - Trải nghiệm người dùng tốt
   - Index structure hiệu quả

4. **Perfect Ranking cho 75% queries**
   - 15/20 queries có AP = 1.0

**⚠️ Điểm Cần Cải Thiện:**

1. **Precision@K Thấp**: Do dataset nhỏ (30 recipes)
2. **Một số query khó**: Query "canh" cần field weighting
3. **Dataset size**: Cần mở rộng lên 100+ recipes

### Visualization

```
MAP Score Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 81.03% (Xuất sắc!)
━━━━━━━━━━━━━━━━━━━━━━━━ 60% (Good)
━━━━━━━━━━━━ 40% (Fair)
━━━━━━ 20% (Poor)

Precision@5 Distribution:
━━━━━━━━━━━━━━━━━━━━━━ 100% (nấm)
━━━━━━━━━━━━━━━ 80% (thịt)
━━━━━━━━━━━ 60% (cà phê)
━━━━━━━━ 40% (xào, chay)
━━━━ 20% (14 queries)
░░░░ 0% (canh)
```

---

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.12+
- Chrome/Chromium browser (for Selenium)
- 2GB RAM minimum
- 500MB disk space

### Cài Đặt Dependencies

```bash
# Clone repository
git clone https://github.com/ChrisLee1901/vietnamese-recipe-search.git
cd vietnamese-recipe-search

# Tạo virtual environment
python -m venv seg
seg\Scripts\activate  # Windows
# source seg/bin/activate  # Linux/Mac

# Cài đặt packages
pip install -r requirements.txt
```

### Requirements.txt

```txt
selenium==4.26.1
beautifulsoup4==4.12.3
underthesea==6.7.0
flask==3.0.3
```

---

## 💻 Sử Dụng

### Chạy Toàn Bộ Pipeline

```bash
python run_all.py
```

Output:
```
================================================================================
MODULE 1: THU THẬP DỮ LIỆU (CRAWLING)
================================================================================
✅ Crawled 30/30 recipes (100% success)

================================================================================
MODULE 2: XỬ LÝ & ĐÁNH CHỈ MỤC
================================================================================
✅ Indexed 1,517 unique terms

================================================================================
MODULE 3: TÌM KIẾM & XẾP HẠNG
================================================================================
✅ BM25 search engine ready

================================================================================
MODULE 4: GIAO DIỆN WEB
================================================================================
✅ Flask server running at http://localhost:5000

================================================================================
MODULE 5: ĐÁNH GIÁ HỆ THỐNG
================================================================================
✅ MAP: 81.03% (Xuất sắc!)
```

### Chạy Riêng Từng Module

```bash
# Module 1: Crawler
python module1_crawler/crawler.py

# Module 2: Indexing
python module2_indexing/text_processor.py

# Module 3: Test search
python module3_ranking/search_engine.py

# Module 4: Web server
python module4_web/app.py

# Module 5: Evaluation
python module5_evaluation/evaluate.py
```

---

## 🎬 Demo

### Web Interface

**Homepage:**
```
┌─────────────────────────────────────────────┐
│     🍲 Vietnamese Recipe Search             │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ Tìm món ăn... (vd: gà, bún, canh)    │ │
│  └───────────────────────────────────────┘ │
│              [  Tìm kiếm  ]                 │
└─────────────────────────────────────────────┘
```

**Search Results:**
```
┌─────────────────────────────────────────────┐
│  Kết quả cho: "gà"                   (2)    │
├─────────────────────────────────────────────┤
│  ⭐ Score: 6.79                             │
│  🍲 Lẩu Gà Ớt Hiểm                         │
│  Lẩu GÀ Ớt Hiểm là món ăn đậm chất...     │
│  🔗 cooky.vn/lau-ga-ot-hiem                │
├─────────────────────────────────────────────┤
│  ⭐ Score: 6.52                             │
│  🍲 Ức Gà Sốt Cam                          │
│  Ức GÀ sốt cam là một món ăn dễ làm...    │
│  🔗 cooky.vn/uc-ga-sot-cam                 │
└─────────────────────────────────────────────┘
```

### Screenshots

🖼️ Truy cập http://localhost:5000 để xem demo trực tiếp!

---

## 🛠️ Công Nghệ

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Core language |
| Selenium | 4.26.1 | Web scraping (JavaScript rendering) |
| BeautifulSoup4 | 4.12.3 | HTML parsing |
| Underthesea | 6.7.0 | Vietnamese NLP (tokenization) |
| Flask | 3.0.3 | Web framework |

### Algorithms

- **BM25**: Probabilistic ranking function
- **TF-IDF**: Term frequency-inverse document frequency
- **Inverted Index**: Fast term lookup
- **Vietnamese Tokenization**: Word segmentation for Vietnamese

---

## 📂 Cấu Trúc Project

```
vietnamese-recipe-search/
├── 📁 module1_crawler/          # Web Crawler
│   ├── __init__.py
│   └── crawler.py               # Selenium + BeautifulSoup
│
├── 📁 module2_indexing/         # Text Processing & Indexing
│   ├── __init__.py
│   └── text_processor.py        # Underthesea + Inverted Index
│
├── 📁 module3_ranking/          # Search & Ranking
│   ├── __init__.py
│   └── search_engine.py         # BM25 implementation
│
├── 📁 module4_web/              # Web Interface
│   ├── __init__.py
│   ├── app.py                   # Flask app
│   └── 📁 templates/
│       ├── index.html           # Homepage
│       ├── results.html         # Search results
│       └── recipe.html          # Recipe detail
│
├── 📁 module5_evaluation/       # System Evaluation
│   ├── __init__.py
│   └── evaluate.py              # Metrics calculation
│
├── 📁 data/                     # Crawled data
│   └── recipes.json             # 30 recipes
│
├── 📁 index/                    # Inverted index
│   └── inverted_index.json      # 1,517 terms
│
├── 📄 run_all.py                # Pipeline runner
├── 📄 requirements.txt          # Dependencies
├── 📄 README.md                 # This file
├── 📄 .gitignore                # Git ignore rules
└── 📄 evaluation_results.json   # Evaluation metrics
```

---

## 🎓 Tham Khảo

### Papers
- Robertson, S. E., & Zaragoza, H. (2009). **The Probabilistic Relevance Framework: BM25 and Beyond**
- Manning, C. D., et al. (2008). **Introduction to Information Retrieval**

### Libraries
- [Underthesea Documentation](https://github.com/undertheseanlp/underthesea)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)

---

## 🔮 Future Work

### Planned Improvements

1. **Expand Dataset** - Target: 100-500 recipes
2. **Advanced NLP** - Synonym expansion, spelling correction
3. **Enhanced Ranking** - Field weighting, ML re-ranking
4. **Better UI/UX** - Faceted search, recommendations
5. **Performance** - Caching, database optimization

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 👥 Contributors

- **ChrisLee1901** - Project Lead & Full Stack Development
- Email: thiendanh190105@gmail.com
- GitHub: [@ChrisLee1901](https://github.com/ChrisLee1901)

---

## 🙏 Acknowledgments

- **Cooky.vn** - Data source
- **FPT University** - SEG301 Course
- **Underthesea Team** - Vietnamese NLP toolkit
- **Flask Team** - Web framework

---

## 📞 Contact & Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/ChrisLee1901/vietnamese-recipe-search/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/ChrisLee1901/vietnamese-recipe-search/discussions)
- 📧 **Email**: thiendanh190105@gmail.com

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ and ☕ by ChrisLee1901

**Developed for SEG301 - Search Engine Technology | FPT University | Fall 2025**

</div>
