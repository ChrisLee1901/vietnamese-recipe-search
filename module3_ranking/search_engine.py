"""
MODULE 3: TRUY VẤN & XẾP HẠNG KẾT QUẢ
Mục tiêu: Tìm kiếm và xếp hạng kết quả theo độ liên quan (TF-IDF, BM25)
"""

import json
import math
from collections import defaultdict
import sys
import os

# Import từ module 2
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'module2_indexing'))
from text_processor import TextProcessor, InvertedIndex


class SearchEngine:
    """
    Class tìm kiếm và xếp hạng kết quả
    """
    def __init__(self, inverted_index, documents):
        """
        Args:
            inverted_index: InvertedIndex object
            documents: danh sách tài liệu gốc
        """
        self.index = inverted_index
        self.documents = {doc['url']: doc for doc in documents}
        self.text_processor = TextProcessor()
    
    def calculate_tf_idf(self, term_freq, doc_id, term):
        """
        Tính TF-IDF score
        TF-IDF = TF * IDF
        TF = (term frequency in document)
        IDF = log(N / df)
        """
        # TF (normalized)
        doc_length = self.index.doc_lengths.get(doc_id, 1)
        tf = term_freq / doc_length if doc_length > 0 else 0
        
        # IDF
        idf = self.index.get_idf(term)
        
        # TF-IDF
        return tf * idf
    
    def calculate_bm25(self, term_freq, doc_id, term, k1=1.5, b=0.75):
        """
        Tính BM25 score (thuật toán xếp hạng tốt hơn TF-IDF)
        BM25 = IDF * (f(qi, D) * (k1 + 1)) / (f(qi, D) + k1 * (1 - b + b * |D| / avgdl))
        
        Args:
            term_freq: tần suất term trong tài liệu
            doc_id: ID tài liệu
            term: từ khóa
            k1: tham số điều chỉnh (thường 1.2-2.0)
            b: tham số điều chỉnh độ dài tài liệu (0-1)
        """
        # IDF
        idf = self.index.get_idf(term)
        
        # Document length normalization
        doc_length = self.index.doc_lengths.get(doc_id, 1)
        avg_doc_length = self.index.avg_doc_length
        
        # BM25 formula
        numerator = term_freq * (k1 + 1)
        denominator = term_freq + k1 * (1 - b + b * (doc_length / avg_doc_length))
        
        bm25_score = idf * (numerator / denominator)
        
        return bm25_score
    
    def search(self, query, top_k=10, method='bm25'):
        """
        Tìm kiếm và xếp hạng kết quả
        
        Args:
            query: câu truy vấn
            top_k: số kết quả trả về
            method: phương pháp xếp hạng ('tfidf' hoặc 'bm25')
        
        Returns:
            list: danh sách kết quả đã xếp hạng
        """
        # Xử lý query giống như xử lý document
        query_terms = self.text_processor.process(query)
        
        if not query_terms:
            return []
        
        # Tính score cho mỗi document
        doc_scores = defaultdict(float)
        
        for term in query_terms:
            posting_list = self.index.get_posting_list(term)
            
            for posting in posting_list:
                doc_id = posting['doc_id']
                term_freq = posting['frequency']
                
                # Tính score theo phương pháp được chọn
                if method == 'tfidf':
                    score = self.calculate_tf_idf(term_freq, doc_id, term)
                else:  # bm25
                    score = self.calculate_bm25(term_freq, doc_id, term)
                
                doc_scores[doc_id] += score
        
        # Sắp xếp theo score giảm dần
        ranked_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Lấy top K kết quả
        top_results = ranked_results[:top_k]
        
        # Tạo kết quả chi tiết
        results = []
        for doc_id, score in top_results:
            doc = self.documents.get(doc_id)
            if doc:
                result = {
                    'doc_id': doc_id,
                    'score': score,
                    'title': doc.get('title', ''),
                    'description': doc.get('description', ''),
                    'url': doc.get('url', ''),
                    'ingredients': doc.get('ingredients', []),
                    'instructions': doc.get('instructions', []),
                    'prep_time': doc.get('prep_time', ''),
                    'cook_time': doc.get('cook_time', ''),
                    'servings': doc.get('servings', '')
                }
                results.append(result)
        
        return results
    
    def highlight_keywords(self, text, query):
        """
        Highlight từ khóa trong văn bản
        """
        query_terms = self.text_processor.process(query)
        
        highlighted_text = text
        for term in query_terms:
            # Case-insensitive replace
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            highlighted_text = pattern.sub(f"<mark>{term}</mark>", highlighted_text)
        
        return highlighted_text
    
    def get_snippet(self, text, query, max_length=200):
        """
        Tạo đoạn trích ngắn có chứa từ khóa
        """
        query_terms = self.text_processor.process(query)
        
        # Tìm vị trí xuất hiện đầu tiên của từ khóa
        text_lower = text.lower()
        first_position = len(text)
        
        for term in query_terms:
            pos = text_lower.find(term.lower())
            if pos != -1 and pos < first_position:
                first_position = pos
        
        # Tạo snippet xung quanh từ khóa
        start = max(0, first_position - max_length // 2)
        end = min(len(text), first_position + max_length // 2)
        
        snippet = text[start:end]
        
        # Thêm "..." nếu bị cắt
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        
        return snippet


def demo_search():
    """
    Demo chức năng tìm kiếm
    """
    import os
    import re
    
    print("=" * 60)
    print("MODULE 3: TRUY VẤN & XẾP HẠNG KẾT QUẢ")
    print("=" * 60)
    
    # Lấy đường dẫn tuyệt đối từ script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    # Load index và documents
    index_file = os.path.join(base_dir, 'index', 'inverted_index.json')
    data_file = os.path.join(base_dir, 'data', 'recipes.json')
    
    print("\n📂 Đang tải dữ liệu...")
    
    # Load inverted index
    inverted_index = InvertedIndex()
    inverted_index.load(index_file)
    
    # Load documents
    with open(data_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    # Tạo search engine
    search_engine = SearchEngine(inverted_index, documents)
    
    # Demo queries
    demo_queries = [
        "phở bò",
        "nướng",
        "canh chua",
        "thịt kho",
        "bún"
    ]
    
    print("\n🔍 DEMO TÌM KIẾM:\n")
    
    for query in demo_queries:
        print(f"\n{'='*60}")
        print(f"Query: '{query}'")
        print(f"{'='*60}")
        
        # Tìm kiếm với BM25
        results = search_engine.search(query, top_k=3, method='bm25')
        
        if results:
            print(f"\n✅ Tìm thấy {len(results)} kết quả:\n")
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']}")
                print(f"   Score: {result['score']:.4f}")
                print(f"   Mô tả: {result['description'][:100]}...")
                print(f"   URL: {result['url']}")
                print()
        else:
            print("\n❌ Không tìm thấy kết quả phù hợp\n")
    
    print("\n✅ MODULE 3 HOÀN THÀNH!")
    print("=" * 60)


if __name__ == "__main__":
    import re
    demo_search()
