"""
MODULE 2: XỬ LÝ VĂN BẢN & XÂY DỰNG CHỈ MỤC
Mục tiêu: Làm sạch văn bản và xây dựng Inverted Index
"""

import re
import json
from collections import defaultdict
import math
from underthesea import word_tokenize


class TextProcessor:
    """
    Class xử lý văn bản tiếng Việt
    """
    def __init__(self):
        # Danh sách từ dừng tiếng Việt
        self.stop_words = set([
            'và', 'của', 'là', 'có', 'được', 'trong', 'cho', 'với', 'từ', 'một',
            'các', 'này', 'đó', 'để', 'những', 'bởi', 'như', 'khi', 'đã', 'tại',
            'về', 'vào', 'ra', 'đến', 'lên', 'theo', 'nên', 'nhưng', 'hoặc',
            'thì', 'sẽ', 'rất', 'cũng', 'đang', 'bị', 'làm', 'nào', 'ai', 'gì'
        ])
    
    def tokenize(self, text):
        """
        Tách từ tiếng Việt
        Args:
            text: chuỗi văn bản cần tách
        Returns:
            list: danh sách các từ
        """
        try:
            # Sử dụng underthesea để tách từ tiếng Việt
            tokens = word_tokenize(text, format="text").split()
            return tokens
        except:
            # Fallback: tách đơn giản nếu underthesea lỗi
            return text.split()
    
    def normalize(self, text):
        """
        Chuẩn hóa văn bản: chuyển về chữ thường, loại bỏ ký tự đặc biệt
        """
        # Chuyển về chữ thường
        text = text.lower()
        
        # Loại bỏ ký tự đặc biệt, chỉ giữ chữ cái, số và khoảng trắng
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, tokens):
        """
        Loại bỏ từ dừng
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def process(self, text):
        """
        Xử lý văn bản hoàn chỉnh: normalize -> tokenize -> remove stopwords
        """
        # Chuẩn hóa
        normalized_text = self.normalize(text)
        
        # Tách từ
        tokens = self.tokenize(normalized_text)
        
        # Loại bỏ từ dừng
        filtered_tokens = self.remove_stopwords(tokens)
        
        return filtered_tokens


class InvertedIndex:
    """
    Class xây dựng và quản lý Inverted Index
    """
    def __init__(self):
        self.index = defaultdict(list)  # {term: [(doc_id, frequency, positions), ...]}
        self.doc_lengths = {}  # {doc_id: length}
        self.doc_count = 0
        self.avg_doc_length = 0
        self.text_processor = TextProcessor()
    
    def add_document(self, doc_id, text, field_weight=1.0):
        """
        Thêm tài liệu vào index
        Args:
            doc_id: ID của tài liệu
            text: nội dung văn bản
            field_weight: trọng số của trường (ví dụ: title có trọng số cao hơn)
        """
        # Xử lý văn bản
        tokens = self.text_processor.process(text)
        
        # Đếm tần suất và vị trí của mỗi từ
        term_freq = defaultdict(int)
        term_positions = defaultdict(list)
        
        for position, token in enumerate(tokens):
            term_freq[token] += 1
            term_positions[token].append(position)
        
        # Thêm vào inverted index
        for term, freq in term_freq.items():
            weighted_freq = freq * field_weight
            self.index[term].append({
                'doc_id': doc_id,
                'frequency': weighted_freq,
                'positions': term_positions[term]
            })
        
        # Lưu độ dài tài liệu
        self.doc_lengths[doc_id] = len(tokens)
    
    def build_from_documents(self, documents):
        """
        Xây dựng index từ danh sách tài liệu
        Args:
            documents: list các dict chứa thông tin tài liệu
        """
        print("🔨 Đang xây dựng Inverted Index...")
        
        for doc in documents:
            doc_id = doc['url']  # Sử dụng URL làm doc_id
            
            # Index các trường với trọng số khác nhau
            # Title có trọng số cao nhất
            self.add_document(doc_id, doc.get('title', ''), field_weight=3.0)
            
            # Description có trọng số trung bình
            self.add_document(doc_id, doc.get('description', ''), field_weight=2.0)
            
            # Ingredients
            ingredients_text = ' '.join(doc.get('ingredients', []))
            self.add_document(doc_id, ingredients_text, field_weight=1.5)
            
            # Instructions
            instructions_text = ' '.join(doc.get('instructions', []))
            self.add_document(doc_id, instructions_text, field_weight=1.0)
        
        self.doc_count = len(documents)
        self.avg_doc_length = sum(self.doc_lengths.values()) / self.doc_count if self.doc_count > 0 else 0
        
        print(f"✅ Đã xây dựng index cho {self.doc_count} tài liệu")
        print(f"   - Tổng số terms: {len(self.index)}")
        print(f"   - Độ dài tài liệu trung bình: {self.avg_doc_length:.2f} từ")
    
    def get_posting_list(self, term):
        """
        Lấy posting list của một term
        """
        processed_term = self.text_processor.process(term)
        if processed_term:
            return self.index.get(processed_term[0], [])
        return []
    
    def get_document_frequency(self, term):
        """
        Lấy số tài liệu chứa term
        """
        return len(self.get_posting_list(term))
    
    def get_idf(self, term):
        """
        Tính IDF (Inverse Document Frequency)
        IDF = log(N / df)
        """
        df = self.get_document_frequency(term)
        if df == 0:
            return 0
        return math.log(self.doc_count / df)
    
    def save(self, filepath):
        """
        Lưu index vào file
        """
        data = {
            'index': dict(self.index),
            'doc_lengths': self.doc_lengths,
            'doc_count': self.doc_count,
            'avg_doc_length': self.avg_doc_length
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Đã lưu index vào: {filepath}")
    
    def load(self, filepath):
        """
        Tải index từ file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.index = defaultdict(list, data['index'])
        self.doc_lengths = data['doc_lengths']
        self.doc_count = data['doc_count']
        self.avg_doc_length = data['avg_doc_length']
        
        print(f"📂 Đã tải index từ: {filepath}")
        print(f"   - Số tài liệu: {self.doc_count}")
        print(f"   - Số terms: {len(self.index)}")


def main():
    """
    Hàm chính để xây dựng index
    """
    import os
    
    print("=" * 60)
    print("MODULE 2: XỬ LÝ VĂN BẢN & XÂY DỰNG CHỈ MỤC")
    print("=" * 60)
    
    # Lấy đường dẫn tuyệt đối từ script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    # Đọc dữ liệu từ Module 1
    data_file = os.path.join(base_dir, 'data', 'recipes.json')
    print(f"\n📂 Đang đọc dữ liệu từ: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"✅ Đã đọc {len(documents)} tài liệu")
    
    # Xây dựng Inverted Index
    inverted_index = InvertedIndex()
    inverted_index.build_from_documents(documents)
    
    # Lưu index
    index_file = os.path.join(base_dir, 'index', 'inverted_index.json')
    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    inverted_index.save(index_file)
    
    # Demo: hiển thị một số term
    print("\n📊 MẪU INDEX (một số term):")
    sample_terms = list(inverted_index.index.keys())[:5]
    for term in sample_terms:
        posting_list = inverted_index.index[term]
        print(f"\n   Term: '{term}'")
        print(f"   - Document Frequency: {len(posting_list)}")
        print(f"   - IDF: {inverted_index.get_idf(term):.4f}")
        if posting_list:
            first_posting = posting_list[0]
            print(f"   - Ví dụ: doc_id={first_posting['doc_id'][:50]}..., freq={first_posting['frequency']}")
    
    print("\n✅ MODULE 2 HOÀN THÀNH!")
    print("=" * 60)


if __name__ == "__main__":
    main()
