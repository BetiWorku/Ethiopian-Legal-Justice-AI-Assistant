import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import retrieval


def test_search_returns_structured_results():
    response = retrieval.search_legal(
        "What does Ethiopian law say about equality before the law?",
        top_k=3,
        language="am",
    )

    assert response["results"], "expected at least one retrieval result"
    assert response["results"][0]["payload"]["text"]
    assert response["results"][0]["payload"]["article"]
    assert "25" in str(response["results"][0]["payload"]["article"]), (
        "expected the top result to be Article 25 for an equality-before-the-law query"
    )


def test_unknown_pages_are_rendered_as_not_available():
    result = retrieval._normalize_result(
        {
            "article": "Article 25",
            "title": "የእኩልነት መብት",
            "page": "Unknown",
            "text": "sample text",
        },
        1.0,
        source="faiss",
    )

    assert result["payload"]["pages"] == ""


def test_article_number_queries_return_the_matching_article():
    response = retrieval.search_legal("what is article 16", top_k=3, language="am")

    assert response["results"], "expected article 16 to return a result"
    assert "16" in str(response["results"][0]["payload"]["article"])
