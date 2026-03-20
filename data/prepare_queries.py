from pathlib import Path

from datasets import load_dataset


def sample_ubuntu_queries(num_samples: int = 50):
    """
    Load the Ubuntu Dialogue Corpus and print user utterances that you can
    manually adapt into e-commerce customer support queries.
    """
    print("Loading Ubuntu Dialogue Corpus (this may take some time on first run)...")
    dataset = load_dataset("rguo12/ubuntu_dialogue_corpus", "v2.0")
    train_data = dataset["train"]

    print(f"Total train examples: {len(train_data)}")
    print(f"Showing first {num_samples} user utterances for manual adaptation:\n")

    count = 0
    for example in train_data:
        # Many examples are stored as multi-turn conversations.
        # We take the 'utterances' field if available and print the first user message.
        utterances = example.get("utterances")
        if not utterances:
            continue

        # Each utterance is typically a dict with 'speaker' and 'text'
        for utt in utterances:
            text = utt.get("text", "").strip()
            speaker = utt.get("speaker", "").strip().lower()

            # You can adjust this heuristic if the structure of the dataset differs.
            # Here we just show non-empty texts.
            if text:
                print(f"- [{speaker}] {text}")
                count += 1
                if count >= num_samples:
                    return


if __name__ == "__main__":
    # Save a small log for reference (optional)
    out_dir = Path(__file__).resolve().parent
    out_file = out_dir / "ubuntu_samples.txt"

    # Capture printed samples into a file as well
    import io
    import sys

    buffer = io.StringIO()
    stdout_backup = sys.stdout
    sys.stdout = buffer

    try:
        sample_ubuntu_queries(num_samples=50)
    finally:
        sys.stdout = stdout_backup

    text = buffer.getvalue()
    print(text)  # still show on console

    out_file.write_text(text, encoding="utf-8")
    print(f"\nSaved sample utterances to {out_file}")
