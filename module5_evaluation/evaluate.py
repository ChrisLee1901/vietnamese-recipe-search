"""
MODULE 5: ĐÁNH GIÁ HỆ THỐNG
Mục tiêu: Đánh giá chất lượng hệ thống tìm kiếm (Precision@K, MAP)
"""

import json
import os
import sys
from collections import defaultdict

# Import từ các module khác
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module2_indexing.text_processor import InvertedIndex
from module3_ranking.search_engine import SearchEngine


class Evaluator:
    """
    Class đánh giá hệ thống tìm kiếm
    """
    def __init__(self, search_engine):
        """
        Args:
            search_engine: SearchEngine object
        """
        self.search_engine = search_engine
    
    def precision_at_k(self, retrieved_docs, relevant_docs, k=10):
        """
        Tính Precision@K
        Precision@K = (số document liên quan trong top K) / K
        
        Args:
            retrieved_docs: danh sách document ID được trả về (theo thứ tự)
            relevant_docs: set các document ID liên quan
            k: số document xét trong top K
        
        Returns:
            float: Precision@K score
        """
        top_k = retrieved_docs[:k]
        relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant_docs)
        
        return relevant_in_top_k / k if k > 0 else 0.0
    
    def recall_at_k(self, retrieved_docs, relevant_docs, k=10):
        """
        Tính Recall@K
        Recall@K = (số document liên quan trong top K) / (tổng số document liên quan)
        """
        top_k = retrieved_docs[:k]
        relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant_docs)
        total_relevant = len(relevant_docs)
        
        return relevant_in_top_k / total_relevant if total_relevant > 0 else 0.0
    
    def average_precision(self, retrieved_docs, relevant_docs):
        """
        Tính Average Precision (AP)
        AP = (sum of Precision@i for all relevant docs) / (total relevant docs)
        
        Args:
            retrieved_docs: danh sách document ID được trả về (theo thứ tự)
            relevant_docs: set các document ID liên quan
        
        Returns:
            float: Average Precision score
        """
        if not relevant_docs:
            return 0.0
        
        precisions = []
        relevant_count = 0
        
        for i, doc_id in enumerate(retrieved_docs, 1):
            if doc_id in relevant_docs:
                relevant_count += 1
                precision_at_i = relevant_count / i
                precisions.append(precision_at_i)
        
        return sum(precisions) / len(relevant_docs) if precisions else 0.0
    
    def mean_average_precision(self, query_results):
        """
        Tính Mean Average Precision (MAP)
        MAP = average of AP across all queries
        
        Args:
            query_results: dict {query: (retrieved_docs, relevant_docs)}
        
        Returns:
            float: MAP score
        """
        aps = []
        
        for query, (retrieved_docs, relevant_docs) in query_results.items():
            ap = self.average_precision(retrieved_docs, relevant_docs)
            aps.append(ap)
        
        return sum(aps) / len(aps) if aps else 0.0
    
    def evaluate_query(self, query, relevant_docs, k_values=[5, 10]):
        """
        Đánh giá một query
        
        Args:
            query: câu truy vấn
            relevant_docs: set các document ID liên quan
            k_values: list các giá trị K để tính Precision@K
        
        Returns:
            dict: kết quả đánh giá
        """
        # Tìm kiếm
        results = self.search_engine.search(query, top_k=50, method='bm25')
        retrieved_docs = [r['doc_id'] for r in results]
        
        # Tính các metrics
        metrics = {}
        
        # Precision@K và Recall@K
        for k in k_values:
            metrics[f'Precision@{k}'] = self.precision_at_k(retrieved_docs, relevant_docs, k)
            metrics[f'Recall@{k}'] = self.recall_at_k(retrieved_docs, relevant_docs, k)
        
        # Average Precision
        metrics['AP'] = self.average_precision(retrieved_docs, relevant_docs)
        
        # F1-Score@10
        p10 = metrics.get('Precision@10', 0)
        r10 = metrics.get('Recall@10', 0)
        metrics['F1@10'] = 2 * (p10 * r10) / (p10 + r10) if (p10 + r10) > 0 else 0
        
        return metrics, retrieved_docs
    
    def evaluate_all(self, test_queries):
        """
        Đánh giá toàn bộ hệ thống với tập queries
        
        Args:
            test_queries: dict {query: set(relevant_doc_ids)}
        
        Returns:
            dict: kết quả đánh giá tổng hợp
        """
        all_metrics = defaultdict(list)
        query_results = {}
        
        print("\n📊 ĐÁNH GIÁ CHI TIẾT TỪNG QUERY:")
        print("=" * 80)
        
        for query, relevant_docs in test_queries.items():
            print(f"\n🔍 Query: '{query}'")
            print(f"   Relevant docs: {len(relevant_docs)}")
            
            metrics, retrieved_docs = self.evaluate_query(query, relevant_docs)
            query_results[query] = (retrieved_docs, relevant_docs)
            
            # In kết quả
            print(f"   Precision@5:  {metrics['Precision@5']:.4f}")
            print(f"   Precision@10: {metrics['Precision@10']:.4f}")
            print(f"   Recall@5:     {metrics['Recall@5']:.4f}")
            print(f"   Recall@10:    {metrics['Recall@10']:.4f}")
            print(f"   AP:           {metrics['AP']:.4f}")
            print(f"   F1@10:        {metrics['F1@10']:.4f}")
            
            # Lưu metrics
            for metric_name, value in metrics.items():
                all_metrics[metric_name].append(value)
        
        # Tính trung bình
        avg_metrics = {}
        for metric_name, values in all_metrics.items():
            avg_metrics[f'Avg_{metric_name}'] = sum(values) / len(values)
        
        # Tính MAP
        avg_metrics['MAP'] = self.mean_average_precision(query_results)
        
        return avg_metrics


def create_test_queries():
    """
    Tạo tập queries test với ground truth (relevant documents) dựa trên data đã crawl
    """
    test_queries = {
        # Query 1: Trà dâu
        "trà dâu": {
            "https://www.cooky.vn/cong-thuc/tra-dau-ngam-55209"
        },
        
        # Query 2: Gà
        "gà": {
            "https://www.cooky.vn/cong-thuc/lau-ga-ot-hiem-cooky-39462",
            "https://www.cooky.vn/cong-thuc/uc-ga-sot-cam-me-46665"
        },
        
        # Query 3: Canh
        "canh": {
            "https://www.cooky.vn/cong-thuc/canh-bap-cai-cuon-thit-55161",
            "https://www.cooky.vn/cong-thuc/canh-du-du-ham-nam-rom-48084"
        },
        
        # Query 4: Kho
        "kho": {
            "https://www.cooky.vn/cong-thuc/ca-basa-kho-to-3030",
            "https://www.cooky.vn/cong-thuc/lam-thit-kho-tau-don-tet-16508",
            "https://www.cooky.vn/cong-thuc/nam-kho-tieu-chay-24273"
        },
        
        # Query 5: Bún
        "bún": {
            "https://www.cooky.vn/cong-thuc/bun-chay-kieu-hue-20185",
            "https://www.cooky.vn/cong-thuc/bun-moc-nam-48965"
        },
        
        # Query 6: Sườn
        "sườn xào": {
            "https://www.cooky.vn/cong-thuc/suon-xao-chua-ngot-28068?itm_source=home_z1_p5_search&itm_medium=desktop&itm_content=textlink&itm_campaign=010818_Sườn+xào+chua+ngọt"
        },
        
        # Query 7: Cháo
        "cháo": {
            "https://www.cooky.vn/cong-thuc/chao-thit-heo-bi-do-393?itm_source=home_z3_p1_chefrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Cháo+thịt+heo+bí+đỏ"
        },
        
        # Query 8: Bánh
        "bánh": {
            "https://www.cooky.vn/cong-thuc/banh-bong-lan-tra-xanh-bang-noi-com-dien-15298?itm_source=home_z3_p3_chefrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Bánh+bông+lan+trà+xanh+bằng+nồi+cơm+điện"
        },
        
        # Query 9: Xào
        "xào": {
            "https://www.cooky.vn/cong-thuc/suon-xao-chua-ngot-28068?itm_source=home_z1_p5_search&itm_medium=desktop&itm_content=textlink&itm_campaign=010818_Sườn+xào+chua+ngọt",
            "https://www.cooky.vn/cong-thuc/thit-bo-xao-bong-cai-xanh-14611"
        },
        
        # Query 10: Cơm
        "cơm chiên": {
            "https://www.cooky.vn/cong-thuc/com-chien-duong-chau-4014?itm_source=home_z3_p6_chefrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Cơm+chiên+Dương+Châu"
        },
        
        # Query 11: Lẩu
        "lẩu": {
            "https://www.cooky.vn/cong-thuc/lau-ga-ot-hiem-cooky-39462?itm_source=home_z4_p1_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Lẩu+gà+ớt+hiểm"
        },
        
        # Query 12: Smoothie
        "smoothie": {
            "https://www.cooky.vn/cong-thuc/smoothie-xoai-chuoi-kiwi-smoothie-healthy-bowl-50880?itm_source=home_z3_p2_chefrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Smoothie+xoài+chuối+kiwi+-+smoothie+healthy+bowl"
        },
        
        # Query 13: Chay
        "chay": {
            "https://www.cooky.vn/cong-thuc/bun-chay-kieu-hue-20185",
            "https://www.cooky.vn/cong-thuc/nam-kho-tieu-chay-24273",
            "https://www.cooky.vn/cong-thuc/dau-hu-om-rau-nam-chay-48083"
        },
        
        # Query 14: Cà phê
        "cà phê": {
            "https://www.cooky.vn/cong-thuc/latte-art-chuan-barista-55850?itm_source=home_z4_p2_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Latte+Art+Chuẩn+Barista",
            "https://www.cooky.vn/cong-thuc/ca-phe-cold-brew-macchiato-55855?itm_source=home_z4_p6_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Cà+Phê+Cold+Brew+Macchiato",
            "https://www.cooky.vn/cong-thuc/homemade-cappuccino-55849?itm_source=home_z4_p7_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Homemade+Cappuccino"
        },
        
        # Query 15: Sữa chua
        "sữa chua": {
            "https://www.cooky.vn/cong-thuc/cheesecake-dau-sua-chua-55848?itm_source=home_z4_p3_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Cheesecake+Dâu+Sữa+Chua",
            "https://www.cooky.vn/cong-thuc/sua-chua-tran-chau-trai-cay-55755?itm_source=home_z4_p4_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Sữa+Chua+Trân+Châu+Trái+Cây",
            "https://www.cooky.vn/cong-thuc/sua-chua-dao-vai-thach-la-dua-55847?itm_source=home_z4_p5_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Sữa+Chua+Đào+Vải+Thạch+Lá+Dứa"
        },
        
        # Query 16: Thịt
        "thịt": {
            "https://www.cooky.vn/cong-thuc/canh-bap-cai-cuon-thit-55161",
            "https://www.cooky.vn/cong-thuc/chao-thit-heo-bi-do-393?itm_source=home_z3_p1_chefrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Cháo+thịt+heo+bí+đỏ",
            "https://www.cooky.vn/cong-thuc/lam-thit-kho-tau-don-tet-16508?itm_source=home_z4_p8_cookyrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Thịt+Kho+Tàu+Đón+Tết",
            "https://www.cooky.vn/cong-thuc/thit-bo-xao-bong-cai-xanh-14611"
        },
        
        # Query 17: Nấm
        "nấm": {
            "https://www.cooky.vn/cong-thuc/bun-moc-nam-48965",
            "https://www.cooky.vn/cong-thuc/nam-kho-tieu-chay-24273",
            "https://www.cooky.vn/cong-thuc/dau-hu-om-rau-nam-chay-48083",
            "https://www.cooky.vn/cong-thuc/canh-du-du-ham-nam-rom-48084",
            "https://www.cooky.vn/cong-thuc/bi-do-um-nam-50925"
        },
        
        # Query 18: Bò
        "bò": {
            "https://www.cooky.vn/cong-thuc/thit-bo-xao-bong-cai-xanh-14611"
        },
        
        # Query 19: Cá
        "cá": {
            "https://www.cooky.vn/cong-thuc/ca-basa-kho-to-3030?itm_source=home_z3_p5_chefrecipe&itm_medium=desktop&itm_content=recipe&itm_campaign=Cá+basa+kho+tộ"
        },
        
        # Query 20: Đậu hũ
        "đậu hũ": {
            "https://www.cooky.vn/cong-thuc/dau-hu-om-rau-nam-chay-48083"
        }
    }
    
    return test_queries


def main():
    """
    Hàm chính để đánh giá hệ thống
    """
    print("=" * 80)
    print("MODULE 5: ĐÁNH GIÁ HỆ THỐNG")
    print("=" * 80)
    
    # Load dữ liệu
    base_dir = os.path.dirname(os.path.dirname(__file__))
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
    
    # Tạo evaluator
    evaluator = Evaluator(search_engine)
    
    # Tạo test queries
    test_queries = create_test_queries()
    print(f"✅ Đã tạo {len(test_queries)} test queries")
    
    # Đánh giá
    avg_metrics = evaluator.evaluate_all(test_queries)
    
    # In kết quả tổng hợp
    print("\n" + "=" * 80)
    print("📈 KẾT QUẢ ĐÁNH GIÁ TỔNG HỢP:")
    print("=" * 80)
    
    print("\n🎯 Độ chính xác (Precision):")
    print(f"   Avg Precision@5:  {avg_metrics['Avg_Precision@5']:.4f} ({avg_metrics['Avg_Precision@5']*100:.2f}%)")
    print(f"   Avg Precision@10: {avg_metrics['Avg_Precision@10']:.4f} ({avg_metrics['Avg_Precision@10']*100:.2f}%)")
    
    print("\n📊 Độ phủ (Recall):")
    print(f"   Avg Recall@5:     {avg_metrics['Avg_Recall@5']:.4f} ({avg_metrics['Avg_Recall@5']*100:.2f}%)")
    print(f"   Avg Recall@10:    {avg_metrics['Avg_Recall@10']:.4f} ({avg_metrics['Avg_Recall@10']*100:.2f}%)")
    
    print("\n⭐ Chất lượng tổng thể:")
    print(f"   MAP (Mean Average Precision): {avg_metrics['MAP']:.4f} ({avg_metrics['MAP']*100:.2f}%)")
    print(f"   Avg F1@10:                    {avg_metrics['Avg_F1@10']:.4f} ({avg_metrics['Avg_F1@10']*100:.2f}%)")
    
    # Đánh giá kết quả
    print("\n💡 ĐÁNH GIÁ:")
    map_score = avg_metrics['MAP']
    if map_score >= 0.8:
        rating = "Xuất sắc! ⭐⭐⭐⭐⭐"
    elif map_score >= 0.6:
        rating = "Tốt ⭐⭐⭐⭐"
    elif map_score >= 0.4:
        rating = "Khá ⭐⭐⭐"
    elif map_score >= 0.2:
        rating = "Trung bình ⭐⭐"
    else:
        rating = "Cần cải thiện ⭐"
    
    print(f"   Chất lượng hệ thống: {rating}")
    
    # Lưu kết quả
    results_file = os.path.join(base_dir, 'evaluation_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(avg_metrics, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Đã lưu kết quả đánh giá vào: {results_file}")
    
    print("\n✅ MODULE 5 HOÀN THÀNH!")
    print("=" * 80)


if __name__ == "__main__":
    main()
