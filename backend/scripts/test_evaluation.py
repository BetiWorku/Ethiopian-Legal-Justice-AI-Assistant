import sys
import os
import json
import re

# Add the scripts directory to the path to import from retrieval.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from retrieval import search_legal

# The 15 Test Questions
test_questions = [
    {"id": 1, "category": "Direct", "question": "What does Ethiopian law say about equality before the law?", "expected": "Article 25"},
    {"id": 2, "category": "Direct", "question": "What is the right to freedom of expression?", "expected": "Article 29"},
    {"id": 3, "category": "Direct", "question": "Explain the right to life.", "expected": "Article 14"},
    {"id": 4, "category": "Direct", "question": "What does the constitution say about privacy?", "expected": "Article 26"},
    {"id": 5, "category": "Direct", "question": "What are the rights of the accused?", "expected": "Article 20"},
    {"id": 6, "category": "Paraphrased", "question": "Are all citizens treated the same by the courts?", "expected": "Article 25"},
    {"id": 7, "category": "Paraphrased", "question": "Can I speak my mind freely without government interference?", "expected": "Article 29"},
    {"id": 8, "category": "Paraphrased", "question": "Does the state protect my personal information and home?", "expected": "Article 26"},
    {"id": 9, "category": "Article-Number", "question": "What is article 25?", "expected": "Article 25"},
    {"id": 10, "category": "Article-Number", "question": "Show me article 29.", "expected": "Article 29"},
    {"id": 11, "category": "Broad-Topic", "question": "What are the fundamental human rights provisions?", "expected": "Chapter 3 (e.g., Art 14-28)"},
    {"id": 12, "category": "Broad-Topic", "question": "How is the government structured under the constitution?", "expected": "Chapter 4 (e.g., Art 45-61)"},
    {"id": 13, "category": "Amharic", "question": "የእኩልነት መብት ምንድነው?", "expected": "Article 25"},
    {"id": 14, "category": "Cross-Language", "question": "What does Ethiopian law say about ግል ሕይወት (privacy)?", "expected": "Article 26"},
    {"id": 15, "category": "Unsupported", "question": "How do I file for a divorce in Addis Ababa?", "expected": "N/A (No Result)"}
]

def extract_article_num(article_str):
    """Extracts the integer from 'Article 25' or 'Art 45-61'"""
    # Look for "Art X" or "Article X" in strings like "Chapter 4 (e.g., Art 45-61)"
    match = re.search(r'(?:Art|Article)\s*(\d+)', article_str, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Fallback to any number if 'Art' isn't found
    match = re.search(r'\d+', article_str)
    return int(match.group()) if match else None

def run_evaluation():
    print("=" * 80)
    print("STARTING RETRIEVAL EVALUATION (15 QUESTIONS)")
    print("=" * 80)
    
    hits = 0
    mrr_sum = 0.0
    results_log = []

    for i, test in enumerate(test_questions, 1):
        print(f"\n[Test {i}/15] Category: {test['category']}")
        print(f"Question: {test['question']}")
        print(f"Expected: {test['expected']}")
        print("-" * 40)
        
        # Call the search function from retrieval.py
        response = search_legal(test['question'], top_k=3)
        
        retrieved_articles = [res['article'] for res in response.get('results', [])]
        print(f"Retrieved Top-3: {retrieved_articles}")
        
        # Calculate Hit Rate and MRR
        rank = 0
        is_hit = False
        
        if test['expected'] == "N/A (No Result)":
            # If expected is N/A, a hit means the system returned no results
            if not retrieved_articles:
                is_hit = True
                rank = 1
        else:
            # Check for exact match or range match (for Chapter questions)
            expected_art_num = extract_article_num(test['expected'])
            
            for idx, art in enumerate(retrieved_articles, 1):
                if test['expected'] in art:
                    is_hit = True
                    rank = idx
                    break
                
                # Handle Broad Topics (e.g., Chapter 3 -> Art 14-28)
                if "Chapter" in test['expected'] and expected_art_num:
                    retrieved_num = extract_article_num(art)
                    # Check if retrieved article falls within the expected chapter range
                    # Chapter 3 is 14-28 (Range: 14 to 14+14=28)
                    # Chapter 4 is 45-61 (Range: 45 to 45+16=61)
                    range_offset = 16 if "Chapter 4" in test['expected'] else 14
                    if retrieved_num and retrieved_num >= expected_art_num and retrieved_num <= expected_art_num + range_offset:
                        is_hit = True
                        rank = idx
                        break
        
        if is_hit:
            hits += 1
            mrr_sum += (1.0 / rank)
            print(f"✅ HIT! Rank: {rank}")
        else:
            print(f"❌ MISS!")
            
        results_log.append({
            "id": i,
            "category": test['category'],
            "question": test['question'],
            "expected": test['expected'],
            "retrieved": retrieved_articles,
            "hit": is_hit,
            "rank": rank
        })

    # Final Metrics Calculation
    hit_rate = (hits / len(test_questions)) * 100
    mrr = mrr_sum / len(test_questions)
    
    print("\n" + "=" * 80)
    print("EVALUATION METRICS SUMMARY")
    print("=" * 80)
    print(f"Total Questions : 15")
    print(f"Hits            : {hits}")
    print(f"Hit Rate @ 3    : {hit_rate:.2f}%")
    print(f"MRR (Mean Reciprocal Rank) : {mrr:.4f}")
    print("=" * 80)
    
    # Save results to JSON for the report
    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "metrics": {
                "hit_rate": hit_rate,
                "mrr": mrr
            },
            "details": results_log
        }, f, ensure_ascii=False, indent=4)
    print("\nDetailed results saved to 'evaluation_results.json'")

if __name__ == "__main__":
    run_evaluation()