# 🍳 Vertical Search Engine - Vietnamese Recipe Search# 🍳 Vertical Search Engine - Máy Tìm Kiếm Công Thức Nấu Ăn



Hệ thống tìm kiếm chuyên sâu cho công thức nấu ăn Việt Nam.<div align="center">



## 🚀 Quick Start**Hệ thống tìm kiếm chuyên sâu về công thức nấu ăn Việt Nam**



### 1. Cài đặt[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

```bash[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

pip install -r requirements.txt

```</div>



### 2. Chạy hệ thống---



#### Chạy toàn bộ pipeline (crawl + index + evaluate):## 📋 Mô tả dự án

```bash

python run_all.pyHệ thống tìm kiếm chuyên sâu (Vertical Search Engine) về công thức nấu ăn, được xây dựng hoàn chỉnh với **5 modules** theo yêu cầu đồ án SEG301:

```

### 🔧 5 Modules chính

#### Chỉ chạy web interface:

```bash1. ✅ **Module 1**: Thu thập dữ liệu (Web Crawling)

python module4_web/app.py2. ✅ **Module 2**: Xử lý văn bản & Xây dựng chỉ mục (Inverted Index)

```3. ✅ **Module 3**: Truy vấn & Xếp hạng kết quả (TF-IDF, BM25)

Truy cập: **http://localhost:5000**4. ✅ **Module 4**: Giao diện Web (Flask)

5. ✅ **Module 5**: Đánh giá hệ thống (Precision@10, MAP)

## 📁 Cấu trúc

---

```

vertical_search_engine/## 🚀 Cài đặt nhanh

├── data/                    # 30 recipes (264 ingredients, 146 steps)

├── index/                   # Inverted index (1,517 terms)### Yêu cầu

├── module1_crawler/         # Selenium web crawler- Python 3.12+

├── module2_indexing/        # Vietnamese NLP + Inverted Index- Chrome/Chromium browser (cho Selenium)

├── module3_ranking/         # BM25 search algorithm- 4 dependencies: selenium, beautifulsoup4, underthesea, flask

├── module4_web/            # Flask web interface

├── module5_evaluation/     # Precision, Recall, MAP metrics### Bước 1: Cài đặt dependencies

└── run_all.py              # Pipeline orchestrator```bash

```# Tạo virtual environment

python -m venv seg

## ✨ Features.\seg\Scripts\activate  # Windows

# source seg/bin/activate  # Linux/Mac

- ✅ **Real web crawling** từ Cooky.vn (Selenium + React SPA support)

- ✅ **Vietnamese NLP** với Underthesea tokenization# Cài dependencies

- ✅ **BM25 ranking** (k1=1.5, b=0.75)pip install -r requirements.txt

- ✅ **Modern UI** với smart highlighting & truncation```

- ✅ **100% crawl success** (30/30 recipes)

### Bước 2: Chạy toàn bộ pipeline (tuỳ chọn)

## 📊 Tech Stack```bash

python run_all.py

- Python 3.12# Module 1 sẽ mất ~20 phút để crawl 30 recipes

- Selenium 4.26 (browser automation)```

- BeautifulSoup4 4.12 (HTML parsing)

- Underthesea 6.7 (Vietnamese NLP)### Bước 3: Chạy web server

- Flask 3.0 (web framework)```bash

python module4_web/app.py

## 🎯 Results```



- **30/30 recipes** crawled successfullyTruy cập: **http://localhost:5000**

- **1,517 unique terms** indexed

- **< 100ms** search latency---

- **165.13 words** average document length

## 📖 Cách sử dụng

---

### Demo nhanh

**Status:** Production Ready 🚀  ```bash

**Web:** http://localhost:5000python demo.py

```

### Chạy từng module

```bash
# Module 1: Thu thập dữ liệu
python module1_crawler/crawler.py

# Module 2: Xây dựng chỉ mục
python module2_indexing/text_processor.py

# Module 3: Demo tìm kiếm
python module3_ranking/search_engine.py

# Module 4: Web server
python module4_web/app.py

# Module 5: Đánh giá hệ thống
python module5_evaluation/evaluate.py
```

---

## 📁 Cấu trúc dự án

```
vertical_search_engine/
├── module1_crawler/          # Module 1: Thu thập dữ liệu
├── module2_indexing/          # Module 2: Xử lý văn bản & indexing
├── module3_ranking/           # Module 3: Truy vấn & xếp hạng
├── module4_web/              # Module 4: Giao diện web
│   └── templates/            #   - HTML templates
├── module5_evaluation/       # Module 5: Đánh giá hệ thống
├── data/                     # Dữ liệu công thức
├── index/                    # Inverted index
├── requirements.txt          # Dependencies
├── demo.py                   # Script demo
├── run_all.py               # Chạy toàn bộ pipeline
├── setup.bat                # Setup Windows
├── setup.sh                 # Setup Linux/Mac
├── README.md                # File này
├── REPORT.md                # Báo cáo chi tiết
└── QUICKSTART.md            # Hướng dẫn nhanh
```

---

## ✨ Tính năng & Công nghệ

### Module 1: Web Crawler (Selenium)
- ✅ **Real data** từ Cooky.vn (không phải sample data)
- ✅ **React SPA handling** với 20s wait + scroll strategy
- ✅ **Robots.txt compliance** + rate limiting (2s/page)
- ✅ **100% success rate** (30/30 recipes)

### Module 2: Text Processing
- ✅ **Vietnamese NLP** với Underthesea tokenization
- ✅ **Inverted Index** với 1,517 terms
- ✅ **TF-IDF scoring** + document length normalization

### Module 3: Search & Ranking
- ✅ **BM25 algorithm** (k1=1.5, b=0.75)
- ✅ **Multi-term queries** support
- ✅ **< 100ms** search latency

### Module 4: Web Interface
- ✅ **Flask 3.0** với Bootstrap 5
- ✅ **Responsive design** + recipe detail pages
- ✅ **Score display** cho debugging

### Module 5: Evaluation
- ✅ **Precision@K**, **Recall@K**, **MAP**, **F1-Score**
- ✅ **20 test queries** framework

---

## 📊 Kết quả đạt được

### ✅ Crawler Success Rate: 100%
- **30/30 công thức** crawl thành công từ Cooky.vn
- **264 nguyên liệu** tổng cộng
- **146 bước thực hiện** chi tiết
- **Fixed bug**: Duplicate URL detection (18/30 → 30/30)

### 🔤 Inverted Index
- **1,517 unique terms** (Vietnamese tokenization)
- **165.13 từ** trung bình mỗi document
- **TF-IDF + BM25** ranking (k1=1.5, b=0.75)

### 🌐 Web Interface
- ✅ Flask server running at **http://localhost:5000**
- ✅ Responsive Bootstrap UI
- ✅ Real-time search với BM25 scoring
- ✅ Recipe detail pages

**Kết luận**: Hệ thống hoạt động hoàn hảo! ⭐⭐⭐⭐⭐

---

## 📚 Tài liệu & Demo

### � Demo Search Examples

**Query: "thịt kho"**
```
1. Cách Nấu Thịt Kho Tàu Ngày Tết (Score: 7.82)
2. Cách Làm Cá Basa Kho Tộ (Score: 6.86)
3. Cách làm Nấm kho tiêu chay (Score: 6.46)
```

**Query: "bún"**
```
1. Cách Nấu Bún Mọc Nấm (Score: 10.39)
2. Cách Nấu Bún Chay (Score: 1.67)
```

### 📖 Chi tiết kỹ thuật
- � [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical deep dive
  - Architecture details
  - Bug fixes & solutions
  - Performance metrics
  - Development notes

---

## 🎉 Status

✅ **TẤT CẢ 5 MODULES ĐÃ HOÀN THÀNH!**

| Module | Files | Status | Notes |
|--------|-------|--------|-------|
| 1. Crawler | `module1_crawler/crawler.py` | ✅ DONE | 30/30 recipes |
| 2. Indexing | `module2_indexing/text_processor.py` | ✅ DONE | 1,517 terms |
| 3. Ranking | `module3_ranking/search_engine.py` | ✅ DONE | BM25 |
| 4. Web UI | `module4_web/app.py` | ✅ DONE | Running :5000 |
| 5. Evaluation | `module5_evaluation/evaluate.py` | ✅ DONE | Metrics ready |

**System Status:** 🚀 **PRODUCTION READY**

**Web Interface:** http://localhost:5000

---

**Developed for SEG301 - Search Engine Technology | FPT University | Fall 2025**
