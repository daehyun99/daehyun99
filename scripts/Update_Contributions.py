import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

# --- 설정 ---
# 1. GitHub 토큰 (https://github.com/settings/tokens 에서 발급)
#    보안을 위해 환경 변수로 설정하는 것을 권장합니다.
#    (예: export GITHUB_TOKEN='ghp_...')
# g = Github(os.environ.get("GITHUB_TOKEN"))
MY_GITHUB_TOKEN = os.environ.get("YOUR_GITHUB_TOKEN")
g = Github(MY_GITHUB_TOKEN)
# 2. 내 GitHub 유저 이름
MY_USERNAME = "daehyun99"

# 3. 대상 저장소
REPO_NAME = "pgmpy/pgmpy"
# --- 설정 끝 ---

repo = g.get_repo(REPO_NAME)

print(f"## 📄 {MY_USERNAME} 님의 {REPO_NAME} 이슈 목록")
issues = repo.get_issues(creator=MY_USERNAME, state="all")
for issue in issues:
    # PR이 아닌 순수 이슈만 필터링
    if not issue.pull_request:
        if issue.state == "open":
            status_icon = "🟢"
        else: # state == "closed"
            status_icon = "🔴" # pgmpy에서는 close를 🔴로 사용하심
        
        # 마크다운 형식으로 출력
        print(f"{status_icon}[#{issue.number}]({issue.html_url})")

print(f"\n## 🚀 {MY_USERNAME} 님의 {REPO_NAME} PR 목록")

# 🔴 [수정] 'author=MY_USERNAME' 파라미터를 삭제합니다.
#    이 메서드는 author 인자를 받지 않습니다.
pulls = repo.get_pulls(state="all") 

# 이 루프가 author를 정확히 필터링해줍니다.
for pr in pulls:
    if pr.user.login != MY_USERNAME:
        continue

    if pr.state == "open":
        status_icon = "🟢"
    elif pr.merged:
        status_icon = "🟣"
    else: # state == "closed" and not merged
        status_icon = "🔴"
    
    # 마크다운 형식으로 출력
    print(f"{status_icon}[#{pr.number}]({pr.html_url})")
