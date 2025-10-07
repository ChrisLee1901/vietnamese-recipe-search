"""
Script chạy toàn bộ pipeline: Crawler -> Indexing -> Web
"""

import os
import sys
import subprocess


def run_module(module_name, script_path):
    """
    Chạy một module
    """
    print("\n" + "=" * 80)
    print(f"🚀 ĐANG CHẠY: {module_name}")
    print("=" * 80)
    
    try:
        # Chạy script
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,
            text=True
        )
        
        print(f"✅ {module_name} hoàn thành!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy {module_name}: {e}")
        return False


def main():
    """
    Chạy toàn bộ pipeline
    """
    print("=" * 80)
    print("🎯 CHẠY TOÀN BỘ HỆ THỐNG VERTICAL SEARCH ENGINE")
    print("=" * 80)
    
    base_dir = os.path.dirname(__file__)
    
    # Module 1: Crawler
    crawler_script = os.path.join(base_dir, 'module1_crawler', 'crawler.py')
    if not run_module("MODULE 1: Web Crawler", crawler_script):
        print("❌ Pipeline dừng lại do lỗi!")
        return
    
    # Module 2: Indexing
    indexing_script = os.path.join(base_dir, 'module2_indexing', 'text_processor.py')
    if not run_module("MODULE 2: Text Processing & Indexing", indexing_script):
        print("❌ Pipeline dừng lại do lỗi!")
        return
    
    # Module 3: Search (demo)
    search_script = os.path.join(base_dir, 'module3_ranking', 'search_engine.py')
    if not run_module("MODULE 3: Search & Ranking (Demo)", search_script):
        print("⚠️  Module 3 có lỗi nhưng tiếp tục...")
    
    # Module 5: Evaluation
    eval_script = os.path.join(base_dir, 'module5_evaluation', 'evaluate.py')
    if not run_module("MODULE 5: System Evaluation", eval_script):
        print("⚠️  Module 5 có lỗi nhưng tiếp tục...")
    
    print("\n" + "=" * 80)
    print("🎉 ĐÃ HOÀN THÀNH TOÀN BỘ PIPELINE!")
    print("=" * 80)
    
    print("\n📝 BƯỚC TIẾP THEO:")
    print("   1. Kiểm tra dữ liệu trong thư mục 'data/'")
    print("   2. Kiểm tra index trong thư mục 'index/'")
    print("   3. Chạy web server:")
    print("      python module4_web/app.py")
    print("   4. Truy cập: http://localhost:5000")
    
    print("\n📊 Kết quả đánh giá:")
    print("   - Xem file: evaluation_results.json")


if __name__ == "__main__":
    main()
