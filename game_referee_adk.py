import random
from typing import Dict

# simple local ADK-style helpers
def tool(func):
    return func

class Agent:
    def __init__(self, name: str):
        self.name = name


# game memory (single source of truth)
def initialize_game_state() -> Dict:
    return {
        "round": 1,
        "max_rounds": 3,
        "scores": {"user": 0, "bot": 0},
        "bomb_used": {"user": False, "bot": False}
    }


@tool
def validate_move(move: str, player: str, state: Dict) -> Dict:
    move = move.lower().strip()
    valid_moves = {"rock", "paper", "scissors", "bomb"}

    if move not in valid_moves:
        return {"valid": False, "move": None, "reason": "Invalid input"}

    if move == "bomb" and state["bomb_used"][player]:
        return {"valid": False, "move": None, "reason": "Bomb already used"}

    return {"valid": True, "move": move, "reason": None}


@tool
def resolve_round(user_move: str, bot_move: str) -> str:
    if user_move == bot_move:
        return "draw"

    if user_move == "bomb":
        return "user"

    if bot_move == "bomb":
        return "bot"

    wins_against = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    return "user" if wins_against[user_move] == bot_move else "bot"


@tool
def update_game_state(
    state: Dict,
    result: str,
    user_move: str,
    bot_move: str
) -> Dict:
    if user_move == "bomb":
        state["bomb_used"]["user"] = True

    if bot_move == "bomb":
        state["bomb_used"]["bot"] = True

    if result == "user":
        state["scores"]["user"] += 1
    elif result == "bot":
        state["scores"]["bot"] += 1

    state["round"] += 1
    return state


# bot plays independently every round
def get_bot_move(state: Dict) -> str:
    moves = ["rock", "paper", "scissors"]

    if not state["bomb_used"]["bot"] and random.random() < 0.15:
        return "bomb"

    return random.choice(moves)


class GameRefereeAgent(Agent):
    def __init__(self):
        super().__init__(name="GameReferee")
        self.state = initialize_game_state()

    def explain_rules(self) -> str:
        return (
            "Rules:\n"
            "• Best of 3 rounds\n"
            "• Moves: rock, paper, scissors, bomb (once)\n"
            "• Bomb beats everything\n"
            "• Invalid input wastes the round"
        )

    def handle_turn(self, user_input: str) -> str:
        state = self.state

        if state["round"] > state["max_rounds"]:
            return self.final_result()

        validation = validate_move(user_input, "user", state)
        bot_move = get_bot_move(state)

        if not validation["valid"]:
            self.state = update_game_state(
                state=state,
                result="draw",
                user_move="",
                bot_move=bot_move
            )
            return (
                f"Round {state['round'] - 1}/{state['max_rounds']}\n"
                "Invalid move. Round wasted.\n"
                f"Bot played: {bot_move}\n"
            )

        user_move = validation["move"]
        result = resolve_round(user_move, bot_move)

        self.state = update_game_state(
            state=state,
            result=result,
            user_move=user_move,
            bot_move=bot_move
        )

        return (
            f"Round {state['round'] - 1}/{state['max_rounds']}\n"
            f"You played: {user_move}\n"
            f"Bot played: {bot_move}\n"
            f"Winner: {result}\n"
            f"Score → You: {state['scores']['user']} | "
            f"Bot: {state['scores']['bot']}\n"
        )

    def final_result(self) -> str:
        user = self.state["scores"]["user"]
        bot = self.state["scores"]["bot"]

        if user > bot:
            return "Game Over. Final Result: You win 🎉"
        elif bot > user:
            return "Game Over. Final Result: Bot wins 🤖"
        else:
            return "Game Over. Final Result: Draw 🤝"


# basic chat-style loop
if __name__ == "__main__":
    agent = GameRefereeAgent()
    print(agent.explain_rules())

    while True:
        user_input = input("\nYour move: ")
        response = agent.handle_turn(user_input)
        print(response)

        if "Game Over" in response:
            break
