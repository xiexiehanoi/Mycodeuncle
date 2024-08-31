import os
import re
from dotenv import load_dotenv
from transformers import pipeline
from git import Repo

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 가져오기
MODEL_NAME = os.getenv("MODEL_NAME")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def get_changed_files():
    repo = Repo(".")
    changed_files = [item.a_path for item in repo.index.diff(None)]
    return changed_files

def get_language(file_path):
    if file_path.endswith('.py'):
        return 'Python'
    elif file_path.endswith('.js'):
        return 'JavaScript'
    elif file_path.endswith('.java'):
        return 'Java'
    else:
        return 'Unknown'

def review_code(file_path):
    reviewer = pipeline("text2text-generation", model=MODEL_NAME, api_key=HUGGINGFACE_API_KEY)
    with open(file_path, 'r') as file:
        code = file.read()
    
    language = get_language(file_path)
    
    prompt = f"""As a senior {language} developer, review the following code and provide your response in Korean:

1. Key Changes: Summarize the main changes or features (use emoji bullet points).
2. TODO List: List improvements or tasks. Use the format "[ ] Task description".
3. Detailed Review: For each changed part of the code, provide:
   변경: What has been implemented or modified
   문제: Any problems or potential issues
   해결: Suggestions for improving the code

Separate each section with "---".
Ensure all your responses are in Korean.

Code to review:
{code}
"""
    review = reviewer(prompt, max_length=1500, do_sample=True, temperature=0.7)
    
    return review[0]['generated_text']

def process_review(review_text):
    sections = review_text.split("---")
    
    summary = sections[0].strip() if len(sections) > 0 else ""
    todo_list = sections[1].strip() if len(sections) > 1 else ""
    detailed_review = "\n".join(sections[2:]).strip() if len(sections) > 2 else ""
    
    # TODO 항목 추출
    todo_items = re.findall(r'\[ \] .*', todo_list)
    
    # 상세 리뷰 처리
    comments = []
    for block in re.split(r'변경:|문제:|해결:', detailed_review):
        if block.strip():
            comment_type = re.search(r'(변경|문제|해결):', block)
            if comment_type:
                comment_type = comment_type.group(1)
                content = block.replace(comment_type + ":", "").strip()
                comments.append({"type": comment_type, "content": content})
    
    return {
        "summary": summary,
        "todo_items": todo_items,
        "comments": comments
    }

def main():
    changed_files = get_changed_files()
    all_reviews = {}
    overall_summary = []
    overall_todo = []

    for file in changed_files:
        if file.endswith(('.py', '.js', '.java')):
            review = review_code(file)
            processed_review = process_review(review)
            all_reviews[file] = processed_review
            
            # 각 파일의 요약을 전체 요약에 추가
            overall_summary.append(f"파일: {file}\n{processed_review['summary']}")
            
            # 각 파일의 TODO 항목을 전체 TODO 목록에 추가
            overall_todo.extend(processed_review['todo_items'])

    # 전체 요약과 TODO 목록 출력 (push 당 한 번만)
    print("=== 전체 요약 ===")
    print("\n".join(overall_summary))
    
    print("\n=== 전체 TODO 목록 ===")
    for item in overall_todo:
        print(item)

    # 각 파일별 상세 리뷰 출력
    print("\n=== 상세 리뷰 ===")
    for file, review in all_reviews.items():
        print(f"\n파일: {file}")
        for comment in review['comments']:
            print(f"{comment['type']}: {comment['content']}")

if __name__ == "__main__":
    main()