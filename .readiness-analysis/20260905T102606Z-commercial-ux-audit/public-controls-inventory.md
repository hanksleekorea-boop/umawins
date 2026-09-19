# 공개 경로·초기 조작 목록

HTTP 화면 내용 수집이며 브라우저 클릭/자바스크립트 실행 시험이 아니다. 버튼 숫자는 초기 서버 HTML의 button 요소만으로, 링크·조건부 버튼·로그인 뒤 기능을 모두 포괄하지 않는다. disabled만으로 결함이라고 판정하지 않는다. 전체 링크와 입력란은 원본 JSON에 남겼다.

|경로|HTTP|초기 버튼 및 상태|판정 한계|
|---|---:|---|---|
|/|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/m/|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/records|200|内容を確認する (활성)|클릭·입력 결과 미검증|
|/review|200|絞り込む (활성)|클릭·입력 결과 미검증|
|/calibration|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/analysis|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/explanations|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/learn|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/pro-tools|200|計算JSONを保存 (활성)<br>資料を保存 (비활성)|클릭·입력 결과 미검증|
|/onboarding|200|理由付きの開始経路を保存 (활성)<br>今はスキップ (활성)|클릭·입력 결과 미검증|
|/account|200|Googleで続ける (비활성)<br>この端末に明示保存 (활성)<br>共有する (활성)|클릭·입력 결과 미검증|
|/sync|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/data-transfer|200|完全なJSONを保存 (활성)<br>CSV要約を保存 (활성)|클릭·입력 결과 미검증|
|/privacy-controls|200|この端末で同期を許可 (활성)<br>同意を取り消す (비활성)<br>この端末で匿名測定を許可 (활성)<br>匿名測定の同意を取り消す (비활성)<br>削除前の範囲を固定 (활성)|클릭·입력 결과 미검증|
|/wellbeing|200|上限を保存 (활성)<br>休止を開始 (활성)|클릭·입력 결과 미검증|
|/install|200|この端末に追加 (비활성)|클릭·입력 결과 미검증|
|/help|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/support|200|端末内で確認資料を作る (활성)|클릭·입력 결과 미검증|
|/status|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/trust|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/terms|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/privacy|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/accessibility|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/compatibility|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/commercial-readiness|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/monetization|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/offer|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/entitlements|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/operations|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/data-policy|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/ads-readiness|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/dashboard|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/manifest.json|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/robots.txt|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/sitemap.xml|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|
|/ads.txt|404|버튼 없음 / 링크·자산 별도|승인 정보 없는 닫힘 상태; 고장으로 단정 안 함|
|/umametry-public-qr.png|200|버튼 없음 / 링크·자산 별도|클릭·입력 결과 미검증|

→ 이 그림의 뜻: 실제로 확인한 공개 응답과 초기 버튼을 목록화했으며, HTTP 성공을 기능 성공으로 확장하지 않았다.

## 입력 위치가 없는 링크

- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /analysis · この資料をもとに理由を記録する → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
- /learn · 記録で試す → → /records#record-form
