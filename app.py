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

  # プレイヤーキャラ6体（異なる役職・クラスの構成）
  st.session_state.players = [
      {
          "id": 0,
          "name": "ナイト",
          "hp": 70,
          "max_hp": 70,
          "pos": (0, 1),
          "img_url": "images/knight.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "前進",
                  "dr": 0,
                  "dc": 1,
                  "desc": "前方に1マス移動します。",
                  "img_url": "images/knight.jpg",
              },
              {
                  "type": "attack",
                  "name": "シールドバッシュ",
                  "range": [(0, 1)],
                  "damage": 15,
                  "desc": "目前の敵を盾で殴りつける。",
                  "img_url": "images/knight_skill1.jpg",
              },
          ],
      },
      {
          "id": 1,
          "name": "ウォーリア",
          "hp": 60,
          "max_hp": 60,
          "pos": (1, 1),
          "img_url": "images/warrior.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "ダッシュ",
                  "dr": 0,
                  "dc": 1,
                  "desc": "前方に1マス素早く移動。",
                  "img_url": "images/warrior.jpg",
              },
              {
                  "type": "attack",
                  "name": "ワイドスラッシュ",
                  "range": [(-1, 1), (0, 1), (1, 1)],
                  "damage": 20,
                  "desc": "前方の3マスを同時に攻撃する。",
                  "img_url": "images/warrior_skill1.jpg",
              },
          ],
      },
      {
          "id": 2,
          "name": "ローグ",
          "hp": 45,
          "max_hp": 45,
          "pos": (2, 1),
          "img_url": "images/rogue.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "サイドステップ",
                  "dr": 1,
                  "dc": 0,
                  "desc": "真下に1マス素早く回り込む。",
                  "img_url": "images/rogue.jpg",
              },
              {
                  "type": "attack",
                  "name": "バックスタブ",
                  "range": [(0, 2)],
                  "damage": 30,
                  "desc": "2マス先の敵の急所を突く一撃。",
                  "img_url": "images/rogue_skill1.jpg",
              },
          ],
      },
      {
          "id": 3,
          "name": "メイジ",
          "hp": 35,
          "max_hp": 35,
          "pos": (0, 2),
          "img_url": "images/knight.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "テレポート歩行",
                  "dr": 0,
                  "dc": 1,
                  "desc": "位置を少し前方に調整する。",
                  "img_url": "https://images.unsplash.com/photo-1516116216657-548af10f8b73?w=200",
              },
              {
                  "type": "attack",
                  "name": "ファイアボール",
                  "range": [(0, 2), (0, 3)],
                  "damage": 35,
                  "desc": "遠く離れた2〜3マス先の敵を焼く。",
                  "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=200",
              },
          ],
      },
      {
          "id": 4,
          "name": "アーチャー",
          "hp": 40,
          "max_hp": 40,
          "pos": (1, 2),
          "img_url": "images/knight.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "バックペダル",
                  "dr": 0,
                  "dc": -1,
                  "desc": "後方に1マス下がって距離を取る。",
                  "img_url": "https://images.unsplash.com/photo-1516116216657-548af10f8b73?w=200",
              },
              {
                  "type": "attack",
                  "name": "スナイプショット",
                  "range": [(0, 2), (0, 3)],
                  "damage": 25,
                  "desc": "直線上の遠くの敵を正確に射抜く。",
                  "img_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=200",
              },
          ],
      },
      {
          "id": 5,
          "name": "プリースト",
          "hp": 50,
          "max_hp": 50,
          "pos": (2, 2),
          "img_url": "images/knight.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "聖者の歩み",
                  "dr": 0,
                  "dc": 1,
                  "desc": "前方に1マス進む。",
                  "img_url": "https://images.unsplash.com/photo-1516116216657-548af10f8b73?w=200",
              },
              {
                  "type": "attack",
                  "name": "ホーリースマイト",
                  "range": [(0, 1)],
                  "damage": 10,
                  "desc": "前方の敵へ神聖な光でダメージ。",
                  "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=200",
              },
          ],
      },
  ]
  # 敵キャラ6体（異なる役職・モンスターの構成）
  st.session_state.enemies = [
      {
          "id": 0,
          "name": "ゴブリン・ガード",
          "hp": 55,
          "max_hp": 55,
          "pos": (0, 3),
          "damage": 10,
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      },
      {
          "id": 1,
          "name": "ゴブリン・ソルジャー",
          "hp": 45,
          "max_hp": 45,
          "pos": (1, 3),
          "damage": 15,
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      },
      {
          "id": 2,
          "name": "ゴブリン・アサシン",
          "hp": 35,
          "max_hp": 35,
          "pos": (2, 3),
          "damage": 12,
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      },
      {
          "id": 3,
          "name": "ゴブリン・シャーマン",
          "hp": 30,
          "max_hp": 30,
          "pos": (0, 4),
          "damage": 14,
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      },
      {
          "id": 4,
          "name": "オーク・バーサーカー",
          "hp": 70,
          "max_hp": 70,
          "pos": (1, 4),
          "damage": 20,
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      },
      {
          "id": 5,
          "name": "ダーク・アーチャー",
          "hp": 35,
          "max_hp": 35,
          "pos": (2, 4),
          "damage": 16,
          "img_url": "https://images.unsplash.com/photo-1563089145-599997674d42?w=150",
      },
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

st.title("⚔️ タクティカル・デュエルバトル (標準関数画像版)")

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

# --- 3×6 バトルフィールドの描画 (Streamlitのカラムを活用) ---
st.subheader("🗺️ 戦場マップ (3行 × 6列)")

# グリッドの作成 (3行 × 6列をマッピング)
grid_map = [[None for _ in range(6)] for _ in range(3)]

for p in living_players:
  r, c = p["pos"]
  grid_map[r][c] = ("player", p)

for e in living_enemies:
  r, c = e["pos"]
  grid_map[r][c] = ("enemy", e)

# Streamlitの行とカラムを使って綺麗にグリッドを描画
for r in range(3):
  cols = st.columns(6)
  for c in range(6):
    with cols[c]:
      cell_content = grid_map[r][c]
      # 各セルをコンテナ（枠線付き）で囲むことで、内部の要素がはみ出さないように統一
      with st.container(border=True):
        if cell_content is None:
          # 空マス
          st.markdown(
              f"""
                  <div style="height: 70px; display: flex; align-items: center; justify-content: center; color: #ccc; font-size: 12px;">
                      ({r},{c})
                  </div>
                  """,
              unsafe_allow_html=True,
          )
        else:
          entity_type, data = cell_content
          if entity_type == "player":
            is_current = (
                st.session_state.turn_phase == "player_turn"
                and living_players[
                    st.session_state.current_actor_idx % len(living_players)
                ]["id"]
                == data["id"]
            )
            border_color = "orange" if is_current else "green"
            bg_color = "#fff3e0" if is_current else "#e8f5e9"

            # 画像をセル幅に自動フィットさせる（横幅100%）
            st.image(data["img_url"], use_container_width=True)
            
          else:
            # 敵の表示
            st.image(data["img_url"], use_container_width=True)
            
st.markdown("---")

# --- フェーズごとの処理 ---
if st.session_state.turn_phase == "player_turn":
  current_p = living_players[
      st.session_state.current_actor_idx % len(living_players)
  ]

  col_info, col_action = st.columns([1, 3])
  with col_info:
    st.markdown("### 👤 現在の行動キャラ")
    st.image(current_p["img_url"], width=70)
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

  st.markdown("#### 🃏 スキルカード選択")

  card_cols = st.columns(len(current_p["cards"]))

  for idx, card in enumerate(current_p["cards"]):
    with card_cols[idx]:
      # Streamlit標準のコンテナと画像・テキスト表示を使ったカードUI
      with st.container(border=True):
        st.markdown(
            f"**{'[移動]' if card['type']=='move' else '[攻撃]'} {card['name']}**"
        )
        st.image(card["img_url"], use_container_width=True)
        st.markdown(
            f"<div style='font-size: 12px;'>{card['desc']}</div>",
            unsafe_allow_html=True,
        )
        if card["type"] == "attack":
          st.markdown(
              f"<div style='font-size: 12px; color: #d32f2f;'><b>威力:</b>"
              f" {card['damage']}</div>",
              unsafe_allow_html=True,
          )

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
                    f" ({nr}, {nc}) に移動しました。"
                )
              else:
                add_log(f"⚠️ そのマスには既にキャラクターがいます。")
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
