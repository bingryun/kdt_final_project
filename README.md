# 최종프로젝트 보고서 - 오키도키 1조

# 프로젝트 개요

---

## 프로젝트 주제
대한민국 날씨 및 자연재해 데이터 기반 대시보드 및 시스템 구현

## 목표
- 전국 날씨를 볼 수 있는 대시보드 구현
- 여러 API에서 제공하는 날씨 비교 및 최근 N년 해당일자 날씨 정보 제공
- 특보 발생 현황 및 추이 확인 가능한 대시보드 구현
- 연간 자연재해 발생 횟수 및 자연재해 정보 제공 (홍수, 산불, 지진) 
- 당일 긴급재난문자, 홍수예보, 기상특보 발생 시 Slack 알림 구현
- Airflow dag 성공 여부 log → Slack 알림 구현

## 프로젝트 파이프라인

- Airflow를 통해 API에서 제공하는 데이터를 S3와 Redshift에 저장
- 저장된 데이터를 바탕으로 마트테이블 생성 및 대시보드 연결
- AWS Lambda를 이용한 실시간 데이터 처리 및 슬랙 알림 설정

## ERD


## 활용 기술 및 프레임워크

| 데이터 파이프라인 | Apache Airflow, AWS Lambda |
| --- | --- |
| 데이터 레이크 | AWS S3 |
| 데이터 웨어하우스 | AWS Redshift |
| 데이터 시각화 | Apache Superset, Tableau |
| 데이터 처리 | Python - requests, beautifulsoup4, pandas, AWS Athena |
| CI / CD | Git, GitHub Actions |
| 협업 툴 | AWS, GitHub, Slack, Notion, Gather |

# 프로젝트 세부 사항

---

## 프로젝트 작업 및 타임라인

| 주차별 |           작업 이름           |   상태  |                       담당자                      |               마감일              |
|:------:|:-----------------------------:|:-------:|:-------------------------------------------------:|:---------------------------------:|
| 0주차  | 프로젝트주제선정              | 완료    | 전찬수, 남원우, 손봉호, Yonggu Choi, [3기] 곽도영 | 2024년 7월 10일                   |
| 999    | ERD 작성                      | 보관됨  | 전찬수, 남원우, 손봉호, Yonggu Choi, [3기] 곽도영 | 2024년 7월 10일 → 2024년 7월 19일 |
| 999    | API 문서화                    | 보관됨  | 전찬수, 남원우, 손봉호, Yonggu Choi, [3기] 곽도영 | 2024년 7월 10일 → 2024년 7월 19일 |
| 999    | 대시보드 설계                 | 보관됨  | 전찬수, 남원우, 손봉호, Yonggu Choi, [3기] 곽도영 | 2024년 7월 15일 → 2024년 7월 17일 |
| 999    | 아키텍처 및 파이프라인 설계   | 보관됨  | 전찬수, 남원우, 손봉호, [3기] 곽도영, Yonggu Choi | 2024년 7월 15일 → 2024년 7월 17일 |
| 1주차  | 중기예보                      | 완료    | 전찬수                                            | 2024년 7월 17일 → 2024년 7월 21일 |
| 1주차  | 하천 수위 및 강수량           | 완료    | Yonggu Choi                                       | 2024년 7월 17일 → 2024년 7월 23일 |
| 1주차  | 자연재해 발생횟수             | 완료    | 남원우                                            | 2024년 7월 17일 → 2024년 7월 21일 |
| 1주차  | 단기예보 (날씨)               | 완료    | 손봉호                                            | 2024년 7월 17일 → 2024년 7월 22일 |
| 1주차  | 기상 특보                     | 완료    | [3기] 곽도영                                      | 2024년 7월 20일 → 2024년 7월 22일 |
| 1주차  | 지진발생위치 / 산불위험지수   | 완료    | 남원우                                            | 2024년 7월 21일 → 2024년 7월 23일 |
| 1주차  | AWS 환경 구성                 | 완료    | [3기] 곽도영                                      | 2024년 7월 17일 → 2024년 7월 19일 |
| 2주차  | 중기예보                      | 완료    | 전찬수                                            | 2024년 7월 22일 → 2024년 7월 25일 |
| 2주차  | (대시보드)중기예보            | 완료    | 전찬수                                            | 2024년 7월 24일 → 2024년 7월 29일 |
| 2주차  | 기상 특보                     | 완료    | [3기] 곽도영                                      | 2024년 7월 23일 → 2024년 7월 29일 |
| 2주차  | 하천 수위 및 강수량           | 완료    | Yonggu Choi                                       | 2024년 7월 24일 → 2024년 7월 27일 |
| 2주차  | 단기예보                      | 완료    | 손봉호                                            | 2024년 7월 22일 → 2024년 7월 28일 |
| 2주차  | (대시보드)하천 수위 및 강수량 | 완료    | Yonggu Choi                                       | 2024년 7월 24일 → 2024년 7월 29일 |
| 2주차  | (대시보드)단기예보            | 완료    | 손봉호                                            | 2024년 7월 24일 → 2024년 7월 28일 |
| 2주차  | 긴급재난문자 알리미           | 완료    | 손봉호                                            | 2024년 7월 28일 → 2024년 7월 30일 |
| 2주차  | (대시보드)자연재해 발생횟수   | 완료    | 남원우                                            | 2024년 7월 24일 → 2024년 7월 28일 |
| 2주차  | (대시보드)기상특보            | 완료    | [3기] 곽도영                                      | 2024년 7월 29일 → 2024년 7월 30일 |
| 3주차  | CI/CD 자동화 & 테스트         | 완료    | 전찬수, 남원우, 손봉호, Yonggu Choi, [3기] 곽도영 | 2024년 7월 29일 → 2024년 7월 31일 |
| 3주차  | Airflow → SNS                 | 완료    | 전찬수                                            | 2024년 7월 29일 → 2024년 8월 4일  |
| 3주차  | 홍수 예보                     | 완료    | Yonggu Choi                                       | 2024년 7월 29일 → 2024년 7월 30일 |
| 3주차  | 기상특보알림                  | 완료    | [3기] 곽도영                                      | 2024년 7월 30일 → 2024년 8월 1일  |
| 3주차  | 지역구분 세분화               | 완료    | 남원우                                            | 2024년 7월 30일 → 2024년 7월 31일 |
| 3주차  | Airflow 모니터링 도구         | 완료    | 손봉호                                            | 2024년 7월 30일 → 2024년 8월 3일  |
| 3주차  | 통일화                        | 완료    | [3기] 곽도영                                      | 2024년 8월 2일 → 2024년 8월 4일   |
| 3주차  | Airflow 서버 분산             | 완료    | Yonggu Choi                                       | 2024년 8월 1일 → 2024년 8월 5일   |
| 3주차  | 지진관련 재난문자 처리        | 완료    | 남원우                                            | 2024년 7월 31일 → 2024년 8월 5일  |
| 4주차  | 마무리 작업                   | 진행 중 | 전찬수, 남원우, 손봉호, Yonggu Choi, [3기] 곽도영 | 2024년 8월 5일 → 2024년 8월 19일  |
| 4주차  | 보고서 및 발표자료 작성       | 진행 중 | 전찬수, 남원우, 손봉호, [3기] 곽도영, Yonggu Choi | 2024년 8월 5일 → 2024년 8월 19일  |


# 팀원 및 역할

---

| 팀원 | 역할 |
| --- | --- |
| 곽도영 | 과거/ 현재 기상 특보, AWS 환경 생성 |
| 남원우 | 연간 자연 재해, 산불 지수, 24년 지진 정보 |
| 손봉호 | 단기 예보, 긴급 재난 문자 알림, Airflow 모니터링 시도 |
| 전찬수 | 중기 예보, API 별 날씨 비교 , CI/CD git action , airflow log → sns 알림 |
| 최용구 | 자연 재해 - 홍수 예보, 하천, 강수량 / AWS Infra 구축 보조 / Airflow 서버 분산 시도 |

# 프로젝트 결과

---

## Superset

### Tab 1. 날씨

종합

온도 예측

강수확률 예측

- 해당 일자의 온도 및 강수확률 맵차트
    - (06, 12, 18시 업데이트) // 진한 색상 → 강수확률 및 온도 높음

예상 날씨 정보

- 시도별 시청, 도청 위치의 온도, 강수 확률 및 날씨 정보 예측 테이블
    - (06, 12, 18시 업데이트)

긴급재난문자 최근 50건

- 해당 일자 긴급 재난 문자 최근 50건 테이블
    - 새로운 데이터 있을 때 마다 업데이트 (최소 3분)

- 중기기온, 육상 정보를 합쳐 테이블 시각화

- 최근 4년간 오늘의 날씨 정보

- 5년간 기상특보별 통계 자료

- 연간 특보 비율 정보

- 중기기온, 육상 정보를 합쳐 기온, 강수확률 정보를 시각화

- 기상청과 weatherAPI 예보 비교

- 현재 시도별 폭염 특보 지역수

- 계절별 특보 추이

### Tab 2. 자연재해

**종합**

**세부 설명 (홍수)**

- 2024년 기준 각 지역별 1회 이상 홍수 예보 지역에 대한 가장 최신 예보 표시

- 2024년 기준 홍수 예보 전체 목록 표시

**세부 설명 (수위)**

- 각 하천별 상태별 절대 기준 수위를 상대 수위 비율로 환산하여 개수 표시
    - 관심 수위(attn_count): 20% 이상
    - 경계 수위(warn_count): 50% 이상
    - 위험 수위(danger_count): 80% 이상

- 하천 수위 세부 현황 (20% 이상)
  - 좌측 개수에 해당하는 세부 하천 목록 표시

- 오늘자 기준 하천별 수위 현황 표시

**세부 설명 (강수량)**

- 오늘 기준 하천 관측소 기준 강수량에 대한 시도별 평균 표시

- 좌측 지도 표시 데이터에 대한 세부 평균 표시

- 5년간 자연재해별 발생횟수
- 24년 데이터는 주기적으로 최신화
    - 산사태는 데이터 없음

- 24년 국내에서 발생한 지진 정보
    - 긴급재난문자에 지진 키워드 포함시 업데이트

- 가장 최근에 저장된 산불지수 데이터
    - 3시간 간격 업데이트
- 시군구단위 평균산불지수 데이터를 이용iso 코드에따라 시도 단위로 표현
    - 검은색에 가까울수록 높음

## Tableau

- 곽도영    
    - 계절별 특보 발생 빈도수 비교 막대 그래프
    - 시군구 단위의 현재 특보 현황 지도(5분단위 업데이트)
        - 특보 종류 : 강풍, 호우, 한파, 건조, 해일, 지진해일, 풍랑, 태풍, 대설,황사, 폭염, 안개
    - 특보 해제 예고 시간 리스트 (5분 단위 업데이트)
- 남원우
    - 태블로의 기능을 이용하여 시군구 단위의 구역으로 산불지수차트 표현
- 손봉호
    - Apache Superset과 같은 정보지만 더 세세한 지역별(시군구) 온도 및 강수 확률을 보여줄 수 있음
        - 매일 06,12,18시 업데이트
    - 시도별 시청, 도청 위치의 온도, 강수 확률 및 날씨 정보 예측 테이블
        - (06, 12, 18시 업데이트)
    - 해당 일자의 긴급재난문자 최근 20건 테이블

- 전찬수
    - 매개변수를 통해서 차트들의 지역 필터링함
    - 중기기온, 육상정보를 수집하여 필터링된 지역의 최저기온, 최고기온 시각화
    - 중기기온, 육상정보를 수집하여 필터링된 지역의 최저기온, 최고기온, 구름정보, 강수정보, 강수확률을 테이블로 정보 제공
    - 과거 4년간 오늘의 날씨 정보 제공 (20200806, 20210806, 20220806, 20230806)
    - 기상청과 weatherAPI의 예보 정보 (최고기온, 최저기온)을 비교하여 차트로 제공

- 최용구
    - 홍수
      - 홍수 예보 발령 현황
        - 홍수 예보는 Superset과 동일하게 1회 이상 예보 발표된 곳에 대해 가장 최신 정보만 표시
      - 2024년 홍수 예보 전체 목록
    - 하천 수위
        - 하천 수위 개황
        - 하천 수위 세부 현황 (20% 이상)
        - 하천별 수위 세부 현황 (오늘 기준)
            - 우측에 원 크기에 대한 상대 수위 비율 표시, 색깔별 범례 표시
    - 강수량
      - 하천 관측소 기준 강수량 시도별 평균 (오늘) - 지도 표시
      - 하천 관측소 기준 강수량 시도별 평균

## Slack 알림

### 긴급재난문자
  - 3분 단위로 api를 호출하여 새로운 긴급재난문자 발생 시 Slack 알림 발송

### 홍수예보

### 기상특보

### Airflow log 알림


# Trial & Error
