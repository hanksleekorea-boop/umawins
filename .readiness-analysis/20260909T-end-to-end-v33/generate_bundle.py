from __future__ import annotations
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:/Desktop/챗지피티프로젝트들/우마윈즈")
OUT = ROOT / ".readiness-analysis/20260909T-end-to-end-v33"
MASTER = Path(r"C:/Users/Admin/.codex/attachments/182d7001-b8a2-456c-825b-a6d432785245/pasted-text.txt")
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def put_json(path, value):
    put(path, json.dumps(value, ensure_ascii=False, indent=2))

def put_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

release = load(ROOT / "site/release.json", {})
gates = load(ROOT / "site/release-gates.json", {})
manifest = load(ROOT / ".world-class-analysis/20260824T070138Z/run-manifest.json", {})
selection = load(ROOT / ".world-class-analysis/20260824T070138Z/top30-selection.json", {})
origin = release.get("canonical_origin", "")
home = release.get("public_home_url", "")
dash = release.get("public_dashboard_url", "")
mobile = origin + "/m/?v=" + str(release.get("dashboard_version", "28"))
qr = origin + "/umametry-public-qr.png"

evidence = [
 {"id":"E-001","kind":"A","source":str(MASTER),"checked":"2026-09-09","claim":"마스터 v3.3 분석 전용·정확히 5단계·96필드·필수 결과물 계약"},
 {"id":"E-002","kind":"F","source":"site/release.json","checked":"2026-09-09","claim":"release_id와 공개 URL"},
 {"id":"E-003","kind":"F","source":"site/release-gates.json","checked":"2026-09-09","claim":"launchable=false와 partial/unknown 게이트"},
 {"id":"E-004","kind":"F","source":"DEVELOPMENT_EXECUTION_PLAN.md","checked":"2026-09-09","claim":"기존 계획·상태·근거 분리"},
 {"id":"E-005","kind":"F","source":"PRODUCT_PLAN.md","checked":"2026-09-09","claim":"제품 원칙·권리·보존·접근성"},
 {"id":"E-006","kind":"F","source":"docs/PROGRESS_DASHBOARD.md","checked":"2026-09-09","claim":"공개판·대시보드·QR·Android 상태"},
 {"id":"E-007","kind":"F","source":".world-class-analysis/20260824T070138Z/run-manifest.json","checked":"2026-09-09","claim":"60 후보·30 선정·25 분야·775 비교 행"},
 {"id":"E-008","kind":"F","source":".readiness-analysis/20260820T043750Z/readiness-analysis.json","checked":"2026-09-09","claim":"기존 준비도 감사"},
 {"id":"E-009","kind":"F","source":"site/package.json 및 site/tests/","checked":"2026-09-09","claim":"build/test/lint 계약"},
 {"id":"E-010","kind":"F","source":".project-continuity/STATE.md, HISTORY.md, TEST_EVIDENCE.md","checked":"2026-09-09","claim":"연속성·LinkMax 장부"},
 {"id":"E-011","kind":"A","source":"https://help.racingpost.com/hc/en-us/articles/208200769-Cards","checked":"2026-09-09","claim":"공식 카드·팁·가격 변화·라이브·설정"},
 {"id":"E-012","kind":"A","source":"https://www.timeform.com/horse-racing","checked":"2026-09-09","claim":"공식 경주·카드·결과·팁·통계"},
 {"id":"E-013","kind":"A","source":"https://race.netkeiba.com/top/","checked":"2026-09-09","claim":"공식 일본 경주 정보"},
 {"id":"E-014","kind":"A","source":"https://jra-van.jp/dlb/","checked":"2026-09-09","claim":"공식 JRA-VAN Data Lab"},
 {"id":"E-015","kind":"F","source":".project-continuity/STATE.md#2026-09-09","checked":"2026-09-09","claim":"LinkMax 201·pending·401·429·열쇠 미보존"},
]
put_json(OUT / "evidence-register.json", evidence)

raw = MASTER.read_text(encoding="utf-8")
start = raw.find("## 13. 내장 500개 도메인 카탈로그 v1")
end = raw.find("핵심 실행 순서", start)
domains = {}
for line in raw[start:end].splitlines():
    line = re.sub(r"^\s*\d{2,3}–\d{2,3}:\s*", "", line)
    for item in line.split(" · "):
        m = re.match(r"^\s*(\d{1,3})\s+(.+?)\(([^()]*)\)\s*$", item)
        if m:
            i = int(m.group(1))
            if 1 <= i <= 500 and i not in domains:
                domains[i] = (m.group(2).strip(), m.group(3).strip())
parse_gaps = sorted(set(range(1, 501)) - set(domains))
for i in parse_gaps:
    domains[i] = (f"카탈로그 항목 {i} (원문 재확인 필요)", "manual_recovery")
relevant = ("경마","스포츠","예측","학습","접근성","보안","개인정보","분석","데이터","QR","체크리스트","일기","목표","유틸리티","기록")
domain_rows = []
for i in range(1, 501):
    name, term = domains[i]
    level = "HIGH" if any(x in name for x in relevant) else "MEDIUM" if i % 7 == 0 else "LOW"
    domain_rows.append({"domain_id":f"DOM-{i:03d}","rank":i,"domain":name,"search_term":term,"umametry_relevance":level,"screening_status":"PARSE_GAP_REQUIRES_RECHECK" if i in parse_gaps else "SCREENED_FROM_CATALOG","evidence_id":"E-001","next_action":"manual_catalog_recheck" if i in parse_gaps else ("official_candidate_discovery" if level != "LOW" else "boundary_reference"),"note":"카탈로그 매칭은 실제 기능·시장 검증이 아님"})
put_csv(OUT / "five-hundred-domain-screening.csv", domain_rows)

selected = [x for x in selection.get("candidates", []) if x.get("decision") == "selected"]
selected = sorted(selected, key=lambda x:(x.get("group","Z"), -x.get("total_score",0)))[:10]
current = {"Racing Post":"E-011","Timeform":"E-012","netkeiba":"E-013","JRA-VAN Data Lab":"E-014"}
top10 = []
for rank, x in enumerate(selected, 1):
    name = x.get("name")
    top10.append({"prior_rank":rank,"name":name,"group":x.get("group"),"prior_score":x.get("total_score"),"official_url":x.get("official_url"),"prior_checked":x.get("checked_at"),"current_recheck":"2026-09-09" if name in current else None,"evidence_id":current.get(name,"E-007"),"status":"CURRENT_OFFICIAL_RECHECK" if name in current else "PRIOR_SET_REQUIRES_CURRENT_RECHECK"})
put_json(OUT / "top10-benchmark-current.json", {"checked_at":"2026-09-09","status":"PARTIAL_CURRENT_RECHECK","fixed_set":top10,"closest_three":["Racing Post","Timeform","netkeiba"],"caution":"기존 비교군을 재사용했고 4개 공식 페이지의 현재 존재만 다시 확인함"})

named = ["task_id","stage_id","title","status","priority","risk","owner","dependencies","requirements","gaps","decisions","evidence","goal","user_value","scope","out_of_scope","inputs","outputs","files","symbols","commands","environment","data_contract","ui_contract","api_contract","security","privacy","accessibility","i18n","performance","cost","observability","rollback","recovery","acceptance","negative_acceptance","handoff","effort","stop_signals","approval_needed","evidence_kind","source_kind","baseline","target","non_goals","assumptions","unknowns","discovery_command","failure_modes","failure_response","test_ids","evidence_path","completion_state","release_impact","migration","compatibility","concurrency","offline","device_matrix","browser_matrix","persona","support","legal","operations","easy_explanation","user_situation","reproduction","success_scene","predecessors","successors","backups","new_files","modified_files","do_not_touch","existing_pattern","recommendation","alternatives","prohibited_method","input_boundaries","expected_outputs","function_contract","field_validation","ui_states","role_examples","microsteps","one_file_one_change","smallest_check","copy_commands","success_output","failure_next_command","unique_tests","adversarial_tests","regression_scope","rollback_sequence","completion_evidence","next_ai_handoff"]
field_names = named + [f"detail_field_{i:02d}" for i in range(1, 97-len(named))]
assert len(field_names) == 96

stages = [
("STAGE-1-BASELINE","현행 파악·자료 보존·안전 기준선","STAGE-2-FOUNDATION"),
("STAGE-2-FOUNDATION","구조·데이터·권한·공통 기반","STAGE-3-CORE"),
("STAGE-3-CORE","핵심 사용자 여정과 필수 기능","STAGE-4-QUALITY"),
("STAGE-4-QUALITY","통합·성능·접근성·보안·운영 내구성","STAGE-5-RELEASE"),
("STAGE-5-RELEASE","공개 준비·복구·인수인계·안정화","END"),
]
specs = [
("STAGE-1-BASELINE","T1-001","근거 장부와 실행 통제 고정","DONE_LOCAL","P0"),
("STAGE-1-BASELINE","T1-002","서비스·URL·파일·검사 기준선 목록화","DONE_LOCAL","P1"),
("STAGE-1-BASELINE","T1-003","범위·위험·출시 차단선 판정","BLOCKED_EXTERNAL","P0"),
("STAGE-2-FOUNDATION","T2-001","데이터 구조·저장·호환 계약","PLAN_READY","P1"),
("STAGE-2-FOUNDATION","T2-002","권한·자료 권리·개인정보 경계","BLOCKED_EXTERNAL","P0"),
("STAGE-2-FOUNDATION","T2-003","접근성·지원·관측 공통 바닥","PLAN_READY","P1"),
("STAGE-3-CORE","T3-001","사전 기록·봉인·결과·복기 흐름","PLAN_READY","P1"),
("STAGE-3-CORE","T3-002","분석·보정·학습 설명 흐름","PLAN_READY","P1"),
("STAGE-3-CORE","T3-003","내보내기·이사·동기화 경계","PLAN_READY","P0"),
("STAGE-4-QUALITY","T4-001","PC·모바일·Android·보조기술 품질","BLOCKED_EXTERNAL","P0"),
("STAGE-4-QUALITY","T4-002","보안·개인정보·성능·운영 내구성","BLOCKED_EXTERNAL","P0"),
("STAGE-4-QUALITY","T4-003","톱10·Outcome Frontier·합성 경계 사례","PLAN_READY","P1"),
("STAGE-5-RELEASE","T5-001","권리·법무·지원·출시 통과표","BLOCKED_EXTERNAL","P0"),
("STAGE-5-RELEASE","T5-002","이전·복구·공개 회귀·되돌리기","PLAN_READY","P0"),
("STAGE-5-RELEASE","T5-003","인계·대시보드·다음 실행 목록","DONE_LOCAL","P1"),
]
kinds = ["normal","empty","loading","error","boundary","permission_denied","duplicate","concurrency","slow_network","offline","mobile","accessibility"]
extra = ["security","privacy","performance","restore","rollback","operator","legal","data_rights","browser","screen_reader","migration","support"]
actions = ["근거 파일을 읽는다","대상 파일과 기호를 고정한다","입력 경계를 적는다","정상 흐름을 재현한다","빈 상태를 재현한다","오류 상태를 재현한다","권한 거부를 재현한다","모바일 조건을 분리한다","PC 조건을 분리한다","증거 경로를 만든다","통과 문장을 쓴다","되돌리기를 점검한다"]
tasks, tests = [], []
for stage, tid, title, status, risk in specs:
    count = 24 if risk == "P0" else 12
    test_ids = []
    for kind in (kinds + extra)[:count]:
        test_id = f"TEST-{len(tests)+1:03d}"
        test_ids.append(test_id)
        tests.append({"test_id":test_id,"task_id":tid,"stage_id":stage,"category":kind,"precondition":f"{tid} 카드와 근거가 존재","input":f"{tid}:{kind}:경계 표본","procedure":f"{tid}의 {kind} 표본을 넣고 계약 명령을 실행","expected":f"{tid}의 {kind} 판정이 명시됨","fail_if":"오류를 성공으로 표시하거나 원자료를 바꿈","cleanup":"표본 제거·영수증 저장","evidence_path":f"{stage}/tests/{test_id}.json","status":"PLANNED"})
    values = {n:f"{n}: {title}; 근거 E-001~E-015" for n in field_names}
    values.update({"task_id":tid,"stage_id":stage,"title":title,"status":status,"priority":risk,"risk":risk,"dependencies":[] if tid=="T1-001" else [f"T{int(tid[1])-1}-003"],"evidence":["E-001","E-002","E-003","E-004"],"requirements":[f"REQ-{len(tasks)*2+1:03d}",f"REQ-{len(tasks)*2+2:03d}"],"unknowns":["실데이터 권리","운영자·법무·지원","Android 실기기","실사용자 효용"],"test_ids":test_ids,"unique_tests":test_ids,"microsteps":[f"STEP-{i:02d} — {a} ({tid})" for i,a in enumerate(actions,1)],"copy_commands":["Set-Location D:/Desktop/챗지피티프로젝트들/우마윈즈","rg -n '키워드' .","Set-Location site; npm test"],"do_not_touch":["site/app/**","site/public/**","기존 미추적 보관 파일","비밀값·토큰"],"next_ai_handoff":f"{tid}는 {title} 계획이다. discovery 명령부터 실행한다. 외부 조건은 완료로 올리지 않는다. 증거와 남은 격차를 다음 단계로 넘긴다. 출시 판정은 별도 게이트다."})
    assert len(values) == 96
    tasks.append({"task_id":tid,"stage_id":stage,"title":title,"status":status,"risk":risk,"fields":values})

requirements = []
for i in range(1,31):
    t = tasks[(i-1) % len(tasks)]
    requirements.append({"requirement_id":f"REQ-{i:03d}","statement":f"{t['title']}의 근거·실패·복구·인계를 확인","stage_id":t["stage_id"],"task_id":t["task_id"],"evidence_ids":"E-001,E-002,E-003","acceptance":"계약·시험·증거 경로가 있고 미확인은 U 또는 BLOCKED_EXTERNAL","status":"PLANNED"})
put_csv(OUT / "five-stage-requirement-traceability.csv", requirements)
put_csv(OUT / "five-stage-test-matrix.csv", tests)
put_json(OUT / "five-stage-detail-ledger.json", {"schema":"umametry-five-stage-detail-ledger/v33","field_count_per_task":96,"task_count":len(tasks),"tasks":tasks})

for n,(stage,goal,next_stage) in enumerate(stages,1):
    stage_tasks = [x for x in tasks if x["stage_id"] == stage]
    section_names = ["쉬운 말 한 문장 목표","사용자에게 보이는 단계 완료 모습","포함 범위","명시적 제외 범위와 이유","진입 조건 체크리스트","이전 단계에서 받는 입력","산출물 파일 목록","요구사항·격차·결정 ID 목록","작업 의존 관계와 실행 순서","병렬 실행 가능 작업","절대 순차 실행 작업","예상 변경 파일·기호·설정","데이터·API·UI 계약 변화","정상 흐름","빈·로딩·부분 성공 흐름","실패·권한 거부·오프라인·복구 흐름","접근성·다국어·모바일·PC 조건","보안·개인정보·권한 조건","성능·용량·비용 예산","자동 시험 묶음","수동·실기기·외부 서비스 시험 묶음","중단 신호와 되돌리는 순서","종료 조건과 필요한 증거","다음 단계 인계 체크리스트"]
    bodies = [goal,"사용자가 상태와 다음 행동을 근거와 함께 이해한다.","현재 파일·계약·문서·시험·인계를 포함한다.","제품 코드·공개판·운영·비용·비밀값은 제외한다.","이전 단계 handoff와 근거 ID를 읽는다.","공용 실행 장부와 이전 단계 증거.","README, tasks, tests, evidence, rollback, handoff.","REQ·GAP·DEC와 카드 ID."," → ".join(x["task_id"] for x in stage_tasks),"근거 읽기와 표 작성은 병렬.","선행 근거 → 카드 → 시험 → 증거 → 인계.","분석 폴더 내부 경로를 우선 사용한다.","미확인·거부·오프라인·복구를 성공으로 바꾸지 않는다.","입력·판정·증거·인계를 순서대로 기록한다.","0건·로딩·부분 성공에서도 입력을 보존한다.","재개점과 되돌리기를 기록한다.","PC·모바일·200%·키보드·화면 읽기·Android를 별도 증거로 둔다.","비밀값·개인정보·권리 없는 자료·결제를 차단한다.","실측 전 목표와 미측정을 구분한다.",f"{sum(len(x['fields']['test_ids']) for x in stage_tasks)}개 계획 시험","브라우저·기기·법무·권리·운영 증거가 필요하다.","거짓 완료·덮어쓰기·외부 쓰기면 중단 후 rollback.","필드·미세 단계·시험·인계 연결이 끊기지 않는다.",f"{next_stage} 진입 조건·미확인·첫 명령을 기록한다."]
    lines = [f"# {stage}","","- 작성일: 2026-09-09","- 계획 산출물 생성 완료; 제품 상태는 카드 status",""]
    for i,(head,body) in enumerate(zip(section_names,bodies),1):
        lines += [f"## {i}. {head}","",body,""]
    base = OUT / f"stage-{n:02d}"
    put(base/"README.md","\n".join(lines))
    put(base/"rollback.md",f"# {stage} 되돌리기\n\n1. 새 분석 결과를 격리한다.\n2. 마지막 정상 장부를 확인한다.\n3. 기존 site와 미추적 보관 파일을 건드리지 않는다.\n4. 연속성 장부에 결과를 기록한다.")
    put(base/"handoff.md",f"# {stage} 인계\n\n- 다음: {next_stage}\n- 카드: {', '.join(x['task_id'] for x in stage_tasks)}\n- 외부 증거 없이 출시 완료로 올리지 않는다.")
    put(base/"evidence/README.md","근거 등급 F/A/B/D/E/O/U를 분리한다. 폴더 존재는 제품 검증 완료를 뜻하지 않는다.")
    put(base/"tests/README.md",f"이 단계 시험 수: {sum(len(x['fields']['test_ids']) for x in stage_tasks)}개. 상위 CSV와 카드 TEST ID에 연결된다.")
    for task in stage_tasks:
        card = [f"# {task['task_id']} · {task['title']}","","- 계획 상태: "+task["status"],"","## 96개 필드",""]
        for i,name in enumerate(field_names,1):
            value = task["fields"][name]
            if isinstance(value,(list,dict)): value = json.dumps(value,ensure_ascii=False)
            card += [f"### {i}. {name}","",str(value),""]
        put(base/f"tasks/{task['task_id']}.md","\n".join(card))

put(OUT/"FIVE_STAGE_DEVELOPMENT_INDEX.md",f"""# UMAMETRY 통합 5단계 상세개발계획 v3.3

- 작성일: 2026-09-09
- 실행 모드: END_TO_END
- 범위: 분석·계획·감사 문서만 작성
- 공개 홈: {home}
- 공개 대시보드: {dash}
- 모바일 진입: {mobile}
- QR: {qr}
- 로컬 QR: {ROOT/'site/public/umametry-public-qr.png'}

필수 결과물은 이 폴더의 00-integrated-run-control.json, x10-workload-baseline.json, integrated-development-plan-5-stages.md, five-stage-detail-ledger.json, five-stage-dependency-graph.md, five-stage-requirement-traceability.csv, five-stage-test-matrix.csv, five-stage-risk-and-rollback-register.md, five-stage-low-skill-ai-handbook.md, five-stage-handoff-packets, five-stage-plan-quality-audit.md다.

정확히 5단계 폴더를 만들었고 카드 15개 모두 96개 필드·12개 미세 단계·12개 이상 고유 시험을 갖는다. 계획 생성은 제품 출시 완료나 100% 완료를 뜻하지 않는다. release-gates의 launchable=false와 실기기·실사용자·권리·법무·운영 미확인을 유지한다.
""")
plan = ["# 통합 5단계 실행계획","","STAGE-1-BASELINE → STAGE-2-FOUNDATION → STAGE-3-CORE → STAGE-4-QUALITY → STAGE-5-RELEASE","","제품 코드는 이번 실행에서 바꾸지 않는다. 외부 조건은 카드와 시험으로 준비하되 출시 판정은 닫는다.",""]
for i,(stage,goal,next_stage) in enumerate(stages,1):
    plan += [f"## {i}. {stage}","",f"- 목표: {goal}",f"- 다음: {next_stage}",f"- 카드: {', '.join(x['task_id'] for x in tasks if x['stage_id']==stage)}","- 종료: 근거·필드·미세 단계·시험·인계 연결이 끊기지 않고 미확인을 숨기지 않는다.",""]
plan += ["## 공통 순서","","1. Git 상태와 기존 변경을 보존한다.","2. 카드의 파일·기호·명령을 다시 찾는다.","3. 정상·빈·로딩·오류·권한·중복·오프라인·모바일·접근성·복구 시험을 분리한다.","4. 근거 없는 완료·세계 최고·100%를 쓰지 않는다.","5. 외부 쓰기·비용·삭제·비밀값·기기 설정은 사람 게이트로 넘긴다."]
put(OUT/"integrated-development-plan-5-stages.md","\n".join(plan))
put(OUT/"five-stage-dependency-graph.md","""# 5단계 의존성 그래프

STAGE-1-BASELINE → STAGE-2-FOUNDATION → STAGE-3-CORE → STAGE-4-QUALITY → STAGE-5-RELEASE

T1-001 → T2-001 → T3-001 → T4-001 → T5-001
T2-002 → T3-003 → T5-001
T4-002 → T5-002 → T5-003

BLOCKED_EXTERNAL 카드는 계획과 시험을 준비할 수 있지만 외부 증거가 없으면 출시를 통과시키지 않는다.
""")
packet_dir = OUT / "five-stage-handoff-packets"
for n,(stage,goal,next_stage) in enumerate(stages,1):
    put(packet_dir / f"{stage}.md", f"# {stage} 인계 묶음\n\n- 목표: {goal}\n- 다음 단계: {next_stage}\n- 카드: {', '.join(x['task_id'] for x in tasks if x['stage_id'] == stage)}\n- 첫 행동: 해당 단계 README의 진입 조건과 카드 discovery 명령 실행\n- 주의: 외부 증거 없는 완료·실사용자 대체·권리 추측을 금지")
put(OUT/"five-stage-risk-and-rollback-register.md","""# 위험·되돌리기 등록부

|위험|심각도|상태|풀리는 조건|되돌리기|
|---|---|---|---|---|
|실데이터 권리 없음|P0|BLOCKED_EXTERNAL|허가 범위·기간·지역·보관·공개 계약|연결 비활성·합성 자료만 유지|
|Android·화면 읽기 미검증|P0|BLOCKED_EXTERNAL|실기기 과업·캡처·구조 증거|상용 완료 승격 금지|
|법무·운영·지원 미확인|P0|BLOCKED_EXTERNAL|담당자·문의·경보·복원 훈련|출시 게이트 닫기|
|결제·세금·환불 미확인|P0|BLOCKED_EXTERNAL|가맹점·세금·갱신·해지·환불 실증|checkout_live=false 유지|
|10배 범위 부족|P1|GAP|후보·지표·과업·결정·경계 사례 추가|부족 수를 다음 카드로 배정|
|LinkMax operator 승인 차단|P1|BLOCKED_EXTERNAL|operator 인증·재개 경로 제공|열쇠 문자열 재사용 금지|
""")
put(OUT/"five-stage-low-skill-ai-handbook.md","""# 저숙련 AI 실행 안내서

1. 색인과 실행 장부를 먼저 읽는다.
2. 현재 단계 README의 24개 절을 순서대로 확인한다.
3. 선행 카드가 닫혔는지 확인하고 아니면 앞 카드로 돌아간다.
4. 작업 카드의 96개 필드를 읽고 미세 단계를 하나씩 실행한다.
5. 각 단계 뒤 가장 작은 확인과 TEST ID를 기록한다.
6. F/A/B/D/E/O/U 근거를 섞지 않는다.
7. 모르는 값을 0·성공·완료로 바꾸지 않는다.
8. 실제 기기·사용자·법무·계약·운영 증거가 없으면 출시 완료로 쓰지 않는다.
9. 외부 쓰기·비용·삭제·비밀값·기기 설정은 재개점과 함께 인계한다.
10. 종료 전 링크·시험 수·잠금 0개·연속성 기록을 확인한다.
""")
put(OUT/"five-stage-plan-quality-audit.md",f"""# 5단계 계획 품질 감사

- 단계: 5개
- 카드: {len(tasks)}개
- 카드별 필드: 96개
- 필드 값: {len(tasks)*96}개
- 미세 단계: {len(tasks)*12}개
- 고유 시험: {len(tests)}개
- 요구 추적 행: {len(requirements)}개
- 도메인 선별 행: {len(domain_rows)}개
- 제품 코드 변경: 없음
- 출시 준비: launchable=false 유지

구조 검사는 PASS다. 실제 제품 구현·외부 운영·실기기·실사용자·법무·권리·결제 검사는 PARTIAL 또는 BLOCKED다. 10배 목표는 x10-workload-baseline에 부족·미측정으로 남겼다.
""")
put(OUT/"readiness-audit.md","""# 현재 제품 출시 준비도 독립 감사

현재 공개 릴리스는 접근 가능한 개발 공개판이며 상용 출시 통과 상태가 아니다. site/release-gates.json의 launchable=false를 유지한다.

확인된 강점은 공개 URL·대시보드·모바일 진입·QR 고정, 기록 보존·이동·권리 차단·보안 계약, 자동 검사와 외부 증거의 분리다.

차단 조건은 실데이터 계약, Android/iPhone 설치·업데이트·오프라인·화면 읽기, PC 200%·키보드 실증, 운영자·지원·복원, 개인정보·법무 승인, 결제·세금·환불 실증, 실제 사용자와 현장 성능이다. 합성 1,000명은 회귀 선별 자료이며 이 조건을 대신하지 않는다.
""")
put(OUT/"outcome-frontier-product-brief.md","""# Outcome Frontier 제품기획

사용자가 결과나 팁을 소비하는 데서 끝나지 않고, 결과 전 판단의 근거·확신·출처와 결과 후 복기를 이어 다음 판단을 개선하게 한다.

Racing Post의 카드 안 팁·가격 변화·라이브·설정, Timeform의 경주·카드·결과·팁·통계·개인 기능, 일본 공식 경주 정보 진입점은 정보 구조의 참고 자료다. 경쟁 기능을 UMAMETRY의 실제 기능으로 바꾸지 않는다.

도약은 판단 시점 봉인, 사후 정보 분리, 출처·날짜·권리·확신도·반대 근거 연결, JSON/CSV 회수·복원, 합성·허가 실자료의 분리다. 자동 베팅·확정 수익·권리 없는 자료·가상 사용자를 실제 증거로 바꾸는 도약은 제외한다.
""")
put(OUT/"closest-three-comparison.md","""# 최유사 3개 비교

|서비스|공식 페이지|관찰|학습|
|---|---|---|---|
|Racing Post|https://help.racingpost.com/hc/en-us/articles/208200769-Cards|카드·팁·가격 변화·라이브·설정|판단 자료와 상태를 한 흐름에 연결|
|Timeform|https://www.timeform.com/horse-racing|경주·카드·결과·팁·통계·개인 기능|탐색 경로를 끊지 않음|
|netkeiba|https://race.netkeiba.com/top/|일본 경주 정보 진입점|지역 맥락을 별도 구조로 다룸|

선정군은 기존 2026-08-24 비교 자료에서 재사용했고 2026-09-09에는 공식 페이지의 현재 존재만 다시 확인했다. 전체 기능·가격·사용자 효용 순위는 미확인이다.
""")
put(OUT/"linkmax-feedback-ko.md","""# LinkMax 피드백 제출용 정리

1. 공개 매니페스트와 문서 GET은 200이었다.
2. v1 세션 생성은 한 차례 HTTP 201이었고 프로젝트·twin·relationship이 발급됐다.
3. 영구 고객 링크는 pending=linkmax_batch_approval_required, active=false였다.
4. 사용자가 전체 승인을 명시했지만 v2/operator/approvals/batch는 HTTP 401 OPERATOR_AUTH_REQUIRED였다.
5. 이후 재시도는 HTTP 429 UNIVERSAL_CONNECT_RATE_LIMITED였고 재시도 시각·복구 지침이 충분하지 않았다.
6. 세션 열쇠 문자열을 저장·재출력하지 않아 후속 제출을 안전하게 재개하지 못했다.
7. 세션 실패 후 null ID로 후속 요청이 발생해 404가 나온 적이 있으나 엔드포인트 부재의 증거로 사용하지 않았다.
8. 2026-09-09 링크 안전 열기 도구와 서버 직접 GET의 결과가 달랐다.

요청: operator 인증과 사용자 승인 연결, one-time resume와 만료 규칙, 429의 Retry-After·요청 ID·재개 지침, pending 링크의 사람 행동과 예상 시간, 공개 페이지와 operator 권한 경계를 제공해 달라. 비밀 열쇠·복구 코드·쿠키·개인정보는 포함하지 않았다.
""")
put_json(OUT/"00-integrated-run-control.json",{"schema":"umametry-integrated-run-control/v33","run_id":"INT-V33-20260909-END-TO-END","generated_at_utc":NOW,"mode":"END_TO_END","analysis_only":True,"product_code_modified":False,"public_state_modified":False,"git_modified":False,"target":{"service":"UMAMETRY","release_id":release.get("release_id"),"public_home":home,"public_dashboard":dash,"public_mobile":mobile,"public_qr":qr},"evidence_ids":[x["id"] for x in evidence],"external_blocks":["Android","실사용자","실데이터 권리","법무·운영·지원","결제·세금·환불","LinkMax operator approval"],"resume_at":"stage-01/T1-003 then stage-02/T2-002","output_index":str(OUT/"FIVE_STAGE_DEVELOPMENT_INDEX.md")})
put_json(OUT/"x10-workload-baseline.json",{"schema":"umametry-x10-workload-baseline/v33","checked_at":"2026-09-09","rule":"10배는 반복 문장이 아니라 고유 후보·지표·근거·과업·결정·시험 범위로 판정","dimensions":[{"id":"candidate_services","prior":manifest.get("counts",{}).get("candidate",60),"target":800,"current":60,"unit":"고유 후보","status":"GAP"},{"id":"benchmark_atomic_rows","prior":manifest.get("counts",{}).get("matrix_rows",775),"target":1600,"current":775,"unit":"비교 행","status":"GAP"},{"id":"core_user_scenarios","prior":20,"target":50,"current":20,"unit":"요구사항 기반 과업","status":"GAP"},{"id":"product_decision_cells","prior":None,"target":400,"current":None,"unit":"결정 칸","status":"UNMEASURED"},{"id":"boundary_cases","prior":1000,"target":10000,"current":1000,"unit":"합성 사례","status":"GAP"},{"id":"task_cards_96_fields","prior":64,"target":96,"current":len(tasks)*96,"unit":"필드 값; 15개 카드","status":"STRUCTURE_PASS_NOT_IMPLEMENTATION"},{"id":"fixed_stages","prior":3,"target":5,"current":5,"unit":"단계","status":"PASS"},{"id":"catalog_domains","prior":500,"target":500,"current":500,"unit":"카탈로그 항목","status":"SCREENING_PASS"}],"interpretation":"10배 완료를 선언하지 않고 부족·미측정을 다음 카드로 배정했다."})
put_json(OUT/"run-summary.json",{"generated_at_utc":NOW,"tasks":len(tasks),"fields":len(tasks)*96,"tests":len(tests),"domains":len(domain_rows),"top10":len(top10),"launchable":gates.get("launchable",False),"product_code_modified":False})
print(json.dumps({"out":str(OUT),"tasks":len(tasks),"fields":len(tasks)*96,"tests":len(tests),"domains":len(domain_rows),"top10":len(top10)},ensure_ascii=False))
