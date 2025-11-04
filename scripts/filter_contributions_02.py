import os




def read_lines_to_set(filepath: str) -> set:
    """파일을 읽어 각 줄을 set으로 반환합니다. 공백과 개행 문자를 제거합니다."""
    if not os.path.exists(filepath):
        print(f"정보: '{filepath}' 파일을 찾을 수 없습니다. 빈 목록으로 처리합니다.")
        return set()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # 양 끝 공백/개행을 제거하고, 빈 줄이 아닌 것만 set에 추가
            lines = {line.strip() for line in f if line.strip()}
        return lines
    except Exception as e:
        print(f"오류: '{filepath}' 파일 읽기 중 오류 발생: {e}")
        return set()

def filter_and_write_file(stage_filepath: str, committed_items: set):
    """
    Stage 파일을 읽어 Committed 아이템에 없는 내용만 필터링한 후,
    다시 동일한 Stage 파일에 덮어씁니다.
    """
    print(f"\n처리 중: '{stage_filepath}'")
    
    # 1. Stage 파일 읽기
    stage_items = read_lines_to_set(stage_filepath)
    if not stage_items:
        print(f"-> 처리할 내용이 없습니다.")
        return 0

    # 2. 필터링: stage_items 에는 있지만 committed_items 에는 없는 것
    new_items = [item for item in stage_items if item not in committed_items]
    
    # 3. 정렬 (원본 순서를 유지하기 위해 stage_items 순서대로 다시 정렬)
    #    set은 순서가 없으므로, 원본 리스트에서 순서를 찾아 정렬하는 것이 좋습니다.
    #    간단하게는 그냥 new_items 리스트를 사용해도 무방합니다. (순서가 중요하지 않다면)
    #    여기서는 new_items 리스트를 그대로 사용합니다.
    
    # 4. 동일 파일에 덮어쓰기
    try:
        with open(stage_filepath, 'w', encoding='utf-8') as f:
            if not new_items:
                f.write("") # 새로운 내용이 없으면 빈 파일로 만듦
            else:
                f.write("\n".join(new_items))
                f.write("\n") # 파일 마지막에 개행 문자 추가
        
        print(f"-> 완료: 총 {len(stage_items)}개 중 {len(new_items)}개의 새로운 내역을 파일에 덮어썼습니다.")
        return len(new_items)
        
    except Exception as e:
        print(f"오류: '{stage_filepath}' 파일 쓰기 중 오류 발생: {e}")
        return 0


def filter_contributions(OUTPUT_DIR, STAGE_ISSUE_FILE, STAGE_PR_FILE, COMMIT_FILE):
    print("--- 새로운 기여 내역 필터링 스크립트 시작 ---")

    # 1. 'data' 디렉터리가 없으면 생성 (파일 쓰기 오류 방지)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. 이미 커밋된 내역 불러오기
    print(f"'{COMMIT_FILE}'에서 이미 반영된 내역을 불러옵니다...")
    committed_items_set = read_lines_to_set(COMMIT_FILE)
    print(f"-> 총 {len(committed_items_set)}개의 기여 내역을 확인했습니다.")

    # 3. 이슈 파일 필터링 및 덮어쓰기
    new_issue_count = filter_and_write_file(STAGE_ISSUE_FILE, committed_items_set)

    # 4. PR 파일 필터링 및 덮어쓰기
    new_pr_count = filter_and_write_file(STAGE_PR_FILE, committed_items_set)

    print("\n--- 스크립트 완료 ---")
    print(f"새로운 이슈: {new_issue_count}개")
    print(f"새로운 PR: {new_pr_count}개")
    print(f"'{STAGE_ISSUE_FILE}'와 '{STAGE_PR_FILE}'의 내용을 확인하세요.")
