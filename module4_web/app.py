"""
MODULE 4: GIAO DIỆN WEB
Mục tiêu: Xây dựng web interface với Flask
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import sys
import re

# Import từ các module khác
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module2_indexing.text_processor import InvertedIndex, TextProcessor
from module3_ranking.search_engine import SearchEngine

app = Flask(__name__)

# Global variables
search_engine = None
documents = []


def load_data():
    """
    Load index và documents khi khởi động
    """
    global search_engine, documents
    
    # Đường dẫn tới data và index
    base_dir = os.path.dirname(os.path.dirname(__file__))
    index_file = os.path.join(base_dir, 'index', 'inverted_index.json')
    data_file = os.path.join(base_dir, 'data', 'recipes.json')
    
    print("📂 Đang tải dữ liệu...")
    
    # Load inverted index
    inverted_index = InvertedIndex()
    inverted_index.load(index_file)
    
    # Load documents
    with open(data_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    # Tạo search engine
    search_engine = SearchEngine(inverted_index, documents)
    
    print("✅ Đã tải dữ liệu thành công!")


@app.route('/')
def index():
    """
    Trang chủ
    """
    return render_template('index.html')


@app.route('/search')
def search():
    """
    Xử lý tìm kiếm và trả về kết quả
    """
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 10
    
    if not query:
        return render_template('index.html')
    
    # Tìm kiếm
    all_results = search_engine.search(query, top_k=100, method='bm25')
    
    # Phân trang
    total_results = len(all_results)
    total_pages = (total_results + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    results = all_results[start_idx:end_idx]
    
    # Highlight từ khóa trong kết quả (sử dụng logic cải tiến)
    for result in results:
        result['highlighted_title'] = highlight_text_improved(result['title'], query)
        result['highlighted_description'] = truncate_and_highlight(result['description'], query, max_length=200)
    
    return render_template('results.html', 
                          query=query, 
                          results=results,
                          total_results=total_results,
                          page=page,
                          total_pages=total_pages)


@app.route('/recipe/<path:recipe_url>')
def recipe_detail(recipe_url):
    """
    Hiển thị chi tiết công thức
    """
    # Tìm recipe theo URL
    recipe = None
    for doc in documents:
        if doc['url'] == recipe_url:
            recipe = doc
            break
    
    if recipe:
        return render_template('recipe.html', recipe=recipe)
    else:
        return "Recipe not found", 404


@app.route('/api/search')
def api_search():
    """
    API endpoint cho tìm kiếm (JSON response)
    """
    query = request.args.get('q', '')
    top_k = int(request.args.get('top_k', 10))
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    results = search_engine.search(query, top_k=top_k, method='bm25')
    
    return jsonify({
        'query': query,
        'total_results': len(results),
        'results': results
    })


def highlight_text_improved(text, query):
    """
    Highlight từ khóa trong text với logic thông minh hơn
    Sử dụng Vietnamese NLP tokenization để highlight chính xác
    """
    if not text:
        return text
    
    # Process query giống như search engine
    processor = TextProcessor()
    query_terms = processor.process(query)
    
    if not query_terms:
        return text
    
    highlighted = text
    for term in query_terms:
        # Replace underscore với space cho compound words
        term_display = term.replace('_', ' ')
        
        # Tìm và highlight (case-insensitive, word boundary)
        # \b ensures word boundary so "gà" won't match inside "ngà"
        pattern = re.compile(r'\b(' + re.escape(term_display) + r')\b', re.IGNORECASE)
        highlighted = pattern.sub(r'<mark>\1</mark>', highlighted)
    
    return highlighted


def truncate_and_highlight(text, query, max_length=200):
    """
    Cắt text và highlight từ khóa
    Ưu tiên hiển thị phần có từ khóa
    """
    if not text:
        return text
    
    # Process query
    processor = TextProcessor()
    query_terms = processor.process(query)
    
    if not query_terms:
        # Không có query terms, chỉ cắt text
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text
    
    # Tìm vị trí của từ khóa đầu tiên
    query_lower = query.lower()
    text_lower = text.lower()
    
    keyword_pos = text_lower.find(query_lower)
    
    if keyword_pos == -1:
        # Không tìm thấy exact match, thử từng term
        for term in query_terms:
            term_display = term.replace('_', ' ')
            keyword_pos = text_lower.find(term_display.lower())
            if keyword_pos != -1:
                break
    
    if keyword_pos != -1 and keyword_pos > max_length // 2:
        # Từ khóa nằm xa đầu text, cắt để show context xung quanh
        start = max(0, keyword_pos - max_length // 3)
        end = min(len(text), start + max_length)
        truncated = ('...' if start > 0 else '') + text[start:end] + ('...' if end < len(text) else '')
    else:
        # Từ khóa ở đầu hoặc không tìm thấy, cắt bình thường
        if len(text) > max_length:
            truncated = text[:max_length] + '...'
        else:
            truncated = text
    
    # Highlight sau khi cắt
    return highlight_text_improved(truncated, query)


if __name__ == '__main__':
    print("=" * 60)
    print("MODULE 4: GIAO DIỆN WEB")
    print("=" * 60)
    
    # Load dữ liệu
    load_data()
    
    # Chạy Flask app
    print("\n🌐 Đang khởi động web server...")
    print("📍 Truy cập: http://localhost:5000")
    print("\n⚠️  Nhấn Ctrl+C để dừng server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
