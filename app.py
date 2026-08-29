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
  st.session_state.stage = 1
  # プレイヤーキャラ6体（異なる役職・クラスの構成）
  st.session_state.players = [
      {
          "id": 0,
          "name": "ナイト",
          "hp": 70,
          "max_hp": 70,
          "pos": (0, 2),
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
                  "name": "ファイアシールドバッシュ",
                  "range": [(0, 1)],
                  "damage": 15,
                  "desc": "目前の敵を炎盾で殴りつける。",
                  "img_url": "images/knight_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "フレイムスラッシュ",
                  "range": [(0, 1)],
                  "damage": 22,
                  "desc": "炎属性：前方の敵を燃え盛る剣で斬りつける。",
                  "img_url": "images/knight_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ダークシールド",
                  "range": [(0, 1)],
                  "damage": 18,
                  "desc": "闇属性：闇のオーラを纏った盾で打ち据える。",
                  "img_url": "images/knight_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "ヘルファイアバースト",
                  "range": [(0, 1), (0, 2)],
                  "damage": 30,
                  "desc": "炎・闇：暗黒の炎で広範囲の敵をまとめて焼く。",
                  "img_url": "images/knight_skill4.jpg",
              },
          ],
      },
      {
          "id": 1,
          "name": "ウォーリア",
          "hp": 60,
          "max_hp": 60,
          "pos": (1, 2),
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
                  "type": "move",
                  "name": "後退ダッシュ",
                  "dr": 0,
                  "dc": -1,
                  "desc": "後方に1マス素早く移動。",
                  "img_url": "images/warrior.jpg",
              },
              {
                  "type": "attack",
                  "name": "サンダーアイスワイドスラッシュ",
                  "range": [(-1, 1), (0, 1), (1, 1)],
                  "damage": 20,
                  "desc": "前方の3マスを同時に攻撃する。",
                  "img_url": "images/warrior_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "フロストエッジ",
                  "range": [(0, 1)],
                  "damage": 24,
                  "desc": "氷属性：凍てつく冷気の刃で切り裂く。",
                  "img_url": "images/warrior_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ライトニングブレイク",
                  "range": [(1, 1)],
                  "damage": 26,
                  "desc": "雷属性：電撃を伴う強烈な一撃を叩き込む。",
                  "img_url": "images/warrior_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "グレイシャルサンダー",
                  "range": [(-1, 1), (0, 1), (1, 1)],
                  "damage": 35,
                  "desc": "氷・雷：魔力を宿した乱れ斬りで前方を制圧。",
                  "img_url": "images/warrior_skill4.jpg",
              },
          ],
      },
      {
          "id": 2,
          "name": "ローグ",
          "hp": 45,
          "max_hp": 45,
          "pos": (2, 2),
          "img_url": "images/rogue.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "サイドステップ",
                  "dr": -1,
                  "dc": 0,
                  "desc": "上に1マス素早く回り込む。",
                  "img_url": "images/rogue.jpg",
              },
              {
                  "type": "attack",
                  "name": "ウィンドバックスタブ",
                  "range": [(0, 1), (0, 2)],
                  "damage": 30,
                  "desc": "2マス先の敵の急所を突く一撃。",
                  "img_url": "images/rogue_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "ガイルゲイル",
                  "range": [(0, 1), (0, 2)],
                  "damage": 25,
                  "desc": "風属性：真空の刃を纏い背後を切り抜ける。",
                  "img_url": "images/rogue_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "フラッシュスタブ",
                  "range": [(0, 1), (0, 2)],
                  "damage": 28,
                  "desc": "光属性：目くらましの突き技で急所を貫く。",
                  "img_url": "images/rogue_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "アストラルストーム",
                  "range": [(0, 1), (0, 2)],
                  "damage": 38,
                  "desc": "風・光：疾風と閃光の連続攻撃を浴びせる。",
                  "img_url": "images/rogue_skill4.jpg",
              },
          ],
      },
      {
          "id": 3,
          "name": "メイジ",
          "hp": 35,
          "max_hp": 35,
          "pos": (0, 1),
          "img_url": "images/mage.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "テレポート歩行",
                  "dr": 0,
                  "dc": 1,
                  "desc": "前方に1マス位置を調整する。",
                  "img_url": "images/mage.jpg",
              },
              {
                  "type": "attack",
                  "name": "メテオストライク",
                  "range": [(0, 2), (0, 3)],
                  "damage": 35,
                  "desc": "遠く離れた2〜3マス先の敵を焼く。",
                  "img_url": "images/mage_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "ロックバレット",
                  "range": [(0, 2)],
                  "damage": 30,
                  "desc": "岩属性：巨大な岩を生成して激突させる。",
                  "img_url": "images/mage_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ミラージュフレア",
                  "range": [(0, 3)],
                  "damage": 32,
                  "desc": "幻属性：幻影の炎で敵の精神を揺さぶる。",
                  "img_url": "images/mage_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "メテオライトフォール",
                  "range": [(0, 2), (0, 3)],
                  "damage": 45,
                  "desc": "岩・幻：星屑を纏った隕石を落下させ大爆発。",
                  "img_url": "images/mage_skill4.jpg",
              },
          ],
      },
      {
          "id": 4,
          "name": "アーチャー",
          "hp": 40,
          "max_hp": 40,
          "pos": (1, 1),
          "img_url": "images/archer.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "バックペダル",
                  "dr": 0,
                  "dc": -1,
                  "desc": "後方に1マス下がって距離を取る。",
                  "img_url": "images/archer.jpg",
              },
              {
                  "type": "attack",
                  "name": "ウォータースナイプショット",
                  "range": [(0, 2), (0, 3)],
                  "damage": 25,
                  "desc": "直線上の遠くの敵を正確に射抜く。",
                  "img_url": "images/archer_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "アクアニードル",
                  "range": [(0, 2), (0, 3)],
                  "damage": 22,
                  "desc": "水属性：高圧の水流の矢を放つ。",
                  "img_url": "images/archer_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ポイズンスナイプ",
                  "range": [(0, 3)],
                  "damage": 20,
                  "poison_turns": 3,
                  "p_damage": 5,
                  "desc": "毒属性：猛毒の矢で体力をじわじわ蝕む（3ターン継続）。",
                  "img_url": "images/archer_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "ベノムタイダル",
                  "range": [(0, 2), (0, 3)],
                  "damage": 30,
                  "poison_turns": 2,
                  "p_damage": 8,
                  "desc": "水・毒：毒の水飛沫を浴びせ、強力な毒に侵す（2ターン継続）。",
                  "img_url": "images/archer_skill4.jpg",
              },
          ],
      },
      {
          "id": 5,
          "name": "プリースト",
          "hp": 50,
          "max_hp": 50,
          "pos": (2, 1),
          "img_url": "images/priest.jpg",
          "cards": [
              {
                  "type": "move",
                  "name": "聖者の歩み",
                  "dr": 0,
                  "dc": -1,
                  "desc": "後方に1マス進む。",
                  "img_url": "images/priest.jpg",
              },
              {
                  "type": "attack",
                  "name": "ホーリースマイト",
                  "range": [(0, 2), (0, 3)],
                  "damage": 10,
                  "desc": "遠く離れた2〜3マス先の敵へ神聖な光でダメージ。",
                  "img_url": "images/priest_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "ホーリーランス",
                  "range": [(0, 2), (0, 3)],
                  "damage": 18,
                  "desc": "聖属性：純白の光で槍をかたどり邪悪を浄化。",
                  "img_url": "images/priest_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "スターライトソウル",
                  "range": [(0, 2), (0, 3)],
                  "damage": 28,
                  "desc": "聖・夢：聖なる夢幻の光で敵を滅ぼす。",
                  "img_url": "images/priest_skill3.jpg",
              },
              {
                  "type": "heal",
                  "name": "エリアヒール",
                  "heal": 25,
                  "desc": "回復：神聖な波動で味方全体のHPを中回復。",
                  "img_url": "images/priest_skill4.jpg",
              },
          ],
      },
  ]
  # 敵キャラ6体（ステータス強化版）
  # 後半にかけて激しくインフレする敵キャラのステータス定義
  st.session_state.stage_enemies = {
      1: [
          {"id": 0, "name": "ゴブリン・ガード", "hp": 40, "max_hp": 40, "pos": (0, 3), "damage": 8, "poison_turns": 0, "poison_damage": 0, "img_url": "images/goblin_guard.jpg"},
          {"id": 1, "name": "ゴブリン・ソルジャー", "hp": 35, "max_hp": 35, "pos": (1, 3), "damage": 10, "poison_turns": 0, "poison_damage": 0, "img_url": "images/goblin_soldure.jpg"},
          {"id": 2, "name": "ゴブリン・アサシン", "hp": 30, "max_hp": 30, "pos": (2, 3), "damage": 9, "poison_turns": 0, "poison_damage": 0, "img_url": "images/goblin_assasin.jpg"},
          {"id": 3, "name": "ゴブリン・シャーマン", "hp": 25, "max_hp": 25, "pos": (0, 4), "damage": 10, "poison_turns": 0, "poison_damage": 0, "img_url": "images/goblin_sharman.jpg"},
          {"id": 4, "name": "オーク・バーサーカー", "hp": 50, "max_hp": 50, "pos": (1, 4), "damage": 14, "poison_turns": 0, "poison_damage": 0, "img_url": "images/orc_verserk.jpg"},
          {"id": 5, "name": "ダーク・アーチャー", "hp": 30, "max_hp": 30, "pos": (2, 4), "damage": 12, "poison_turns": 0, "poison_damage": 0, "img_url": "images/dark_archer.jpg"},
      ],
      2: [
          {"id": 0, "name": "ブルー・スライム", "hp": 50, "max_hp": 50, "pos": (0, 3), "damage": 14, "poison_turns": 0, "poison_damage": 0, "img_url": "images/blue_slime.jpg"},
          {"id": 1, "name": "レッド・スライム", "hp": 50, "max_hp": 50, "pos": (1, 3), "damage": 16, "poison_turns": 0, "poison_damage": 0, "img_url": "images/red_slime.jpg"},
          {"id": 2, "name": "イエロー・スライム", "hp": 50, "max_hp": 50, "pos": (2, 3), "damage": 17, "poison_turns": 0, "poison_damage": 0, "img_url": "images/yellow_slime.jpg"},
          {"id": 3, "name": "グリーン・スライム", "hp": 65, "max_hp": 65, "pos": (0, 4), "damage": 12, "poison_turns": 0, "poison_damage": 0, "img_url": "images/green_slime.jpg"},
          {"id": 4, "name": "メタル・スライム", "hp": 30, "max_hp": 30, "pos": (1, 4), "damage": 10, "poison_turns": 0, "poison_damage": 0, "img_url": "images/metal_slime.jpg"},
          {"id": 5, "name": "キング・スライム", "hp": 90, "max_hp": 90, "pos": (2, 4), "damage": 22, "poison_turns": 0, "poison_damage": 0, "img_url": "images/king_slime.jpg"},
      ],
      3: [
          {"id": 0, "name": "スケルトン・ウォリアー", "hp": 70, "max_hp": 70, "pos": (0, 3), "damage": 22, "poison_turns": 0, "poison_damage": 0, "img_url": "images/skeleton_warrior.jpg"},
          {"id": 1, "name": "スケルトン・アーチャー", "hp": 60, "max_hp": 60, "pos": (1, 3), "damage": 25, "poison_turns": 0, "poison_damage": 0, "img_url": "images/skeleton_archer.jpg"},
          {"id": 2, "name": "ゾンビ", "hp": 90, "max_hp": 90, "pos": (2, 3), "damage": 20, "poison_turns": 0, "poison_damage": 0, "img_url": "images/zombie.jpg"},
          {"id": 3, "name": "グール", "hp": 70, "max_hp": 70, "pos": (0, 4), "damage": 28, "poison_turns": 0, "poison_damage": 0, "img_url": "images/ghoul.jpg"},
          {"id": 4, "name": "レイス", "hp": 55, "max_hp": 55, "pos": (1, 4), "damage": 32, "poison_turns": 0, "poison_damage": 0, "img_url": "images/wraith.jpg"},
          {"id": 5, "name": "ボーン・ナイト", "hp": 110, "max_hp": 110, "pos": (2, 4), "damage": 36, "poison_turns": 0, "poison_damage": 0, "img_url": "images/bone_knight.jpg"},
      ],
      4: [
          {"id": 0, "name": "ファイア・インプ", "hp": 80, "max_hp": 80, "pos": (0, 3), "damage": 30, "poison_turns": 0, "poison_damage": 0, "img_url": "images/fire_imp.jpg"},
          {"id": 1, "name": "マグマ・リザード", "hp": 100, "max_hp": 100, "pos": (1, 3), "damage": 33, "poison_turns": 0, "poison_damage": 0, "img_url": "images/magma_lizard.jpg"},
          {"id": 2, "name": "フレイム・ハウンド", "hp": 90, "max_hp": 90, "pos": (2, 3), "damage": 36, "poison_turns": 0, "poison_damage": 0, "img_url": "images/flame_hound.jpg"},
          {"id": 3, "name": "サラマンダー", "hp": 110, "max_hp": 110, "pos": (0, 4), "damage": 40, "poison_turns": 0, "poison_damage": 0, "img_url": "images/salamander.jpg"},
          {"id": 4, "name": "ヴォルケーノ・ゴーレム", "hp": 150, "max_hp": 150, "pos": (1, 4), "damage": 46, "poison_turns": 0, "poison_damage": 0, "img_url": "images/volcano_golem.jpg"},
          {"id": 5, "name": "フレーム・ドラゴン", "hp": 180, "max_hp": 180, "pos": (2, 4), "damage": 54, "poison_turns": 0, "poison_damage": 0, "img_url": "images/flame_dragon.jpg"},
      ],
      5: [
          {"id": 0, "name": "フロスト・ウルフ", "hp": 100, "max_hp": 100, "pos": (0, 3), "damage": 38, "poison_turns": 0, "poison_damage": 0, "img_url": "images/frost_wolf.jpg"},
          {"id": 1, "name": "アイス・バット", "hp": 80, "max_hp": 80, "pos": (1, 3), "damage": 35, "poison_turns": 0, "poison_damage": 0, "img_url": "images/ice_bat.jpg"},
          {"id": 2, "name": "イエティ", "hp": 170, "max_hp": 170, "pos": (2, 3), "damage": 50, "poison_turns": 0, "poison_damage": 0, "img_url": "images/yeti.jpg"},
          {"id": 3, "name": "フローズン・メイジ", "hp": 90, "max_hp": 90, "pos": (0, 4), "damage": 42, "poison_turns": 0, "poison_damage": 0, "img_url": "images/frozen_mage.jpg"},
          {"id": 4, "name": "ブリザード・スピリット", "hp": 110, "max_hp": 110, "pos": (1, 4), "damage": 46, "poison_turns": 0, "poison_damage": 0, "img_url": "images/blizzard_spirit.jpg"},
          {"id": 5, "name": "フロスト・ジャイアント", "hp": 200, "max_hp": 200, "pos": (2, 4), "damage": 58, "poison_turns": 0, "poison_damage": 0, "img_url": "images/frost_giant.jpg"},
      ],
      # --- ここから後半：急激にインフレ ---
      6: [
          {"id": 0, "name": "サンダー・バード", "hp": 160, "max_hp": 160, "pos": (0, 3), "damage": 65, "poison_turns": 0, "poison_damage": 0, "img_url": "images/thunder_bird.jpg"},
          {"id": 1, "name": "ライトニング・エレメンタル", "hp": 140, "max_hp": 140, "pos": (1, 3), "damage": 70, "poison_turns": 0, "poison_damage": 0, "img_url": "images/lightning_elemental.jpg"},
          {"id": 2, "name": "ストーム・ナイト", "hp": 220, "max_hp": 220, "pos": (2, 3), "damage": 78, "poison_turns": 0, "poison_damage": 0, "img_url": "images/storm_knight.jpg"},
          {"id": 3, "name": "ウィンド・シルフ", "hp": 120, "max_hp": 120, "pos": (0, 4), "damage": 58, "poison_turns": 0, "poison_damage": 0, "img_url": "images/wind_sylph.jpg"},
          {"id": 4, "name": "ボルト・ガルーダ", "hp": 260, "max_hp": 260, "pos": (1, 4), "damage": 88, "poison_turns": 0, "poison_damage": 0, "img_url": "images/bolt_garuda.jpg"},
          {"id": 5, "name": "雷神の化身", "hp": 350, "max_hp": 350, "pos": (2, 4), "damage": 100, "poison_turns": 0, "poison_damage": 0, "img_url": "images/rai_avatar.jpg"},
      ],
      7: [
          {"id": 0, "name": "ポイズン・トード", "hp": 200, "max_hp": 200, "pos": (0, 3), "damage": 70, "poison_turns": 0, "poison_damage": 0, "img_url": "images/poison_toad.jpg"},
          {"id": 1, "name": "ヴェノム・スパイダー", "hp": 180, "max_hp": 180, "pos": (1, 3), "damage": 78, "poison_turns": 0, "poison_damage": 0, "img_url": "images/venom_spider.jpg"},
          {"id": 2, "name": "スワンプ・サーペント", "hp": 270, "max_hp": 270, "pos": (2, 3), "damage": 90, "poison_turns": 0, "poison_damage": 0, "img_url": "images/swamp_serpent.jpg"},
          {"id": 3, "name": "プラント・ウィップ", "hp": 220, "max_hp": 220, "pos": (0, 4), "damage": 80, "poison_turns": 0, "poison_damage": 0, "img_url": "images/plant_whip.jpg"},
          {"id": 4, "name": "マッド・アサシン", "hp": 200, "max_hp": 200, "pos": (1, 4), "damage": 95, "poison_turns": 0, "poison_damage": 0, "img_url": "images/mud_assassin.jpg"},
          {"id": 5, "name": "毒竜ヒドラ", "hp": 400, "max_hp": 400, "pos": (2, 4), "damage": 115, "poison_turns": 0, "poison_damage": 0, "img_url": "images/hydra.jpg"},
      ],
      8: [
          {"id": 0, "name": "ブロンズ・ゴーレム", "hp": 300, "max_hp": 300, "pos": (0, 3), "damage": 90, "poison_turns": 0, "poison_damage": 0, "img_url": "images/bronze_golem.jpg"},
          {"id": 1, "name": "ガーディアン・アイ", "hp": 190, "max_hp": 190, "pos": (1, 3), "damage": 85, "poison_turns": 0, "poison_damage": 0, "img_url": "images/guardian_eye.jpg"},
          {"id": 2, "name": "マジック・オートマトン", "hp": 250, "max_hp": 250, "pos": (2, 3), "damage": 100, "poison_turns": 0, "poison_damage": 0, "img_url": "images/automaton.jpg"},
          {"id": 3, "name": "アーク・サーベイヤー", "hp": 220, "max_hp": 220, "pos": (0, 4), "damage": 105, "poison_turns": 0, "poison_damage": 0, "img_url": "images/surveyor.jpg"},
          {"id": 4, "name": "デストロイ・タンク", "hp": 380, "max_hp": 380, "pos": (1, 4), "damage": 120, "poison_turns": 0, "poison_damage": 0, "img_url": "images/destroy_tank.jpg"},
          {"id": 5, "name": "古代魔導兵器", "hp": 480, "max_hp": 480, "pos": (2, 4), "damage": 140, "poison_turns": 0, "poison_damage": 0, "img_url": "images/ancient_weapon.jpg"},
      ],
      9: [
          {"id": 0, "name": "デーモン・スカウト", "hp": 280, "max_hp": 280, "pos": (0, 3), "damage": 110, "poison_turns": 0, "poison_damage": 0, "img_url": "images/demon_scout.jpg"},
          {"id": 1, "name": "ヘル・ハウンド", "hp": 320, "max_hp": 320, "pos": (1, 3), "damage": 120, "poison_turns": 0, "poison_damage": 0, "img_url": "images/hell_hound.jpg"},
          {"id": 2, "name": "サキュバス", "hp": 250, "max_hp": 250, "pos": (2, 3), "damage": 105, "poison_turns": 0, "poison_damage": 0, "img_url": "images/succubus.jpg"},
          {"id": 3, "name": "アビス・ナイト", "hp": 420, "max_hp": 420, "pos": (0, 4), "damage": 135, "poison_turns": 0, "poison_damage": 0, "img_url": "images/abyss_knight.jpg"},
          {"id": 4, "name": "ケルベロス", "hp": 460, "max_hp": 460, "pos": (1, 4), "damage": 150, "poison_turns": 0, "poison_damage": 0, "img_url": "images/cerberus.jpg"},
          {"id": 5, "name": "魔界貴族ロード", "hp": 550, "max_hp": 550, "pos": (2, 4), "damage": 170, "poison_turns": 0, "poison_damage": 0, "img_url": "images/demon_lord.jpg"},
      ],
      10: [
          {"id": 0, "name": "ダーク・ガーディアン", "hp": 480, "max_hp": 480, "pos": (0, 3), "damage": 140, "poison_turns": 0, "poison_damage": 0, "img_url": "images/dark_guardian.jpg"},
          {"id": 1, "name": "カオス・メイジ", "hp": 380, "max_hp": 380, "pos": (1, 3), "damage": 160, "poison_turns": 0, "poison_damage": 0, "img_url": "images/chaos_mage.jpg"},
          {"id": 2, "name": "ドレッド・ナイト", "hp": 520, "max_hp": 520, "pos": (2, 3), "damage": 175, "poison_turns": 0, "poison_damage": 0, "img_url": "images/dread_knight.jpg"},
          {"id": 3, "name": "シャドウ・ドラゴン", "hp": 650, "max_hp": 650, "pos": (0, 4), "damage": 195, "poison_turns": 0, "poison_damage": 0, "img_url": "images/shadow_dragon.jpg"},
          {"id": 4, "name": "魔王の側近", "hp": 720, "max_hp": 720, "pos": (1, 4), "damage": 215, "poison_turns": 0, "poison_damage": 0, "img_url": "images/boss_aide.jpg"},
          {"id": 5, "name": "魔王アーク・デストロイヤー", "hp": 1000, "max_hp": 1000, "pos": (2, 4), "damage": 250, "poison_turns": 0, "poison_damage": 0, "img_url": "images/last_boss.jpg"},
      ],
  }
  st.session_state.enemies = st.session_state.stage_enemies[st.session_state.stage]
  st.session_state.turn_phase = "player_turn"
  st.session_state.current_actor_idx = 0
  st.session_state.battle_log = [
      f"ステージ {st.session_state.stage} 開始！プレイヤー側のターンです。スキルカードを選択してください。"
  ]


def add_log(msg):
  st.session_state.battle_log.insert(0, msg)


# --- 敵の列シフト処理 (4列目 -> 3列目) ---
def update_enemy_positions():
  # 生存している敵のみ対象
  alive_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]
  
  # 各行(row 0, 1, 2)ごとにチェック
  for r in range(3):
    # 列3と列4にいる生存敵を特定
    col3_enemy = next((e for e in alive_enemies if e["pos"] == (r, 3)), None)
    col4_enemy = next((e for e in alive_enemies if e["pos"] == (r, 4)), None)
    
    # 3列目が不在で、4列目に敵がいる場合、4列目の敵を3列目に移動
    if col3_enemy is None and col4_enemy is not None:
      col4_enemy["pos"] = (r, 3)
      add_log(f"🔄 {col4_enemy['name']} が空いた3列目に前進しました！")


# --- 勝利・敗北判定 ---
living_players = [p for p in st.session_state.players if p["hp"] > 0]
living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]

st.title(f"⚔️ タクティカル・デュエルバトル (ステージ {st.session_state.stage} / 10)")

if not living_enemies:
  if st.session_state.stage < 10:
    st.success(f"🎉 ステージ {st.session_state.stage} クリア！")
    
    # --- ステージクリアによる味方全体の強化処理 ---
    for p in st.session_state.players:
      p["max_hp"] = int(p["max_hp"] * 1.2)
      p["hp"] = p["max_hp"]
      
      for card in p["cards"]:
        if "damage" in card:
          card["damage"] = int(card["damage"] * 1.2)
        if "heal" in card:
          card["heal"] = int(card["heal"] * 1.2)
        if "p_damage" in card:
          card["p_damage"] = int(card["p_damage"] * 1.2)
    
    add_log("✨ 勝利の報酬として、味方全体のステータスとスキル能力が上昇しました！")

    if st.button("次のステージに進む"):
      st.session_state.stage += 1
      import copy
      st.session_state.enemies = copy.deepcopy(st.session_state.stage_enemies[st.session_state.stage])
      st.session_state.turn_phase = "player_turn"
      st.session_state.current_actor_idx = 0
      add_log(f"ステージ {st.session_state.stage} に突入しました！")
      st.rerun()
  else:
    st.success("🏆 【完全勝利】全10ステージを制覇し、世界を救いました！")
    if st.button("最初からもう一度プレイする"):
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

grid_map = [[None for _ in range(6)] for _ in range(3)]

for p in living_players:
  r, c = p["pos"]
  grid_map[r][c] = ("player", p)

for e in living_enemies:
  r, c = e["pos"]
  grid_map[r][c] = ("enemy", e)

# 現在の行動キャラの取得
current_p = living_players[
    st.session_state.current_actor_idx % len(living_players)
] if living_players else None

for r in range(3):
  cols = st.columns(6)
  for c in range(6):
    with cols[c]:
      cell_content = grid_map[r][c]
      
      # 攻撃可能ハイライト判定（プレイヤーのターンかつ行動キャラが存在する場合）
      is_attackable = False
      if st.session_state.turn_phase == "player_turn" and current_p and cell_content:
        etype, edata = cell_content
        if etype == "enemy":
          pr, pc = current_p["pos"]
          er, ec = edata["pos"]
          # 各カードの射程範囲をチェックし、どれか一つでも届くなら攻撃可能とする
          for card in current_p["cards"]:
            if card["type"] == "attack":
              if any((pr + dr, pc + dc) == (er, ec) for dr, dc in card["range"]):
                is_attackable = True
                break

      # ハイライト用の枠線カラーやスタイル設定
      border_style = "border: 2px solid #ff4b4b;" if is_attackable else "border: 1px solid #ddd;"
      
      with st.container(border=True):
        if cell_content is None:
          st.markdown(
              f"""
                  <div style="height: 70px; display: flex; align-items: center; justify-content: center; color: #ccc; font-size: 12px; {border_style}">
                      ({r},{c})
                  </div>
                  """,
              unsafe_allow_html=True,
          )
        else:
          entity_type, data = cell_content
          if entity_type == "player":
            st.image(data["img_url"], use_container_width=True)
            st.markdown(f"<div style='font-size:11px; text-align:center;'><b>{data['name']}</b></div>", unsafe_allow_html=True)
            hp_ratio = max(0.0, min(1.0, data["hp"] / data["max_hp"]))
            st.progress(hp_ratio, text=f"HP: {data['hp']}/{data['max_hp']}")
          else:
            # 攻撃可能な敵にはマークを付与して視覚的にわかりやすくする
            highlight_label = " 🎯【攻撃可能】" if is_attackable else ""
            st.image(data["img_url"], use_container_width=True)
            st.markdown(f"<div style='font-size:11px; text-align:center;'><b>{data['name']}</b>{highlight_label}</div>", unsafe_allow_html=True)
            hp_ratio = max(0.0, min(1.0, data["hp"] / data["max_hp"]))
            st.progress(hp_ratio, text=f"HP: {data['hp']}/{data['max_hp']}")
            
st.markdown("---")

# --- フェーズごとの処理 ---
if st.session_state.turn_phase == "player_turn":
  # --- ターン開始時の毒ダメージ処理 ---
  for e in living_enemies:
    if e["hp"] > 0 and e["poison_turns"] > 0:
      e["hp"] -= e["poison_damage"]
      if e["hp"] < 0:
        e["hp"] = 0
      e["poison_turns"] -= 1
      add_log(f"☠️ {e['name']} は毒により {e['poison_damage']} の継続ダメージを受けた！（残り {e['poison_turns']} ターン）")
  
  # 毒ダメージ後の敵の死亡・シフト処理
  update_enemy_positions()
  
  # 生存リストを更新
  living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]
  current_p = living_players[
      st.session_state.current_actor_idx % len(living_players)
  ]

  col_info, col_action = st.columns([1, 3])
  with col_info:
    st.markdown("### 👤 現在の行動キャラ")
    st.image(current_p["img_url"], width=70)
    st.markdown(f"**{current_p['name']}**")
    hp_ratio = max(0.0, min(1.0, current_p["hp"] / current_p["max_hp"]))
    st.progress(hp_ratio, text=f"HP: {current_p['hp']}/{current_p['max_hp']}")

  with col_action:
    st.markdown("### 🎯 ターゲットの選択")
    target_type_tab = st.radio("行動対象の選択", ["敵を攻撃する", "味方を回復する"], horizontal=True)
    
    if target_type_tab == "敵を攻撃する":
      enemy_options = {
          f"{e['name']} (位置: {e['pos']}, HP: {e['hp']})": e
          for e in living_enemies
      }
      selected_label = st.selectbox("ターゲットの敵を選択", list(enemy_options.keys()))
      target_enemy = enemy_options[selected_label]
    else:
      player_options = {
          f"{p['name']} (HP: {p['hp']}/{p['max_hp']})": p
          for p in living_players
      }
      selected_label = st.selectbox("ターゲットの味方を選択", list(player_options.keys()))
      target_enemy = player_options[selected_label]

  st.markdown("#### 🃏 スキルカード選択")

  card_cols = st.columns(len(current_p["cards"]))

  for idx, card in enumerate(current_p["cards"]):
    with card_cols[idx]:
      with st.container(border=True):
        badge = "[移動]" if card['type']=='move' else ("[回復]" if card['type']=='heal' else "[攻撃]")
        st.markdown(f"**{badge} {card['name']}**")
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
        elif card["type"] == "heal":
          st.markdown(
              f"<div style='font-size: 12px; color: #2e7d32;'><b>回復量:</b>"
              f" {card['heal']}</div>",
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
            if target_type_tab != "敵を攻撃する":
              add_log(f"⚠️ 攻撃スキルは敵を選択して実行してください。")
            else:
              pr, pc = current_p["pos"]
              er, ec = target_enemy["pos"]
              valid_hit = any(
                  (pr + dr, pc + dc) == (er, ec) for dr, dc in card["range"]
              )

              if valid_hit:
                target_enemy["hp"] -= card["damage"]
                if target_enemy["hp"] < 0:
                  target_enemy["hp"] = 0
                
                # --- 敵撃破時の列シフトチェック ---
                update_enemy_positions()

                # --- 毒の付与処理 ---
                hit_msg = f"✨ {current_p['name']} の '{card['name']}' が {target_enemy['name']} に命中！ {card['damage']} のダメージ！"
                if "poison_turns" in card:
                  target_enemy["poison_turns"] = card["poison_turns"]
                  target_enemy["poison_damage"] = card["p_damage"]
                  hit_msg += f" ＞ **【毒】状態**を付与した！"
                
                add_log(hit_msg)
              else:
                add_log(f"❌ {card['name']} の攻撃範囲外です（届きません）！")

          elif card["type"] == "heal":
            heal_amount = card["heal"]
            for p in living_players:
              p["hp"] += heal_amount
              if p["hp"] > p["max_hp"]:
                p["hp"] = p["max_hp"]
            add_log(
                f"💚 {current_p['name']} の '{card['name']}' 発動！"
                f" 味方全員のHPが {heal_amount} 回復した！"
            )

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
