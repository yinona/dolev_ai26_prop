"""Generate the training/application pipeline figure for the proposal.

Flow (matches §Approach in main.tex):
  TRAINING:  MD sim → Feature extraction → CNN → Output (prediction)
             MD sim → DXA (ground truth) → Loss ← Output
             Loss → backprop → CNN
  APPLICATION:  MD sim → Feature extraction → Trained CNN → Output (GB activity map)
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# --- figure sized to \textwidth → no scaling, matplotlib pt = document pt ---
fig, ax = plt.subplots(figsize=(6.5, 1.82))
ax.set_xlim(0, 6.5)
ax.set_ylim(0, 1.82)
ax.axis("off")

# --- colours ---
C = dict(
    data="#dbeafe", cnn="#e9d5ff", dxa="#fef3c7",
    loss="#fee2e2", out="#dcfce7", edge="#64748b",
    arr="#334155", bp="#b91c1c",
)

# --- dimensions ---
BH = 0.28          # main-row box height
BH_SM = 0.22       # feedback-row box height
GAP = 0.14         # horizontal gap between boxes
PAD = 0.03         # arrow clearance from box edge
W = dict(md=1.20, feat=1.35, cnn=1.08, out=1.22)   # box widths
X0 = 0.32          # left margin


def box(x, y, w, h, title, sub, colour, tfs=9, sfs=7):
    """Rounded box with centred title and subtitle (no bold)."""
    ax.add_patch(FancyBboxPatch(
        (x, y - h / 2), w, h,
        boxstyle="round,pad=0.02", lw=0.6,
        edgecolor=C["edge"], facecolor=colour))
    if sub:
        ax.text(x + w / 2, y + h * 0.14, title,
                ha="center", va="center", fontsize=tfs)
        ax.text(x + w / 2, y - h * 0.23, sub,
                ha="center", va="center", fontsize=sfs, color="#475569")
    else:
        ax.text(x + w / 2, y, title,
                ha="center", va="center", fontsize=tfs)
    return x + w


def harr(x1, y, x2, **kw):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=kw.get("c", C["arr"]),
                                lw=kw.get("lw", 0.7),
                                linestyle=kw.get("ls", "-")))


def varr(x, y1, y2, **kw):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=kw.get("c", C["arr"]),
                                lw=kw.get("lw", 0.7),
                                linestyle=kw.get("ls", "-")))


# ================================================================
#  TRAINING
# ================================================================
y_hdr = 1.70          # header text
y_t   = 1.38          # training-row box centres
y_fb  = 0.96          # feedback-row box centres

ax.text(0.06, y_hdr, "TRAINING  (grain interior, DXA available)",
        fontsize=9.5, color="#1e293b")

# main training row
p = {}  # stores left/right x of every box
x = X0
for key, w, title, sub, col in [
    ("md",   W["md"],   "MD simulation",      "LAMMPS, FCC Cu",          C["data"]),
    ("feat", W["feat"], "Feature extraction",  "stress, velocity, energy", C["data"]),
    ("cnn",  W["cnn"],  "CNN",                 "predict dislocations",     C["cnn"]),
    ("out",  W["out"],  "Output",              "CNN prediction",           C["out"]),
]:
    p[key + "L"] = x
    p[key + "R"] = box(x, y_t, w, BH, title, sub, col)
    x = p[key + "R"] + GAP

for a, b in [("md", "feat"), ("feat", "cnn"), ("cnn", "out")]:
    harr(p[a + "R"] + PAD, y_t, p[b + "L"] - PAD)

# feedback row: DXA (below MD) and Loss (below CNN)
dxa_w, loss_w = 1.02, 0.92
dxa_l = p["mdL"] + (W["md"] - dxa_w) / 2
loss_l = p["cnnL"] + (W["cnn"] - loss_w) / 2

box(dxa_l, y_fb, dxa_w, BH_SM, "DXA labels", "ground truth", C["dxa"], 8, 6.5)
box(loss_l, y_fb, loss_w, BH_SM, "Loss", "CNN vs DXA",      C["loss"], 8, 6.5)

# MD → DXA (down)
varr(p["mdL"] + W["md"] / 2, y_t - BH / 2 - 0.02, y_fb + BH_SM / 2 + 0.02)

# DXA → Loss (right)
harr(dxa_l + dxa_w + PAD, y_fb, loss_l - PAD)

# Output → Loss (right-angle path: down from Output, then left to Loss)
ax.annotate(
    "", xy=(loss_l + loss_w + 0.01, y_fb),
    xytext=(p["outL"] + W["out"] / 2, y_t - BH / 2 - 0.03),
    arrowprops=dict(arrowstyle="-|>", color=C["arr"], lw=0.7,
                    connectionstyle="angle,angleA=-90,angleB=180"))

# Loss → CNN (backprop, dashed upward)
bp_x = loss_l + loss_w / 2
varr(bp_x, y_fb + BH_SM / 2 + 0.02, y_t - BH / 2 - 0.02,
     c=C["bp"], lw=0.8)

# ================================================================
#  APPLICATION
# ================================================================
y_hdr2 = 0.56
y_a    = 0.24

ax.text(0.06, y_hdr2, "APPLICATION  (grain boundary, DXA fails)",
        fontsize=9.5, color="#1e293b")

x = X0
for key, w, title, sub, col in [
    ("a_md",   W["md"],   "MD simulation",      "bicrystal / high-angle GB", C["data"]),
    ("a_feat", W["feat"], "Feature extraction",  "same features",             C["data"]),
    ("a_cnn",  W["cnn"],  "Trained CNN",         "predict GB activity",       C["cnn"]),
    ("a_out",  W["out"],  "Output",              "GB activity map",           C["out"]),
]:
    p[key + "L"] = x
    p[key + "R"] = box(x, y_a, w, BH, title, sub, col)
    x = p[key + "R"] + GAP

for a, b in [("a_md", "a_feat"), ("a_feat", "a_cnn"), ("a_cnn", "a_out")]:
    harr(p[a + "R"] + PAD, y_a, p[b + "L"] - PAD)

# ================================================================
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
out_path = Path(__file__).resolve().parents[1] / "graphs" / "pipeline.pdf"
out_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0.03)
print(f"Saved {out_path}")
