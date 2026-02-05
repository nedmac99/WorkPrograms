import sys
import csv
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

FILE_PATH = BASE_DIR / "output_progress.csv"


DEV_POINTS = {
    "QM Warranty": 0.75,
    "PM": 0.25,
    "Minor Repair": 0.50,
    "Flat Rate": 1.0,
    "Manufacture Warranty": 1.0,
}

STRATUS_POINTS = 0.75
HOMEFILL_POINTS = 2.0

# Per-unit points for newly added unit types
UNIT_POINTS = {
    "Perfecto 2V": {
        "QM Warranty": 1.0,
        "Flat Rate": 1.25,
        "Manufacture Warranty": 1.25,
    },
    "M10": {
        "QM Warranty": 1.25,
        "Flat Rate": 1.75,
        "Manufacture Warranty": 1.75,
    },
    "Rhythm LM5A": {
        "QM Warranty": 0.75,
        "Flat Rate": 1.0,
        "Manufacture Warranty": 1.0,
    },
    "Rhythm LM5BA": {
        "QM Warranty": 0.75,
        "Flat Rate": 1.0,
        "Manufacture Warranty": 1.0,
    },
    "Rhythm LM5CA": {
        "QM Warranty": 0.75,
        "Flat Rate": 1.0,
        "Manufacture Warranty": 1.0,
    },
    "POC": {
        "Repair": 2.0,
    },
}


def load_progress():
    if FILE_PATH.exists():
        try:
            with FILE_PATH.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    state = {
                        "output": int(row.get("output", 0)),
                        "weighted_output": float(row.get("weighted_output", 0.0)),
                        "count_stratus": int(row.get("count_stratus", 0)),
                        "count_stratus_flat": int(row.get("count_stratus_flat", 0)),
                        "count_stratus_manuf": int(row.get("count_stratus_manuf", 0)),
                        "count_homefill": int(row.get("count_homefill", 0)),
                        "count_homefill_flat": int(row.get("count_homefill_flat", 0)),
                        "count_homefill_manuf": int(row.get("count_homefill_manuf", 0)),
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
                        # New unit type counters
                        "count_perfecto_qm": int(row.get("count_perfecto_qm", 0)),
                        "count_perfecto_flat": int(row.get("count_perfecto_flat", 0)),
                        "count_perfecto_manuf": int(row.get("count_perfecto_manuf", 0)),
                        "count_m10_qm": int(row.get("count_m10_qm", 0)),
                        "count_m10_flat": int(row.get("count_m10_flat", 0)),
                        "count_m10_manuf": int(row.get("count_m10_manuf", 0)),
                        "count_lm5a_qm": int(row.get("count_lm5a_qm", 0)),
                        "count_lm5a_flat": int(row.get("count_lm5a_flat", 0)),
                        "count_lm5a_manuf": int(row.get("count_lm5a_manuf", 0)),
                        "count_lm5ba_qm": int(row.get("count_lm5ba_qm", 0)),
                        "count_lm5ba_flat": int(row.get("count_lm5ba_flat", 0)),
                        "count_lm5ba_manuf": int(row.get("count_lm5ba_manuf", 0)),
                        "count_lm5ca_qm": int(row.get("count_lm5ca_qm", 0)),
                        "count_lm5ca_flat": int(row.get("count_lm5ca_flat", 0)),
                        "count_lm5ca_manuf": int(row.get("count_lm5ca_manuf", 0)),
                        "count_poc_repair": int(row.get("count_poc_repair", 0)),
                        "start_date": row.get("start_date") or "",
                        "start_of_day_output": int(row.get("start_of_day_output", 0)),
                    }
                    # migrate/sync Stratus totals vs subcategories
                    sub = state.get("count_stratus_flat", 0) + state.get("count_stratus_manuf", 0)
                    if sub > 0:
                        state["count_stratus"] = sub
                    elif state.get("count_stratus", 0) > 0 and sub == 0:
                        state["count_stratus_flat"] = state.get("count_stratus", 0)
                        state["count_stratus_manuf"] = 0
                    # ensure start-of-day values
                    today = date.today().isoformat()
                    if state.get("start_date") != today:
                        state["start_date"] = today
                        state["start_of_day_output"] = state.get("output", 0)
                        # write back immediately so other processes see it
                        save_progress(state)
                    return state
        except Exception:
            pass
    return {
        "output": 0,
        "weighted_output": 0.0,
        "count_stratus": 0,
        "count_stratus_flat": 0,
        "count_stratus_manuf": 0,
        "count_homefill": 0,
        "count_homefill_flat": 0,
        "count_homefill_manuf": 0,
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
        # New unit type counters (defaults)
        "count_perfecto_qm": 0,
        "count_perfecto_flat": 0,
        "count_perfecto_manuf": 0,
        "count_m10_qm": 0,
        "count_m10_flat": 0,
        "count_m10_manuf": 0,
        "count_lm5a_qm": 0,
        "count_lm5a_flat": 0,
        "count_lm5a_manuf": 0,
        "count_lm5ba_qm": 0,
        "count_lm5ba_flat": 0,
        "count_lm5ba_manuf": 0,
        "count_lm5ca_qm": 0,
        "count_lm5ca_flat": 0,
        "count_lm5ca_manuf": 0,
        "count_poc_repair": 0,
        "start_date": date.today().isoformat(),
        "start_of_day_output": 0,
    }


def save_progress(state):
    with FILE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "output",
                "weighted_output",
                "count_stratus",
                "count_stratus_flat",
                "count_stratus_manuf",
                "count_homefill",
                "count_homefill_flat",
                "count_homefill_manuf",
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
                # New unit types
                "count_perfecto_qm",
                "count_perfecto_flat",
                "count_perfecto_manuf",
                "count_m10_qm",
                "count_m10_flat",
                "count_m10_manuf",
                "count_lm5a_qm",
                "count_lm5a_flat",
                "count_lm5a_manuf",
                "count_lm5ba_qm",
                "count_lm5ba_flat",
                "count_lm5ba_manuf",
                "count_lm5ca_qm",
                "count_lm5ca_flat",
                "count_lm5ca_manuf",
                "count_poc_repair",
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
                "count_stratus_flat": state.get("count_stratus_flat", 0),
                "count_stratus_manuf": state.get("count_stratus_manuf", 0),
                "count_homefill": state.get("count_homefill", 0),
                "count_homefill_flat": state.get("count_homefill_flat", 0),
                "count_homefill_manuf": state.get("count_homefill_manuf", 0),
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
                # New unit types
                "count_perfecto_qm": state.get("count_perfecto_qm", 0),
                "count_perfecto_flat": state.get("count_perfecto_flat", 0),
                "count_perfecto_manuf": state.get("count_perfecto_manuf", 0),
                "count_m10_qm": state.get("count_m10_qm", 0),
                "count_m10_flat": state.get("count_m10_flat", 0),
                "count_m10_manuf": state.get("count_m10_manuf", 0),
                "count_lm5a_qm": state.get("count_lm5a_qm", 0),
                "count_lm5a_flat": state.get("count_lm5a_flat", 0),
                "count_lm5a_manuf": state.get("count_lm5a_manuf", 0),
                "count_lm5ba_qm": state.get("count_lm5ba_qm", 0),
                "count_lm5ba_flat": state.get("count_lm5ba_flat", 0),
                "count_lm5ba_manuf": state.get("count_lm5ba_manuf", 0),
                "count_lm5ca_qm": state.get("count_lm5ca_qm", 0),
                "count_lm5ca_flat": state.get("count_lm5ca_flat", 0),
                "count_lm5ca_manuf": state.get("count_lm5ca_manuf", 0),
                "count_poc_repair": state.get("count_poc_repair", 0),
                "start_date": state.get("start_date", date.today().isoformat()),
                "start_of_day_output": state.get("start_of_day_output", 0),
            }
        )


class WeightedOutputApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weighted Output Tracker")
        # Bold font for totals in breakdown
        try:
            self.bold_font = tkfont.nametofont("TkDefaultFont").copy()
            self.bold_font.configure(weight="bold")
        except Exception:
            self.bold_font = (None, 10, "bold")
        self.state = load_progress()
        # ensure keys exist for older CSVs
        for k in ("count_stratus","count_homefill","count_homefill_flat","count_homefill_manuf",
            "count_qm","count_pm","count_minor","count_flat","count_manuf",
            "count_1025_qm","count_1025_pm","count_1025_minor","count_1025_flat","count_1025_manuf",
            # new unit types
            "count_perfecto_qm","count_perfecto_flat","count_perfecto_manuf",
            "count_m10_qm","count_m10_flat","count_m10_manuf",
            "count_lm5a_qm","count_lm5a_flat","count_lm5a_manuf",
            "count_lm5ba_qm","count_lm5ba_flat","count_lm5ba_manuf",
            "count_lm5ca_qm","count_lm5ca_flat","count_lm5ca_manuf",
            "count_poc_repair"):
            self.state.setdefault(k, 0)
        # ensure start-of-day on startup
        self._ensure_start_of_day()

        self._build_ui()
        self._refresh_totals()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Totals row
        totals = ttk.Frame(container)
        totals.grid(row=0, column=0, sticky="ew")
        totals.columnconfigure(1, weight=1)
        totals.columnconfigure(3, weight=1)
        totals.columnconfigure(6, weight=1)
        totals.columnconfigure(9, weight=1)

        ttk.Label(totals, text="Total Output:").grid(row=0, column=0, sticky="w")
        self.output_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.output_var).grid(row=0, column=1, sticky="w")

        # Started today with (editable) next to Total Output
        ttk.Label(totals, text="Started today with:").grid(row=0, column=2, sticky="e", padx=(24, 0))
        self.start_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.start_var).grid(row=0, column=3, sticky="w")
        ttk.Button(totals, text="Edit", command=self._edit_start_of_day).grid(row=0, column=4, sticky="w", padx=(6,0))

        # Today's Output further right
        ttk.Label(totals, text="Today's Output:").grid(row=0, column=5, sticky="e", padx=(24, 0))
        self.today_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.today_var).grid(row=0, column=6, sticky="w")
        ttk.Button(totals, text="Edit", command=self._edit_today_output).grid(row=0, column=7, sticky="w", padx=(6,0))

        ttk.Label(totals, text="Weighted Output:").grid(row=0, column=8, sticky="e", padx=(24, 0))
        self.weighted_var = tk.StringVar()
        ttk.Label(totals, textvariable=self.weighted_var).grid(row=0, column=9, sticky="w")

        ttk.Separator(container, orient="horizontal").grid(row=1, column=0, sticky="ew", pady=8)

        notebook = ttk.Notebook(container)
        notebook.grid(row=2, column=0, sticky="nsew")
        container.rowconfigure(2, weight=1)

        add_tab = ttk.Frame(notebook, padding=12)
        rem_tab = ttk.Frame(notebook, padding=12)
        brk_tab = ttk.Frame(notebook, padding=12)
        notebook.add(add_tab, text="Add")
        notebook.add(rem_tab, text="Remove")
        notebook.add(brk_tab, text="Breakdown")

        # Add Tab
        self._build_add_tab(add_tab)
        # Remove Tab
        self._build_remove_tab(rem_tab)
        # Breakdown Tab
        self._build_breakdown_tab(brk_tab)
        ttk.Button(brk_tab, text="Edit breakdown", command=self._open_edit_breakdown).grid(row=1, column=0, pady=(12,0), sticky="w")

    def _build_add_tab(self, parent):
        # Stratus add (subcategories)
        str_frame = ttk.LabelFrame(parent, text="Stratus (enter per-type quantities)", padding=8)
        str_frame.grid(row=0, column=0, sticky="ew")
        self.add_s_flat = tk.StringVar(value="0")
        self.add_s_manuf = tk.StringVar(value="0")
        self._row_inputs(str_frame, 0, [
            ("Stratus Flat Rate", self.add_s_flat),
            ("Stratus Manufacture Warranty", self.add_s_manuf),
        ])
        ttk.Button(str_frame, text="Add", command=self._add_stratus).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Homefill add (subcategories)
        hf_frame = ttk.LabelFrame(parent, text="Homefill (enter per-type quantities)", padding=8)
        hf_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.add_h_flat = tk.StringVar(value="0")
        self.add_h_manuf = tk.StringVar(value="0")
        self._row_inputs(hf_frame, 0, [
            ("Homefill Flat Rate", self.add_h_flat),
            ("Homefill Manufacture Warranty", self.add_h_manuf),
        ])
        ttk.Button(hf_frame, text="Add", command=self._add_homefill).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 525 add
        dev = ttk.LabelFrame(parent, text="525 (enter per-warranty quantities)", padding=8)
        dev.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        self.add_q = tk.StringVar(value="0")
        self.add_p = tk.StringVar(value="0")
        self.add_m = tk.StringVar(value="0")
        self.add_f = tk.StringVar(value="0")
        self.add_w = tk.StringVar(value="0")

        self._row_inputs(dev, 0, [
            ("QM Warranty", self.add_q),
            ("PM", self.add_p),
            ("Minor Repair", self.add_m),
            ("Flat Rate", self.add_f),
            ("Manufacture Warranty", self.add_w),
        ])

        ttk.Button(dev, text="Add", command=self._add_525).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 1025 add
        dev10 = ttk.LabelFrame(parent, text="1025 (enter per-warranty quantities)", padding=8)
        dev10.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        self.add10_q = tk.StringVar(value="0")
        self.add10_p = tk.StringVar(value="0")
        self.add10_m = tk.StringVar(value="0")
        self.add10_f = tk.StringVar(value="0")
        self.add10_w = tk.StringVar(value="0")

        self._row_inputs(dev10, 0, [
            ("QM Warranty", self.add10_q),
            ("PM", self.add10_p),
            ("Minor Repair", self.add10_m),
            ("Flat Rate", self.add10_f),
            ("Manufacture Warranty", self.add10_w),
        ])

        ttk.Button(dev10, text="Add", command=self._add_1025).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Perfecto 2V add
        perfecto = ttk.LabelFrame(parent, text="Perfecto 2V (enter per-warranty quantities)", padding=8)
        perfecto.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        self.add_perfecto_qm = tk.StringVar(value="0")
        self.add_perfecto_flat = tk.StringVar(value="0")
        self.add_perfecto_manuf = tk.StringVar(value="0")
        self._row_inputs(perfecto, 0, [
            ("QM Warranty", self.add_perfecto_qm),
            ("Flat Rate", self.add_perfecto_flat),
            ("Manufacture Warranty", self.add_perfecto_manuf),
        ])
        ttk.Button(perfecto, text="Add", command=self._add_perfecto).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # M10 add
        m10 = ttk.LabelFrame(parent, text="M10 (enter per-warranty quantities)", padding=8)
        m10.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.add_m10_qm = tk.StringVar(value="0")
        self.add_m10_flat = tk.StringVar(value="0")
        self.add_m10_manuf = tk.StringVar(value="0")
        self._row_inputs(m10, 0, [
            ("QM Warranty", self.add_m10_qm),
            ("Flat Rate", self.add_m10_flat),
            ("Manufacture Warranty", self.add_m10_manuf),
        ])
        ttk.Button(m10, text="Add", command=self._add_m10).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Rhythm LM5A add
        lm5a = ttk.LabelFrame(parent, text="Rhythm LM5A (enter per-warranty quantities)", padding=8)
        lm5a.grid(row=6, column=0, sticky="ew", pady=(10, 0))
        self.add_lm5a_qm = tk.StringVar(value="0")
        self.add_lm5a_flat = tk.StringVar(value="0")
        self.add_lm5a_manuf = tk.StringVar(value="0")
        self._row_inputs(lm5a, 0, [
            ("QM Warranty", self.add_lm5a_qm),
            ("Flat Rate", self.add_lm5a_flat),
            ("Manufacture Warranty", self.add_lm5a_manuf),
        ])
        ttk.Button(lm5a, text="Add", command=self._add_lm5a).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Rhythm LM5BA add
        lm5ba = ttk.LabelFrame(parent, text="Rhythm LM5BA (enter per-warranty quantities)", padding=8)
        lm5ba.grid(row=7, column=0, sticky="ew", pady=(10, 0))
        self.add_lm5ba_qm = tk.StringVar(value="0")
        self.add_lm5ba_flat = tk.StringVar(value="0")
        self.add_lm5ba_manuf = tk.StringVar(value="0")
        self._row_inputs(lm5ba, 0, [
            ("QM Warranty", self.add_lm5ba_qm),
            ("Flat Rate", self.add_lm5ba_flat),
            ("Manufacture Warranty", self.add_lm5ba_manuf),
        ])
        ttk.Button(lm5ba, text="Add", command=self._add_lm5ba).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Rhythm LM5CA add
        lm5ca = ttk.LabelFrame(parent, text="Rhythm LM5CA (enter per-warranty quantities)", padding=8)
        lm5ca.grid(row=8, column=0, sticky="ew", pady=(10, 0))
        self.add_lm5ca_qm = tk.StringVar(value="0")
        self.add_lm5ca_flat = tk.StringVar(value="0")
        self.add_lm5ca_manuf = tk.StringVar(value="0")
        self._row_inputs(lm5ca, 0, [
            ("QM Warranty", self.add_lm5ca_qm),
            ("Flat Rate", self.add_lm5ca_flat),
            ("Manufacture Warranty", self.add_lm5ca_manuf),
        ])
        ttk.Button(lm5ca, text="Add", command=self._add_lm5ca).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # POC add
        poc = ttk.LabelFrame(parent, text="POC (enter quantity)", padding=8)
        poc.grid(row=9, column=0, sticky="ew", pady=(10, 0))
        self.add_poc_repair = tk.StringVar(value="0")
        self._row_inputs(poc, 0, [
            ("Repair", self.add_poc_repair),
        ])
        ttk.Button(poc, text="Add", command=self._add_poc).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Flow these sections into columns when nearing bottom
        self.add_sections = [
            str_frame, hf_frame, dev, dev10, perfecto, m10, lm5a, lm5ba, lm5ca, poc
        ]
        parent.bind("<Configure>", lambda e: self._flow_layout(parent, self.add_sections, columns=2))
        self._flow_layout(parent, self.add_sections, columns=2)

    def _build_remove_tab(self, parent):
        # Stratus remove (subcategories)
        str_frame = ttk.LabelFrame(parent, text="Stratus (enter per-type quantities)", padding=8)
        str_frame.grid(row=0, column=0, sticky="ew")
        self.rem_s_flat = tk.StringVar(value="0")
        self.rem_s_manuf = tk.StringVar(value="0")
        self._row_inputs(str_frame, 0, [
            ("Stratus Flat Rate", self.rem_s_flat),
            ("Stratus Manufacture Warranty", self.rem_s_manuf),
        ])
        ttk.Button(str_frame, text="Remove", command=self._remove_stratus).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Homefill remove (subcategories)
        hf_frame = ttk.LabelFrame(parent, text="Homefill (enter per-type quantities)", padding=8)
        hf_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.rem_h_flat = tk.StringVar(value="0")
        self.rem_h_manuf = tk.StringVar(value="0")
        self._row_inputs(hf_frame, 0, [
            ("Homefill Flat Rate", self.rem_h_flat),
            ("Homefill Manufacture Warranty", self.rem_h_manuf),
        ])
        ttk.Button(hf_frame, text="Remove", command=self._remove_homefill).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 525 remove
        dev = ttk.LabelFrame(parent, text="525 (enter per-warranty quantities)", padding=8)
        dev.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        self.rem_q = tk.StringVar(value="0")
        self.rem_p = tk.StringVar(value="0")
        self.rem_m = tk.StringVar(value="0")
        self.rem_f = tk.StringVar(value="0")
        self.rem_w = tk.StringVar(value="0")

        self._row_inputs(dev, 0, [
            ("QM Warranty", self.rem_q),
            ("PM", self.rem_p),
            ("Minor Repair", self.rem_m),
            ("Flat Rate", self.rem_f),
            ("Manufacture Warranty", self.rem_w),
        ])

        ttk.Button(dev, text="Remove", command=self._remove_525).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # 1025 remove
        dev10 = ttk.LabelFrame(parent, text="1025 (enter per-warranty quantities)", padding=8)
        dev10.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        self.rem10_q = tk.StringVar(value="0")
        self.rem10_p = tk.StringVar(value="0")
        self.rem10_m = tk.StringVar(value="0")
        self.rem10_f = tk.StringVar(value="0")
        self.rem10_w = tk.StringVar(value="0")

        self._row_inputs(dev10, 0, [
            ("QM Warranty", self.rem10_q),
            ("PM", self.rem10_p),
            ("Minor Repair", self.rem10_m),
            ("Flat Rate", self.rem10_f),
            ("Manufacture Warranty", self.rem10_w),
        ])

        ttk.Button(dev10, text="Remove", command=self._remove_1025).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Perfecto 2V remove
        perfecto = ttk.LabelFrame(parent, text="Perfecto 2V (enter per-warranty quantities)", padding=8)
        perfecto.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        self.rem_perfecto_qm = tk.StringVar(value="0")
        self.rem_perfecto_flat = tk.StringVar(value="0")
        self.rem_perfecto_manuf = tk.StringVar(value="0")
        self._row_inputs(perfecto, 0, [
            ("QM Warranty", self.rem_perfecto_qm),
            ("Flat Rate", self.rem_perfecto_flat),
            ("Manufacture Warranty", self.rem_perfecto_manuf),
        ])
        ttk.Button(perfecto, text="Remove", command=self._remove_perfecto).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # M10 remove
        m10 = ttk.LabelFrame(parent, text="M10 (enter per-warranty quantities)", padding=8)
        m10.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.rem_m10_qm = tk.StringVar(value="0")
        self.rem_m10_flat = tk.StringVar(value="0")
        self.rem_m10_manuf = tk.StringVar(value="0")
        self._row_inputs(m10, 0, [
            ("QM Warranty", self.rem_m10_qm),
            ("Flat Rate", self.rem_m10_flat),
            ("Manufacture Warranty", self.rem_m10_manuf),
        ])
        ttk.Button(m10, text="Remove", command=self._remove_m10).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Rhythm LM5A remove
        lm5a = ttk.LabelFrame(parent, text="Rhythm LM5A (enter per-warranty quantities)", padding=8)
        lm5a.grid(row=6, column=0, sticky="ew", pady=(10, 0))
        self.rem_lm5a_qm = tk.StringVar(value="0")
        self.rem_lm5a_flat = tk.StringVar(value="0")
        self.rem_lm5a_manuf = tk.StringVar(value="0")
        self._row_inputs(lm5a, 0, [
            ("QM Warranty", self.rem_lm5a_qm),
            ("Flat Rate", self.rem_lm5a_flat),
            ("Manufacture Warranty", self.rem_lm5a_manuf),
        ])
        ttk.Button(lm5a, text="Remove", command=self._remove_lm5a).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Rhythm LM5BA remove
        lm5ba = ttk.LabelFrame(parent, text="Rhythm LM5BA (enter per-warranty quantities)", padding=8)
        lm5ba.grid(row=7, column=0, sticky="ew", pady=(10, 0))
        self.rem_lm5ba_qm = tk.StringVar(value="0")
        self.rem_lm5ba_flat = tk.StringVar(value="0")
        self.rem_lm5ba_manuf = tk.StringVar(value="0")
        self._row_inputs(lm5ba, 0, [
            ("QM Warranty", self.rem_lm5ba_qm),
            ("Flat Rate", self.rem_lm5ba_flat),
            ("Manufacture Warranty", self.rem_lm5ba_manuf),
        ])
        ttk.Button(lm5ba, text="Remove", command=self._remove_lm5ba).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Rhythm LM5CA remove
        lm5ca = ttk.LabelFrame(parent, text="Rhythm LM5CA (enter per-warranty quantities)", padding=8)
        lm5ca.grid(row=8, column=0, sticky="ew", pady=(10, 0))
        self.rem_lm5ca_qm = tk.StringVar(value="0")
        self.rem_lm5ca_flat = tk.StringVar(value="0")
        self.rem_lm5ca_manuf = tk.StringVar(value="0")
        self._row_inputs(lm5ca, 0, [
            ("QM Warranty", self.rem_lm5ca_qm),
            ("Flat Rate", self.rem_lm5ca_flat),
            ("Manufacture Warranty", self.rem_lm5ca_manuf),
        ])
        ttk.Button(lm5ca, text="Remove", command=self._remove_lm5ca).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # POC remove
        poc = ttk.LabelFrame(parent, text="POC (enter quantity)", padding=8)
        poc.grid(row=9, column=0, sticky="ew", pady=(10, 0))
        self.rem_poc_repair = tk.StringVar(value="0")
        self._row_inputs(poc, 0, [
            ("Repair", self.rem_poc_repair),
        ])
        ttk.Button(poc, text="Remove", command=self._remove_poc).grid(row=2, column=0, pady=(6, 0), sticky="w")

        # Flow these sections into columns when nearing bottom
        self.rem_sections = [
            str_frame, hf_frame, dev, dev10, perfecto, m10, lm5a, lm5ba, lm5ca, poc
        ]
        parent.bind("<Configure>", lambda e: self._flow_layout(parent, self.rem_sections, columns=2))
        self._flow_layout(parent, self.rem_sections, columns=2)

    def _row_inputs(self, parent, start_row, pairs):
        # Helper to place label/entry pairs in grid, two per row if space
        col = 0
        row = start_row
        for label, var in pairs:
            ttk.Label(parent, text=label+":").grid(row=row, column=col, sticky="w", pady=2)
            ttk.Entry(parent, textvariable=var, width=8).grid(row=row, column=col+1, padx=(6, 18))
            col += 2
            if col >= 6:
                col = 0
                row += 1

    def _refresh_totals(self):
        # rollover start-of-day if the date changed
        self._ensure_start_of_day()
        self.output_var.set(str(self.state["output"]))
        self.weighted_var.set(f"{self.state['weighted_output']:.2f}")
        self.start_var.set(str(self.state.get("start_of_day_output", 0)))
        # compute today's output as total minus start-of-day
        today = max(0, self.state.get("output", 0) - self.state.get("start_of_day_output", 0))
        self.today_var.set(str(today))
        # refresh breakdown labels if present
        if hasattr(self, "bd_labels"):
            self._refresh_breakdown()

    def _ensure_start_of_day(self):
        today = date.today().isoformat()
        if self.state.get("start_date") != today:
            self.state["start_date"] = today
            self.state["start_of_day_output"] = self.state.get("output", 0)
            save_progress(self.state)

    # ---- Add handlers ----
    def _add_stratus(self):
        s_flat = self._parse_nonneg(self.add_s_flat)
        s_manuf = self._parse_nonneg(self.add_s_manuf)
        qty = s_flat + s_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Stratus quantity to add.")
            return
        self.state["output"] += qty
        self.state["weighted_output"] += STRATUS_POINTS * qty
        self.state["count_stratus_flat"] = self.state.get("count_stratus_flat", 0) + s_flat
        self.state["count_stratus_manuf"] = self.state.get("count_stratus_manuf", 0) + s_manuf
        self.state["count_stratus"] = self.state.get("count_stratus", 0) + qty
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {qty} Stratus unit(s).")

    def _add_homefill(self):
        h_flat = self._parse_nonneg(self.add_h_flat)
        h_manuf = self._parse_nonneg(self.add_h_manuf)
        qty = h_flat + h_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Homefill quantity to add.")
            return
        self.state["output"] += qty
        self.state["weighted_output"] += HOMEFILL_POINTS * qty
        self.state["count_homefill_flat"] = self.state.get("count_homefill_flat", 0) + h_flat
        self.state["count_homefill_manuf"] = self.state.get("count_homefill_manuf", 0) + h_manuf
        self.state["count_homefill"] = self.state.get("count_homefill", 0) + qty
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {qty} Homefill unit(s).")

    def _add_525(self):
        q = self._parse_nonneg(self.add_q)
        p = self._parse_nonneg(self.add_p)
        m = self._parse_nonneg(self.add_m)
        f = self._parse_nonneg(self.add_f)
        w = self._parse_nonneg(self.add_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_qm"] = self.state.get("count_qm", 0) + q
        self.state["count_pm"] = self.state.get("count_pm", 0) + p
        self.state["count_minor"] = self.state.get("count_minor", 0) + m
        self.state["count_flat"] = self.state.get("count_flat", 0) + f
        self.state["count_manuf"] = self.state.get("count_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} unit(s) across 525 warranties.")

    def _add_1025(self):
        q = self._parse_nonneg(self.add10_q)
        p = self._parse_nonneg(self.add10_p)
        m = self._parse_nonneg(self.add10_m)
        f = self._parse_nonneg(self.add10_f)
        w = self._parse_nonneg(self.add10_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_1025_qm"] = self.state.get("count_1025_qm", 0) + q
        self.state["count_1025_pm"] = self.state.get("count_1025_pm", 0) + p
        self.state["count_1025_minor"] = self.state.get("count_1025_minor", 0) + m
        self.state["count_1025_flat"] = self.state.get("count_1025_flat", 0) + f
        self.state["count_1025_manuf"] = self.state.get("count_1025_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} unit(s) across 1025 warranties.")

    def _add_perfecto(self):
        q = self._parse_nonneg(self.add_perfecto_qm)
        f = self._parse_nonneg(self.add_perfecto_flat)
        w = self._parse_nonneg(self.add_perfecto_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Perfecto 2V quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            UNIT_POINTS["Perfecto 2V"]["QM Warranty"] * q
            + UNIT_POINTS["Perfecto 2V"]["Flat Rate"] * f
            + UNIT_POINTS["Perfecto 2V"]["Manufacture Warranty"] * w
        )
        self.state["count_perfecto_qm"] = self.state.get("count_perfecto_qm", 0) + q
        self.state["count_perfecto_flat"] = self.state.get("count_perfecto_flat", 0) + f
        self.state["count_perfecto_manuf"] = self.state.get("count_perfecto_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} Perfecto 2V unit(s).")

    def _add_m10(self):
        q = self._parse_nonneg(self.add_m10_qm)
        f = self._parse_nonneg(self.add_m10_flat)
        w = self._parse_nonneg(self.add_m10_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one M10 quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            UNIT_POINTS["M10"]["QM Warranty"] * q
            + UNIT_POINTS["M10"]["Flat Rate"] * f
            + UNIT_POINTS["M10"]["Manufacture Warranty"] * w
        )
        self.state["count_m10_qm"] = self.state.get("count_m10_qm", 0) + q
        self.state["count_m10_flat"] = self.state.get("count_m10_flat", 0) + f
        self.state["count_m10_manuf"] = self.state.get("count_m10_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} M10 unit(s).")

    def _add_lm5a(self):
        q = self._parse_nonneg(self.add_lm5a_qm)
        f = self._parse_nonneg(self.add_lm5a_flat)
        w = self._parse_nonneg(self.add_lm5a_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Rhythm LM5A quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            UNIT_POINTS["Rhythm LM5A"]["QM Warranty"] * q
            + UNIT_POINTS["Rhythm LM5A"]["Flat Rate"] * f
            + UNIT_POINTS["Rhythm LM5A"]["Manufacture Warranty"] * w
        )
        self.state["count_lm5a_qm"] = self.state.get("count_lm5a_qm", 0) + q
        self.state["count_lm5a_flat"] = self.state.get("count_lm5a_flat", 0) + f
        self.state["count_lm5a_manuf"] = self.state.get("count_lm5a_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} Rhythm LM5A unit(s).")

    def _add_lm5ba(self):
        q = self._parse_nonneg(self.add_lm5ba_qm)
        f = self._parse_nonneg(self.add_lm5ba_flat)
        w = self._parse_nonneg(self.add_lm5ba_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Rhythm LM5BA quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            UNIT_POINTS["Rhythm LM5BA"]["QM Warranty"] * q
            + UNIT_POINTS["Rhythm LM5BA"]["Flat Rate"] * f
            + UNIT_POINTS["Rhythm LM5BA"]["Manufacture Warranty"] * w
        )
        self.state["count_lm5ba_qm"] = self.state.get("count_lm5ba_qm", 0) + q
        self.state["count_lm5ba_flat"] = self.state.get("count_lm5ba_flat", 0) + f
        self.state["count_lm5ba_manuf"] = self.state.get("count_lm5ba_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} Rhythm LM5BA unit(s).")

    def _add_lm5ca(self):
        q = self._parse_nonneg(self.add_lm5ca_qm)
        f = self._parse_nonneg(self.add_lm5ca_flat)
        w = self._parse_nonneg(self.add_lm5ca_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Rhythm LM5CA quantity to add.")
            return
        self.state["output"] += total
        self.state["weighted_output"] += (
            UNIT_POINTS["Rhythm LM5CA"]["QM Warranty"] * q
            + UNIT_POINTS["Rhythm LM5CA"]["Flat Rate"] * f
            + UNIT_POINTS["Rhythm LM5CA"]["Manufacture Warranty"] * w
        )
        self.state["count_lm5ca_qm"] = self.state.get("count_lm5ca_qm", 0) + q
        self.state["count_lm5ca_flat"] = self.state.get("count_lm5ca_flat", 0) + f
        self.state["count_lm5ca_manuf"] = self.state.get("count_lm5ca_manuf", 0) + w
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {total} Rhythm LM5CA unit(s).")

    def _add_poc(self):
        r = self._parse_nonneg(self.add_poc_repair)
        if r == 0:
            messagebox.showinfo("No Action", "Enter at least one POC Repair quantity to add.")
            return
        self.state["output"] += r
        self.state["weighted_output"] += UNIT_POINTS["POC"]["Repair"] * r
        self.state["count_poc_repair"] = self.state.get("count_poc_repair", 0) + r
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Added", f"Added {r} POC Repair unit(s).")

    # ---- Remove handlers ----
    def _remove_stratus(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        s_flat = self._parse_nonneg(self.rem_s_flat)
        s_manuf = self._parse_nonneg(self.rem_s_manuf)
        qty = s_flat + s_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Stratus quantity to remove.")
            return
        if qty > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if s_flat > self.state.get("count_stratus_flat", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Stratus Flat Rate than recorded.")
            return
        if s_manuf > self.state.get("count_stratus_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Stratus Manufacture Warranty than recorded.")
            return
        self.state["output"] -= qty
        self.state["weighted_output"] -= STRATUS_POINTS * qty
        self.state["count_stratus_flat"] -= s_flat
        self.state["count_stratus_manuf"] -= s_manuf
        self.state["count_stratus"] -= qty
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {qty} Stratus unit(s).")

    def _remove_homefill(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        h_flat = self._parse_nonneg(self.rem_h_flat)
        h_manuf = self._parse_nonneg(self.rem_h_manuf)
        qty = h_flat + h_manuf
        if qty == 0:
            messagebox.showinfo("No Action", "Enter at least one Homefill quantity to remove.")
            return
        if qty > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if h_flat > self.state.get("count_homefill_flat", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Homefill Flat Rate than recorded.")
            return
        if h_manuf > self.state.get("count_homefill_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Homefill Manufacture Warranty than recorded.")
            return
        self.state["output"] -= qty
        self.state["weighted_output"] -= HOMEFILL_POINTS * qty
        self.state["count_homefill_flat"] -= h_flat
        self.state["count_homefill_manuf"] -= h_manuf
        self.state["count_homefill"] -= qty
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {qty} Homefill unit(s).")

    def _remove_525(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_q)
        p = self._parse_nonneg(self.rem_p)
        m = self._parse_nonneg(self.rem_m)
        f = self._parse_nonneg(self.rem_f)
        w = self._parse_nonneg(self.rem_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        # per-category checks
        if q > self.state.get("count_qm", 0):
            messagebox.showwarning("Too Many", "Cannot remove more QM Warranty than recorded.")
            return
        if p > self.state.get("count_pm", 0):
            messagebox.showwarning("Too Many", "Cannot remove more PM than recorded.")
            return
        if m > self.state.get("count_minor", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Minor Repair than recorded.")
            return
        if f > self.state.get("count_flat", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Flat Rate than recorded.")
            return
        if w > self.state.get("count_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more Manufacture Warranty than recorded.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_qm"] -= q
        self.state["count_pm"] -= p
        self.state["count_minor"] -= m
        self.state["count_flat"] -= f
        self.state["count_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} unit(s) across 525 warranties.")

    def _remove_1025(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem10_q)
        p = self._parse_nonneg(self.rem10_p)
        m = self._parse_nonneg(self.rem10_m)
        f = self._parse_nonneg(self.rem10_f)
        w = self._parse_nonneg(self.rem10_w)
        total = q + p + m + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        # per-category checks
        if q > self.state.get("count_1025_qm", 0) or \
           p > self.state.get("count_1025_pm", 0) or \
           m > self.state.get("count_1025_minor", 0) or \
           f > self.state.get("count_1025_flat", 0) or \
           w > self.state.get("count_1025_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for 1025 categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            DEV_POINTS["QM Warranty"] * q
            + DEV_POINTS["PM"] * p
            + DEV_POINTS["Minor Repair"] * m
            + DEV_POINTS["Flat Rate"] * f
            + DEV_POINTS["Manufacture Warranty"] * w
        )
        self.state["count_1025_qm"] -= q
        self.state["count_1025_pm"] -= p
        self.state["count_1025_minor"] -= m
        self.state["count_1025_flat"] -= f
        self.state["count_1025_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} unit(s) across 1025 warranties.")

    def _remove_perfecto(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_perfecto_qm)
        f = self._parse_nonneg(self.rem_perfecto_flat)
        w = self._parse_nonneg(self.rem_perfecto_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Perfecto 2V quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if q > self.state.get("count_perfecto_qm", 0) or f > self.state.get("count_perfecto_flat", 0) or w > self.state.get("count_perfecto_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for Perfecto 2V categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            UNIT_POINTS["Perfecto 2V"]["QM Warranty"] * q
            + UNIT_POINTS["Perfecto 2V"]["Flat Rate"] * f
            + UNIT_POINTS["Perfecto 2V"]["Manufacture Warranty"] * w
        )
        self.state["count_perfecto_qm"] -= q
        self.state["count_perfecto_flat"] -= f
        self.state["count_perfecto_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} Perfecto 2V unit(s).")

    def _remove_m10(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_m10_qm)
        f = self._parse_nonneg(self.rem_m10_flat)
        w = self._parse_nonneg(self.rem_m10_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one M10 quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if q > self.state.get("count_m10_qm", 0) or f > self.state.get("count_m10_flat", 0) or w > self.state.get("count_m10_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for M10 categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            UNIT_POINTS["M10"]["QM Warranty"] * q
            + UNIT_POINTS["M10"]["Flat Rate"] * f
            + UNIT_POINTS["M10"]["Manufacture Warranty"] * w
        )
        self.state["count_m10_qm"] -= q
        self.state["count_m10_flat"] -= f
        self.state["count_m10_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} M10 unit(s).")

    def _remove_lm5a(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_lm5a_qm)
        f = self._parse_nonneg(self.rem_lm5a_flat)
        w = self._parse_nonneg(self.rem_lm5a_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Rhythm LM5A quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if q > self.state.get("count_lm5a_qm", 0) or f > self.state.get("count_lm5a_flat", 0) or w > self.state.get("count_lm5a_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for Rhythm LM5A categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            UNIT_POINTS["Rhythm LM5A"]["QM Warranty"] * q
            + UNIT_POINTS["Rhythm LM5A"]["Flat Rate"] * f
            + UNIT_POINTS["Rhythm LM5A"]["Manufacture Warranty"] * w
        )
        self.state["count_lm5a_qm"] -= q
        self.state["count_lm5a_flat"] -= f
        self.state["count_lm5a_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} Rhythm LM5A unit(s).")

    def _remove_lm5ba(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_lm5ba_qm)
        f = self._parse_nonneg(self.rem_lm5ba_flat)
        w = self._parse_nonneg(self.rem_lm5ba_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Rhythm LM5BA quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if q > self.state.get("count_lm5ba_qm", 0) or f > self.state.get("count_lm5ba_flat", 0) or w > self.state.get("count_lm5ba_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for Rhythm LM5BA categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            UNIT_POINTS["Rhythm LM5BA"]["QM Warranty"] * q
            + UNIT_POINTS["Rhythm LM5BA"]["Flat Rate"] * f
            + UNIT_POINTS["Rhythm LM5BA"]["Manufacture Warranty"] * w
        )
        self.state["count_lm5ba_qm"] -= q
        self.state["count_lm5ba_flat"] -= f
        self.state["count_lm5ba_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} Rhythm LM5BA unit(s).")

    def _remove_lm5ca(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        q = self._parse_nonneg(self.rem_lm5ca_qm)
        f = self._parse_nonneg(self.rem_lm5ca_flat)
        w = self._parse_nonneg(self.rem_lm5ca_manuf)
        total = q + f + w
        if total == 0:
            messagebox.showinfo("No Action", "Enter at least one Rhythm LM5CA quantity to remove.")
            return
        if total > self.state["output"]:
            messagebox.showwarning("Too Many", "Cannot remove more than total output.")
            return
        if q > self.state.get("count_lm5ca_qm", 0) or f > self.state.get("count_lm5ca_flat", 0) or w > self.state.get("count_lm5ca_manuf", 0):
            messagebox.showwarning("Too Many", "Cannot remove more than recorded for Rhythm LM5CA categories.")
            return
        self.state["output"] -= total
        self.state["weighted_output"] -= (
            UNIT_POINTS["Rhythm LM5CA"]["QM Warranty"] * q
            + UNIT_POINTS["Rhythm LM5CA"]["Flat Rate"] * f
            + UNIT_POINTS["Rhythm LM5CA"]["Manufacture Warranty"] * w
        )
        self.state["count_lm5ca_qm"] -= q
        self.state["count_lm5ca_flat"] -= f
        self.state["count_lm5ca_manuf"] -= w
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {total} Rhythm LM5CA unit(s).")

    def _remove_poc(self):
        if self.state["output"] == 0:
            messagebox.showwarning("No Units", "No units to remove.")
            return
        r = self._parse_nonneg(self.rem_poc_repair)
        if r == 0:
            messagebox.showinfo("No Action", "Enter at least one POC Repair quantity to remove.")
            return
        if r > self.state.get("count_poc_repair", 0):
            messagebox.showwarning("Too Many", "Cannot remove more POC Repair than recorded.")
            return
        self.state["output"] -= r
        self.state["weighted_output"] -= UNIT_POINTS["POC"]["Repair"] * r
        self.state["count_poc_repair"] -= r
        if self.state["output"] == 0:
            self.state["weighted_output"] = 0.0
        save_progress(self.state)
        self._refresh_totals()
        messagebox.showinfo("Removed", f"Removed {r} POC Repair unit(s).")

    # ---- breakdown tab ----
    def _build_breakdown_tab(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        grid = ttk.Frame(parent)
        grid.grid(row=0, column=0, sticky="nw")
        grid2 = ttk.Frame(parent)
        grid2.grid(row=0, column=1, sticky="nw", padx=(16,0))
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=0, column=2, sticky="ne", padx=(16,0))

        self.bd_labels = {}
        self.bd_title_vars = {}
        row = 0

        # Stratus total (bold)
        title_stratus = tk.StringVar(value="Stratus:")
        ttk.Label(grid, textvariable=title_stratus, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=2)
        var_stratus = tk.StringVar()
        ttk.Label(grid, textvariable=var_stratus, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_stratus"] = var_stratus
        self.bd_title_vars["title_stratus"] = title_stratus
        row += 1
        # Stratus subcategories
        title_s_flat = tk.StringVar(value="Stratus Flat Rate:")
        ttk.Label(grid, textvariable=title_s_flat).grid(row=row, column=0, sticky="w", pady=2)
        var_s_flat = tk.StringVar()
        ttk.Label(grid, textvariable=var_s_flat).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_stratus_flat"] = var_s_flat
        self.bd_title_vars["title_stratus_flat"] = title_s_flat
        row += 1
        title_s_manuf = tk.StringVar(value="Stratus Manufacture Warranty:")
        ttk.Label(grid, textvariable=title_s_manuf).grid(row=row, column=0, sticky="w", pady=2)
        var_s_manuf = tk.StringVar()
        ttk.Label(grid, textvariable=var_s_manuf).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_stratus_manuf"] = var_s_manuf
        self.bd_title_vars["title_stratus_manuf"] = title_s_manuf
        row += 1

        # Homefill total (bold)
        title_homefill = tk.StringVar(value="Homefill:")
        ttk.Label(grid, textvariable=title_homefill, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=(8,2))
        var_homefill = tk.StringVar()
        ttk.Label(grid, textvariable=var_homefill, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_homefill"] = var_homefill
        self.bd_title_vars["title_homefill"] = title_homefill
        row += 1
        # Homefill subcategories
        title_h_flat = tk.StringVar(value="Homefill Flat Rate:")
        ttk.Label(grid, textvariable=title_h_flat).grid(row=row, column=0, sticky="w", pady=2)
        var_h_flat = tk.StringVar()
        ttk.Label(grid, textvariable=var_h_flat).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_homefill_flat"] = var_h_flat
        self.bd_title_vars["title_homefill_flat"] = title_h_flat
        row += 1
        title_h_manuf = tk.StringVar(value="Homefill Manufacture Warranty:")
        ttk.Label(grid, textvariable=title_h_manuf).grid(row=row, column=0, sticky="w", pady=2)
        var_h_manuf = tk.StringVar()
        ttk.Label(grid, textvariable=var_h_manuf).grid(row=row, column=1, sticky="w")
        self.bd_labels["count_homefill_manuf"] = var_h_manuf
        self.bd_title_vars["title_homefill_manuf"] = title_h_manuf
        row += 1

        # 525 total (bold)
        title_525 = tk.StringVar(value="525:")
        ttk.Label(grid, textvariable=title_525, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=(8,2))
        var_525_total = tk.StringVar()
        ttk.Label(grid, textvariable=var_525_total, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["total_525"] = var_525_total
        self.bd_title_vars["title_525"] = title_525
        row += 1
        # 525 subcategories
        for title, key in [
            ("525 QM Warranty", "count_qm"),
            ("525 PM", "count_pm"),
            ("525 Minor Repair", "count_minor"),
            ("525 Flat Rate", "count_flat"),
            ("525 Manufacture Warranty", "count_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid, textvariable=tvar).grid(row=row, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid, textvariable=var).grid(row=row, column=1, sticky="w")
            self.bd_labels[key] = var
            # map title vars by suffix for easy refresh
            suffix = key.split("_")[-1]
            self.bd_title_vars[f"title_525_{suffix}"] = tvar
            row += 1

        # 1025 total (bold)
        title_1025 = tk.StringVar(value="1025:")
        ttk.Label(grid, textvariable=title_1025, font=self.bold_font).grid(row=row, column=0, sticky="w", pady=(8,2))
        var_1025_total = tk.StringVar()
        ttk.Label(grid, textvariable=var_1025_total, font=self.bold_font).grid(row=row, column=1, sticky="w")
        self.bd_labels["total_1025"] = var_1025_total
        self.bd_title_vars["title_1025"] = title_1025
        row += 1
        # 1025 subcategories
        for title, key in [
            ("1025 QM Warranty", "count_1025_qm"),
            ("1025 PM", "count_1025_pm"),
            ("1025 Minor Repair", "count_1025_minor"),
            ("1025 Flat Rate", "count_1025_flat"),
            ("1025 Manufacture Warranty", "count_1025_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid, textvariable=tvar).grid(row=row, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid, textvariable=var).grid(row=row, column=1, sticky="w")
            self.bd_labels[key] = var
            # map title vars by 1025 suffix
            suffix = key.split("_")[-1]
            self.bd_title_vars[f"title_1025_{suffix}"] = tvar
            row += 1

        # Right-side table: points structure
        self._build_points_table(table_frame)

        # Perfecto 2V total (bold)
        title_perfecto = tk.StringVar(value="Perfecto 2V:")
        ttk.Label(grid2, textvariable=title_perfecto, font=self.bold_font).grid(row=0, column=0, sticky="w", pady=(8,2))
        var_perfecto_total = tk.StringVar()
        ttk.Label(grid2, textvariable=var_perfecto_total, font=self.bold_font).grid(row=0, column=1, sticky="w")
        self.bd_labels["count_perfecto_total"] = var_perfecto_total
        self.bd_title_vars["title_perfecto"] = title_perfecto
        r2 = 1
        for title, key, tkey in [
            ("Perfecto 2V QM Warranty", "count_perfecto_qm", "title_perfecto_qm"),
            ("Perfecto 2V Flat Rate", "count_perfecto_flat", "title_perfecto_flat"),
            ("Perfecto 2V Manufacture Warranty", "count_perfecto_manuf", "title_perfecto_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid2, textvariable=tvar).grid(row=r2, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid2, textvariable=var).grid(row=r2, column=1, sticky="w")
            self.bd_labels[key] = var
            self.bd_title_vars[tkey] = tvar
            r2 += 1

        # M10 total (bold)
        title_m10 = tk.StringVar(value="M10:")
        ttk.Label(grid2, textvariable=title_m10, font=self.bold_font).grid(row=r2, column=0, sticky="w", pady=(8,2))
        var_m10_total = tk.StringVar()
        ttk.Label(grid2, textvariable=var_m10_total, font=self.bold_font).grid(row=r2, column=1, sticky="w")
        self.bd_labels["count_m10_total"] = var_m10_total
        self.bd_title_vars["title_m10"] = title_m10
        r2 += 1
        for title, key, tkey in [
            ("M10 QM Warranty", "count_m10_qm", "title_m10_qm"),
            ("M10 Flat Rate", "count_m10_flat", "title_m10_flat"),
            ("M10 Manufacture Warranty", "count_m10_manuf", "title_m10_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid2, textvariable=tvar).grid(row=r2, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid2, textvariable=var).grid(row=r2, column=1, sticky="w")
            self.bd_labels[key] = var
            self.bd_title_vars[tkey] = tvar
            r2 += 1

        # Rhythm LM5A total (bold)
        title_lm5a = tk.StringVar(value="Rhythm LM5A:")
        ttk.Label(grid2, textvariable=title_lm5a, font=self.bold_font).grid(row=r2, column=0, sticky="w", pady=(8,2))
        var_lm5a_total = tk.StringVar()
        ttk.Label(grid2, textvariable=var_lm5a_total, font=self.bold_font).grid(row=r2, column=1, sticky="w")
        self.bd_labels["count_lm5a_total"] = var_lm5a_total
        self.bd_title_vars["title_lm5a"] = title_lm5a
        r2 += 1
        for title, key, tkey in [
            ("Rhythm LM5A QM Warranty", "count_lm5a_qm", "title_lm5a_qm"),
            ("Rhythm LM5A Flat Rate", "count_lm5a_flat", "title_lm5a_flat"),
            ("Rhythm LM5A Manufacture Warranty", "count_lm5a_manuf", "title_lm5a_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid2, textvariable=tvar).grid(row=r2, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid2, textvariable=var).grid(row=r2, column=1, sticky="w")
            self.bd_labels[key] = var
            self.bd_title_vars[tkey] = tvar
            r2 += 1

        # Rhythm LM5BA total (bold)
        title_lm5ba = tk.StringVar(value="Rhythm LM5BA:")
        ttk.Label(grid2, textvariable=title_lm5ba, font=self.bold_font).grid(row=r2, column=0, sticky="w", pady=(8,2))
        var_lm5ba_total = tk.StringVar()
        ttk.Label(grid2, textvariable=var_lm5ba_total, font=self.bold_font).grid(row=r2, column=1, sticky="w")
        self.bd_labels["count_lm5ba_total"] = var_lm5ba_total
        self.bd_title_vars["title_lm5ba"] = title_lm5ba
        r2 += 1
        for title, key, tkey in [
            ("Rhythm LM5BA QM Warranty", "count_lm5ba_qm", "title_lm5ba_qm"),
            ("Rhythm LM5BA Flat Rate", "count_lm5ba_flat", "title_lm5ba_flat"),
            ("Rhythm LM5BA Manufacture Warranty", "count_lm5ba_manuf", "title_lm5ba_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid2, textvariable=tvar).grid(row=r2, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid2, textvariable=var).grid(row=r2, column=1, sticky="w")
            self.bd_labels[key] = var
            self.bd_title_vars[tkey] = tvar
            r2 += 1

        # Rhythm LM5CA total (bold)
        title_lm5ca = tk.StringVar(value="Rhythm LM5CA:")
        ttk.Label(grid2, textvariable=title_lm5ca, font=self.bold_font).grid(row=r2, column=0, sticky="w", pady=(8,2))
        var_lm5ca_total = tk.StringVar()
        ttk.Label(grid2, textvariable=var_lm5ca_total, font=self.bold_font).grid(row=r2, column=1, sticky="w")
        self.bd_labels["count_lm5ca_total"] = var_lm5ca_total
        self.bd_title_vars["title_lm5ca"] = title_lm5ca
        r2 += 1
        for title, key, tkey in [
            ("Rhythm LM5CA QM Warranty", "count_lm5ca_qm", "title_lm5ca_qm"),
            ("Rhythm LM5CA Flat Rate", "count_lm5ca_flat", "title_lm5ca_flat"),
            ("Rhythm LM5CA Manufacture Warranty", "count_lm5ca_manuf", "title_lm5ca_manuf"),
        ]:
            tvar = tk.StringVar(value=f"{title}:")
            ttk.Label(grid2, textvariable=tvar).grid(row=r2, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            ttk.Label(grid2, textvariable=var).grid(row=r2, column=1, sticky="w")
            self.bd_labels[key] = var
            self.bd_title_vars[tkey] = tvar
            r2 += 1

        # POC total (bold)
        title_poc = tk.StringVar(value="POC:")
        ttk.Label(grid2, textvariable=title_poc, font=self.bold_font).grid(row=r2, column=0, sticky="w", pady=(8,2))
        var_poc_total = tk.StringVar()
        ttk.Label(grid2, textvariable=var_poc_total, font=self.bold_font).grid(row=r2, column=1, sticky="w")
        self.bd_labels["count_poc_total"] = var_poc_total
        self.bd_title_vars["title_poc"] = title_poc
        r2 += 1
        # POC subcategory
        tvar = tk.StringVar(value="POC Repair:")
        ttk.Label(grid2, textvariable=tvar).grid(row=r2, column=0, sticky="w", pady=2)
        var = tk.StringVar()
        ttk.Label(grid2, textvariable=var).grid(row=r2, column=1, sticky="w")
        self.bd_labels["count_poc_repair"] = var
        self.bd_title_vars["title_poc_repair"] = tvar
        r2 += 1

        # No dynamic flow needed here; content already split into two columns with table separate

        self._refresh_breakdown()

    def _refresh_breakdown(self):
        # Stratus
        self.bd_labels["count_stratus"].set(str(self.state.get("count_stratus", 0)))
        self.bd_labels["count_stratus_flat"].set(str(self.state.get("count_stratus_flat", 0)))
        self.bd_labels["count_stratus_manuf"].set(str(self.state.get("count_stratus_manuf", 0)))
        # Stratus points in titles
        s_total = self.state.get("count_stratus", 0)
        s_flat = self.state.get("count_stratus_flat", 0)
        s_manuf = self.state.get("count_stratus_manuf", 0)
        self.bd_title_vars["title_stratus"].set(f"Stratus ({STRATUS_POINTS * s_total:.2f} pts):")
        self.bd_title_vars["title_stratus_flat"].set(f"Stratus Flat Rate ({STRATUS_POINTS * s_flat:.2f} pts):")
        self.bd_title_vars["title_stratus_manuf"].set(f"Stratus Manufacture Warranty ({STRATUS_POINTS * s_manuf:.2f} pts):")
        # Homefill
        self.bd_labels["count_homefill"].set(str(self.state.get("count_homefill", 0)))
        self.bd_labels["count_homefill_flat"].set(str(self.state.get("count_homefill_flat", 0)))
        self.bd_labels["count_homefill_manuf"].set(str(self.state.get("count_homefill_manuf", 0)))
        # Homefill points in titles
        h_total = self.state.get("count_homefill", 0)
        h_flat = self.state.get("count_homefill_flat", 0)
        h_manuf = self.state.get("count_homefill_manuf", 0)
        self.bd_title_vars["title_homefill"].set(f"Homefill ({HOMEFILL_POINTS * h_total:.2f} pts):")
        self.bd_title_vars["title_homefill_flat"].set(f"Homefill Flat Rate ({HOMEFILL_POINTS * h_flat:.2f} pts):")
        self.bd_title_vars["title_homefill_manuf"].set(f"Homefill Manufacture Warranty ({HOMEFILL_POINTS * h_manuf:.2f} pts):")
        # 525 total and subcats
        qm = self.state.get("count_qm", 0)
        pm = self.state.get("count_pm", 0)
        minor = self.state.get("count_minor", 0)
        flat = self.state.get("count_flat", 0)
        manuf = self.state.get("count_manuf", 0)
        total_525 = qm + pm + minor + flat + manuf
        self.bd_labels["total_525"].set(str(total_525))
        self.bd_labels["count_qm"].set(str(qm))
        self.bd_labels["count_pm"].set(str(pm))
        self.bd_labels["count_minor"].set(str(minor))
        self.bd_labels["count_flat"].set(str(flat))
        self.bd_labels["count_manuf"].set(str(manuf))
        # 525 points in titles
        pts_525_total = (
            DEV_POINTS["QM Warranty"] * qm
            + DEV_POINTS["PM"] * pm
            + DEV_POINTS["Minor Repair"] * minor
            + DEV_POINTS["Flat Rate"] * flat
            + DEV_POINTS["Manufacture Warranty"] * manuf
        )
        self.bd_title_vars["title_525"].set(f"525 ({pts_525_total:.2f} pts):")
        self.bd_title_vars["title_525_qm"].set(f"525 QM Warranty ({DEV_POINTS['QM Warranty'] * qm:.2f} pts):")
        self.bd_title_vars["title_525_pm"].set(f"525 PM ({DEV_POINTS['PM'] * pm:.2f} pts):")
        self.bd_title_vars["title_525_minor"].set(f"525 Minor Repair ({DEV_POINTS['Minor Repair'] * minor:.2f} pts):")
        self.bd_title_vars["title_525_flat"].set(f"525 Flat Rate ({DEV_POINTS['Flat Rate'] * flat:.2f} pts):")
        self.bd_title_vars["title_525_manuf"].set(f"525 Manufacture Warranty ({DEV_POINTS['Manufacture Warranty'] * manuf:.2f} pts):")
        # 1025 total and subcats
        q10 = self.state.get("count_1025_qm", 0)
        p10 = self.state.get("count_1025_pm", 0)
        m10 = self.state.get("count_1025_minor", 0)
        f10 = self.state.get("count_1025_flat", 0)
        w10 = self.state.get("count_1025_manuf", 0)
        total_1025 = q10 + p10 + m10 + f10 + w10
        self.bd_labels["total_1025"].set(str(total_1025))
        self.bd_labels["count_1025_qm"].set(str(q10))
        self.bd_labels["count_1025_pm"].set(str(p10))
        self.bd_labels["count_1025_minor"].set(str(m10))
        self.bd_labels["count_1025_flat"].set(str(f10))
        self.bd_labels["count_1025_manuf"].set(str(w10))
        # 1025 points in titles
        pts_1025_total = (
            DEV_POINTS["QM Warranty"] * q10
            + DEV_POINTS["PM"] * p10
            + DEV_POINTS["Minor Repair"] * m10
            + DEV_POINTS["Flat Rate"] * f10
            + DEV_POINTS["Manufacture Warranty"] * w10
        )
        self.bd_title_vars["title_1025"].set(f"1025 ({pts_1025_total:.2f} pts):")
        self.bd_title_vars["title_1025_qm"].set(f"1025 QM Warranty ({DEV_POINTS['QM Warranty'] * q10:.2f} pts):")
        self.bd_title_vars["title_1025_pm"].set(f"1025 PM ({DEV_POINTS['PM'] * p10:.2f} pts):")
        self.bd_title_vars["title_1025_minor"].set(f"1025 Minor Repair ({DEV_POINTS['Minor Repair'] * m10:.2f} pts):")
        self.bd_title_vars["title_1025_flat"].set(f"1025 Flat Rate ({DEV_POINTS['Flat Rate'] * f10:.2f} pts):")
        self.bd_title_vars["title_1025_manuf"].set(f"1025 Manufacture Warranty ({DEV_POINTS['Manufacture Warranty'] * w10:.2f} pts):")

        # Perfecto 2V
        perf_qm = self.state.get("count_perfecto_qm", 0)
        perf_flat = self.state.get("count_perfecto_flat", 0)
        perf_manuf = self.state.get("count_perfecto_manuf", 0)
        perf_total = perf_qm + perf_flat + perf_manuf
        if "count_perfecto_total" not in self.bd_labels:
            # Build section lazily if not present
            pass
        else:
            self.bd_labels["count_perfecto_total"].set(str(perf_total))
            self.bd_labels["count_perfecto_qm"].set(str(perf_qm))
            self.bd_labels["count_perfecto_flat"].set(str(perf_flat))
            self.bd_labels["count_perfecto_manuf"].set(str(perf_manuf))
            pts = (
                UNIT_POINTS["Perfecto 2V"]["QM Warranty"] * perf_qm
                + UNIT_POINTS["Perfecto 2V"]["Flat Rate"] * perf_flat
                + UNIT_POINTS["Perfecto 2V"]["Manufacture Warranty"] * perf_manuf
            )
            self.bd_title_vars["title_perfecto"].set(f"Perfecto 2V ({pts:.2f} pts):")
            self.bd_title_vars["title_perfecto_qm"].set(f"Perfecto 2V QM Warranty ({UNIT_POINTS['Perfecto 2V']['QM Warranty'] * perf_qm:.2f} pts):")
            self.bd_title_vars["title_perfecto_flat"].set(f"Perfecto 2V Flat Rate ({UNIT_POINTS['Perfecto 2V']['Flat Rate'] * perf_flat:.2f} pts):")
            self.bd_title_vars["title_perfecto_manuf"].set(f"Perfecto 2V Manufacture Warranty ({UNIT_POINTS['Perfecto 2V']['Manufacture Warranty'] * perf_manuf:.2f} pts):")

        # M10
        m10_qm = self.state.get("count_m10_qm", 0)
        m10_flat = self.state.get("count_m10_flat", 0)
        m10_manuf = self.state.get("count_m10_manuf", 0)
        m10_total = m10_qm + m10_flat + m10_manuf
        if "count_m10_total" in self.bd_labels:
            self.bd_labels["count_m10_total"].set(str(m10_total))
            self.bd_labels["count_m10_qm"].set(str(m10_qm))
            self.bd_labels["count_m10_flat"].set(str(m10_flat))
            self.bd_labels["count_m10_manuf"].set(str(m10_manuf))
            pts = (
                UNIT_POINTS["M10"]["QM Warranty"] * m10_qm
                + UNIT_POINTS["M10"]["Flat Rate"] * m10_flat
                + UNIT_POINTS["M10"]["Manufacture Warranty"] * m10_manuf
            )
            self.bd_title_vars["title_m10"].set(f"M10 ({pts:.2f} pts):")
            self.bd_title_vars["title_m10_qm"].set(f"M10 QM Warranty ({UNIT_POINTS['M10']['QM Warranty'] * m10_qm:.2f} pts):")
            self.bd_title_vars["title_m10_flat"].set(f"M10 Flat Rate ({UNIT_POINTS['M10']['Flat Rate'] * m10_flat:.2f} pts):")
            self.bd_title_vars["title_m10_manuf"].set(f"M10 Manufacture Warranty ({UNIT_POINTS['M10']['Manufacture Warranty'] * m10_manuf:.2f} pts):")

        # Rhythm LM5A
        a_qm = self.state.get("count_lm5a_qm", 0)
        a_flat = self.state.get("count_lm5a_flat", 0)
        a_manuf = self.state.get("count_lm5a_manuf", 0)
        a_total = a_qm + a_flat + a_manuf
        if "count_lm5a_total" in self.bd_labels:
            self.bd_labels["count_lm5a_total"].set(str(a_total))
            self.bd_labels["count_lm5a_qm"].set(str(a_qm))
            self.bd_labels["count_lm5a_flat"].set(str(a_flat))
            self.bd_labels["count_lm5a_manuf"].set(str(a_manuf))
            pts = (
                UNIT_POINTS["Rhythm LM5A"]["QM Warranty"] * a_qm
                + UNIT_POINTS["Rhythm LM5A"]["Flat Rate"] * a_flat
                + UNIT_POINTS["Rhythm LM5A"]["Manufacture Warranty"] * a_manuf
            )
            self.bd_title_vars["title_lm5a"].set(f"Rhythm LM5A ({pts:.2f} pts):")
            self.bd_title_vars["title_lm5a_qm"].set(f"Rhythm LM5A QM Warranty ({UNIT_POINTS['Rhythm LM5A']['QM Warranty'] * a_qm:.2f} pts):")
            self.bd_title_vars["title_lm5a_flat"].set(f"Rhythm LM5A Flat Rate ({UNIT_POINTS['Rhythm LM5A']['Flat Rate'] * a_flat:.2f} pts):")
            self.bd_title_vars["title_lm5a_manuf"].set(f"Rhythm LM5A Manufacture Warranty ({UNIT_POINTS['Rhythm LM5A']['Manufacture Warranty'] * a_manuf:.2f} pts):")

        # Rhythm LM5BA
        b_qm = self.state.get("count_lm5ba_qm", 0)
        b_flat = self.state.get("count_lm5ba_flat", 0)
        b_manuf = self.state.get("count_lm5ba_manuf", 0)
        b_total = b_qm + b_flat + b_manuf
        if "count_lm5ba_total" in self.bd_labels:
            self.bd_labels["count_lm5ba_total"].set(str(b_total))
            self.bd_labels["count_lm5ba_qm"].set(str(b_qm))
            self.bd_labels["count_lm5ba_flat"].set(str(b_flat))
            self.bd_labels["count_lm5ba_manuf"].set(str(b_manuf))
            pts = (
                UNIT_POINTS["Rhythm LM5BA"]["QM Warranty"] * b_qm
                + UNIT_POINTS["Rhythm LM5BA"]["Flat Rate"] * b_flat
                + UNIT_POINTS["Rhythm LM5BA"]["Manufacture Warranty"] * b_manuf
            )
            self.bd_title_vars["title_lm5ba"].set(f"Rhythm LM5BA ({pts:.2f} pts):")
            self.bd_title_vars["title_lm5ba_qm"].set(f"Rhythm LM5BA QM Warranty ({UNIT_POINTS['Rhythm LM5BA']['QM Warranty'] * b_qm:.2f} pts):")
            self.bd_title_vars["title_lm5ba_flat"].set(f"Rhythm LM5BA Flat Rate ({UNIT_POINTS['Rhythm LM5BA']['Flat Rate'] * b_flat:.2f} pts):")
            self.bd_title_vars["title_lm5ba_manuf"].set(f"Rhythm LM5BA Manufacture Warranty ({UNIT_POINTS['Rhythm LM5BA']['Manufacture Warranty'] * b_manuf:.2f} pts):")

        # Rhythm LM5CA
        c_qm = self.state.get("count_lm5ca_qm", 0)
        c_flat = self.state.get("count_lm5ca_flat", 0)
        c_manuf = self.state.get("count_lm5ca_manuf", 0)
        c_total = c_qm + c_flat + c_manuf
        if "count_lm5ca_total" in self.bd_labels:
            self.bd_labels["count_lm5ca_total"].set(str(c_total))
            self.bd_labels["count_lm5ca_qm"].set(str(c_qm))
            self.bd_labels["count_lm5ca_flat"].set(str(c_flat))
            self.bd_labels["count_lm5ca_manuf"].set(str(c_manuf))
            pts = (
                UNIT_POINTS["Rhythm LM5CA"]["QM Warranty"] * c_qm
                + UNIT_POINTS["Rhythm LM5CA"]["Flat Rate"] * c_flat
                + UNIT_POINTS["Rhythm LM5CA"]["Manufacture Warranty"] * c_manuf
            )
            self.bd_title_vars["title_lm5ca"].set(f"Rhythm LM5CA ({pts:.2f} pts):")
            self.bd_title_vars["title_lm5ca_qm"].set(f"Rhythm LM5CA QM Warranty ({UNIT_POINTS['Rhythm LM5CA']['QM Warranty'] * c_qm:.2f} pts):")
            self.bd_title_vars["title_lm5ca_flat"].set(f"Rhythm LM5CA Flat Rate ({UNIT_POINTS['Rhythm LM5CA']['Flat Rate'] * c_flat:.2f} pts):")
            self.bd_title_vars["title_lm5ca_manuf"].set(f"Rhythm LM5CA Manufacture Warranty ({UNIT_POINTS['Rhythm LM5CA']['Manufacture Warranty'] * c_manuf:.2f} pts):")

        # POC
        poc_repair = self.state.get("count_poc_repair", 0)
        if "count_poc_total" in self.bd_labels:
            self.bd_labels["count_poc_total"].set(str(poc_repair))
            self.bd_labels["count_poc_repair"].set(str(poc_repair))
            pts = UNIT_POINTS["POC"]["Repair"] * poc_repair
            self.bd_title_vars["title_poc"].set(f"POC ({pts:.2f} pts):")
            self.bd_title_vars["title_poc_repair"].set(f"POC Repair ({pts:.2f} pts):")

    def _build_points_table(self, parent):
        cols = ("Unit", "Warranty", "Pts/unit")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=18)
        for c in cols:
            tree.heading(c, text=c)
        # Set column widths moderately
        tree.column("Unit", width=110, anchor="w")
        tree.column("Warranty", width=180, anchor="w")
        tree.column("Pts/unit", width=90, anchor="center")

        # Data rows describing the points structure
        rows = [
            ("Stratus", "Flat Rate", f"{STRATUS_POINTS:.2f}"),
            ("Stratus", "Manufacture Warranty", f"{STRATUS_POINTS:.2f}"),
            ("Homefill", "Flat Rate", f"{HOMEFILL_POINTS:.2f}"),
            ("Homefill", "Manufacture Warranty", f"{HOMEFILL_POINTS:.2f}"),
            ("525", "QM Warranty", f"{DEV_POINTS['QM Warranty']:.2f}"),
            ("525", "PM", f"{DEV_POINTS['PM']:.2f}"),
            ("525", "Minor Repair", f"{DEV_POINTS['Minor Repair']:.2f}"),
            ("525", "Flat Rate", f"{DEV_POINTS['Flat Rate']:.2f}"),
            ("525", "Manufacture Warranty", f"{DEV_POINTS['Manufacture Warranty']:.2f}"),
            ("1025", "QM Warranty", f"{DEV_POINTS['QM Warranty']:.2f}"),
            ("1025", "PM", f"{DEV_POINTS['PM']:.2f}"),
            ("1025", "Minor Repair", f"{DEV_POINTS['Minor Repair']:.2f}"),
            ("1025", "Flat Rate", f"{DEV_POINTS['Flat Rate']:.2f}"),
            ("1025", "Manufacture Warranty", f"{DEV_POINTS['Manufacture Warranty']:.2f}"),
            ("Perfecto 2V", "QM Warranty", f"{UNIT_POINTS['Perfecto 2V']['QM Warranty']:.2f}"),
            ("Perfecto 2V", "Flat Rate", f"{UNIT_POINTS['Perfecto 2V']['Flat Rate']:.2f}"),
            ("Perfecto 2V", "Manufacture Warranty", f"{UNIT_POINTS['Perfecto 2V']['Manufacture Warranty']:.2f}"),
            ("M10", "QM Warranty", f"{UNIT_POINTS['M10']['QM Warranty']:.2f}"),
            ("M10", "Flat Rate", f"{UNIT_POINTS['M10']['Flat Rate']:.2f}"),
            ("M10", "Manufacture Warranty", f"{UNIT_POINTS['M10']['Manufacture Warranty']:.2f}"),
            ("Rhythm LM5A", "QM Warranty", f"{UNIT_POINTS['Rhythm LM5A']['QM Warranty']:.2f}"),
            ("Rhythm LM5A", "Flat Rate", f"{UNIT_POINTS['Rhythm LM5A']['Flat Rate']:.2f}"),
            ("Rhythm LM5A", "Manufacture Warranty", f"{UNIT_POINTS['Rhythm LM5A']['Manufacture Warranty']:.2f}"),
            ("Rhythm LM5BA", "QM Warranty", f"{UNIT_POINTS['Rhythm LM5BA']['QM Warranty']:.2f}"),
            ("Rhythm LM5BA", "Flat Rate", f"{UNIT_POINTS['Rhythm LM5BA']['Flat Rate']:.2f}"),
            ("Rhythm LM5BA", "Manufacture Warranty", f"{UNIT_POINTS['Rhythm LM5BA']['Manufacture Warranty']:.2f}"),
            ("Rhythm LM5CA", "QM Warranty", f"{UNIT_POINTS['Rhythm LM5CA']['QM Warranty']:.2f}"),
            ("Rhythm LM5CA", "Flat Rate", f"{UNIT_POINTS['Rhythm LM5CA']['Flat Rate']:.2f}"),
            ("Rhythm LM5CA", "Manufacture Warranty", f"{UNIT_POINTS['Rhythm LM5CA']['Manufacture Warranty']:.2f}"),
            ("POC", "Repair", f"{UNIT_POINTS['POC']['Repair']:.2f}"),
        ]
        for r in rows:
            tree.insert("", "end", values=r)
        ttk.Label(parent, text="Points by Unit + Warranty", font=self.bold_font).grid(row=0, column=0, sticky="w", pady=(0,6))
        tree.grid(row=1, column=0, sticky="nsew")
        parent.rowconfigure(1, weight=1)

    def _open_edit_breakdown(self):
        total = self.state.get("output", 0)
        win = tk.Toplevel(self)
        win.title("Edit Breakdown")
        win.transient(self)
        win.grab_set()

        ttk.Label(win, text=f"Total output: {total}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8,4))

        entries = {}
        fields = [
            ("Stratus Flat Rate", "count_stratus_flat"),
            ("Stratus Manufacture Warranty", "count_stratus_manuf"),
            ("Homefill Flat Rate", "count_homefill_flat"),
            ("Homefill Manufacture Warranty", "count_homefill_manuf"),
            ("525 QM Warranty", "count_qm"),
            ("525 PM", "count_pm"),
            ("525 Minor Repair", "count_minor"),
            ("525 Flat Rate", "count_flat"),
            ("525 Manufacture Warranty", "count_manuf"),
            ("1025 QM Warranty", "count_1025_qm"),
            ("1025 PM", "count_1025_pm"),
            ("1025 Minor Repair", "count_1025_minor"),
            ("1025 Flat Rate", "count_1025_flat"),
            ("1025 Manufacture Warranty", "count_1025_manuf"),
            ("Perfecto 2V QM Warranty", "count_perfecto_qm"),
            ("Perfecto 2V Flat Rate", "count_perfecto_flat"),
            ("Perfecto 2V Manufacture Warranty", "count_perfecto_manuf"),
            ("M10 QM Warranty", "count_m10_qm"),
            ("M10 Flat Rate", "count_m10_flat"),
            ("M10 Manufacture Warranty", "count_m10_manuf"),
            ("Rhythm LM5A QM Warranty", "count_lm5a_qm"),
            ("Rhythm LM5A Flat Rate", "count_lm5a_flat"),
            ("Rhythm LM5A Manufacture Warranty", "count_lm5a_manuf"),
            ("Rhythm LM5BA QM Warranty", "count_lm5ba_qm"),
            ("Rhythm LM5BA Flat Rate", "count_lm5ba_flat"),
            ("Rhythm LM5BA Manufacture Warranty", "count_lm5ba_manuf"),
            ("Rhythm LM5CA QM Warranty", "count_lm5ca_qm"),
            ("Rhythm LM5CA Flat Rate", "count_lm5ca_flat"),
            ("Rhythm LM5CA Manufacture Warranty", "count_lm5ca_manuf"),
            ("POC Repair", "count_poc_repair"),
        ]
        for i, (label, key) in enumerate(fields, start=1):
            ttk.Label(win, text=label+":").grid(row=i, column=0, sticky="w")
            var = tk.StringVar(value=str(self.state.get(key, 0)))
            e = ttk.Entry(win, textvariable=var, width=10)
            e.grid(row=i, column=1, sticky="w")
            entries[key] = var

        status = tk.StringVar(value="Enter non-negative integers that sum to total.")
        ttk.Label(win, textvariable=status, foreground="#555").grid(row=len(fields)+1, column=0, columnspan=2, sticky="w", pady=(6,6))

        def on_save():
            try:
                s_flat = int(entries["count_stratus_flat"].get().strip())
                s_manuf = int(entries["count_stratus_manuf"].get().strip())
                h_flat = int(entries["count_homefill_flat"].get().strip())
                h_manuf = int(entries["count_homefill_manuf"].get().strip())
                q = int(entries["count_qm"].get().strip())
                p = int(entries["count_pm"].get().strip())
                m = int(entries["count_minor"].get().strip())
                f = int(entries["count_flat"].get().strip())
                w = int(entries["count_manuf"].get().strip())
                q10 = int(entries["count_1025_qm"].get().strip())
                p10 = int(entries["count_1025_pm"].get().strip())
                m10 = int(entries["count_1025_minor"].get().strip())
                f10 = int(entries["count_1025_flat"].get().strip())
                w10 = int(entries["count_1025_manuf"].get().strip())
                perf_qm = int(entries["count_perfecto_qm"].get().strip())
                perf_flat = int(entries["count_perfecto_flat"].get().strip())
                perf_manuf = int(entries["count_perfecto_manuf"].get().strip())
                mm_qm = int(entries["count_m10_qm"].get().strip())
                mm_flat = int(entries["count_m10_flat"].get().strip())
                mm_manuf = int(entries["count_m10_manuf"].get().strip())
                a_qm = int(entries["count_lm5a_qm"].get().strip())
                a_flat = int(entries["count_lm5a_flat"].get().strip())
                a_manuf = int(entries["count_lm5a_manuf"].get().strip())
                b_qm = int(entries["count_lm5ba_qm"].get().strip())
                b_flat = int(entries["count_lm5ba_flat"].get().strip())
                b_manuf = int(entries["count_lm5ba_manuf"].get().strip())
                c_qm = int(entries["count_lm5ca_qm"].get().strip())
                c_flat = int(entries["count_lm5ca_flat"].get().strip())
                c_manuf = int(entries["count_lm5ca_manuf"].get().strip())
                poc_r = int(entries["count_poc_repair"].get().strip())
            except Exception:
                messagebox.showerror("Invalid", "All fields must be integers.")
                return
            if any(x < 0 for x in (s_flat,s_manuf,h_flat,h_manuf,q,p,m,f,w,q10,p10,m10,f10,w10,
                                    perf_qm,perf_flat,perf_manuf,mm_qm,mm_flat,mm_manuf,
                                    a_qm,a_flat,a_manuf,b_qm,b_flat,b_manuf,c_qm,c_flat,c_manuf,poc_r)):
                messagebox.showerror("Invalid", "Values must be non-negative.")
                return
            s = s_flat + s_manuf
            h = h_flat + h_manuf
            ssum = s + h + q + p + m + f + w + q10 + p10 + m10 + f10 + w10 
            ssum += perf_qm + perf_flat + perf_manuf 
            ssum += mm_qm + mm_flat + mm_manuf 
            ssum += a_qm + a_flat + a_manuf 
            ssum += b_qm + b_flat + b_manuf 
            ssum += c_qm + c_flat + c_manuf 
            ssum += poc_r
            if ssum != total:
                messagebox.showerror("Sum Mismatch", f"Sum of entries ({ssum}) must equal total output ({total}).")
                return
            # Commit
            self.state["count_stratus"] = s
            self.state["count_stratus_flat"] = s_flat
            self.state["count_stratus_manuf"] = s_manuf
            self.state["count_homefill"] = h
            self.state["count_homefill_flat"] = h_flat
            self.state["count_homefill_manuf"] = h_manuf
            self.state["count_qm"] = q
            self.state["count_pm"] = p
            self.state["count_minor"] = m
            self.state["count_flat"] = f
            self.state["count_manuf"] = w
            self.state["count_1025_qm"] = q10
            self.state["count_1025_pm"] = p10
            self.state["count_1025_minor"] = m10
            self.state["count_1025_flat"] = f10
            self.state["count_1025_manuf"] = w10
            self.state["count_perfecto_qm"] = perf_qm
            self.state["count_perfecto_flat"] = perf_flat
            self.state["count_perfecto_manuf"] = perf_manuf
            self.state["count_m10_qm"] = mm_qm
            self.state["count_m10_flat"] = mm_flat
            self.state["count_m10_manuf"] = mm_manuf
            self.state["count_lm5a_qm"] = a_qm
            self.state["count_lm5a_flat"] = a_flat
            self.state["count_lm5a_manuf"] = a_manuf
            self.state["count_lm5ba_qm"] = b_qm
            self.state["count_lm5ba_flat"] = b_flat
            self.state["count_lm5ba_manuf"] = b_manuf
            self.state["count_lm5ca_qm"] = c_qm
            self.state["count_lm5ca_flat"] = c_flat
            self.state["count_lm5ca_manuf"] = c_manuf
            self.state["count_poc_repair"] = poc_r
            self.state["weighted_output"] = (
                STRATUS_POINTS * s
                + HOMEFILL_POINTS * h
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
                + UNIT_POINTS["Perfecto 2V"]["QM Warranty"] * perf_qm
                + UNIT_POINTS["Perfecto 2V"]["Flat Rate"] * perf_flat
                + UNIT_POINTS["Perfecto 2V"]["Manufacture Warranty"] * perf_manuf
                + UNIT_POINTS["M10"]["QM Warranty"] * mm_qm
                + UNIT_POINTS["M10"]["Flat Rate"] * mm_flat
                + UNIT_POINTS["M10"]["Manufacture Warranty"] * mm_manuf
                + UNIT_POINTS["Rhythm LM5A"]["QM Warranty"] * a_qm
                + UNIT_POINTS["Rhythm LM5A"]["Flat Rate"] * a_flat
                + UNIT_POINTS["Rhythm LM5A"]["Manufacture Warranty"] * a_manuf
                + UNIT_POINTS["Rhythm LM5BA"]["QM Warranty"] * b_qm
                + UNIT_POINTS["Rhythm LM5BA"]["Flat Rate"] * b_flat
                + UNIT_POINTS["Rhythm LM5BA"]["Manufacture Warranty"] * b_manuf
                + UNIT_POINTS["Rhythm LM5CA"]["QM Warranty"] * c_qm
                + UNIT_POINTS["Rhythm LM5CA"]["Flat Rate"] * c_flat
                + UNIT_POINTS["Rhythm LM5CA"]["Manufacture Warranty"] * c_manuf
                + UNIT_POINTS["POC"]["Repair"] * poc_r
            )
            save_progress(self.state)
            self._refresh_totals()
            win.destroy()

        btns = ttk.Frame(win)
        btns.grid(row=len(fields)+2, column=0, columnspan=2, pady=(6,8))
        ttk.Button(btns, text="Save", command=on_save).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=win.destroy).grid(row=0, column=1)

    # ---- layout helpers ----
    def _flow_layout(self, parent, frames, columns=2, margin_ratio=0.9):
        try:
            self.update_idletasks()
            max_h = parent.winfo_height()
            if max_h <= 1:
                max_h = int(self.winfo_screenheight() * 0.5)
            for fr in frames:
                fr.grid_forget()
            col = 0
            row_idx = [0] * columns
            col_heights = [0] * columns
            for fr in frames:
                h = fr.winfo_reqheight() + 10  # rough padding
                if col_heights[col] + h > max_h * margin_ratio and col < columns - 1:
                    col += 1
                fr.grid(row=row_idx[col], column=col, sticky="ew", pady=(10, 0))
                row_idx[col] += 1
                col_heights[col] += h
            for c in range(columns):
                parent.columnconfigure(c, weight=1)
        except Exception:
            # Best-effort; ignore layout errors
            pass

    # ---- parsing helpers ----
    def _parse_nonneg(self, var: tk.StringVar) -> int:
        try:
            v = int(var.get().strip())
            return max(0, v)
        except Exception:
            return 0

    def _parse_pos(self, var: tk.StringVar):
        try:
            v = int(var.get().strip())
            if v > 0:
                return v
            return None
        except Exception:
            return None

    def _on_close(self):
        try:
            save_progress(self.state)
        finally:
            self.destroy()

    def _edit_today_output(self):
        win = tk.Toplevel(self)
        win.title("Edit Today's Output")
        win.transient(self)
        win.grab_set()

        current = max(0, self.state.get("output", 0) - self.state.get("start_of_day_output", 0))
        ttk.Label(win, text=f"Current value: {current}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8,4))
        ttk.Label(win, text="New value:").grid(row=1, column=0, sticky="w")
        var = tk.StringVar(value=str(current))
        entry = ttk.Entry(win, textvariable=var, width=10)
        entry.grid(row=1, column=1, sticky="w")

        status = tk.StringVar(value="Enter a non-negative integer.")
        ttk.Label(win, textvariable=status, foreground="#555").grid(row=2, column=0, columnspan=2, sticky="w", pady=(6,6))

        def on_save():
            try:
                val = int(var.get().strip())
            except Exception:
                messagebox.showerror("Invalid", "Value must be an integer.")
                return
            if val < 0:
                messagebox.showerror("Invalid", "Value must be non-negative.")
                return
            total = self.state.get("output", 0)
            # Adjust start_of_day_output so that today's output equals val
            new_start = total - val
            if new_start < 0:
                new_start = 0
            self.state["start_of_day_output"] = new_start
            save_progress(self.state)
            self._refresh_totals()
            win.destroy()

        btns = ttk.Frame(win)
        btns.grid(row=3, column=0, columnspan=2, pady=(6,8))
        ttk.Button(btns, text="Save", command=on_save).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=win.destroy).grid(row=0, column=1)

    def _edit_start_of_day(self):
        win = tk.Toplevel(self)
        win.title("Edit Started Today With")
        win.transient(self)
        win.grab_set()

        current = self.state.get("start_of_day_output", 0)
        ttk.Label(win, text=f"Current value: {current}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(8,4))
        ttk.Label(win, text="New value:").grid(row=1, column=0, sticky="w")
        var = tk.StringVar(value=str(current))
        entry = ttk.Entry(win, textvariable=var, width=10)
        entry.grid(row=1, column=1, sticky="w")

        status = tk.StringVar(value="Enter a non-negative integer. Optional: ≤ current total output.")
        ttk.Label(win, textvariable=status, foreground="#555").grid(row=2, column=0, columnspan=2, sticky="w", pady=(6,6))

        def on_save():
            try:
                val = int(var.get().strip())
            except Exception:
                messagebox.showerror("Invalid", "Value must be an integer.")
                return
            if val < 0:
                messagebox.showerror("Invalid", "Value must be non-negative.")
                return
            # Optional guard: cannot exceed current output (can relax if desired)
            total = self.state.get("output", 0)
            if val > total:
                if not messagebox.askyesno("Confirm", f"Entered value ({val}) exceeds current total output ({total}). Save anyway?"):
                    return
            self.state["start_of_day_output"] = val
            save_progress(self.state)
            self._refresh_totals()
            win.destroy()

        btns = ttk.Frame(win)
        btns.grid(row=3, column=0, columnspan=2, pady=(6,8))
        ttk.Button(btns, text="Save", command=on_save).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancel", command=win.destroy).grid(row=0, column=1)


if __name__ == "__main__":
    app = WeightedOutputApp()
    app.mainloop()
