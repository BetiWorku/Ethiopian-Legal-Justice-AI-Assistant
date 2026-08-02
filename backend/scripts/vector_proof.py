import numpy as np
from sentence_transformers import SentenceTransformer


print("Loading E5 model...")

model = SentenceTransformer("intfloat/multilingual-e5-base")



def calculate_math_similarity():

    print("\n" + "="*60)
    print("🧮 MATH PROOF: How Computer Matches Meaning (Cosine Similarity)")
    print("="*60)


    # 1. User's question (Query)
    user_question = "query: What is equality before the law?"


    # 2. Relevant legal article (Article 25)
    article_25_text = (
        "passage: Article 25: All persons are equal before the law "
        "and are entitled without any discrimination to the equal protection of the law."
    )


    # 3. Different legal article for comparison (Article 4)
    article_4_text = (
        "passage: Article 4: Courts to try suits unless barred."
    )


    # 4. Convert texts into 768-dimensional numerical vectors
    print("\nConverting texts to 768-dimensional vectors...")


    vec_question = model.encode(
        user_question,
        normalize_embeddings=True
    )


    vec_article_25 = model.encode(
        article_25_text,
        normalize_embeddings=True
    )


    vec_article_4 = model.encode(
        article_4_text,
        normalize_embeddings=True
    )



    # 4.1 Display vector dimensions and index values
    print("\n" + "="*60)
    print("VECTOR INFORMATION")
    print("="*60)


    print(f"Question Vector Dimension: {len(vec_question)}")
    print(f"Article 25 Vector Dimension: {len(vec_article_25)}")
    print(f"Article 4 Vector Dimension: {len(vec_article_4)}")


    print("\nThe vector contains indexes from 0 to 767")
    print("Total numerical values: 768")


    # Display first 10 values of each vector
    print("\n" + "-"*60)
    print("QUESTION VECTOR (First 10 Values)")
    print("-"*60)


    for i, value in enumerate(vec_question[:10]):
        print(f"Index [{i}]: {value:.6f}")


    print("\n" + "-"*60)
    print("ARTICLE 25 VECTOR (First 10 Values)")
    print("-"*60)


    for i, value in enumerate(vec_article_25[:10]):
        print(f"Index [{i}]: {value:.6f}")


    print("\n" + "-"*60)
    print("ARTICLE 4 VECTOR (First 10 Values)")
    print("-"*60)


    for i, value in enumerate(vec_article_4[:10]):
        print(f"Index [{i}]: {value:.6f}")


    print("\n... Remaining values continue until Index [767]")



    # 5. Calculate Cosine Similarity
    #
    # Because vectors are normalized,
    # cosine similarity is calculated using dot product.
    #
    # Higher score means the meanings are more similar.

    similarity_25 = np.dot(
        vec_question,
        vec_article_25
    )


    similarity_4 = np.dot(
        vec_question,
        vec_article_4
    )



    # 6. Display similarity calculation results

    print("\n" + "="*60)
    print("RESULTS (Cosine Similarity Scores)")
    print("="*60)


    print(f"User Question:")
    print(user_question)


    print("-"*60)


    print(
        f"Similarity with Article 25 (Equality): "
        f"{similarity_25:.4f} "
        f"({similarity_25 * 100:.2f}%)"
    )


    print(
        f"Similarity with Article 4 (Courts):    "
        f"{similarity_4:.4f} "
        f"({similarity_4 * 100:.2f}%)"
    )


    print("="*60)



    # 7. Explanation of vector search

    print("\n💡 EXPLANATION FOR DEMO:")

    print(
        "1. The computer does not directly understand legal words."
    )

    print(
        "2. The multilingual-e5-base model converts each text into "
        "a vector containing 768 numerical values."
    )

    print(
        "3. Each index represents one mathematical feature of the text meaning."
    )

    print(
        "4. The system compares the question vector with legal article "
        "vectors using Cosine Similarity."
    )

    print(
        "5. Article 25 receives a higher similarity score because its "
        "meaning is closer to the user's question."
    )



if __name__ == "__main__":

    calculate_math_similarity()