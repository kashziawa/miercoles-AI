# ノートブック上で使う pip のセル記法は通常の Python スクリプトでは使えないため、
# ここでは依存関係の有無を確認してから読み込みます。
try:
    import japanize_matplotlib
except ModuleNotFoundError:
    print("japanize-matplotlib が未インストールのため、日本語表示は無効です。")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. データ生成
# ------------------------------
# ※ シードを固定していないため、実行するたびに異なるデータが生成されます

# 架空の球団(12球団)
teams = [
    "東京イーグルス", "大阪タイガース", "名古屋ドラゴンズ",
    "福岡ホークス", "札幌ベアーズ", "横浜マリナーズ",
    "広島カープス", "千葉マリンズ", "仙台イーグレット",
    "京都サムライズ", "神戸ウェイブス", "埼玉ライオンズ"
]

# 選手生成(投手・野手)
positions = ["投手", "捕手", "内野手", "外野手"]
players = []
player_id = 1
for team in teams:
    for _ in range(25):  # 1球団25名想定
        pos = np.random.choice(positions, p=[0.4, 0.1, 0.3, 0.2])
        players.append({
            "player_id": player_id,
            "team": team,
            "position": pos,
            "name": f"選手{player_id:04d}"
        })
        player_id += 1

players_df = pd.DataFrame(players)

# 試合日程生成(総当たり、各カード3試合)
game_records = []
game_id = 1
start_date = pd.Timestamp("2026-03-28")

for home in teams:
    for away in teams:
        if home == away:
            continue
        for _ in range(3):
            game_date = start_date + pd.Timedelta(days=game_id % 150)
            game_records.append({
                "game_id": game_id,
                "date": game_date,
                "home_team": home,
                "away_team": away,
            })
            game_id += 1

games_df = pd.DataFrame(game_records)

# 試合結果(スコア)生成
def generate_score():
    return np.random.poisson(lam=4.2)

games_df["home_score"] = [generate_score() for _ in range(len(games_df))]
games_df["away_score"] = [generate_score() for _ in range(len(games_df))]

# 同点なら延長でどちらかに1点追加
tie_mask = games_df["home_score"] == games_df["away_score"]
adjust = np.random.choice([0, 1], size=tie_mask.sum())
games_df.loc[tie_mask, "home_score"] += adjust

games_df["winner"] = np.where(
    games_df["home_score"] > games_df["away_score"],
    games_df["home_team"],
    games_df["away_team"]
)

# 打撃成績生成(スタメン9人想定、簡略化)
batting_records = []
batters = players_df[players_df["position"] != "投手"]

for _, game in games_df.iterrows():
    for team_name in [game["home_team"], game["away_team"]]:
        team_batters = batters[batters["team"] == team_name].sample(9)
        for _, batter in team_batters.iterrows():
            at_bats = np.random.randint(2, 6)
            hits = np.random.binomial(at_bats, 0.27)
            home_runs = np.random.binomial(1, 0.06)
            rbi = np.random.poisson(0.8)
            batting_records.append({
                "game_id": game["game_id"],
                "player_id": batter["player_id"],
                "name": batter["name"],
                "team": team_name,
                "at_bats": at_bats,
                "hits": hits,
                "home_runs": home_runs,
                "rbi": rbi
            })

batting_df = pd.DataFrame(batting_records)

# 投手成績生成(先発投手のみ簡略化)
pitching_records = []
pitchers = players_df[players_df["position"] == "投手"]

for _, game in games_df.iterrows():
    for team_name in [game["home_team"], game["away_team"]]:
        pitcher = pitchers[pitchers["team"] == team_name].sample(1).iloc[0]
        innings = round(np.random.uniform(5, 9), 1)
        earned_runs = np.random.poisson(3)
        strikeouts = np.random.poisson(6)
        walks = np.random.poisson(2)
        pitching_records.append({
            "game_id": game["game_id"],
            "player_id": pitcher["player_id"],
            "name": pitcher["name"],
            "team": team_name,
            "innings_pitched": innings,
            "earned_runs": earned_runs,
            "strikeouts": strikeouts,
            "walks": walks
        })

pitching_df = pd.DataFrame(pitching_records)

print("=== データ生成完了 ===")
print("球団数:", len(teams))
print("選手数:", len(players_df))
print("試合数:", len(games_df))
print("打撃記録数:", len(batting_df))
print("投手記録数:", len(pitching_df))

# ------------------------------
# 2. 定量分析
# ------------------------------

# --- チーム勝敗表 ---
team_stats = []
for team in teams:
    wins = (games_df["winner"] == team).sum()
    home_games = games_df[games_df["home_team"] == team]
    away_games = games_df[games_df["away_team"] == team]
    total_games = len(home_games) + len(away_games)
    losses = total_games - wins
    win_pct = wins / total_games if total_games > 0 else 0

    runs_scored = home_games["home_score"].sum() + away_games["away_score"].sum()
    runs_allowed = home_games["away_score"].sum() + away_games["home_score"].sum()

    team_stats.append({
        "team": team,
        "games": total_games,
        "wins": wins,
        "losses": losses,
        "win_pct": round(win_pct, 3),
        "runs_scored": runs_scored,
        "runs_allowed": runs_allowed,
        "run_diff": runs_scored - runs_allowed
    })

team_stats_df = pd.DataFrame(team_stats).sort_values("win_pct", ascending=False).reset_index(drop=True)
print("\n=== チーム成績(勝率順) ===")
print(team_stats_df.to_string(index=False))

# --- 個人打撃成績(打率) ---
batting_summary = batting_df.groupby(["player_id", "name", "team"]).agg(
    total_at_bats=("at_bats", "sum"),
    total_hits=("hits", "sum"),
    total_home_runs=("home_runs", "sum"),
    total_rbi=("rbi", "sum")
).reset_index()

batting_summary["batting_avg"] = round(
    batting_summary["total_hits"] / batting_summary["total_at_bats"], 3
)

top_batters = batting_summary[batting_summary["total_at_bats"] >= 50].sort_values(
    "batting_avg", ascending=False
).head(10)

print("\n=== 打率ランキング TOP10(規定打席以上) ===")
print(top_batters.to_string(index=False))

# --- 個人投手成績(防御率) ---
pitching_summary = pitching_df.groupby(["player_id", "name", "team"]).agg(
    total_innings=("innings_pitched", "sum"),
    total_earned_runs=("earned_runs", "sum"),
    total_strikeouts=("strikeouts", "sum"),
    total_walks=("walks", "sum")
).reset_index()

pitching_summary["era"] = round(
    (pitching_summary["total_earned_runs"] * 9) / pitching_summary["total_innings"], 2
)

top_pitchers = pitching_summary[pitching_summary["total_innings"] >= 30].sort_values(
    "era"
).head(10)

print("\n=== 防御率ランキング TOP10(規定投球回以上) ===")
print(top_pitchers.to_string(index=False))

# --- リーグ全体サマリー ---
league_summary = {
    "総試合数": len(games_df),
    "総得点数": games_df["home_score"].sum() + games_df["away_score"].sum(),
    "平均得点/試合": round((games_df["home_score"] + games_df["away_score"]).mean(), 2),
    "リーグ平均打率": round(batting_df["hits"].sum() / batting_df["at_bats"].sum(), 3),
    "リーグ平均防御率": round(
        (pitching_df["earned_runs"].sum() * 9) / pitching_df["innings_pitched"].sum(), 2
    )
}

print("\n=== リーグ全体サマリー ===")
for k, v in league_summary.items():
    print(f"{k}: {v}")

# ------------------------------
# 3. グラフ出力
# ------------------------------

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# グラフ1: チーム勝率ランキング
ax1 = axes[0, 0]
sorted_teams = team_stats_df.sort_values("win_pct", ascending=True)
ax1.barh(sorted_teams["team"], sorted_teams["win_pct"], color="steelblue")
ax1.set_xlabel("勝率")
ax1.set_title("チーム勝率ランキング")
ax1.axvline(0.5, color="gray", linestyle="--", linewidth=1)

# グラフ2: 得失点差(散布図)
ax2 = axes[0, 1]
ax2.scatter(team_stats_df["runs_scored"], team_stats_df["runs_allowed"],
            s=100, color="orangered")
for _, row in team_stats_df.iterrows():
    ax2.annotate(row["team"], (row["runs_scored"], row["runs_allowed"]),
                 fontsize=8, xytext=(3, 3), textcoords="offset points")
max_val = max(team_stats_df["runs_scored"].max(), team_stats_df["runs_allowed"].max())
ax2.plot([0, max_val], [0, max_val], color="gray", linestyle="--")
ax2.set_xlabel("総得点")
ax2.set_ylabel("総失点")
ax2.set_title("チーム別 得点 vs 失点")

# グラフ3: 打率TOP10
ax3 = axes[1, 0]
ax3.bar(top_batters["name"], top_batters["batting_avg"], color="seagreen")
ax3.set_ylabel("打率")
ax3.set_title("打率ランキング TOP10")
ax3.tick_params(axis="x", rotation=75)

# グラフ4: 防御率TOP10
ax4 = axes[1, 1]
ax4.bar(top_pitchers["name"], top_pitchers["era"], color="mediumpurple")
ax4.set_ylabel("防御率")
ax4.set_title("防御率ランキング TOP10")
ax4.tick_params(axis="x", rotation=75)

plt.tight_layout()
plt.show()

# 追加グラフ: 1試合あたりの得点分布
plt.figure(figsize=(8, 5))
total_runs_per_game = games_df["home_score"] + games_df["away_score"]
plt.hist(total_runs_per_game, bins=range(0, total_runs_per_game.max() + 2),
         color="cornflowerblue", edgecolor="black")
plt.xlabel("1試合の合計得点")
plt.ylabel("試合数")
plt.title("1試合あたりの得点分布")
plt.show()
