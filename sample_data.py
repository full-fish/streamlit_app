import random
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    products = [
    "닥터알파 수분 장벽 크림",
    "라포레 진정 시카 크림",
    "더마큐어 세라마이드 크림",
    "하이드라랩 딥모이스트 크림",
    "바이오힐 보습 리페어 크림",
    "에스트라 아토베리어 크림",
    "라운드랩 자작나무 수분크림",
    "피지오겔 데일리 모이스처 크림",

    "라운드랩 독도 토너",
    "아누아 어성초 77 토너",
    "닥터지 그린 마일드 토너",
    "마녀공장 비피다 토너",
    "아이오페 더마 리페어 토너",
    "에스트라 아토베리어 토너",

    "마녀공장 갈락토미 에센스",
    "아이오페 비타민 C 세럼",
    "이니스프리 그린티 씨드 세럼",
    "토리든 다이브인 저분자 세럼",
    "닥터지 레드 블레미쉬 앰플",
    "라로슈포제 히알루 B5 세럼",

    "라운드랩 약산성 클렌징폼",
    "닥터지 그린 딥 포밍 클렌저",
    "에스트라 약산성 클렌저",
    "토리든 밸런스 클렌징 폼",
    "마녀공장 퓨어 클렌징 오일",
    "센텔리안24 마데카 클렌저",
    ]

    main_categories = {
        "스킨케어": ["크림", "토너", "에센스", "세럼"],
        "클렌징": ["폼클렌저", "오일", "워터"]
    }

    sub_categories = {
        "크림": ["보습", "장벽강화", "진정"],
        "토너": ["수분공급", "피부결정돈", "진정"],
        "에센스": ["광채", "미백", "탄력"],
        "세럼": ["미백", "주름개선", "보습"],
        "클렌저": ["세정", "저자극", "피지관리"],
    }

    skin_types = ["건성", "지성", "복합성", "민감성"]

    rows = []

    for idx, product in enumerate(products):
        if "크림" in product:
            main_cat = "스킨케어"
            sub_cat = "크림"
        elif "토너" in product:
            main_cat = "스킨케어"
            sub_cat = "토너"
        elif "에센스" in product or "앰플" in product or "세럼" in product:
            main_cat = "스킨케어"
            sub_cat = "세럼"
        else:
            main_cat = "클렌징"
            sub_cat = "폼클렌저"

        score = round(random.uniform(1.0, 5.0), 2)
        brand = product.split()[0]
        price = random.randint(15000, 45000)
        image_url = f"https://tr.rbxcdn.com/180DAY-981c49e917ba903009633ed32b3d0ef7/420/420/Hat/Webp/noFilter"

        # 추천뱃지 기준(지금은 평점으로 해뒀고 추후에 수정해야 함)
        if score >= 4.7:
            badge = "BEST"
        elif score >= 4.3:
            badge = "추천"
        else:
            badge = ""

        rows.append({
            "product_id" : idx + 1,
            "product": product,
            "brand" : brand,
            "price" : price,
            "image_url": image_url,
            "main_category": main_cat,
            "sub_category": sub_cat,
            "skin_type": random.choice(skin_types),
            "keyword": random.choice(sub_categories.get(sub_cat, ["보습"])),
            "score": score,
            "badge": badge
        })

    return pd.DataFrame(rows)
