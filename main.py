from scripts.load_contributions_01 import load_contributions
from scripts.filter_contributions_02 import filter_contributions

import os
from dotenv import load_dotenv
# .env 파일에서 환경 변수를 로드
load_dotenv()

MY_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
MY_USERNAME = "daehyun99" 

REPO_NAMES = [
    "pgmpy/pgmpy",
    "pytorch/pytorch"
]

if __name__ == "__main__":
    for REPO_NAME in REPO_NAMES:

        OUTPUT_BASE = "data"
        OUTPUT_DIR = os.path.join(OUTPUT_BASE, REPO_NAME.split('/')[-1])
        OUTPUT_FILENAME1 = os.path.join(OUTPUT_DIR, "stage_issue.txt")
        OUTPUT_FILENAME2 = os.path.join(OUTPUT_DIR, "stage_pr.txt")

        COMMIT_FILE = os.path.join(OUTPUT_BASE, "commit.txt")
        STAGE_ISSUE_FILE = os.path.join(OUTPUT_DIR, "stage_issue.txt")
        STAGE_PR_FILE = os.path.join(OUTPUT_DIR, "stage_pr.txt")

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        load_contributions(MY_GITHUB_TOKEN, MY_USERNAME, REPO_NAME, OUTPUT_DIR, OUTPUT_FILENAME1, OUTPUT_FILENAME2)
        filter_contributions(OUTPUT_DIR, STAGE_ISSUE_FILE, STAGE_PR_FILE, COMMIT_FILE)
