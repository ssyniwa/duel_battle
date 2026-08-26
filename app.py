import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Tactical Duel Battle", layout="wide", page_icon="⚔️"
)

# --- ゲーム状態の初期化 ---
if "initialized" not in st.session_state:
  st.session_state.initialized = True
  # プレイヤーキャラ6体 (位置: (row, col))
  st.session_state.players = [
    {
        "id": i,
        "name": f"戦士 {i+1}",
        "hp": 50,
        "max_hp": 50,
        "pos": (i % 3, i // 3),  # 左側の領域 (col 0-1)
        "skills": [
            {
                "name": "直線上斬り",
                "range": [(0, 1), (0, 2)],
                "damage": 25,
                "desc": "前方へ直線のダメージ",
            },
            {
                "name": "広範囲スラッシュ",
                "range": [(-1, 1), (0, 1), (1, 1)],
                "damage": 15,
                "desc": "前方の3マスを同時攻撃",
            },
        ],
    }
    for i in range(6)
  ]

  # 敵キャラ6体
  st.session_state.enemies = [
    {
        "id": i,
        "name": f"ゴブリン {i+1}",
        "hp": 40,
        "max_hp": 40,
        "pos": (i % 3, 4 + (i // 3)),  # 右側の領域 (col 4-5)
    }
    for i in range(6)
  ]

  st.session_state.current_actor_idx = 0  # 現在行動するプレイヤーのインデックス
  st.session_state.battle_log = ["バトル開始！味方のターンです。"]
  st.session_state.game_over = False


def add_log(msg):
  st.session_state.battle_log.insert(0, msg)


# --- メイン画面 ---
st.title("⚔️ タクティカル・デュエルバトル")
st.markdown(
    "左側のプレイヤー（6体）を順番に動かし、スキルカードを選んで右側の敵を全滅させよう！"
)

# 終了判定
living_players = [p for p in st.session_state.players if p["hp"] > 0]
living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]

if not living_enemies:
  st.success("🎉 プレイヤー側の勝利！すべての敵を倒しました！")
  if st.button("もう一度プレイ"):
    del st.session_state.initialized
    st.rerun()
  st.stop()

if not living_players:
  st.error("💀 敗北…プレイヤーが全滅しました。")
  if st.button("もう一度プレイ"):
    del st.session_state.initialized
    st.rerun()
  st.stop()


# --- 3×6 バトルフィールドの描画 ---
st.subheader("🗺️ 戦場 (3行 × 6列)")

# 3x6グリッドの作成
grid = [["・" for _ in range(6)] for _ in range(3)]

# 敵の配置を反映
for e in living_enemies:
  r, c = e["pos"]
  grid[r][c] = f"👹{e['name']}({e['hp']})"

# プレイヤーの配置を反映
for p in living_players:
  r, c = p["pos"]
  is_current = (
      living_players[st.session_state.current_actor_idx % len(living_players)][
          "id"
      ]
      == p["id"]
  )
  prefix = "👉" if is_current else "🛡️"
  grid[r][c] = f"{prefix}{p['name']}({p['hp']})"

# 表形式で表示
st.table(grid)



# --- ターン制・行動選択UI ---
current_p = living_players[
    st.session_state.current_actor_idx % len(living_players)
]

st.markdown(
    f"### 現在の行動キャラ: **{current_p['name']}** (HP: {current_p['hp']}/{current_p['max_hp']})"
)

col1, col2 = st.columns(2)

with col1:
  st.markdown("#### 🃏 スキルカード選択")
  selected_skill = None

  # スキルカードをボタン（またはカード風）で表示
  for idx, skill in enumerate(current_p["skills"]):
    if st.button(
        f"**{skill['name']}** (威力: {skill['damage']})\n\n{skill['desc']}",
        key=f"skill_{current_p['id']}_{idx}",
    ):
      selected_skill = skill

with col2:
  st.markdown("#### 🎯 攻撃対象の選択")
  enemy_options = {
      f"{e['name']} (位置: {e['pos']}, HP: {e['hp']})": e
      for e in living_enemies
  }
  selected_enemy_label = st.selectbox(
      "攻撃する敵を選んでください", list(enemy_options.keys())
  )
  target_enemy = enemy_options[selected_enemy_label]

# スキル実行ボタン
if selected_skill:
  pr, pc = current_p["pos"]
  er, ec = target_enemy["pos"]

  # 攻撃範囲の検証（簡易版：相対座標が一致するか）
  valid_hit = False
  for dr, dc in selected_skill["range"]:
    if (pr + dr, pc + dc) == (er, ec):
      valid_hit = True
      break

  if valid_hit:
    target_enemy["hp"] -= selected_skill["damage"]
    if target_enemy["hp"] < 0:
      target_enemy["hp"] = 0
    add_log(
        f"✨ {current_p['name']} が '{selected_skill['name']}' を"
        f" {target_enemy['name']} に命中させ、{selected_skill['damage']} のダメージ！"
    )
  else:
    add_log(
        f"❌ {selected_skill['name']} の攻撃範囲外です！(届きませんでした)"
    )

  # 次のキャラへターンを進める
  st.session_state.current_actor_idx = (
      st.session_state.current_actor_idx + 1
  ) % len(living_players)
  st.rerun()

# スキルを使わず「待機（パス）」する場合
if st.button("行動をパスする"):
  add_log(f"💤 {current_p['name']} は待機しました。")
  st.session_state.current_actor_idx = (
      st.session_state.current_actor_idx + 1
  ) % len(living_players)
  st.rerun()


# --- バトルログ ---
st.subheader("📜 バトルログ")
for log in st.session_state.battle_log[:5]:  # 直近5件を表示
  st.text(log)
