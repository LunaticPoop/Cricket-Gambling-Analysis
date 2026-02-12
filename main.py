import pandas as pd
import requests
import time

API_KEY = "tBMfe0EWTo6YuRvH1jWRC6fE32vyGeKV9AV8C6hn"
URL = "https://api.scaledown.xyz/compress/raw/"


# ===============================
# 1️⃣ Compress Prompt
# ===============================
def compress_prompt(context: str, prompt: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    payload = {
        "context": context.strip(),
        "prompt": prompt.strip(),
        "scaledown": {"rate": "auto"}
    }

    time.sleep(1)

    response = requests.post(URL, json=payload, headers=headers)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"ScaleDown failed: {data}")

    return data


# ===============================
# 2️⃣ Generate Prompt
# ===============================
def generate_cricket_prompt(match: dict):
    context = """
You are a cricket analytics AI.
Generate structured insights without giving betting advice.
"""

    prompt = f"""
Teams: {match['team_a']} vs {match['team_b']}
Format: {match['format']}
Venue: {match['venue']}
Pitch: {match['pitch']}
Weather: {match['weather']}
Opening Odds: {match['opening_odds']}
Latest Odds: {match['latest_odds']}
"""

    return context, prompt


# ===============================
# 3️⃣ Dataset Loader
# ===============================
def load_match_from_dataset(match_id: int) -> dict:
    df = pd.read_csv("matches.csv")
    row = df[df["match_id"] == match_id].iloc[0]

    return {
        "team_a": row["team_a"],
        "team_b": row["team_b"],
        "format": row["format"],
        "venue": row["venue"],
        "pitch": row["pitch"],
        "weather": row["weather"],
        "team_a_form": row["team_a_form"],
        "team_b_form": row["team_b_form"],
        "opening_odds": float(row["opening_odds"]),
        "latest_odds": float(row["latest_odds"])
    }


# ===============================
# 4️⃣ Probability
# ===============================
def implied_probability(odds: float) -> float:
    return (1 / odds) * 100


def create_range(center: float, spread: float = 3) -> str:
    lower = round(center - spread, 1)
    upper = round(center + spread, 1)
    return f"{lower}–{upper}%"


# ===============================
# 5️⃣ Market Shift
# ===============================
def detect_market_shift(opening_odds, latest_odds):
    open_prob = 1 / opening_odds
    latest_prob = 1 / latest_odds
    change = (latest_prob - open_prob) * 100

    if change > 5:
        return "Market is strongly favoring this team now."
    elif change > 2:
        return "Market confidence has increased a little."
    elif change < -5:
        return "Market confidence dropped sharply."
    elif change < -2:
        return "Market confidence dropped slightly."
    else:
        return "Market has been stable."


# ===============================
# 6️⃣ Toss Simulation
# ===============================
def simulate_toss(center_prob: float):
    return {
        "If batting first": create_range(center_prob - 3),
        "If chasing": create_range(center_prob + 3)
    }


# ===============================
# 7️⃣ Volatility
# ===============================
def calculate_volatility(opening_odds, latest_odds, format_type):
    shift = abs(opening_odds - latest_odds)
    score = shift * 10

    if format_type == "T20":
        score += 5

    if score > 8:
        return "High"
    elif score > 4:
        return "Medium"
    else:
        return "Low"


# ===============================
# 8️⃣ Venue Profiles
# ===============================
VENUE_PROFILE = {
    "Wankhede Stadium": "High scoring ground where chasing is easier.",
    "Eden Gardens": "Spin bowlers usually do well here.",
    "Edgbaston": "Seam bowlers can get movement here.",
    "MCG": "Balanced pitch with big boundaries."
}


# ===============================
# 9️⃣ Confidence
# ===============================
def calculate_confidence(opening_odds, latest_odds):
    shift = abs(opening_odds - latest_odds)

    if shift > 0.3:
        return "High"
    elif shift > 0.15:
        return "Medium"
    else:
        return "Low"


# ===============================
# 🔟 Run Analysis
# ===============================
def run_analysis(match_data):
    try:
        context, prompt = generate_cricket_prompt(match_data)
        compressed = compress_prompt(context, prompt)
        results = compressed["results"]

        center = implied_probability(match_data["latest_odds"])

        analysis = {
            "win_probability": {
                match_data["team_a"]: create_range(center),
                match_data["team_b"]: create_range(100 - center)
            },
            "toss_scenarios": simulate_toss(center),
            "market_signal": detect_market_shift(
                match_data["opening_odds"],
                match_data["latest_odds"]
            ),
            "volatility": calculate_volatility(
                match_data["opening_odds"],
                match_data["latest_odds"],
                match_data["format"]
            ),
            "venue_profile": VENUE_PROFILE.get(
                match_data["venue"],
                "Neutral pitch conditions."
            ),
            "confidence": calculate_confidence(
                match_data["opening_odds"],
                match_data["latest_odds"]
            )
        }

        return {
            "compression_ratio": round(
                results["compressed_prompt_tokens"]
                / results["original_prompt_tokens"], 2
            ),
            "latency_ms": compressed["latency_ms"],
            "analysis": analysis
        }

    except Exception as e:
        print("Error:", e)
        return None


# ===============================
# 🧸 Toddler Mode
# ===============================
def toddler_mode(match_name, output):
    a = output["analysis"]
    teams = list(a["win_probability"].keys())
    team_a = teams[0]

    return f"""
🧸 Match: {match_name}

🟢 {team_a} has about {a['win_probability'][team_a]} chance of winning.

🏟 Venue insight: {a['venue_profile']}

🔄 Toss scenarios:
   - {list(a['toss_scenarios'].keys())[0]} → {list(a['toss_scenarios'].values())[0]}
   - {list(a['toss_scenarios'].keys())[1]} → {list(a['toss_scenarios'].values())[1]}

📈 Market update: {a['market_signal']}

⚡ Risk level: {a['volatility']}

🧠 Confidence level: {a['confidence']}

⏱️ System processed this in {output['latency_ms']} ms.
""".strip()


# ===============================
# ▶️ ENTRY POINT
# ===============================
if __name__ == "__main__":
    match_ids = [1, 2, 3, 4]

    print("\n=== FULL TODDLER MODE INTELLIGENCE ===\n")

    for match_id in match_ids:
        match = load_match_from_dataset(match_id)
        result = run_analysis(match)

        if result:
            name = f"{match['team_a']} vs {match['team_b']}"
            print(toddler_mode(name, result))
            print("\n" + "-" * 60 + "\n")
