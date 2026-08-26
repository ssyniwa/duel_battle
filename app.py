import random
import streamlit as st

# --- ページ設定 ---
st.set_page_config(
    page_title="Tactical Duel Battle - Visual Edition",
    layout="wide",
    page_icon="⚔️",
)

# --- ゲーム状態の初期化 ---
if "initialized" not in st.session_state:
  st.session_state.initialized = True

  # プレイヤーキャラ6体 (3x2配置、左側エリア)
  st.session_state.players = [
      {
          "id": i,
          "name": f"戦士 {i+1}",
          "hp": 60,
          "max_hp": 60,
          "pos": (i % 3, i // 3),  # (row, col) [col: 0 or 1]
          # キャラごとのアバター画像（プレースホルダー）
          "img_url": (
              "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
              if i % 2 == 0
              else "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"
          ),
          "cards": [
              {
                  "type": "move",
                  "name": "ステップ移動",
                  "dr": 0,
                  "dc": 1,
                  "desc": "前方に1マス移動します。",
                  "img_url": "https://images.unsplash.com/photo-1516116216657-548af10f8b73?w=200",
              },
              {
                  "type": "attack",
                  "name": "直線上斬り",
                  "range": [(0, 1), (0, 2)],
                  "damage": 25,
                  "desc": "前方へ直線の強力なダメージ。",
                  "img_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=200",
              },
              {
                  "type": "attack",
                  "name": "ワイドスラッシュ",
                  "range": [(-1, 1), (0, 1), (1, 1)],
                  "damage": 15,
                  "desc": "前方の3マスを同時に攻撃します。",
                  "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=200",
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
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      }
      for i in range(6)
  ]

  st.session_state.turn_phase = "player_turn"
  st.session_state.current_actor_idx = 0
  st.session_state.battle_log = [
      "バトル開始！プレイヤー側のターンです。スキルカードを選択してください。"
  ]


def add_log(msg):
  st.session_state.battle_log.insert(0, msg)


# --- 勝利・敗北判定 ---
living_players = [p for p in st.session_state.players if p["hp"] > 0]
living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]

st.title("⚔️ タクティカル・デュエルバトル (画像ビジュアル版)")

if not living_enemies:
  st.success("🎉 【勝利】すべての敵を撃破しました！")
  if st.button("もう一度プレイする"):
    del st.session_state.initialized
    st.rerun()
  st.stop()

if not living_players:
  st.error("💀 【敗北】プレイヤーが全滅しました…")
  if st.button("もう一度プレイする"):
    del st.session_state.initialized
    st.rerun()
  st.stop()

# --- 3×6 バトルフィールドの視覚化 (カスタムHTMLグリッド) ---
st.subheader("🗺️ 戦場マップ (3行 × 6列)")

# 3x6の空マス配列を準備
grid_data = [["" for _ in range(6)] for _ in range(3)]

# 敵の配置をセット
for e in living_enemies:
  r, c = e["pos"]
  grid_data[r][
      c
  ] = f"""<div style="background-color: #ffebee; border: 2px solid #ef5350; border-radius: 6px; padding: 5px; text-align: center;">
        <img src="{e['img_url']}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">
        <div style="font-size: 11px; font-weight: bold; color: #c62828;">👹 {e['name']}</div>
        <div style="font-size: 10px; color: #d32f2f;">HP: {e['hp']}</div>
    </div>"""

# プレイヤーの配置をセット
for p in living_players:
  r, c = p["pos"]
  is_current = (
      st.session_state.turn_phase == "player_turn"
      and living_players[
          st.session_state.current_actor_idx % len(living_players)
      ]["id"]
      == p["id"]
  )
  border_color = "#2e7d32" if not is_current else "#ff9800"
  bg_color = "#e8f5e9" if not is_current else "#fff3e0"
  badge = "👉行動中" if is_current else "🛡️味方"

  grid_data[r][
      c
  ] = f"""<div style="background-color: {bg_color}; border: 2px solid {border_color}; border-radius: 6px; padding: 5px; text-align: center;">
        <img src="{p['img_url']}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">
        <div style="font-size: 11px; font-weight: bold; color: #2e7d32;">{p['name']}</div>
        <div style="font-size: 10px; color: #388e3c;">HP: {p['hp']} | {badge}</div>
    </div>"""

# HTMLテーブルとして3x6グリッドを描画
table_html = (
    '<table style="width:100%; border-collapse: collapse; text-align: center;">'
)
for r in range(3):
  table_html += "<tr>"
  for c in range(6):
    cell_content = (
        grid_data[r][c]
        if grid_data[r][c] != ""
        else '<div style="color: #ccc; padding: 15px;">・</div>'
    )
    table_html += f'<td style="border: 1px solid #ddd; width: 16.6%; vertical-align: middle; height: 90px;">{cell_content}</td>'
  table_html += "</tr>"
table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)
st.markdown("---")

# --- フェーズごとの処理 ---
if st.session_state.turn_phase == "player_turn":
  current_p = living_players[
      st.session_state.current_actor_idx % len(living_players)
  ]

  col_info, col_action = st.columns([1, 3])
  with col_info:
    st.markdown("### 👤 手番キャラ")
    st.image(current_p["img_url"], width=80)
    st.markdown(
        f"**{current_p['name']}**<br>HP: {current_p['hp']}/{current_p['max_hp']}",
        unsafe_allow_html=True,
    )

  with col_action:
    st.markdown("### 🎯 攻撃対象の敵を選択")
    enemy_options = {
        f"{e['name']} (位置: {e['pos']}, HP: {e['hp']})": e
        for e in living_enemies
    }
    selected_enemy_label = st.selectbox(
        "ターゲットを選択", list(enemy_options.keys())
    )
    target_enemy = enemy_options[selected_enemy_label]

  st.markdown("#### 🃏 スキルカード選択（画像付きTCGカード）")

  card_cols = st.columns(len(current_p["cards"]))

  for idx, card in enumerate(current_p["cards"]):
    with card_cols[idx]:
      # 画像つきTCGカードのデザイン (HTML)
      card_html = f"""
            <div style="
                border: 2px solid #3f51b5;
                border-radius: 10px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #333;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.15);
                overflow: hidden;
                height: 240px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                margin-bottom: 10px;
            ">
                <div>
                    <div style="background: #3f51b5; color: white; font-size: 10px; font-weight: bold; padding: 3px 6px; text-align: right;">
                        {'[移動]' if card['type']=='move' else '[攻撃]'}
                    </div>
                    <div style="padding: 6px;">
                        <div style="font-size: 13px; font-weight: bold; color: #1a237e; margin-bottom: 4px;">{card['name']}</div>
                        <img src="{card['img_url']}" style="width: 100%; height: 75px; object-fit: cover; border-radius: 4px;">
                    </div>
                </div>
                <div style="padding: 0 6px 6px 6px; font-size: 11px; color: #333; line-height: 1.2;">
                    {card['desc']}<br>
                    {'<b>威力:</b> ' + str(card['damage']) if card['type']=='attack' else ''}
                </div>
            </div>
            """
      st.markdown(card_html, unsafe_allow_html=True)

      # カード使用ボタン
      if st.button("このカードを使う", key=f"card_{current_p['id']}_{idx}"):
        if card["type"] == "move":
          pr, pc = current_p["pos"]
          nr, nc = pr + card["dr"], pc + card["dc"]
          if 0 <= nr < 3 and 0 <= nc < 6:
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
              add_log(f"⚠️ そのマスには既にキャラクターが存在します。")
          else:
            add_log(f"⚠️ マップの範囲外へは移動できません。")

        elif card["type"] == "attack":
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
            add_log(f"❌ {card['name']} の攻撃範囲外です（届きません）！")

        # ターン進行
        st.session_state.current_actor_idx += 1
        if st.session_state.current_actor_idx >= len(living_players):
          st.session_state.turn_phase = "enemy_turn"
          st.session_state.current_actor_idx = 0
          add_log(
              "🔄 プレイヤー全員の行動終了。敵の反撃ターンに移行します！"
          )
        st.rerun()

  if st.button("このキャラクターの行動をパスする"):
    add_log(f"💤 {current_p['name']} はその場で待機しました。")
    st.session_state.current_actor_idx += 1
    if st.session_state.current_actor_idx >= len(living_players):
      st.session_state.turn_phase = "enemy_turn"
      st.session_state.current_actor_idx = 0
      add_log("🔄 敵の反撃ターンに移行します！")
    st.rerun()

elif st.session_state.turn_phase == "enemy_turn":
  st.warning("⚠️ **敵の反撃ターン中**です。")
  if st.button("👹 敵の攻撃を実行してプレイヤーターンに戻る", type="primary"):
    for e in living_enemies:
      if not living_players:
        break
      target_p = random.choice(living_players)
      target_p["hp"] -= e["damage"]
      if target_p["hp"] < 0:
        target_p["hp"] = 0
      add_log(
          f"💥 {e['name']} の反撃！ {target_p['name']} に"
          f" {e['damage']} のダメージ！"
      )
      living_players = [p for p in st.session_state.players if p["hp"] > 0]

    st.session_state.turn_phase = "player_turn"
    st.session_state.current_actor_idx = 0
    add_log("🛡️ 敵のターンが終了しました。プレイヤー側のターンです！")
    st.rerun()

# --- バトルログ ---
st.markdown("---")
st.subheader("📜 バトルログ")
for log in st.session_state.battle_log[:5]:
  st.text(log)
