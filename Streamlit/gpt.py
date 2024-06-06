import os
import numpy as np
import faiss
import openai
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from langdetect import detect

# 바뀐 부분
api_key = os.getenv('API_KEY')

if not api_key:
    raise FileNotFoundError("환경 변수를 찾을 수 없습니다.")

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
vector_db_dir = os.path.join(current_dir, '..', 'VectorDB')

# Load FAISS index
index_path = os.path.join(vector_db_dir, 'vector_db.index')
if not os.path.isfile(index_path):
    raise FileNotFoundError(f"FAISS 인덱스 파일을 찾을 수 없습니다: {index_path}")

index = faiss.read_index(index_path)
index_dimension = index.d  # Check the dimension of the index

# Load file paths
file_paths_path = os.path.join(vector_db_dir, 'file_paths.txt')
if not os.path.isfile(file_paths_path):
    raise FileNotFoundError(f"파일 경로 파일을 찾을 수 없습니다: {file_paths_path}")

with open(file_paths_path, 'r', encoding='utf-8') as f:
    file_paths = [line.strip() for line in f]

# Load all documents
documents = []
for path in file_paths:
    full_path = os.path.join(vector_db_dir, path)  # Ensure the path is correct relative to the vector_db_dir
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"문서 파일을 찾을 수 없습니다: {full_path}")
    with open(full_path, 'r', encoding='utf-8') as file:
        documents.append(file.read())



# 파일 경로와 링크 URL 매핑
file_path_to_url = {
    r'../Data/ER32217 재학생장학금 지급지침.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawFullView.do?SEQ=199&SEQ_HISTORY=526',
    r'../Data/FR00601 보건및기타.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_당직.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_복무.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_복무_2.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_복무_3.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_시간외야간r및휴일근무.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_임용및퇴직 복지후생.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_총칙.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00601 취업규칙_출장및파견 전보및사무인계.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=76&SEQ_HISTORY=996&PAGE_MODE=1&LAWGROUP=1&TREE_MODE=0',
    r'../Data/FR00602 여비규칙_1.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=77&LAWGROUP=1&PAGE=1&SEQ_HISTORY=0',
    r'../Data/FR00602 여비규칙_국내출장비.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawFullView.do?SEQ=77&SEQ_HISTORY=987',
    r'../Data/FR00602 여비규칙_국내출장비_2.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=77&LAWGROUP=1&PAGE=1&SEQ_HISTORY=0',
    r'../Data/FR00602 여비규칙_국외출장비.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail_areaC.do?SEQ=77&LAWGROUP=1&PAGE=1&SEQ_HISTORY=0',
    r'../Data/FR00602 여비규칙_국외출장비_2.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/FR00602 여비규칙_보칙.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_계약의 이행.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_계약의 체결.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_계약의 체결_2.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_구매절차 및 방법.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_구매절차 및 방법_2.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_기타.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/FR00807 물품구매요령_총칙.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=105&LAWGROUP=1&PAGE=1',
    r'../Data/국내여비 정액표.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/국내이전비 정액표.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/국외여비 정액표.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/국외이전비 정액표.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/장기체제자 월액표.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawDetail.do?SEQ=77&LAWGROUP=1&PAGE=1',
    r'../Data/기계공학부_학위취득절차_박사과정.txt': 'https://me.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000000339/view.do',
    r'../Data/기계공학부_학위취득절차_박사과정2.txt': 'https://me.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000000339/view.do',
    r'../Data/기계공학부_학위취득절차_석사과정.txt': 'https://me.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000000339/view.do',
    r'../Data/지구환경공학부_학위취득절차_': 'https://env1.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000000400/view.do',
    r'../Data/화학과_학위취득절차_박사.txt': 'https://chem.gist.ac.kr/thumbnail/html/viewer/BBS_202102191216481360.hwp/document.html',
    r'../Data/광주과학기술원_학위수여규정_1.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawFullView.do?SEQ=64&SEQ_HISTORY=1076',
    r'../Data/광주과학기술원_학위수여규정_2.txt': 'https://law.gist.ac.kr/lmxsrv/law/lawFullView.do?SEQ=64&SEQ_HISTORY=1076'
    # 필요한 다른 파일들도 여기에 추가
}


# 임베딩 생성 함수
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        engine="text-embedding-ada-002"
    )
    return np.array(response['data'][0]['embedding'], dtype=np.float32)


def search(query, top_k=3):
    # 쿼리 벡터화
    query_embedding = get_embedding(query).reshape(1, -1)

    # 차원 일치 여부 확인
    if query_embedding.shape[1] != index_dimension:
        raise ValueError(f"Query embedding dimension {query_embedding.shape[1]} does not match index dimension {index_dimension}")

    # FAISS 인덱스에서 유사한 문서 검색
    D, I = index.search(query_embedding, top_k)

    results = [(file_paths[i], documents[i]) for i in I[0]]
    return results


def generate_answer(query, conversation_history, top_k=2):
    # 관련 문서 검색
    relevant_docs = search(query, top_k)

    # 관련 문서들을 하나의 문자열로 결합
    context = "\n\n".join(doc for _, doc in relevant_docs)
    reference_links = list(set(file_path_to_url.get(path, path) for path, _ in relevant_docs))
    references = "\n".join(reference_links)

    language = detect(query)

    if language == 'ko':
        system_message = ("이 챗봇은 광주과학기술원(GIST) 구성원들의 규정 관련 질문에 대한 답변을 제공하기 위해 "
                          "만들어진 챗봇입니다. 챗봇은 데이터베이스에 있는 정보를 기반으로 질문에 답변합니다. "
                          "또한 사용자의 질문이 불완전한 경우 챗봇은 데이터베이스를 기반으로 추가 정보를 요청해야 합니다. "
                          "예를 들어 '보다 정확한 답변을 드리기 위해 몇 가지 추가 정보가 필요합니다. 필요한 추가 정보]와 같은 세부 정보를 "
                          "제공해 주시겠습니까?")
    else:
        system_message = ("This GPT is a chatbot designed to provide answers to questions related to regulations for members of the Gwangju Institute of Science and Technology (GIST). "
                          "It should respond in a friendly manner. The chatbot will answer questions based on information in the database.Additionally, if the user's question is incomplete, the chatbot should request additional information based on the database. "
                          "For example: [To provide you with a more accurate answer, I need some additional information. Could you please provide details such as [necessary additional information]?")
    conversation_history.append({"role": "user", "content": query})

    # OpenAI GPT-4 모델을 사용하여 답변 생성
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            *conversation_history,
            {"role": "user", "content": f"Here are some documents:\n\n{context}\n\nQuestion: {query}\nAnswer:"}
        ],
        max_tokens=1000  # max_tokens 값을 증가시켜 잘리는 문제 방지
    )

    answer = response.choices[0].message['content'].strip()
    conversation_history.append({"role": "assistant", "content": answer})
    return answer, references, conversation_history


# Streamlit 앱 설정
st.image(r"../poligi.png", use_column_width=True)
st.header("🤖 Gist Policy App (Demo)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('질문: ', '', key='input')
    submitted = st.form_submit_button('전송')

if submitted and user_input:
    answer, references, st.session_state['conversation_history'] = generate_answer(user_input, st.session_state['conversation_history'])
    st.session_state.past.append(user_input)
    st.session_state.generated.append((answer, references))

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        user_question = st.session_state['past'][i]
        bot_answer, references = st.session_state['generated'][i]
        st.write(f'**질문:** {user_question}')
        st.write(f'**답변:** {bot_answer}')
        st.write(f'**참조한 문서 경로:**\n{references}')
        st.markdown("---")  
