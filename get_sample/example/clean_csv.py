import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('bugs_chart.csv')

# 데이터 정리 함수
def clean_text(text):
    # 불필요한 공백과 줄바꿈 제거
    text = text.replace('\n', '').replace('\r', '').strip()
    # 양쪽의 따옴표 제거
    text = text.strip('"')
    return text

# 데이터프레임의 모든 셀에 대해 정리 함수 적용
df = df.applymap(clean_text)

# 정리된 데이터프레임을 다시 CSV 파일로 저장
df.to_csv('bugs_chart_cleaned.csv', index=False)
print("정리된 CSV 파일 저장 완료: bugs_chart_cleaned.csv")
