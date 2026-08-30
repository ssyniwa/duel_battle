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
                  "name": "下進",
                  "dr": 1,
                  "dc": 0,
                  "desc": "下方に1マス移動します。",
                  "img_url": "images/knight.jpg",
              },
              {
                  "type": "attack",
                  "name": "ファイアシールドバッシュ",
                  "range": [(0, 1), (0, 2)],
                  "damage": 15,
                  "desc": "目前の敵を炎盾で殴りつける。",
                  "img_url": "images/knight_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "フレイムスラッシュ",
                  "range": [(0, 1), (0, 2)],
                  "damage": 22,
                  "desc": "炎属性：前方の敵を燃え盛る剣で斬りつける。",
                  "img_url": "images/knight_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ダークシールド",
                  "range": [(0, 1), (0, 2)],
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
                  "dr": 1,
                  "dc": 0,
                  "desc": "下方に1マス素早く移動。",
                  "img_url": "images/warrior.jpg",
              },
              {
                  "type": "move",
                  "name": "後退ダッシュ",
                  "dr": -1,
                  "dc": 0,
                  "desc": "上方に1マス素早く移動。",
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
                  "range": [(-1, 1), (0, 1), (1, 1)],
                  "damage": 24,
                  "desc": "氷属性：凍てつく冷気の刃で切り裂く。",
                  "img_url": "images/warrior_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ライトニングブレイク",
                  "range": [(-1, 1), (0, 1), (1, 1)],
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
                  "dr": 1,
                  "dc": 0,
                  "desc": "下方に1マス位置を調整する。",
                  "img_url": "images/mage.jpg",
              },
              {
                  "type": "attack",
                  "name": "メテオストライク",
                  "range": [(0, 2), (0, 3), (1, 2), (1, 3)],
                  "damage": 35,
                  "desc": "遠く離れた2〜3マス先の敵を焼く。",
                  "img_url": "images/mage_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "ロックバレット",
                  "range": [(0, 2), (0, 3), (1, 2), (1, 3)],
                  "damage": 30,
                  "desc": "岩属性：巨大な岩を生成して激突させる。",
                  "img_url": "images/mage_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ミラージュフレア",
                  "range": [(0, 2), (0, 3), (1, 2), (1, 3)],
                  "damage": 32,
                  "desc": "幻属性：幻影の炎で敵の精神を揺さぶる。",
                  "img_url": "images/mage_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "メテオライトフォール",
                  "range": [(0, 2), (0, 3), (1, 2), (1, 3)],
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
                  "dr": 1,
                  "dc": 0,
                  "desc": "下方に1マス下がって距離を取る。",
                  "img_url": "images/archer.jpg",
              },
              {
                  "type": "move",
                  "name": "バックペダル2",
                  "dr": -1,
                  "dc": 0,
                  "desc": "上方に1マス下がって距離を取る。",
                  "img_url": "images/archer.jpg",
              },
              {
                  "type": "attack",
                  "name": "ウォータースナイプショット",
                  "range": [(0, 2), (0, 3), (1, 2), (-1, 2)],
                  "damage": 25,
                  "desc": "直線上の遠くの敵を正確に射抜く。",
                  "img_url": "images/archer_skill1.jpg",
              },
              {
                  "type": "attack",
                  "name": "アクアニードル",
                  "range": [(0, 2), (0, 3), (1, 2), (-1, 2)],
                  "damage": 22,
                  "desc": "水属性：高圧の水流の矢を放つ。",
                  "img_url": "images/archer_skill2.jpg",
              },
              {
                  "type": "attack",
                  "name": "ポイズンスナイプ",
                  "range": [(0, 2), (0, 3), (1, 2), (-1, 2)],
                  "damage": 20,
                  "poison_turns": 3,
                  "p_damage": 5,
                  "desc": "毒属性：猛毒の矢で体力をじわじわ蝕む（3ターン継続）。",
                  "img_url": "images/archer_skill3.jpg",
              },
              {
                  "type": "attack",
                  "name": "ベノムタイダル",
                  "range": [(0, 2), (0, 3), (1, 2), (-1, 2)],
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
                  "dr":-1,
                  "dc": 0,
                  "desc": "上方に1マス進む。",
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
      6: [
          {"id": 0, "name": "サンダー・バード", "hp": 300, "max_hp": 300, "pos": (0, 3), "damage": 110, "poison_turns": 0, "poison_damage": 0, "img_url": "images/thunder_bird.jpg"},
          {"id": 1, "name": "ライトニング・エレメンタル", "hp": 260, "max_hp": 260, "pos": (1, 3), "damage": 120, "poison_turns": 0, "poison_damage": 0, "img_url": "images/lightning_elemental.jpg"},
          {"id": 2, "name": "ストーム・ナイト", "hp": 400, "max_hp": 400, "pos": (2, 3), "damage": 135, "poison_turns": 0, "poison_damage": 0, "img_url": "images/storm_knight.jpg"},
          {"id": 3, "name": "ウィンド・シルフ", "hp": 220, "max_hp": 220, "pos": (0, 4), "damage": 95, "poison_turns": 0, "poison_damage": 0, "img_url": "images/wind_sylph.jpg"},
          {"id": 4, "name": "ボルト・ガルーダ", "hp": 480, "max_hp": 480, "pos": (1, 4), "damage": 150, "poison_turns": 0, "poison_damage": 0, "img_url": "images/bolt_garuda.jpg"},
          {"id": 5, "name": "雷神の化身", "hp": 650, "max_hp": 650, "pos": (2, 4), "damage": 175, "poison_turns": 0, "poison_damage": 0, "img_url": "images/rai_avatar.jpg"},
      ],
      7: [
          {"id": 0, "name": "ポイズン・トード", "hp": 380, "max_hp": 380, "pos": (0, 3), "damage": 125, "poison_turns": 0, "poison_damage": 0, "img_url": "images/poison_toad.jpg"},
          {"id": 1, "name": "ヴェノム・スパイダー", "hp": 340, "max_hp": 340, "pos": (1, 3), "damage": 135, "poison_turns": 0, "poison_damage": 0, "img_url": "images/venom_spider.jpg"},
          {"id": 2, "name": "スワンプ・サーペント", "hp": 520, "max_hp": 520, "pos": (2, 3), "damage": 155, "poison_turns": 0, "poison_damage": 0, "img_url": "images/swamp_serpent.jpg"},
          {"id": 3, "name": "プラント・ウィップ", "hp": 410, "max_hp": 410, "pos": (0, 4), "damage": 140, "poison_turns": 0, "poison_damage": 0, "img_url": "images/plant_whip.jpg"},
          {"id": 4, "name": "マッド・アサシン", "hp": 380, "max_hp": 380, "pos": (1, 4), "damage": 165, "poison_turns": 0, "poison_damage": 0, "img_url": "images/mud_assassin.jpg"},
          {"id": 5, "name": "毒竜ヒドラ", "hp": 750, "max_hp": 750, "pos": (2, 4), "damage": 195, "poison_turns": 0, "poison_damage": 0, "img_url": "images/hydra.jpg"},
      ],
      8: [
          {"id": 0, "name": "ブロンズ・ゴーレム", "hp": 580, "max_hp": 580, "pos": (0, 3), "damage": 160, "poison_turns": 0, "poison_damage": 0, "img_url": "images/bronze_golem.jpg"},
          {"id": 1, "name": "ガーディアン・アイ", "hp": 360, "max_hp": 360, "pos": (1, 3), "damage": 150, "poison_turns": 0, "poison_damage": 0, "img_url": "images/guardian_eye.jpg"},
          {"id": 2, "name": "マジック・オートマトン", "hp": 480, "max_hp": 480, "pos": (2, 3), "damage": 175, "poison_turns": 0, "poison_damage": 0, "img_url": "images/automaton.jpg"},
          {"id": 3, "name": "アーク・サーベイヤー", "hp": 420, "max_hp": 420, "pos": (0, 4), "damage": 185, "poison_turns": 0, "poison_damage": 0, "img_url": "images/surveyor.jpg"},
          {"id": 4, "name": "デストロイ・タンク", "hp": 720, "max_hp": 720, "pos": (1, 4), "damage": 210, "poison_turns": 0, "poison_damage": 0, "img_url": "images/destroy_tank.jpg"},
          {"id": 5, "name": "古代魔導兵器", "hp": 920, "max_hp": 920, "pos": (2, 4), "damage": 245, "poison_turns": 0, "poison_damage": 0, "img_url": "images/ancient_weapon.jpg"},
      ],
      9: [
          {"id": 0, "name": "デーモン・スカウト", "hp": 550, "max_hp": 550, "pos": (0, 3), "damage": 200, "poison_turns": 0, "poison_damage": 0, "img_url": "images/demon_scout.jpg"},
          {"id": 1, "name": "ヘル・ハウンド", "hp": 620, "max_hp": 620, "pos": (1, 3), "damage": 220, "poison_turns": 0, "poison_damage": 0, "img_url": "images/hell_hound.jpg"},
          {"id": 2, "name": "サキュバス", "hp": 490, "max_hp": 490, "pos": (2, 3), "damage": 195, "poison_turns": 0, "poison_damage": 0, "img_url": "images/succubus.jpg"},
          {"id": 3, "name": "アビス・ナイト", "hp": 820, "max_hp": 820, "pos": (0, 4), "damage": 245, "poison_turns": 0, "poison_damage": 0, "img_url": "images/abyss_knight.jpg"},
          {"id": 4, "name": "ケルベロス", "hp": 900, "max_hp": 900, "pos": (1, 4), "damage": 275, "poison_turns": 0, "poison_damage": 0, "img_url": "images/cerberus.jpg"},
          {"id": 5, "name": "魔界貴族ロード", "hp": 1100, "max_hp": 1100, "pos": (2, 4), "damage": 315, "poison_turns": 0, "poison_damage": 0, "img_url": "images/demon_lord.jpg"},
      ],
      10: [
          {"id": 0, "name": "ダーク・ガーディアン", "hp": 980, "max_hp": 980, "pos": (0, 3), "damage": 260, "poison_turns": 0, "poison_damage": 0, "img_url": "images/dark_guardian.jpg"},
          {"id": 1, "name": "カオス・メイジ", "hp": 760, "max_hp": 760, "pos": (1, 3), "damage": 300, "poison_turns": 0, "poison_damage": 0, "img_url": "images/chaos_mage.jpg"},
          {"id": 2, "name": "ドレッド・ナイト", "hp": 1050, "max_hp": 1050, "pos": (2, 3), "damage": 325, "poison_turns": 0, "poison_damage": 0, "img_url": "images/dread_knight.jpg"},
          {"id": 3, "name": "シャドウ・ドラゴン", "hp": 1300, "max_hp": 1300, "pos": (0, 4), "damage": 365, "poison_turns": 0, "poison_damage": 0, "img_url": "images/shadow_dragon.jpg"},
          {"id": 4, "name": "魔王の側近", "hp": 1500, "max_hp": 1500, "pos": (1, 4), "damage": 405, "poison_turns": 0, "poison_damage": 0, "img_url": "images/boss_aide.jpg"},
          {"id": 5, "name": "魔王アーク・デストロイヤー", "hp": 2500, "max_hp": 2500, "pos": (2, 4), "damage": 500, "poison_turns": 0, "poison_damage": 0, "img_url": "images/last_boss.jpg"},
      ],
  }
  st.session_state.enemies = st.session_state.stage_enemies[st.session_state.stage]
  st.session_state.current_actor_id = st.session_state.players[0]["id"]  # プレイヤーのIDで管理
  st.session_state.current_enemy_idx = 0
  st.session_state.turn_phase = "player_turn"  # "player_turn" または "enemy_turn"
  st.session_state.battle_log = [
      f"ステージ {st.session_state.stage} 開始！味方1体が行動します。"
  ]


def add_log(msg):
  st.session_state.battle_log.insert(0, msg)


# --- 敵の列シフト処理 (4列目 -> 3列目) ---
def update_enemy_positions():
  alive_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]
  for r in range(3):
    col3_enemy = next((e for e in alive_enemies if e["pos"] == (r, 3)), None)
    col4_enemy = next((e for e in alive_enemies if e["pos"] == (r, 4)), None)
    
    if col3_enemy is None and col4_enemy is not None:
      col4_enemy["pos"] = (r, 3)
      add_log(f"🔄 {col4_enemy['name']} が空いた3列目に前進しました！")

def advance_to_next_player():
  living = [p for p in st.session_state.players if p["hp"] > 0]
  if not living:
    return

  # 現在の actor_id を持つプレイヤーの、生存リスト内での位置（インデックス）を探す
  current_idx = 0
  for i, p in enumerate(living):
    if p["id"] == st.session_state.current_actor_id:
      current_idx = i
      break

  # 次の人のインデックス
  next_idx = (current_idx + 1) % len(living)
  st.session_state.current_actor_id = living[next_idx]["id"]
# --- 勝利・敗北判定 ---
living_players = [p for p in st.session_state.players if p["hp"] > 0]
living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]

st.title(f"⚔️ タクティカル・デュエルバトル (ステージ {st.session_state.stage} / 10)")

if not living_enemies:
  if st.session_state.stage < 10:
    st.success(f"🎉 ステージ {st.session_state.stage} クリア！")
    
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
      
      # --- 【追加】ステージ進行時に味方キャラの位置を初期配置にリセット ---
      initial_positions = [(0, 2), (1, 2), (2, 2), (0, 1), (1, 1), (2, 1)]
      for i, p in enumerate(st.session_state.players):
        if i < len(initial_positions):
          p["pos"] = initial_positions[i]
      # ------------------------------------------------------------------

      st.session_state.current_actor_id = st.session_state.players[0]["id"]  # プレイヤーのIDで管理
      st.session_state.current_enemy_idx = 0
      st.session_state.turn_phase = "player_turn"
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

# --- 3×6 バトルフィールドの描画 ---
st.subheader("🗺️ 戦場マップ (3行 × 6列)")

grid_map = [[None for _ in range(6)] for _ in range(3)]

for p in living_players:
  r, c = p["pos"]
  grid_map[r][c] = ("player", p)

for e in living_enemies:
  r, c = e["pos"]
  grid_map[r][c] = ("enemy", e)

# 現在のIDを持つ生存プレイヤーを探す。存在しない（倒された）場合は最初の生存プレイヤーにフォールバック
current_p = next((p for p in living_players if p["id"] == st.session_state.current_actor_id), None)
if current_p is None and living_players:
  current_p = living_players[0]
  st.session_state.current_actor_id = current_p["id"]

for r in range(3):
  cols = st.columns(6)
  for c in range(6):
    with cols[c]:
      cell_content = grid_map[r][c]
      
      is_attackable = False
      if st.session_state.turn_phase == "player_turn" and current_p and cell_content:
        etype, edata = cell_content
        if etype == "enemy":
          pr, pc = current_p["pos"]
          er, ec = edata["pos"]
          for card in current_p["cards"]:
            if card["type"] == "attack":
              if any((pr + dr, pc + dc) == (er, ec) for dr, dc in card["range"]):
                is_attackable = True
                break

      with st.container(border=True):
        if cell_content is None:
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
            st.image(data["img_url"], use_container_width=True)
            st.markdown(f"<div style='font-size:11px; text-align:center;'><b>{data['name']}</b></div>", unsafe_allow_html=True)
            hp_ratio = max(0.0, min(1.0, data["hp"] / data["max_hp"]))
            st.progress(hp_ratio, text=f"HP: {data['hp']}/{data['max_hp']}")
          else:
            highlight_label = " 🎯【攻撃可能】" if is_attackable else ""
            st.image(data["img_url"], use_container_width=True)
            st.markdown(f"<div style='font-size:11px; text-align:center;'><b>{data['name']}</b>{highlight_label}</div>", unsafe_allow_html=True)
            hp_ratio = max(0.0, min(1.0, data["hp"] / data["max_hp"]))
            st.progress(hp_ratio, text=f"HP: {data['hp']}/{data['max_hp']}")
            
st.markdown("---")

# --- 交互ターン制の処理 ---
if st.session_state.turn_phase == "player_turn":
  # 生存している全敵の毒処理
  for e in living_enemies:
    if e["hp"] > 0 and e["poison_turns"] > 0:
      e["hp"] -= e["poison_damage"]
      if e["hp"] < 0:
        e["hp"] = 0
      e["poison_turns"] -= 1
      add_log(f"☠️ {e['name']} は毒により {e['poison_damage']} の継続ダメージを受けた！（残り {e['poison_turns']} ターン）")
  
  update_enemy_positions()
  living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]
  if not living_enemies or not living_players:
    st.rerun()

  

  # 現在のIDを持つ生存プレイヤーを探す。存在しない（倒された）場合は最初の生存プレイヤーにフォールバック
  current_p = next((p for p in living_players if p["id"] == st.session_state.current_actor_id), None)
  if current_p is None and living_players:
    current_p = living_players[0]
    st.session_state.current_actor_id = current_p["id"]

  # --- 自動パス判定：移動も攻撃も不可能な状態かチェック ---
  can_move = False
  can_attack = False

  for card in current_p["cards"]:
    if card["type"] == "move":
      pr, pc = current_p["pos"]
      nr, nc = pr + card["dr"], pc + card["dc"]
      if 0 <= nr < 3 and 0 <= nc < 6:
        occupied = any(p["pos"] == (nr, nc) for p in living_players) or any(e["pos"] == (nr, nc) for e in living_enemies)
        if not occupied:
          can_move = True
    elif card["type"] == "attack":
      pr, pc = current_p["pos"]
      for e in living_enemies:
        er, ec = e["pos"]
        if any((pr + dr, pc + dc) == (er, ec) for dr, dc in card["range"]):
          can_attack = True
          break
    elif card["type"] == "heal":
      can_attack = True # 回復スキル持ちは常に行動可能とみなす

 # 現在のキャラの行（r）と列（c）を取得
  pr, pc = current_p["pos"]
  
  # 上のマス（r - 1, c）および下のマス（r + 1, c）にマップの範囲内で存在する味方がいるか、またそれが生存しているか確認
  up_exists = pr - 1 >= 0
  down_exists = pr + 1 < 3
  
  up_ally_alive = any(p["pos"] == (pr - 1, pc) and p["hp"] > 0 for p in st.session_state.players) if up_exists else False
  down_ally_alive = any(p["pos"] == (pr + 1, pc) and p["hp"] > 0 for p in st.session_state.players) if down_exists else False

  # 「攻撃範囲内に敵がいない」かつ「上または下の存在する味方キャラが生存している」場合に自動パス
  has_surviving_adjacent_ally = (up_exists and up_ally_alive) or (down_exists and down_ally_alive)

  if not can_move and not can_attack and has_surviving_adjacent_ally:
    add_log(f"💤 {current_p['name']} は移動も攻撃もできず、周囲に生存している味方がいるため、自動で待機しました。")
    st.session_state.turn_phase = "player_turn"
    advance_to_next_player()
    st.rerun()
  # ----------------------------------------------------

  col_info, col_action = st.columns([1, 3])
  with col_info:
    st.markdown("### 👤 現在の行動キャラ")
    st.image(current_p["img_url"], width=70)
    st.markdown(f"**{current_p['name']}**")
    hp_ratio = max(0.0, min(1.0, current_p["hp"] / current_p["max_hp"]))
    st.progress(hp_ratio, text=f"HP: {current_p['hp']}/{current_p['max_hp']}")

  with col_action:
    st.markdown("### 🎯 ターゲットの選択")
    
    # --- 【変更】プリースト（id=5）のターンのみ「味方を回復する」を選択肢に含める ---
    if current_p["id"] == 5:
      target_type_tab = st.radio("行動対象の選択", ["敵を攻撃する", "味方を回復する"], horizontal=True)
    else:
      target_type_tab = "敵を攻撃する"
      st.markdown("<div style='font-size: 14px; color: #666; margin-bottom: 10px;'>行動対象: <b>敵を攻撃する</b></div>", unsafe_allow_html=True)
    
    if target_type_tab == "敵を攻撃する":
      # --- 【変更】現在選択しているキャラクターの攻撃カードの範囲内にいる敵のみをフィルタリング ---
      attackable_enemies = []
      pr, pc = current_p["pos"]
      
      for e in living_enemies:
        er, ec = e["pos"]
        is_in_range = False
        for card in current_p["cards"]:
          if card["type"] == "attack":
            if any((pr + dr, pc + dc) == (er, ec) for dr, dc in card["range"]):
              is_in_range = True
              break
        if is_in_range:
          attackable_enemies.append(e)
          
      if attackable_enemies:
        enemy_options = {
            f"{e['name']} (位置: {e['pos']}, HP: {e['hp']})": e
            for e in attackable_enemies
        }
        selected_label = st.selectbox("ターゲットの敵を選択", list(enemy_options.keys()))
        target_enemy = enemy_options[selected_label]
      else:
        st.warning("⚠️ 現在のポジションから攻撃範囲内にいる敵がいません。移動スキルやパスを使用してください。")
        target_enemy = None
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
        
        # --- 【追加】攻撃カードの威力、回復カードの回復力をカード詳細に表示 ---
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

        if st.button("このカードを使う", key=f"card_{current_p['id']}_{idx}"):
          # (以降の処理はそのまま)
          if card["type"] == "move":
            pr, pc = current_p["pos"]
            nr, nc = pr + card["dr"], pc + card["dc"]
            
            # 【修正】マップの範囲内かチェック (3行 × 6列)
            if 0 <= nr < 3 and 0 <= nc < 6:
              # 移動先に他の味方または敵がいるかチェック
              target_player_occupied = any(p["pos"] == (nr, nc) for p in st.session_state.players if p["hp"] > 0)
              target_enemy_occupied = any(e["pos"] == (nr, nc) for e in st.session_state.enemies if e["hp"] > 0)
              
              if not target_player_occupied and not target_enemy_occupied:
                # 【修正】st.session_state.players と current_p の両方の位置を確実涯更新
                for p in st.session_state.players:
                  if p["id"] == current_p["id"]:
                    p["pos"] = (nr, nc)
                current_p["pos"] = (nr, nc)
                
                add_log(
                    f"🏃 {current_p['name']} は '{card['name']}' で"
                    f" ({nr}, {nc}) に移動しました。"
                )
              else:
                add_log(f"⚠️ そのマスには既にキャラクターが存在するため移動できません。")
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
                
                update_enemy_positions()

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

          # 1体の行動が終了したら、即座に敵のターン（フェーズ）に切り替える
          st.session_state.turn_phase = "enemy_turn"
          
          st.rerun()

  if st.button("このキャラクターの行動をパスする"):
    add_log(f"💤 {current_p['name']} はその場で待機しました。")
    st.session_state.turn_phase = "player_turn"  # 敵のターンにせず、味方のターンのまま継続
    advance_to_next_player()
    st.rerun()

elif st.session_state.turn_phase == "enemy_turn":
  st.warning("⚠️ **敵のターン（個別行動）**です。")
  
  # 常に最新の生存敵リストを取得
  living_enemies = [e for e in st.session_state.enemies if e["hp"] > 0]
  
  if living_enemies:
    # 敵の数が減った際のインデックスオーバーを防ぐため、ここで確実に剰余を取る
    
    active_enemy = living_enemies[st.session_state.current_enemy_idx]
    
    if st.button(f"👹 {active_enemy['name']} の行動を実行する", type="primary"):
      target_p = min(living_players, key=lambda p: (p["pos"][1], p["hp"]))
      
      import random as rand
      is_softened = rand.random() < 0.25
      actual_damage = active_enemy["damage"] // 2 if is_softened else active_enemy["damage"]
      
      target_p["hp"] -= actual_damage
      if target_p["hp"] < 0:
        target_p["hp"] = 0
        
      if is_softened:
        add_log(
            f"🎯 {active_enemy['name']} は {target_p['name']} を狙ったが、"
            f"攻撃が少し緩み {actual_damage} のダメージに抑えられた！"
        )
      else:
        add_log(
            f"💥 {active_enemy['name']} は戦術的に {target_p['name']} を集中狙撃した！"
            f" {actual_damage} の手痛いダメージ！"
        )
      
      # 次の敵へインデックスを進める
      st.session_state.current_enemy_idx += 1
      st.session_state.turn_phase = "player_turn"
      
      advance_to_next_player()
        
      add_log(f"🛡️ 敵の行動終了。次の味方のターンです！")
      st.rerun()
  else:
    st.session_state.turn_phase = "player_turn"
    st.rerun()
# --- バトルログ ---
st.markdown("---")
st.subheader("📜 バトルログ")
for log in st.session_state.battle_log[:5]:
  st.text(log)
