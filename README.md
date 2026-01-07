
# AI Game Referee – Rock–Paper–Scissors–Plus

This project implements a **stateful conversational agent** that functions as a referee for a constrained game of **Rock–Paper–Scissors–Plus**.
It was developed for the **upliance.ai – AI Product Engineer (Conversational Agents)** assignment, with emphasis on **agent architecture, state management, and tool-driven logic**.

---

## Functional Overview

The agent runs a **best-of-3** game between a user and the bot.
For each turn, it:

* Accepts user input
* Validates the move against game constraints
* Resolves the round outcome deterministically
* Updates and persists game state
* Generates an explicit, structured response

The game **automatically terminates after three rounds**.

### Rules Enforced

* Valid moves: `rock`, `paper`, `scissors`, `bomb`
* Each player may use `bomb` **once per game**
* `bomb` defeats all other moves
* Invalid input wastes the round

---

## Architecture

The solution follows a clear **separation of concerns**, aligned with production conversational agent design.

### State

A single in-memory state object tracks:

* current round and maximum rounds
* user and bot scores
* bomb usage per player

State persists across conversational turns and is **not embedded in prompts**.

---

### Tools

Core logic is implemented via explicit tools:

* **`validate_move`** — input validation and rule enforcement
* **`resolve_round`** — deterministic outcome computation
* **`update_game_state`** — controlled state mutation

This ensures logic is **testable, deterministic, and decoupled** from response generation.

---

### Agent

The agent acts as an orchestrator:

* sequences tool calls
* controls game flow
* formats user-facing responses
* enforces termination conditions

Business logic resides in tools, not in the agent’s reasoning layer.

---

## Design Rationale

The architecture mirrors real-world conversational systems where:

* state must persist reliably
* rules must be enforced consistently
* tools handle logic and side effects
* agents focus on flow control and communication

The game serves as a minimal proxy for more complex **workflow or policy-enforcement agents**.

---

## Tradeoffs and Extensions

* Bot strategy is intentionally simple
* State is session-scoped (in-memory)
* CLI-based interface prioritizes correctness and clarity

Possible extensions include smarter bot behavior, replay support, and persistent state storage.

---

