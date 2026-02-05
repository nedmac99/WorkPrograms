import csv
import sys
from pathlib import Path
from datetime import date

SEPARATOR = "----------------------------------------------------------------------------------------"


if getattr(sys, "frozen", False):
    base_dir = Path(sys.executable).parent
else:
    base_dir = Path(__file__).parent

file_path = base_dir / "output_progress.csv"

# Points
DEV_POINTS = {
    "QM Warranty": 0.75,
    "PM": 0.25,
    "Minor Repair": 0.50,
    "Flat Rate": 1.0,
    "Manufacture Warranty": 1.0,
}
STRATUS_POINTS = 0.75


def menu():
    print("1. Add unit(s)")
    print("2. Remove unit")
    print("3. View output total")
    print("4. View weighted output")
    print("6. View breakdown")
    print("7. Initialize/Update breakdown")
    print("5. Exit")
    print(SEPARATOR)


def add_unit(state):
    units = input("Enter unit type: (stratus(s) / 525(5) / 1025(10)): ").strip().lower()
    while units not in {"s", "stratus", "5", "525", "10", "1025"}:
        print("Invalid unit. Enter 's'/'stratus' or '5'/'525' or '10'/'1025'.")
        print(SEPARATOR)
        units = input("Enter unit type: (stratus(s) / 525(5) / 1025(10)): ").strip().lower()
    if units in {"s", "stratus"}:
        units = "s"
    elif units in {"5", "525"}:
        units = "5"
    else:
        units = "10"

    qty = get_positive_int("Enter quantity to add: ")

    if units == "s":
        print("Enter quantities to add for Stratus types (0 allowed):")
        print(SEPARATOR)
        s_flat = get_nonnegative_int("Stratus Flat Rate: ")
        s_manuf = get_nonnegative_int("Stratus Manufacture Warranty: ")
        qty = s_flat + s_manuf
        if qty == 0:
            print("No units selected for addition.")
            print(SEPARATOR)
            return
        state["output"] += qty
        state["weighted_output"] += STRATUS_POINTS * qty
        state["count_stratus_flat"] = state.get("count_stratus_flat", 0) + s_flat
        state["count_stratus_manuf"] = state.get("count_stratus_manuf", 0) + s_manuf
        state["count_stratus"] = state.get("count_stratus", 0) + qty
    elif units == "5":
        print("Enter quantities to add for each 525 warranty type (0 allowed):")
        print(SEPARATOR)
        q_cnt = get_nonnegative_int("QM Warranty: ")
        p_cnt = get_nonnegative_int("PM: ")
        m_cnt = get_nonnegative_int("Minor Repair: ")
        f_cnt = get_nonnegative_int("Flat Rate: ")
        w_cnt = get_nonnegative_int("Manufacture Warranty: ")
        total_add = q_cnt + p_cnt + m_cnt + f_cnt + w_cnt
        if total_add == 0:
            print("No units selected for addition.")
            print(SEPARATOR)
            return
        state["output"] += total_add
        state["weighted_output"] += (
            DEV_POINTS["QM Warranty"] * q_cnt
            + DEV_POINTS["PM"] * p_cnt
            + DEV_POINTS["Minor Repair"] * m_cnt
            + DEV_POINTS["Flat Rate"] * f_cnt
            + DEV_POINTS["Manufacture Warranty"] * w_cnt
        )
        state["count_qm"] = state.get("count_qm", 0) + q_cnt
        state["count_pm"] = state.get("count_pm", 0) + p_cnt
        state["count_minor"] = state.get("count_minor", 0) + m_cnt
        state["count_flat"] = state.get("count_flat", 0) + f_cnt
        state["count_manuf"] = state.get("count_manuf", 0) + w_cnt
    else:  # 1025
        print("Enter quantities to add for each 1025 warranty type (0 allowed):")
        print(SEPARATOR)
        q_cnt = get_nonnegative_int("QM Warranty: ")
        p_cnt = get_nonnegative_int("PM: ")
        m_cnt = get_nonnegative_int("Minor Repair: ")
        f_cnt = get_nonnegative_int("Flat Rate: ")
        w_cnt = get_nonnegative_int("Manufacture Warranty: ")
        total_add = q_cnt + p_cnt + m_cnt + f_cnt + w_cnt
        if total_add == 0:
            print("No units selected for addition.")
            print(SEPARATOR)
            return
        state["output"] += total_add
        state["weighted_output"] += (
            DEV_POINTS["QM Warranty"] * q_cnt
            + DEV_POINTS["PM"] * p_cnt
            + DEV_POINTS["Minor Repair"] * m_cnt
            + DEV_POINTS["Flat Rate"] * f_cnt
            + DEV_POINTS["Manufacture Warranty"] * w_cnt
        )
        state["count_1025_qm"] = state.get("count_1025_qm", 0) + q_cnt
        state["count_1025_pm"] = state.get("count_1025_pm", 0) + p_cnt
        state["count_1025_minor"] = state.get("count_1025_minor", 0) + m_cnt
        state["count_1025_flat"] = state.get("count_1025_flat", 0) + f_cnt
        state["count_1025_manuf"] = state.get("count_1025_manuf", 0) + w_cnt
    save_progress(state)


def remove_unit(state):
    if state["output"] == 0:
        print("No units to remove.")
        print(SEPARATOR)
        return

    unit = input("Enter unit type to remove: (stratus(s) / 525(5) / 1025(10)): ").strip().lower()
    while unit not in {"s", "stratus", "5", "525", "10", "1025"}:
        print("Invalid unit. Enter 's'/'stratus' or '5'/'525' or '10'/'1025'.")
        print(SEPARATOR)
        unit = input("Enter unit type to remove: (stratus(s) / 525(5) / 1025(10)): ").strip().lower()
    if unit in {"s", "stratus"}:
        unit = "s"
    elif unit in {"5", "525"}:
        unit = "5"
    else:
        unit = "10"

    if unit == "s":
        print("Enter quantities to remove for Stratus types (0 allowed):")
        print(SEPARATOR)
        s_flat = get_nonnegative_int("Stratus Flat Rate: ")
        s_manuf = get_nonnegative_int("Stratus Manufacture Warranty: ")
        qty = s_flat + s_manuf
        if qty == 0:
            print("No units selected for removal.")
            print(SEPARATOR)
            return
        if qty > state.get("output", 0):
            print("Cannot remove more than total output.")
            print(SEPARATOR)
            return
        if s_flat > state.get("count_stratus_flat", 0):
            print("Cannot remove more Stratus Flat Rate than recorded.")
            print(SEPARATOR)
            return
        if s_manuf > state.get("count_stratus_manuf", 0):
            print("Cannot remove more Stratus Manufacture Warranty than recorded.")
            print(SEPARATOR)
            return
        state["output"] -= qty
        state["weighted_output"] -= STRATUS_POINTS * qty
        state["count_stratus_flat"] -= s_flat
        state["count_stratus_manuf"] -= s_manuf
        state["count_stratus"] -= qty
        if state["output"] == 0:
            state["weighted_output"] = 0.0
    elif unit == "5":
        print("Enter quantities to remove for each 525 warranty type (0 allowed):")
        print(SEPARATOR)
        q_cnt = get_nonnegative_int("QM Warranty: ")
        p_cnt = get_nonnegative_int("PM: ")
        m_cnt = get_nonnegative_int("Minor Repair: ")
        f_cnt = get_nonnegative_int("Flat Rate: ")
        w_cnt = get_nonnegative_int("Manufacture Warranty: ")
        total_remove = q_cnt + p_cnt + m_cnt + f_cnt + w_cnt
        if total_remove == 0:
            print("No units selected for removal.")
            print(SEPARATOR)
            return
        if total_remove > state["output"]:
            print("Cannot remove more than total output.")
            print(SEPARATOR)
            return
        if q_cnt > state.get("count_qm", 0):
            print("Cannot remove more QM Warranty than recorded.")
            print(SEPARATOR)
            return
        if p_cnt > state.get("count_pm", 0):
            print("Cannot remove more PM than recorded.")
            print(SEPARATOR)
            return
        if m_cnt > state.get("count_minor", 0):
            print("Cannot remove more Minor Repair than recorded.")
            print(SEPARATOR)
            return
        if f_cnt > state.get("count_flat", 0):
            print("Cannot remove more Flat Rate than recorded.")
            print(SEPARATOR)
            return
        if w_cnt > state.get("count_manuf", 0):
            print("Cannot remove more Manufacture Warranty than recorded.")
            print(SEPARATOR)
            return
        state["output"] -= total_remove
        state["weighted_output"] -= (
            DEV_POINTS["QM Warranty"] * q_cnt
            + DEV_POINTS["PM"] * p_cnt
            + DEV_POINTS["Minor Repair"] * m_cnt
            + DEV_POINTS["Flat Rate"] * f_cnt
            + DEV_POINTS["Manufacture Warranty"] * w_cnt
        )
        state["count_qm"] -= q_cnt
        state["count_pm"] -= p_cnt
        state["count_minor"] -= m_cnt
        state["count_flat"] -= f_cnt
        state["count_manuf"] -= w_cnt
        if state["output"] == 0:
            state["weighted_output"] = 0.0
    else:  # 1025
        print("Enter quantities to remove for each 1025 warranty type (0 allowed):")
        print(SEPARATOR)
        q_cnt = get_nonnegative_int("QM Warranty (q): ")
        p_cnt = get_nonnegative_int("PM (p): ")
        m_cnt = get_nonnegative_int("Minor Repair (m): ")
        f_cnt = get_nonnegative_int("Flat Rate (f): ")
        w_cnt = get_nonnegative_int("Manufacture Warranty (w): ")
        total_remove = q_cnt + p_cnt + m_cnt + f_cnt + w_cnt
        if total_remove == 0:
            print("No units selected for removal.")
            print(SEPARATOR)
            return
        if total_remove > state["output"]:
            print("Cannot remove more than total output.")
            print(SEPARATOR)
            return
        if q_cnt > state.get("count_1025_qm", 0):
            print("Cannot remove more QM Warranty than recorded for 1025.")
            print(SEPARATOR)
            return
        if p_cnt > state.get("count_1025_pm", 0):
            print("Cannot remove more PM than recorded for 1025.")
            print(SEPARATOR)
            return
        if m_cnt > state.get("count_1025_minor", 0):
            print("Cannot remove more Minor Repair than recorded for 1025.")
            print(SEPARATOR)
            return
        if f_cnt > state.get("count_1025_flat", 0):
            print("Cannot remove more Flat Rate than recorded for 1025.")
            print(SEPARATOR)
            return
        if w_cnt > state.get("count_1025_manuf", 0):
            print("Cannot remove more Manufacture Warranty than recorded for 1025.")
            print(SEPARATOR)
            return
        state["output"] -= total_remove
        state["weighted_output"] -= (
            DEV_POINTS["QM Warranty"] * q_cnt
            + DEV_POINTS["PM"] * p_cnt
            + DEV_POINTS["Minor Repair"] * m_cnt
            + DEV_POINTS["Flat Rate"] * f_cnt
            + DEV_POINTS["Manufacture Warranty"] * w_cnt
        )
        state["count_1025_qm"] -= q_cnt
        state["count_1025_pm"] -= p_cnt
        state["count_1025_minor"] -= m_cnt
        state["count_1025_flat"] -= f_cnt
        state["count_1025_manuf"] -= w_cnt
        if state["output"] == 0:
            state["weighted_output"] = 0.0
    save_progress(state)


def view_output_total(state):
    print(f"Total Output: {state['output']}")
    print(SEPARATOR)


def view_weighted_output(state):
    print(f"Weighted Output: {state['weighted_output']}")
    print(SEPARATOR)


def view_breakdown(state):
    print("Breakdown of Units:")
    print(f"- Stratus: {state.get('count_stratus', 0)}")
    print(f"  - Stratus Flat Rate: {state.get('count_stratus_flat', 0)}")
    print(f"  - Stratus Manufacture Warranty: {state.get('count_stratus_manuf', 0)}")
    print(f"- 525 QM Warranty: {state.get('count_qm', 0)}")
    print(f"- 525 PM: {state.get('count_pm', 0)}")
    print(f"- 525 Minor Repair: {state.get('count_minor', 0)}")
    print(f"- 525 Flat Rate: {state.get('count_flat', 0)}")
    print(f"- 525 Manufacture Warranty: {state.get('count_manuf', 0)}")
    print(f"- 1025 QM Warranty: {state.get('count_1025_qm', 0)}")
    print(f"- 1025 PM: {state.get('count_1025_pm', 0)}")
    print(f"- 1025 Minor Repair: {state.get('count_1025_minor', 0)}")
    print(f"- 1025 Flat Rate: {state.get('count_1025_flat', 0)}")
    print(f"- 1025 Manufacture Warranty: {state.get('count_1025_manuf', 0)}")
    print(SEPARATOR)


def load_progress():
    if file_path.exists():
        try:
            with file_path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    return {
                        "output": int(row.get("output", 0)),
                        "weighted_output": float(row.get("weighted_output", 0.0)),
                        "count_stratus": int(row.get("count_stratus", 0)),
                        "count_qm": int(row.get("count_qm", 0)),
                        "count_pm": int(row.get("count_pm", 0)),
                        "count_minor": int(row.get("count_minor", 0)),
                        "count_flat": int(row.get("count_flat", 0)),
                        "count_manuf": int(row.get("count_manuf", 0)),
                        "count_1025_qm": int(row.get("count_1025_qm", 0)),
                        "count_1025_pm": int(row.get("count_1025_pm", 0)),
                        "count_1025_minor": int(row.get("count_1025_minor", 0)),
                        "count_1025_flat": int(row.get("count_1025_flat", 0)),
                        "count_1025_manuf": int(row.get("count_1025_manuf", 0)),
                        "count_stratus_flat": int(row.get("count_stratus_flat", 0)),
                        "count_stratus_manuf": int(row.get("count_stratus_manuf", 0)),
                        "start_date": row.get("start_date", ""),
                        "start_of_day_output": int(row.get("start_of_day_output", 0)),
                    }
        except Exception:
            pass
    return {
        "output": 0,
        "weighted_output": 0.0,
        "count_stratus": 0,
        "count_qm": 0,
        "count_pm": 0,
        "count_minor": 0,
        "count_flat": 0,
        "count_manuf": 0,
        "count_1025_qm": 0,
        "count_1025_pm": 0,
        "count_1025_minor": 0,
        "count_1025_flat": 0,
        "count_1025_manuf": 0,
        "count_stratus_flat": 0,
        "count_stratus_manuf": 0,
        "start_date": "",
        "start_of_day_output": 0,
    }


def save_progress(state):
    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "output",
                "weighted_output",
                "count_stratus",
                "count_qm",
                "count_pm",
                "count_minor",
                "count_flat",
                "count_manuf",
                "count_1025_qm",
                "count_1025_pm",
                "count_1025_minor",
                "count_1025_flat",
                "count_1025_manuf",
                "count_stratus_flat",
                "count_stratus_manuf",
                "start_date",
                "start_of_day_output",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "output": state["output"],
                "weighted_output": state["weighted_output"],
                "count_stratus": state.get("count_stratus", 0),
                "count_qm": state.get("count_qm", 0),
                "count_pm": state.get("count_pm", 0),
                "count_minor": state.get("count_minor", 0),
                "count_flat": state.get("count_flat", 0),
                "count_manuf": state.get("count_manuf", 0),
                "count_1025_qm": state.get("count_1025_qm", 0),
                "count_1025_pm": state.get("count_1025_pm", 0),
                "count_1025_minor": state.get("count_1025_minor", 0),
                "count_1025_flat": state.get("count_1025_flat", 0),
                "count_1025_manuf": state.get("count_1025_manuf", 0),
                "count_stratus_flat": state.get("count_stratus_flat", 0),
                "count_stratus_manuf": state.get("count_stratus_manuf", 0),
                "start_date": state.get("start_date", ""),
                "start_of_day_output": state.get("start_of_day_output", 0),
            }
        )


# ----- integer input helpers -----
def get_positive_int(prompt: str) -> int:
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print("Please enter a positive integer.")
        print(SEPARATOR)


def get_nonnegative_int(prompt: str) -> int:
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            return int(val)
        print("Please enter a non-negative integer (0 or more).")
        print(SEPARATOR)


def ensure_start_of_day(state):
    today = date.today().isoformat()
    current_start_date = state.get("start_date") or ""
    if current_start_date != today:
        state["start_date"] = today
        state["start_of_day_output"] = int(state.get("output", 0))
        save_progress(state)


def main():
    state = load_progress()
    # Ensure daily start-of-day state is set/rolled over
    ensure_start_of_day(state)
    while True:
        menu()
        choice = input("Select an option: ").strip()
        while choice not in {"1", "2", "3", "4", "5", "6", "7"}:
            print("Please enter 1, 2, 3, 4, 5, 6, or 7.")
            print(SEPARATOR)
            choice = input("Select an option: ").strip()
        if choice == "1":
            add_unit(state)
        elif choice == "2":
            remove_unit(state)
        elif choice == "3":
            view_output_total(state)
        elif choice == "4":
            view_weighted_output(state)
        elif choice == "6":
            view_breakdown(state)
        elif choice == "7":
            initialize_breakdown(state)
        elif choice == "5":
            save_progress(state)
            print("Progress saved.")
            print(SEPARATOR)
            break
        else:
            print("Invalid choice. Please try again.")
            print(SEPARATOR)


def initialize_breakdown(state):
    total = state.get("output", 0)
    print(f"Current total output: {total}")
    if total < 0:
        print("Total output is negative; cannot initialize.")
        print(SEPARATOR)
        return
    print("Enter counts for each category so they sum to the total.")
    print(SEPARATOR)
    s = get_nonnegative_int("Stratus: ")
    s_flat = get_nonnegative_int("Stratus Flat Rate: ")
    s_manuf = get_nonnegative_int("Stratus Manufacture Warranty: ")
    s = s_flat + s_manuf
    q = get_nonnegative_int("525 QM Warranty: ")
    p = get_nonnegative_int("525 PM: ")
    m = get_nonnegative_int("525 Minor Repair: ")
    f = get_nonnegative_int("525 Flat Rate: ")
    w = get_nonnegative_int("525 Manufacture Warranty: ")
    q10 = get_nonnegative_int("1025 QM Warranty: ")
    p10 = get_nonnegative_int("1025 PM: ")
    m10 = get_nonnegative_int("1025 Minor Repair: ")
    f10 = get_nonnegative_int("1025 Flat Rate: ")
    w10 = get_nonnegative_int("1025 Manufacture Warranty: ")
    ssum = s + q + p + m + f + w + q10 + p10 + m10 + f10 + w10
    if ssum != total:
        print(f"Sum of entries ({ssum}) must equal total output ({total}). No changes saved.")
        print(SEPARATOR)
        return
    state["count_stratus"] = s
    state["count_stratus_flat"] = s_flat
    state["count_stratus_manuf"] = s_manuf
    state["count_qm"] = q
    state["count_pm"] = p
    state["count_minor"] = m
    state["count_flat"] = f
    state["count_manuf"] = w
    state["count_1025_qm"] = q10
    state["count_1025_pm"] = p10
    state["count_1025_minor"] = m10
    state["count_1025_flat"] = f10
    state["count_1025_manuf"] = w10
    state["weighted_output"] = (
        STRATUS_POINTS * s
        + DEV_POINTS["QM Warranty"] * q
        + DEV_POINTS["PM"] * p
        + DEV_POINTS["Minor Repair"] * m
        + DEV_POINTS["Flat Rate"] * f
        + DEV_POINTS["Manufacture Warranty"] * w
        + DEV_POINTS["QM Warranty"] * q10
        + DEV_POINTS["PM"] * p10
        + DEV_POINTS["Minor Repair"] * m10
        + DEV_POINTS["Flat Rate"] * f10
        + DEV_POINTS["Manufacture Warranty"] * w10
    )
    save_progress(state)
    print("Breakdown initialized and weighted output updated.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()

