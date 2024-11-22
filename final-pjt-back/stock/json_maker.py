import json

interests_list = [
    "핀테크", "언택트경제", "게임월드", "카리스마창업자", "자율주행차", 
    "컨텐츠강자", "신나는 드라이빙", "이번 휴가는 어디?", "가상현실(VR)", 
    "메타버스 구현", "인공지능", "클라우드", "항공우주&방위산업", "통신", 
    "프랜차이즈", "스트리밍의 시대", "어디 옷이야?", "리튬&배터리", "반도체", 
    "플랫폼 대표주자", "건물주의 꿈", "클린 에너지", "갈증해소", "소비/원자재", 
    "자원/에너지", "소셜미디어", "블록체인", "리테일/유통", "사물인터넷(IOT)", 
    "반려동물", "뷰티의 세계"
]

# fixture 데이터 생성
interests_fixture = [
    {
        "model": "stock.industrycode",  # 앱이름.모델이름
        "pk": idx + 1,
        "fields": {
            "name": interest
        }
    }
    for idx, interest in enumerate(interests_list)
]

# JSON 파일로 저장
with open('interests.json', 'w', encoding='utf-8') as f:
    json.dump(interests_fixture, f, ensure_ascii=False, indent=2)