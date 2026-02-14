#!/usr/bin/env python3
"""世界、在庫切れ - CLI game

Play flow:
1) 消滅ゲーム（必要5項目）
2) 国家欠損 -> 空札色を決定
3) 世界、在庫切れ（5ターン）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random

COLORS = {
    "R": "🟥誇り",
    "B": "🟦信頼",
    "Y": "🟨暇",
}

STAGES_NEED = ["人類に必要", "日本に必要", "京都に必要", "家に必要", "かばんに必要"]

WEAKNESS_HINTS = {
    "R": ["体面", "序列", "権威", "威圧", "武勇", "格", "上下"],
    "B": ["情報", "交流", "観光", "通信", "文化", "メディア", "ネット"],
    "Y": ["昼夜", "時間", "余裕", "生活", "体力", "回復", "眠り"],
}


@dataclass
class Nation:
    name: str
    lost_items: List[str] = field(default_factory=list)
    weakness_color: Optional[str] = None
    past_cards: List[str] = field(default_factory=list)


@dataclass
class WorldState:
    score: Dict[str, int] = field(default_factory=lambda: {"R": 0, "B": 0, "Y": 0})


def ask(prompt: str, valid: Optional[List[str]] = None) -> str:
    while True:
        val = input(prompt).strip()
        if not val:
            continue
        if valid and val not in valid:
            print(f"入力は {valid} のいずれかで。")
            continue
        return val


def choose_card(nation: Nation, turn: int, opponent: Nation) -> Tuple[str, str]:
    print(f"\n[{nation.name}] ターン{turn} の選択")
    print("  色: R=🟥誇り / B=🟦信頼 / Y=🟨暇")
    if turn <= 3:
        color = ask("  出す色 (R/B/Y): ", ["R", "B", "Y"])
    else:
        print(f"  外交フェーズ: 相手({opponent.name})の過去3枚から借りる")
        print(f"  相手の過去: {' '.join(COLORS[c] for c in opponent.past_cards) if opponent.past_cards else '(なし)'}")
        while True:
            color = ask("  借りて出す色 (R/B/Y): ", ["R", "B", "Y"])
            if color in opponent.past_cards:
                break
            print("  その色は相手の過去3枚にないため借りられません。")
    phrase = ask("  一言（短く）: ")
    if len(phrase) > 20:
        print("  長文判定 -> このターンは🟨暇扱いに変更")
        color = "Y"
    return color, phrase


def elimination_phase(a: Nation, b: Nation) -> None:
    print("\n=== 第一部：消滅ゲーム ===")
    used_words = set()
    for stage in STAGES_NEED:
        print(f"\n--- {stage} ---")
        for n in (a, b):
            while True:
                word = ask(f"{n.name} の回答（名詞1語）: ")
                if word in used_words:
                    print("  既出ワードです。別の語を入力してください。")
                    continue
                used_words.add(word)
                n.lost_items.append(word)
                break

    print("\n🏯🏰 城を倒す！ 消滅宣言！")
    for n in (a, b):
        print(f"{n.name}帝国から、{', '.join(n.lost_items)} が……＼消滅しました💥／")


def decide_weakness(n: Nation, opponent: Nation) -> None:
    print(f"\n[{n.name}] 国家欠損を決定")
    for i, item in enumerate(n.lost_items, 1):
        print(f"  {i}. {item}")

    while True:
        idx_raw = ask("いちばん痛い番号を選択: ")
        if idx_raw.isdigit():
            idx = int(idx_raw)
            break
        print("数字で入力してください。")

    idx = max(1, min(idx, len(n.lost_items))) - 1
    chosen = n.lost_items[idx]
    print(f"選択: {chosen}")

    print("弱点色を選んでください（目安）:")
    for k, hints in WEAKNESS_HINTS.items():
        print(f"  {k}: {COLORS[k]} <- {', '.join(hints)}")
    weakness = ask("弱点色 (R/B/Y): ", ["R", "B", "Y"])

    print(f"{opponent.name} は1回だけ差し替え要求できます。")
    veto = ask(f"{opponent.name} 差し替え要求しますか？ (y/n): ", ["y", "n"])
    if veto == "y":
        weakness = ask("差し替え後の弱点色 (R/B/Y): ", ["R", "B", "Y"])

    n.weakness_color = weakness
    print(f"=> {n.name} の空札色は {COLORS[weakness]}")


def score_turn(world: WorldState, a: Nation, b: Nation, c1: str, c2: str, twist: bool) -> None:
    if c1 != c2:
        print("別色なので変化なし。")
        return

    color = c1
    if a.weakness_color == color or b.weakness_color == color:
        print(f"{COLORS[color]} はどちらかの空札。共鳴したが加点なし。")
        return

    if twist:
        nxt = {"R": "B", "B": "Y", "Y": "R"}[color]
        world.score[nxt] += 1
        print(f"ねじれ判定！ {COLORS[color]} 共鳴 -> {COLORS[nxt]} +1")
    else:
        world.score[color] += 1
        print(f"共鳴成立！ {COLORS[color]} +1")


def main_game(a: Nation, b: Nation) -> None:
    print("\n=== 第二部：世界、在庫切れ（基本） ===")
    world = WorldState()

    coin = random.choice(["表", "裏"])
    print(f"事件コイントス（ターン3後適用）: {coin}")

    for turn in range(1, 6):
        print(f"\n===== ターン {turn} =====")
        ca, pa = choose_card(a, turn, b)
        cb, pb = choose_card(b, turn, a)
        if turn <= 3:
            a.past_cards.append(ca)
            b.past_cards.append(cb)

        print(f"{a.name}: {COLORS[ca]}「{pa}」")
        print(f"{b.name}: {COLORS[cb]}「{pb}」")

        twist = (turn == 4 and coin == "裏")
        score_turn(world, a, b, ca, cb, twist)
        print(f"在庫: 🟥{world.score['R']} / 🟦{world.score['B']} / 🟨{world.score['Y']}")

    s = world.score
    mx = max(s.values())
    winners = [k for k, v in s.items() if v == mx]
    if len(winners) > 1:
        end = "白紙合意エンド"
    else:
        end = {
            "R": "開戦エンド",
            "B": "同盟エンド",
            "Y": "内部崩壊エンド",
        }[winners[0]]

    print("\n=== 結果 ===")
    print(f"最終在庫: 🟥{s['R']} / 🟦{s['B']} / 🟨{s['Y']}")
    print(f"エンド: {end}")


def main() -> None:
    print("世界、在庫切れ CLI")
    n1 = Nation(ask("国名1: "))
    n2 = Nation(ask("国名2: "))

    elimination_phase(n1, n2)
    decide_weakness(n1, n2)
    decide_weakness(n2, n1)

    main_game(n1, n2)


if __name__ == "__main__":
    main()
