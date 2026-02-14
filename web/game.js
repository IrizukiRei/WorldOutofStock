const stages = ["①人類", "②日本", "③京都", "④家", "⑤かばん"];
const colors = { R: "🟥誇り", B: "🟦信頼", Y: "🟨暇" };
const nextColor = { R: "B", B: "Y", Y: "R" };

const state = {
  stageIdx: 0,
  seen: new Set(),
  aItems: [],
  bItems: [],
  weak: { A: "R", B: "B" },
  turn: 1,
  scores: { R: 0, B: 0, Y: 0 },
  past: { A: [], B: [] },
  twistTurn4: false,
  tossed: false,
};

const $ = (id) => document.getElementById(id);

function renderElimination() {
  $("stageLabel").textContent = `現在: ${stages[state.stageIdx]}`;
  $("elimLog").textContent = `A国: ${state.aItems.join(", ")}\nB国: ${state.bItems.join(", ")}`;
}

$("addItems").onclick = () => {
  const a = $("aItem").value.trim();
  const b = $("bItem").value.trim();
  if (!a || !b) return alert("両方入力してください。");
  if (state.seen.has(a) || state.seen.has(b)) return alert("重複語は禁止です。");
  state.seen.add(a); state.seen.add(b);
  state.aItems.push(a); state.bItems.push(b);
  $("aItem").value = ""; $("bItem").value = "";
  state.stageIdx += 1;
  if (state.stageIdx >= 5) {
    $("elimination").classList.add("hidden");
    $("inheritance").classList.remove("hidden");
  } else {
    renderElimination();
  }
};

$("startMain").onclick = () => {
  state.weak.A = $("aWeak").value;
  state.weak.B = $("bWeak").value;
  $("inheritance").classList.add("hidden");
  $("mainGame").classList.remove("hidden");
  renderTurn();
};

function normalizeCard(card, text) {
  return text.length > 12 ? "Y" : card;
}

function renderTurn() {
  $("turnLabel").textContent = `Turn ${state.turn}/5 ${state.turn <= 3 ? "(内政)" : "(外交)"}`;
  $("score").textContent = `在庫: ${colors.R}=${state.scores.R} / ${colors.B}=${state.scores.B} / ${colors.Y}=${state.scores.Y}`;
}

function addScore(color, weakA, weakB) {
  if (color === weakA || color === weakB) return `${colors[color]}は空札で+0`;
  state.scores[color] += 1;
  return `${colors[color]} +1`;
}

function endMessage() {
  const entries = Object.entries(state.scores).sort((a, b) => b[1] - a[1]);
  if (entries[0][1] === entries[1][1]) return "白紙合意エンド";
  return entries[0][0] === "R" ? "開戦エンド" : entries[0][0] === "B" ? "同盟エンド" : "内部崩壊エンド";
}

$("playTurn").onclick = () => {
  let aCard = $("aCard").value;
  let bCard = $("bCard").value;
  const aText = $("aText").value.trim();
  const bText = $("bText").value.trim();
  if (!aText || !bText) return alert("短文を入力してください。");

  aCard = normalizeCard(aCard, aText);
  bCard = normalizeCard(bCard, bText);

  if (state.turn <= 3) {
    state.past.A.push(aCard);
    state.past.B.push(bCard);
  } else {
    if (!state.past.B.includes(aCard) || !state.past.A.includes(bCard)) {
      return alert("外交ターンは相手の過去3枚から選んでください。");
    }
  }

  let log = `A:${colors[aCard]}「${aText}」 / B:${colors[bCard]}「${bText}」\n`;

  if (state.turn === 3 && !state.tossed) {
    state.twistTurn4 = Math.random() < 0.5;
    state.tossed = true;
    log += state.twistTurn4 ? "事件: ねじれ判定ON（Turn4のみ）\n" : "事件なし\n";
  }

  if (aCard === bCard) {
    if (state.turn === 4 && state.twistTurn4) {
      const shifted = nextColor[aCard];
      log += `ねじれ発動: ${colors[aCard]}共鳴→${addScore(shifted, state.weak.A, state.weak.B)}`;
    } else {
      log += `共鳴成立: ${addScore(aCard, state.weak.A, state.weak.B)}`;
    }
  } else {
    log += "不共鳴: 変化なし";
  }

  $("turnLog").textContent = log;
  $("aText").value = ""; $("bText").value = "";

  state.turn += 1;
  if (state.turn > 5) {
    $("playTurn").disabled = true;
    $("turnLabel").textContent = `ゲーム終了: ${endMessage()}`;
  }
  renderTurn();
};

renderElimination();
