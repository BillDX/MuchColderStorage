# MuchColderStorage: a haunted data center adventure by gpt-oss-20b

A small Infocom-style text adventure about escaping a haunted data center. It was written by OpenAI's open-weight gpt-oss-20b model running locally in Ollama, driven by the Codex command-line agent.

It's one of three runs of the same prompt:

- [COLD STORAGE](https://mrfuture.com/projects/cold-storage/): Qwen3.8 27B on a 64GB MacBook Pro, through the Pi coding agent ([repo](https://github.com/BillDX/coldstorage)).
- [ColderStorage](https://github.com/BillDX/ColderStorage): DeepSeek V4.1 Flash on Ollama Cloud, through Codex and Ollama.
- MuchColderStorage (this repo): gpt-oss-20b, local, through Codex and Ollama.

The write-up comparing all three: [Codex + Ollama: an easier route to coding with local LLMs](https://mrfuture.com/2026/10/codex-ollama-local-llms/).

The code and tests are the model's output, unedited. This README was added afterwards; the model didn't write one.

## Run it

Python 3, standard library only.

```bash
python3 main.py
```

Commands: `look`, `go <direction>` (or `n`, `s`, `e`, `w`), `take <item>`, `use <item>`, `inventory` and `quit`.

## Test it

```bash
python3 -m unittest test_game.py
```

All 11 tests pass.

## How the run went

- It took six prompts in all. After the first, the model had to be asked for the run command and where the files were, then asked twice to actually save them to disk.
- The result has seven rooms and a short chain of puzzles, and it can be won.

## Known issue

Going north from the Security Office crashes the game with `KeyError: 'Vault'`. The exit points at a room called "Vault", but the room is named "Data Storage Vault", and no test covers that exit. It's left as the model wrote it.

## The prompt

> lets make a fun/funny standalone text adventure game, similar to an infocom adventure, about escaping from a haunted data center. writing it in python seems reasonable. It should have inventory, clever puzzles, humorous descriptions, and multiple goals needed to be able to escape the data center as the main goal. It should be solvable, and the solutions should be fairly logical. But the most important thing is to make it very fun. while coding make sure we use red/green style testing both for unit testing and for overall playthrough testing.
