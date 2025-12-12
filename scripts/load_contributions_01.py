import os
import re  # [추가] 정규표현식 사용을 위해 추가

from github import Github

def load_contributions(MY_GITHUB_TOKEN, MY_USERNAME, REPO_NAME, OUTPUT_DIR, OUTPUT_FILENAME1, OUTPUT_FILENAME2):
    # --- 토큰 유무 확인 ---
    if not MY_GITHUB_TOKEN:
        print("오류: GITHUB_TOKEN을 찾을 수 없습니다.")
        print(".env 파일에 GITHUB_TOKEN='ghp_...' 형식으로 설정했는지 확인하세요.")
        exit() # 토큰 없으면 스크립트 종료

    print(f"GitHub 토큰을 성공적으로 로드했습니다.")

    # Github 객체 생성
    g = Github(MY_GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # 데이터 저장용 리스트 및 딕셔너리 초기화
    issue_markdown_lines = []
    pr_markdown_lines = []
    issue_status_override = {} # [추가] { 이슈번호: "아이콘" } 형태로 저장할 딕셔너리

    # ==============================================================================
    # [순서 변경] PR 목록을 먼저 가져옵니다. (이슈 상태 업데이트를 위해 정보가 필요함)
    # ==============================================================================
    print(f"정보 가져오는 중: {MY_USERNAME} 님의 {REPO_NAME} PR 목록...")
    pulls = repo.get_pulls(state="all") 
    
    for pr in pulls:
        if pr.user.login != MY_USERNAME:
            continue

        # PR 상태 결정
        if pr.state == "open":
            status_icon = "🟢"
        elif pr.merged:
            status_icon = "🟣"
        else: # state == "closed" and not merged
            status_icon = "🔴"
        
        # [추가] PR이 Merged(🟣) 상태이고 본문에 내용이 있다면, 연결된 이슈 번호 찾기
        if status_icon == "🟣" and pr.body:
            # 정규식: #뒤에 오는 숫자를 찾음 (예: "Closes #1", "Fix #12")
            referenced_issues = re.findall(r'#(\d+)', pr.body)
            for issue_num in referenced_issues:
                # 찾은 이슈 번호를 키로, '🟣' 아이콘을 값으로 저장
                issue_status_override[int(issue_num)] = "🟣"

        # 리스트에 마크다운 형식으로 추가
        pr_markdown_lines.append(f"{status_icon}[#{pr.number}]({pr.html_url})")

    # ==============================================================================
    # [순서 변경] 이슈 목록 가져오기 (위에서 만든 override 정보 적용)
    # ==============================================================================
    print(f"정보 가져오는 중: {MY_USERNAME} 님의 {REPO_NAME} 이슈 목록...")
    issues = repo.get_issues(creator=MY_USERNAME, state="all")
    
    for issue in issues:
        if not issue.pull_request:
            # 기본 상태 설정
            if issue.state == "open":
                status_icon = "🟢"
            else: # state == "closed"
                status_icon = "🔴"
            
            # [추가] PR에 의해 Merge된 것으로 확인된 이슈라면 아이콘 덮어쓰기
            if issue.number in issue_status_override:
                status_icon = issue_status_override[issue.number]
            
            # 리스트에 마크다운 형식으로 추가
            issue_markdown_lines.append(f"{status_icon}[#{issue.number}]({issue.html_url})")

    # --- 파일 저장 로직 (기존 동일) ---
    try:
        # 1. 'data' 디렉터리가 없으면 생성
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # 2. 파일에 내용 쓰기
        with open(OUTPUT_FILENAME1, 'w', encoding='utf-8') as f:
            for issue_markdown_line in issue_markdown_lines:
                f.write(issue_markdown_line)
                f.write("\n")

        with open(OUTPUT_FILENAME2, 'w', encoding='utf-8') as f:
            for pr_markdown_line in pr_markdown_lines:
                f.write(pr_markdown_line)
                f.write("\n")

        print(f"\n✅ 성공: 기여 내역을 '{OUTPUT_FILENAME1}, {OUTPUT_FILENAME2}' 파일에 저장했습니다.")
        print(f"   (이슈 {len(issue_markdown_lines)}개, PR {len(pr_markdown_lines)}개)")

    except Exception as e:
        print(f"\n❌ 오류: 파일 저장 중 문제가 발생했습니다.")
        print(f"   {e}")
