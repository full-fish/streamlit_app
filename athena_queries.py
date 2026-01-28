# athena_queries.py
from athena_client import athena_read, quote_list


SQL_ALL_PRODUCTS = """
SELECT
product_id,
product_name,
brand,
category,
category_path,
path,
price,
delivery_type,
product_url,
skin_type,
top_keywords,
avg_rating_with_text,
avg_rating_without_text,
text_review_ratio,
total_reviews,
rating_1,
rating_2,
rating_3,
rating_4,
rating_5,
product_vector_roberta_sentiment,
representative_review_id_roberta_sentiment,
representative_similarity_roberta_sentiment,
product_vector_roberta_semantic,
representative_review_id_roberta_semantic,
representative_similarity_roberta_semantic,
sentiment_score
FROM coupang_db.integrated_products_final_v2
"""


def fetch_all_products():
    return athena_read(SQL_ALL_PRODUCTS)


def fetch_reviews_by_product(product_id: str):
    pid = str(product_id).replace("'", "''")
    sql = f"""
    SELECT
    category,
    product_id,
    id,
    full_text,
    title,
    content,
    has_text,
    score,
    label,
    tokens,
    char_length,
    token_count,
    date,
    collected_at,
    nickname,
    has_image,
    helpful_count,
    sentiment_score,
    roberta_sentiment,
    roberta_semantic
    FROM coupang_db.partitioned_reviews_v2
    WHERE product_id = '{pid}'
    ORDER BY date DESC
    """
    return athena_read(sql)


def search_products_flexible(categories, skin_types, min_rating, max_rating, min_price, max_price, limit=None):
    """
    categories/skin_types가 비어있으면 해당 조건은 WHERE에서 제거(=전체 허용)
    """
    where_parts = ["1=1"]

    if categories:
        categories_in = quote_list(categories)
        where_parts.append(f"category IN ({categories_in})")

    if skin_types:
        skin_types_in = quote_list(skin_types)
        where_parts.append(
            f"""
            (
              CASE
                WHEN skin_type LIKE '복합/혼합%' THEN '복합/혼합'
                ELSE skin_type
              END
            ) IN ({skin_types_in})
            """.strip()
        )

    where_parts.append(f"avg_rating_with_text BETWEEN {float(min_rating)} AND {float(max_rating)}")
    where_parts.append(f"price BETWEEN {int(min_price)} AND {int(max_price)}")

    where_sql = "\n  AND ".join(where_parts)

    limit_sql = f"\nLIMIT {int(limit)}" if limit else ""

    sql = f"""
    SELECT
      product_id,
      product_name,
      brand,
      category,
      price,
      skin_type,
      total_reviews,
      avg_rating_with_text,
      rating_1,
      rating_2,
      rating_3,
      rating_4,
      rating_5,
      sentiment_score,
      top_keywords,
      product_url
    FROM coupang_db.integrated_products_final_v2
    WHERE {where_sql}
    ORDER BY total_reviews DESC, avg_rating_with_text DESC
    {limit_sql}
    """
    return athena_read(sql)
