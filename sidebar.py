import streamlit as st

# 사이드바 함수
def sidebar(df):
    st.sidebar.header("검색 조건")

    # 카테고리
    st.sidebar.subheader("카테고리")

    selected_sub_cat = []

    for main_cat in df["main_category"].unique():
        with st.sidebar.expander(main_cat, expanded=False):
            sub_cats = (df[df["main_category"] == main_cat]["sub_category"].unique().tolist())
            all_key = f"all_{main_cat}"
            all_checked = st.checkbox("전체 선택", key=all_key)

            for sub in sub_cats:
                sub_key = f"sub_{main_cat}_{sub}"

                # 전체 선택
                if all_checked:
                    st.session_state[sub_key] = True
                # 전체 선택 해제
                elif all_key in st.session_state and not st.session_state[all_key]:
                    st.session_state.setdefault(sub_key, False)

                checked = st.checkbox(sub, key=sub_key)

                if checked:
                    selected_sub_cat.append(sub)

    st.sidebar.caption(f"선택된 카테고리: {len(selected_sub_cat)}개")

    # 피부 타입
    st.sidebar.subheader("피부 타입")

    selected_skin = []

    for skin in df["skin_type"].unique():
        if st.sidebar.checkbox(skin, key=f"skin_{skin}"):
            selected_skin.append(skin)    

    # 평점 슬라이더
    st.sidebar.subheader("평점")
    min_rating, max_rating = st.sidebar.slider(
        "평점 범위",
        # 최소 평점
        min_value=1.0,
        # 최대 평점
        max_value=5.0,
        # 초기 선택 값
        value=(3.0, 5.0),
        step=0.1
    )

    return selected_sub_cat, selected_skin, min_rating, max_rating

# 필터링 함수
def product_filter(df, search_text, selected_sub_cat, selected_skin, min_rating, max_rating):
    filtered_df = df.copy()

    # 검색어 조건
    if search_text is not None:
        filtered_df = filtered_df[filtered_df["product"].str.contains(search_text, case=False)]

    # 카테고리 필터
    if selected_sub_cat:
        filtered_df = filtered_df[filtered_df["sub_category"].isin(selected_sub_cat)]

    # 피부 타입 필터
    if selected_skin:
        filtered_df = filtered_df[filtered_df["skin_type"].isin(selected_skin)]

    # 평점 필터
    filtered_df = filtered_df[(df["score"] >= min_rating) & (df["score"] <= max_rating)]

    # 평점 기준 정렬
    filtered_df = filtered_df.sort_values(by="score", ascending=False)

    return filtered_df