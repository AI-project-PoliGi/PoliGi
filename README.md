![Group 1](https://github.com/jaehee831/gist-policy-bot/assets/45239582/c8040cb6-c5b3-4708-80fd-3332f1d8b8e7)
# POLIGI : Gist-policy-bot
광주과학기술원 원내규정집 바탕 챗봇

## 프로젝트 소개
광주과학기술원의 원내규정집을 VectorDB에 저장한 후 retrieval한 내용을 바탕으로 원내구성원들에게 챗봇 형식으로 응답하는 프로젝트입니다. 출장, 재무, 근로, 휴학, 장학, 여비, 휴가 등 다양한 분야에 대해 원규집을 바탕으로 정확한 응답을 생성합니다.

## 개발 기간
* 24.05.05 - 22.06.06

## 개발 환경
![temp_1717685961465 853110627](https://github.com/jaehee831/gist-policy-bot/assets/79001832/cdf84611-959a-4116-8601-5c14166561ba)

## 팀원
| 배성호 [@oy6uns](https://github.com/oy6uns) | 전우석 [@usok1ng](https://github.com/usok1ng) | 최원혁 [@Wonhyeok316](https://github.com/Wonhyeok316) | 이재희 [@jaehee831](https://github.com/jaehee831) | 지유나 [@younaji](https://github.com/younaji) |
| :---: | :---: | :---: | :---: | :---: |
|<img width="900" src="https://github.com/jaehee831/gist-policy-bot/assets/45239582/708221c9-ecd6-4fce-ae84-dc0e06489005">|<img width="800" src="https://github.com/jaehee831/gist-policy-bot/assets/45239582/e4dbced3-ac8d-4dc1-af2f-332361976e1d">|<img width="600" src="https://github.com/jaehee831/gist-policy-bot/assets/45239582/93c1054f-7d1f-4dbb-8dc2-97da7e185dd5">|<img width="800" src="https://github.com/jaehee831/gist-policy-bot/assets/45239582/df63249d-f1ed-4042-82ba-8e75b4cef258">|<img width="900" src="https://github.com/jaehee831/gist-policy-bot/assets/45239582/cfe58a2e-3921-4a9d-9f37-373d2b5c73a5">|
- 배성호 - 발표 자료 제작, 제품 프로토타입 제작, 데이터 전처리 및 수집
- 전우석 - 발표 자료 제작, 인터뷰, 데이터 전처리 및 수집
- 최원혁 - RAG 기능 구현 및 파이프라인 연결, 텍스트 파일 DB화
- 이재희 - 인터뷰, 프론트엔드(Streamlit) 제작
- 지유나 - 프롬프트 엔지니어링, 데이터 전처리 및 수집

  
## 주요 기능
### 📌 원규 관련 질문
사용자는 광주과학기술원 원규집에 나와있는 내용들을 챗봇을 통해 쉽고 빠르게 물어볼 수 있습니다.   
예시 : 해외로 출장을 가려는데, 내가 어떤 종류의 여비를 지원받을 수 있을까?
### 📌 사용자 채팅 내역 기록
챗봇은 사용자의 채팅 내역을 chat_history 변수에 저장함으로써 사용자의 채팅 내역을 기록합니다. 즉, 이전에 입력했던 정보를 불필요하게 다시 입력할 필요가 없습니다.
### 📌 해당 원규의 온라인 링크 제공
해당 답변을 제공한 원규의 정확한 내용을 온라인 링크로 제공합니다.
### 📌 정확한 답변을 위한 추가 정보 요구
사용자의 질문에 정확하게 답변하기 위해 추가적인 정보를 사용자에게 물어봅니다. 챗봇과 대화하는 과정을 통해 사용자는 더 정확한 답변을 얻을 수 있습니다.
### 📌 다양한 언어 제공
사용자의 질문 언어를 자동으로 감지하여, 해당 언어로 다시 답변합니다. 현재 한국어와 영어 두 가지 언어를 지원하고 있습니다.
## 사용 방법
Streamlit 폴더 내부에서
```
streamlit run gpt.py
```
실행.

(환경변수의 OPEN_API_KEY에 자신만의 ChatGPT API Key가 설정되어야 사용 할 수 있음.)

## 활용 예시
![temp_1717685907741 1018538114](https://github.com/jaehee831/gist-policy-bot/assets/79001832/6a785f1c-3379-4242-92b3-53edd1310240)

## 실행 화면
https://github.com/jaehee831/gist-policy-bot/assets/45239582/e2fe326d-36c6-47a3-a018-00e0cdf7ce1f


