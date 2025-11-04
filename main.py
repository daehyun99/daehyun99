

from scripts.load_contributions_01 import load_contributions
from scripts.filter_contributions_02 import filter_contributions

import os
from dotenv import load_dotenv
# .env 파일에서 환경 변수를 로드
load_dotenv()

# --- 설정 ---
MY_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# .env 파일에 MY_USERNAME="daehyun99" 처럼 추가하고 아래 코드로 변경하셔도 좋습니다.
# MY_USERNAME = os.environ.get("MY_USERNAME") 
MY_USERNAME = "daehyun99" # 여기에 직접 입력하셔도 됩니다.
REPO_NAME = "pgmpy/pgmpy"

# --- [수정] 파일 저장 경로 설정 ---
OUTPUT_DIR = "data"
OUTPUT_FILENAME1 = os.path.join(OUTPUT_DIR, "stage_issue.txt")
OUTPUT_FILENAME2 = os.path.join(OUTPUT_DIR, "stage_pr.txt")


COMMIT_FILE = os.path.join(OUTPUT_DIR, "commit.txt")
STAGE_ISSUE_FILE = os.path.join(OUTPUT_DIR, "stage_issue.txt")
STAGE_PR_FILE = os.path.join(OUTPUT_DIR, "stage_pr.txt")


if __name__ == "__main__":
    load_contributions(MY_GITHUB_TOKEN, MY_USERNAME, REPO_NAME, OUTPUT_DIR, OUTPUT_FILENAME1, OUTPUT_FILENAME2)
    filter_contributions(OUTPUT_DIR, STAGE_ISSUE_FILE, STAGE_PR_FILE, COMMIT_FILE)
