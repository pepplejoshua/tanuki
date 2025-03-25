# tanuki

tanuki is a personal project to learn chess in the most roundabout, hands-on way possible—by building a chess platform from scratch. Named after the sly, adaptable tanuki of Japanese folklore, this project blends chess logic, AI, and a bit of mischief to create a tool for learning, playing, and experimenting. It’s a long-term journey, starting simple and growing into something bigger, all while documenting the process (and chaos) on a blog.

## Version 0 (v0): Single-Player Terminal Game
The first step is a bare-bones, single-player chess game that runs in the terminal. Built entirely from scratch (no chess libraries), v0 is about laying the groundwork and having fun while learning.

### What’s in v0:
- **Chess Logic:** A custom-built chess engine with an 8x8 board, piece movement (starting with basics like pawns), and move validation. No fancy rules like castling or en passant yet—just enough to play.
- **Text-Based UI (TUI):** A terminal interface showing the board with Unicode chess symbols (♜♞♝♛♚♟ for Black, ♖♘♗♕♔♙ for White). Players input moves in standard notation (e.g., "e2e4").
- **Basic AI (lvl0):** A simple opponent using the minimax algorithm (depth 2-4) to give you a challenge. No ML yet—just pure search.

### Goals for v0:
- Play a full game against the AI in the terminal.
- Build a solid foundation for future features.
- Learn chess and coding along the way.

### Implementation Progress

#### Piece Movement
| Piece  | Basic Moves | Move Preview | Special Moves |
|--------|-------------|--------------|---------------|
| Pawn   | ✅         | ✅           | ❌ En Passant, Promotion |
| Knight | ✅         | ✅           | N/A |
| Bishop | ✅         | ✅           | N/A |
| Rook   | ✅         | ❌           | ❌ Castling |
| Queen  | ❌         | ❌           | N/A |
| King   | ❌         | ❌           | ❌ Castling |

#### Game Features
| Feature | Status | Notes |
|---------|--------|-------|
| Move Validation | ✅ | For implemented pieces |
| Move Preview | ✅ | Shows possible moves with color coding |
| Move History | ❌ | Needed for en passant, castling |
| Check Detection | ❌ | Required for valid moves |
| Checkmate Detection | ❌ | Required for game end |
| Turn System | ✅ | Alternates between white and black |
| AI Opponent | ❌ | Planned for future |

## Future Vision
Tanuki Chess won’t stop at v0. The long-term dream is a platform where people can learn chess, tweak AI models, and watch epic battles—human vs. AI, AI vs. AI, or whatever wild ideas come up. Here’s the rough vibe:

- **More AI Levels:** From beginner (shallow search) to advanced (deeper search, maybe ML later).
- **Tuning Panel:** Adjust AI styles (aggressive, defensive, chaotic) and watch them compete.
- **Online Hosting:** A web app where anyone can play, upload their own models, or spectate matches.
- **Game Expansion:** Add other strategy games (shogi, perhaps?) and then train an AI that tackles them all.
- **Learning Tools:** Tutor mode with move scoring, suggestions and feedback.

No detailed roadmap yet—this is a playground for experimentation. Each step will build on the last, with plenty of detours to keep it interesting.

## Why Tanuki?
Tanuki’s a trickster with a knack for adapting, just like this project. It’s not about the fastest path to a chess engine—it’s about the scenic route, picking up skills, and making something unique. Let’s see where it takes us!
