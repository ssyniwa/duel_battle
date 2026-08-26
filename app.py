import random
import streamlit as st

# --- ページ設定 ---
st.set_page_config(
    page_title="Tactical Duel Battle - Complete",
    layout="wide",
    page_icon="⚔️",
)

# --- ゲーム状態の初期化 ---
if "initialized" not in st.session_state:
  st.session_state.initialized = True

  # プレイヤーキャラ6体 (3x2配置などを想定、左側エリア)
  st.session_state.players = [
      {
          "id": i,
          "name": f"戦士 {i+1}",
          "hp": 60,
          "max_hp": 60,
          "pos": (i % 3, i // 3),  # (row, col) [col: 0 or 1]
          "cards": [
              {
                  "type": "move",
                  "name": "ステップ移動",
                  "dr": 0,
                  "dc": 1,
                  "desc": "前方に1マス移動します。",
              },
              {
                  "type": "attack",
                  "name": "直線上斬り",
                  "range": [(0, 1), (0, 2)],
                  "damage": 25,
                  "desc": "前方へ直線の強力なダメージ。",
              },
              {
                  "type": "attack",
                  "name": "ワイドスラッシュ",
                  "range": [(-1, 1), (0, 1), (1, 1)],
                  "damage": 15,
                  "desc": "前方の3マスを同時に攻撃します。",
              },
          ],
      }
      for i in range(6)
  ]

  # 敵キャラ6体 (右側エリア: col 4 or 5)
  st.session_state.enemies = [
      {
          "id": i,
          "name": f"ゴブリン {i+1}",
          "hp": 45,
          "max_hp": 45,
          "pos": (i % 3, 4 + (i // 3)),
          "damage": 12,
      }
      for i in range(6)
  ]

  st.session_state.turn_phase = (
      "player_turn"  # "player_turn" or "enemy_turn"
  )
  st.session_state.current_actor_idx = 0  # 現在行動するプレイヤーのインデックス
  st.session_state.battle_log = [
      "バトル開始！プレイヤー側のターンです。行動するキャラのカードを選んでください。"
  ]


def add_log(msg):
  st.session_state.battle_log.insert(0, msg)


# --- 勝利・敗北判定 ---
living_players = [p for p in st.session_state.players if p["hp"] > 0]
living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]

st.title("⚔️ タクティカル・デュエルバトル (完全版)")

if not living_enemies:
  st.success(
      "🎉 【勝利】すべての敵を撃破しました！おめでとうございます！"
  )
  if st.button("もう一度プレイする"):
    del st.session_state.initialized
    st.rerun()
  st.stop()

if not living_players:
  st.error("💀 【敗北】プレイヤーが全滅してしまいました…")
  if st.button("もう一度プレイする"):
    del st.session_state.initialized
    st.rerun()
  st.stop()

# --- 3×6 バトルフィールドの描画 ---
st.subheader("🗺️ 戦場マップ (3行 × 6列)")

grid = [["・" for _ in range(6)] for _ in range(3)]

# 敵の配置
for e in living_enemies:
  r, c = e["pos"]
  grid[r][c] = f"👹{e['name']}({e['hp']})"

# プレイヤーの配置
for p in living_players:
  r, c = p["pos"]
  is_current = (
      st.session_state.turn_phase == "player_turn"
      and living_players[
          st.session_state.current_actor_idx % len(living_players)
      ]["id"]
      == p["id"]
  )
  prefix = "👉" if is_current else "🛡️"
  grid[r][c] = f"{prefix}{p['name']}({p['hp']})"

st.table(grid)

# --- フェーズごとの処理 ---
if st.session_state.turn_phase == "player_turn":
  current_p = living_players[
      st.session_state.current_actor_idx % len(living_players)
  ]

  st.markdown(
      f"### 🛡️ 現在の行動キャラ: **{current_p['name']}** (HP:"
      f" {current_p['hp']}/{current_p['max_hp']})"
  )

  col1, col2 = st.columns([2, 1])

  with col1:
    st.markdown("#### 🃏 スキルカード選択（TCG風デザイン）")
    st.markdown(
        "使いたいカードのボタンを押してください。（攻撃カードは対象の敵を選んでから発動します）"
    )

    # 攻撃対象のセレクトボックスを先に用意
    enemy_options = {
        f"{e['name']} (位置: {e['pos']}, HP: {e['hp']})": e
        for e in living_enemies
    }
    selected_enemy_label = st.selectbox(
        "🎯 攻撃対象の敵を選択", list(enemy_options.keys())
    )
    target_enemy = enemy_options[selected_enemy_label]

    # HTML/CSSによるTCG風カード一覧の表示
    card_cols = st.columns(len(current_p["cards"]))

    for idx, card in enumerate(current_p["cards"]):
      with card_cols[idx]:
        # TCGカード風の見た目をHTMLで構築
        card_html = f"""
                <div style="
                    border: 2px solid #4A90E2;
                    border-radius: 8px;
                    padding: 10px;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    color: #333;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                    height: 160px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                ">
                    <div>
                        <div style="font-size: 11px; font-weight: bold; color: #555;">{'[移動]' if card['type']=='move' else '[攻撃]'}</div>
                        <div style="font-size: 14px; font-weight: bold; color: #111; margin-top: 2px;">{card['name']}</div>
                    </div>
                    <div style="font-size: 11px; color: #444; line-height: 1.2;">
                        {card['desc']}<br>
                        {'<b>威力:</b> ' + str(card['damage']) if card['type']=='attack' else ''}
                    </div>
                </div>
                """
        st.markdown(card_html, unsafe_allow_html=True)

        # カード使用ボタン
        if st.button("このカードを使う", key=f"card_{current_p['id']}_{idx}"):
          if card["type"] == "move":
            # 移動処理 (左方向や上下への移動も可、グリッド内 0〜5 に制限)
            pr, pc = current_p["pos"]
            nr, nc = pr + card["dr"], pc + card["dc"]
            # マップ範囲内かつ他キャラと被らないかチェック
            if 0 <= nr < 3 and 0 <= nc < 6:
              # マスの専有チェック
              occupied = any(
                  p["pos"] == (nr, nc) for p in st.session_state.players
              ) or any(e["pos"] == (nr, nc) for e in st.session_state.enemies)
              if not occupied:
                current_p["pos"] = (nr, nc)
                add_log(
                    f"🏃 {current_p['name']} は '{card['name']}' で"
                    f" ({nr}, {nc}) に移動した！"
                )
              else:
                add_log(
                    f"⚠️ そのマスには既にキャラクターが存在するため移動できません。"
                )
            else:
              add_log(
                  f"⚠️ マップの範囲外へは移動できません。"
              )

          elif card["type"] == "attack":
            # 攻撃処理
            pr, pc = current_p["pos"]
            er, ec = target_enemy["pos"]
            valid_hit = any(
                (pr + dr, pc + dc) == (er, ec) for dr, dc in card["range"]
            )

            if valid_hit:
              target_enemy["hp"] -= card["damage"]
              if target_enemy["hp"] < 0:
                target_enemy["hp"] = 0
              add_log(
                  f"✨ {current_p['name']} の '{card['name']}' が"
                  f" {target_enemy['name']} に命中！ {card['damage']} のダメージ！"
              )
            else:
              add_log(
                  f"❌ {card['name']} の攻撃範囲外です！(敵に届きませんでした)"
              )

          # ターン進行管理
          st.session_state.current_actor_idx += 1
          # 全プレイヤーが行動し終わったら敵のターンへ
          if st.session_state.current_actor_idx >= len(living_players):
            st.session_state.turn_phase = "enemy_turn"
            st.session_state.current_actor_idx = 0
            add_log(
                "🔄 プレイヤー全員の行動が終了しました。敵の反撃ターンに移行します！"
            )
          st.rerun()

  with col2:
    st.markdown("#### ⚙️ その他アクション")
    if st.button("このキャラの行動をパスする", use_container_width=True):
      add_log(f"💤 {current_p['name']} はその場で待機しました。")
      st.session_state.current_actor_idx += 1
      if st.session_state.current_actor_idx >= len(living_players):
        st.session_state.turn_phase = "enemy_turn"
        st.session_state.current_actor_idx = 0
        add_log("🔄 敵の反撃ターンに移行します！")
      st.rerun()

elif st.session_state.turn_phase == "enemy_turn":
  st.warning("⚠️ **敵の反撃ターン中**です。ボタンを押して敵の攻撃を進めましょう！")

  if st.button("👹 敵の攻撃を実行してプレイヤーターンに戻る", type="primary"):
    # 生きている敵がそれぞれランダムまたは一番近いプレイヤーを攻撃
    for e in living_enemies:
      if not living_players:
        break
      # 生きているプレイヤーの中からランダムで1体攻撃対象にする
      target_p = random.choice(living_players)
      target_p["hp"] -= e["damage"]
      if target_p["hp"] < 0:
        target_p["hp"] = 0
      add_log(
          f"💥 {e['name']} の反撃！ {target_p['name']} に"
          f" {e['damage']} のダメージ！"
      )
      # プレイヤーが倒れた場合の処理用リスト更新
      living_players = [p for p in st.session_state.players if p["hp"] > 0]

    # 敵のターン終了 -> プレイヤーターンへ復帰
    st.session_state.turn_phase = "player_turn"
    st.session_state.current_actor_idx = 0
    add_log("🛡️ 敵のターンが終了しました。プレイヤー側のターンです！")
    st.rerun()

# --- バトルログの表示 ---
st.markdown("---")
st.subheader("📜 バトルログ（直近の履歴）")
for log in st.session_state.battle_log[:6]:
  st.text(log)
