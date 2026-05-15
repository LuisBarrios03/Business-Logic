import json
from pathlib import Path
from datetime import datetime, timezone
from pymongo import MongoClient


ROOT_DIR = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT_DIR / "analysis"

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ctf_assistant"
COLLECTION_NAME = "challenges"


def read_text_file(path: Path) -> str:
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8").strip()


def read_json_file(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing metadata file: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_challenge_document(challenge_dir: Path) -> dict:
    metadata_path = challenge_dir / "metadata.json"

    metadata = read_json_file(metadata_path)

    analysis_file = metadata.get("analysis_file", "analysis.md")
    ai_analysis_file = metadata.get("ai_analysis_file", "ai.md")
    solution_file = metadata.get("solution_file", "solution.md")

    document = {
        **metadata,
        "analysis": read_text_file(challenge_dir / analysis_file),
        "ai_analysis": read_text_file(challenge_dir / ai_analysis_file),
        "solution": read_text_file(challenge_dir / solution_file),
        "folder_path": str(challenge_dir.relative_to(ROOT_DIR)),
        "imported_at": datetime.now(timezone.utc).isoformat()
    }

    return document


def import_challenges():
    if not ANALYSIS_DIR.exists():
        raise FileNotFoundError(f"Analysis directory not found: {ANALYSIS_DIR}")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    imported = 0
    skipped = 0
    errors = []

    for challenge_dir in sorted(ANALYSIS_DIR.iterdir()):
        if not challenge_dir.is_dir():
            continue

        if not challenge_dir.name.startswith("XBEN-"):
            continue

        try:
            document = build_challenge_document(challenge_dir)

            challenge_id = document.get("challenge_id")

            if not challenge_id:
                raise ValueError(f"Missing challenge_id in {challenge_dir}")

            collection.update_one(
                {"challenge_id": challenge_id},
                {"$set": document},
                upsert=True
            )

            imported += 1
            print(f"[OK] Imported/updated {challenge_id}")

        except Exception as error:
            skipped += 1
            errors.append((challenge_dir.name, str(error)))
            print(f"[ERROR] {challenge_dir.name}: {error}")

    print("\nImport completed.")
    print(f"Imported/updated: {imported}")
    print(f"Skipped/errors: {skipped}")

    if errors:
        print("\nErrors:")
        for challenge_name, error in errors:
            print(f"- {challenge_name}: {error}")


if __name__ == "__main__":
    import_challenges()
