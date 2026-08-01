import json
import time
import sys
import os

# Add scripts folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from retrieval import search_legal

# Perfect 15 Test Cases (Optimized for Document Filtering)
test_cases = [
    # --- CONSTITUTION (5 Questions) ---
    {"id": 1, "category": "Direct", "question": "What does the constitution say about equality before the law?", "expected": "Article 25", "doc": "Constitution"},
    {"id": 2, "category": "Direct", "question": "What is the right to freedom of expression in the constitution?", "expected": "Article 29", "doc": "Constitution"},
    {"id": 3, "category": "Paraphrased", "question": "Are all citizens treated the same by the courts in the constitution?", "expected": "Article 25", "doc": "Constitution"},
    {"id": 4, "category": "Amharic", "question": "በሕገ መንግሥት የእኩልነት መብት ምንድነው?", "expected": "Article 25", "doc": "Constitution"},
    {"id": 5, "category": "Cross-Language", "question": "What does the constitution say about ግል ሕይወት (privacy)?", "expected": "Article 26", "doc": "Constitution"},
    
    # --- FAMILY CODE (4 Questions) ---
    {"id": 6, "category": "Direct", "question": "What are the essential conditions for a valid marriage in the family code?", "expected": "Article 6", "doc": "Family Code"},
    {"id": 7, "category": "Direct", "question": "What does the family code say about prohibited relatives (ርክርክ)?", "expected": "Article 8", "doc": "Family Code"},
    {"id": 8, "category": "Article-Number", "question": "What is article 6 in the family code?", "expected": "Article 6", "doc": "Family Code"},
    {"id": 9, "category": "Amharic", "question": "በቤተሰብ ሕግ የጋብቻ ውጤቶች ምን ምን ናቸው?", "expected": "Article 47", "doc": "Family Code"},
    
    # --- CIVIL CODE (3 Questions) ---
    {"id": 10, "category": "Article-Number", "question": "What is article 4 in the civil code?", "expected": "Article 4", "doc": "Civil Code"},
    {"id": 11, "category": "Direct", "question": "What is the legal definition of a contract in the civil code?", "expected": "Article 1675", "doc": "Civil Code"},
    {"id": 12, "category": "Paraphrased", "question": "How does the civil code define ownership and property rights?", "expected": "Article 1204", "doc": "Civil Code"},
    
    # --- UNSUPPORTED (2 Questions) ---
    {"id": 13, "category": "Unsupported", "question": "How do I file for a divorce in Addis Ababa?", "expected": "N/A", "doc": "N/A"},
    {"id": 14, "category": "Unsupported", "question": "Can you help me hire a lawyer for tax evasion?", "expected": "N/A", "doc": "N/A"},
    
    # --- ADDITIONAL CONSTITUTION (1 Question) ---
    {"id": 15, "category": "Direct", "question": "Explain the right to life in the constitution.", "expected": "Article 14", "doc": "Constitution"}
]

print("\n" + "="*80)
print("STARTING COMPREHENSIVE RETRIEVAL EVALUATION (Constitution, Civil, Family)")
print("="*80)

hits = 0
mrr_sum = 0.0
detailed_results = []

for test in test_cases:
    print(f"\n[Test {test['id']}/15] Category: {test['category']} | Target Doc: {test.get('doc', 'Any')}")
    print(f"Question: {test['question']}")
    print(f"Expected: {test['expected']}")
    print("-" * 40)
    
    start_time = time.time()
    response = search_legal(test["question"])
    latency = time.time() - start_time
    
    retrieved_articles = [res.get("article", "") for res in response.get("results", [])]
    print(f"Retrieved Top-3: {retrieved_articles}")
    
    is_hit = False
    hit_rank = -1
    
    if test["expected"] == "N/A":
        if not retrieved_articles:
            is_hit = True
            hit_rank = 1
    else:
        for i, art in enumerate(retrieved_articles):
            if test["expected"].lower() in art.lower():
                is_hit = True
                hit_rank = i + 1
                break
                
    if is_hit:
        print(f"✅ HIT! Rank: {hit_rank} (Latency: {latency:.2f}s)")
        hits += 1
        mrr_sum += 1.0 / hit_rank
    else:
        print(f"❌ MISS! (Latency: {latency:.2f}s)")
        
    detailed_results.append({
        "id": test["id"],
        "question": test["question"],
        "expected": test["expected"],
        "retrieved": retrieved_articles,
        "hit": is_hit,
        "rank": hit_rank,
        "latency": round(latency, 2)
    })

hit_rate = (hits / len(test_cases)) * 100
mrr = mrr_sum / len(test_cases)

print("\n" + "="*80)
print("EVALUATION METRICS SUMMARY")
print("="*80)
print(f"Total Questions : {len(test_cases)}")
print(f"Hits            : {hits}")
print(f"Hit Rate @ 3    : {hit_rate:.2f}%")
print(f"MRR (Mean Reciprocal Rank) : {mrr:.4f}")
print("="*80)

# Save detailed results
results_path = os.path.join(os.path.dirname(__file__), 'evaluation_results_v2.json')
with open(results_path, "w", encoding="utf-8") as f:
    json.dump(detailed_results, f, ensure_ascii=False, indent=4)
print(f"Detailed results saved to '{results_path}'")