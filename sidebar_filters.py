import streamlit as st

# 평점 범위 선택 슬라이더
def render_rating_slider(min_val=1.0, max_val=5.0, default=(3.0, 5.0)):
    st.sidebar.subheader("평점")
    min_rating, max_rating = st.sidebar.slider(
        "평점 범위",
        # 최소 평점
        min_value=min_val,
        # 최대 평점
        max_value=max_val,
        # 초기 선택 값
        value=default,
        step=0.1
    )
    return min_rating, max_rating

# 평점 범위 조건에 따라 해당 상품 필터링
def filter_by_rating(df, min_rating, max_rating):
    return df[(df["score"] >= min_rating) & (df["score"] <= max_rating)]