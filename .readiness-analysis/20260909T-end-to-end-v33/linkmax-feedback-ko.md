# LinkMax 피드백 제출용 정리

1. 공개 매니페스트와 문서 GET은 200이었다.
2. v1 세션 생성은 한 차례 HTTP 201이었고 프로젝트·twin·relationship이 발급됐다.
3. 영구 고객 링크는 pending=linkmax_batch_approval_required, active=false였다.
4. 사용자가 전체 승인을 명시했지만 v2/operator/approvals/batch는 HTTP 401 OPERATOR_AUTH_REQUIRED였다.
5. 이후 재시도는 HTTP 429 UNIVERSAL_CONNECT_RATE_LIMITED였고 재시도 시각·복구 지침이 충분하지 않았다.
6. 세션 열쇠 문자열을 저장·재출력하지 않아 후속 제출을 안전하게 재개하지 못했다.
7. 세션 실패 후 null ID로 후속 요청이 발생해 404가 나온 적이 있으나 엔드포인트 부재의 증거로 사용하지 않았다.
8. 2026-09-09 링크 안전 열기 도구와 서버 직접 GET의 결과가 달랐다.

요청: operator 인증과 사용자 승인 연결, one-time resume와 만료 규칙, 429의 Retry-After·요청 ID·재개 지침, pending 링크의 사람 행동과 예상 시간, 공개 페이지와 operator 권한 경계를 제공해 달라. 비밀 열쇠·복구 코드·쿠키·개인정보는 포함하지 않았다.
