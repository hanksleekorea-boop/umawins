import { readFile, writeFile } from 'node:fs/promises';
const path = 'D:/Desktop/챗지피티프로젝트들/우마윈즈/site/content/learning-content.json';
const content = JSON.parse(await readFile(path, 'utf8'));
const updates = {
  'lesson-evidence': {
    body:'出所が示せる事実、そこから自分が考えたこと、まだ確認できないことを三つの欄に分けます。出所名だけで正しさや利用許可を保証するわけではありません。',
    exercise:'合成資料を一つ選び、事実・自分の解釈・未確認の条件を一行ずつ書く。',
    check:'三つの欄を混ぜずに、別の人が確認日と未確認条件を見つけられる。', duration:'5分', sourceRef:'content-policy-v1'
  },
  'lesson-counter': {
    body:'賛成材料だけを集めると、予想に都合のよい理由だけが残ります。先に「どの条件ならこの判断は外れるか」を探して反対根拠に書き、見つからなければ見つからないと表示します。',
    exercise:'同じ合成事例の反対条件を二つ選び、どの条件が事前に確認できるかを示す。',
    check:'反対根拠が一つ以上あり、確認前と確認後の時点が区別されている。', duration:'6分', sourceRef:'content-policy-v1'
  },
  'lesson-uncertainty': {
    body:'資料が古かったり標本が少なかったりすることは失敗ではなく、記録すべき条件です。分からないことを0点や失敗に変えず、結果が確認できるまで保留にします。',
    exercise:'例の中から古い資料と結果未確認を探し、それぞれ次に確認する行動を書く。',
    check:'未確認資料を結果不一致として自動集計せず、確認待ちとして説明する。', duration:'5分', sourceRef:'content-policy-v1'
  },
  'lesson-confidence': {
    body:'確信度は気持ちの強さではなく、明確に定義した命題が成立する可能性についての現在の見積もりです。基本の頻度や資料の限界が分からないときは、幅を持たせるか保留を選びます。',
    exercise:'同じ命題に60%と70%をそれぞれ付け、どの新しい資料が差を生んだかを書く。',
    check:'確信度の数字を的中や利益の保証と説明せず、命題と条件を一緒に話せる。', duration:'7分', sourceRef:'content-policy-v1'
  },
  'lesson-seal': {
    body:'プレビューと最終的な封印を分けます。最終確認の時刻、対象、命題、根拠、不確かさを確認して一度保存し、後から見つかった誤りは別の訂正として残します。',
    exercise:'入力内容をプレビューで変更して確定し、確定前後の時刻と原文・訂正の差を確認する。',
    check:'確定後の原文は変わらず、訂正・結果・振り返りが別の履歴として見える。', duration:'6分', sourceRef:'content-policy-v1'
  },
  'lesson-outcome': {
    body:'結果は一つの出来事で、判断の質は事前に使えた資料・反例・不確かさの記録から見ます。二つを同じ点数にせず、それぞれ説明します。',
    exercise:'当たった合成例と外れた合成例で、事前の根拠と結果後の情報の違いを示す。',
    check:'一つの結果だけで良い判断・悪い判断と断定しない。', duration:'8分', sourceRef:'content-policy-v1'
  },
  'lesson-review': {
    body:'振り返りは後悔を書く場ではなく、次にもう一度実行できる小さな規則を残す場です。変更なし、結果後に初めて分かった情報、判定対象外も正式な選択肢として残します。',
    exercise:'「次は___を確認してから決める」という文を一つ作り、次の記録で使うか選ぶ。',
    check:'規則が観察できる行動で、次の記録で適用・保留・破棄を追跡できる。', duration:'8分', sourceRef:'content-policy-v1'
  },
  'lesson-calibration': {
    body:'Brierは確率と結果の差を平均した一つの指標です。結果未確認や判定対象外を0として入れず、標本と期間が違う数値を順位のように比べません。',
    exercise:'p=0.7の合成命題が一致した場合.09、不一致の場合.49になることを計算し、分母を確認する。',
    check:'数値の横に標本数・期間・除外条件を説明し、小標本で結論を断定しない。', duration:'10分', sourceRef:'content-policy-v1'
  }
};
for (const lesson of content.lessons) Object.assign(lesson, updates[lesson.id]);
content.reviewedAt = '2026-09-05';
await writeFile(path, JSON.stringify(content, null, 2) + '\\n');
console.log('updated', content.lessons.length, 'lessons');
