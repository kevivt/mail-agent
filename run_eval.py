from agent import classify_email
from eval_set import LABELED_EMAILS

def run_eval():
    correct = 0
    errors = []

    for e in LABELED_EMAILS:
        predicted = classify_email(e["subject"], e["sender"], "")
        is_correct = predicted == e["true_label"]
        correct += is_correct
        if not is_correct:
            errors.append({
                "subject": e["subject"],
                "true": e["true_label"],
                "predicted": predicted
            })

    accuracy = correct / len(LABELED_EMAILS) * 100
    print(f"\nAccuracy: {accuracy:.1f}% ({correct}/{len(LABELED_EMAILS)})\n")

    if errors:
        print("Misclassifications:")
        for err in errors:
            print(f"  '{err['subject']}' — true: {err['true']}, predicted: {err['predicted']}")

if __name__ == "__main__":
    run_eval()