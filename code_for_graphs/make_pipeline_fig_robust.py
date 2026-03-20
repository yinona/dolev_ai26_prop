import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

fig, ax = plt.subplots(figsize=(14, 5.5))
ax.set_xlim(-0.5, 15.5)
ax.set_ylim(-5.5, 1.5)
ax.set_aspect("equal")
ax.axis("off")

# ---------- colours ----------
c_sim   = "#dbe9f6"
c_lab   = "#fde8d0"
c_feat  = "#d9f0d3"
c_model = "#e4d6f0"
c_out   = "#f8d7da"
c_gray  = "#b0b0b0"
c_edge  = "#888888"
c_transfer = "#7b4ea3"

# ---------- helper: rounded box ----------
def rbox(ax, x, y, w, h, color, text, fontsize=8, bold_first_line=False, edge=c_edge):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.08", linewidth=0.8,
                         edgecolor=edge, facecolor=color)
    ax.add_patch(box)
    lines = text.split("\n")
    if len(lines) == 1:
        ax.text(x, y, text, ha="center", va="center", fontsize=fontsize)
    else:
        top_y = y + 0.15
        ax.text(x, top_y, lines[0], ha="center", va="center",
                fontsize=fontsize, fontweight="bold" if bold_first_line else "normal")
        ax.text(x, top_y - 0.38, lines[1], ha="center", va="center",
                fontsize=6.5, color="#555555", style="italic")

# ---------- helper: arrow ----------
def arrow(ax, x1, y1, x2, y2, color=c_gray, lw=1.0, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))

# ---------- column x positions ----------
xs = 0.8    # simulation
xl = 3.8    # labels
xf = 7.6    # features
xm = 11.0   # model
xo = 14.0   # output

# ---------- row y positions ----------
y1 = 0.0
y2 = -1.3
y3 = -2.6
y4 = -3.9

bw = 2.2   # box width
bh = 0.85  # box height

# ========== COLUMN HEADERS ==========
for x, label in [(xs, "SIMULATION"), (xl, "SUPERVISION"),
                  (xf, "FEATURES"), (xm, "MODEL"), (xo, "OUTPUT")]:
    ax.text(x, 1.1, label, ha="center", va="center",
            fontsize=8, fontweight="bold", color="#777777", family="sans-serif")

# ========== SIMULATION COLUMN ==========
sim_data = [
    (y1, "Bulk single crystal\nLAMMPS, FCC Cu"),
    (y2, "Bicrystal\nlow-angle GB"),
    (y3, "Bicrystal\nhigh-angle GB"),
    (y4, "Nanocrystalline\ntransfer test"),
]
for y, txt in sim_data:
    rbox(ax, xs, y, bw, bh, c_sim, txt, bold_first_line=True)

# ========== SUPERVISION COLUMN ==========
lab_data = [
    (y1, "DXA\nstrong labels", c_lab),
    (y2, "ILDA\ninterface labels", c_lab),
    (y3, "Outcome-based\nweak supervision", c_lab),
    (y4, "Unlabelled\nevaluation only", "#f0f0f0"),
]
for y, txt, col in lab_data:
    rbox(ax, xl, y, 2.3, bh, col, txt, bold_first_line=True)

# ========== Simulation -> Labels arrows ==========
for y in [y1, y2, y3, y4]:
    arrow(ax, xs + bw/2 + 0.05, y, xl - 2.3/2 - 0.05, y)

# ========== FEATURES COLUMN (one tall box) ==========
feat_h = abs(y1 - y3) + bh
feat_cy = (y1 + y3) / 2
feat_box = FancyBboxPatch((xf - 2.6/2, feat_cy - feat_h/2), 2.6, feat_h,
                           boxstyle="round,pad=0.1", linewidth=0.8,
                           edgecolor=c_edge, facecolor=c_feat)
ax.add_patch(feat_box)
ax.text(xf, feat_cy + 0.85, "Per-atom descriptors", ha="center", va="center",
        fontsize=8, fontweight="bold")
ax.text(xf, feat_cy + 0.4, "Static", ha="center", va="center",
        fontsize=7.5, fontweight="bold", color="#444444")
ax.text(xf, feat_cy + 0.05, "stress, energy, CNA/PTM,\ngrain orientation, dist. to GB",
        ha="center", va="center", fontsize=6.5, color="#555555", linespacing=1.3)
ax.text(xf, feat_cy - 0.55, "Dynamic", ha="center", va="center",
        fontsize=7.5, fontweight="bold", color="#444444")
ax.text(xf, feat_cy - 0.9, r"$D^2_{\min}$, disp. correlations," + "\nneighbour turnover",
        ha="center", va="center", fontsize=6.5, color="#555555", linespacing=1.3)

# ========== Labels -> Features arrows ==========
for y in [y1, y2, y3]:
    arrow(ax, xl + 2.3/2 + 0.05, y, xf - 2.6/2 - 0.05, y)

# ========== MODEL COLUMN ==========
ym1 = (y1 + y2) / 2
ym2 = (y2 + y3) / 2
rbox(ax, xm, ym1, 2.4, bh, c_model, "CNN\nstress-field slices", bold_first_line=True)
rbox(ax, xm, ym2, 2.4, bh, c_model, "GNN / point cloud\natomic neighbourhoods", bold_first_line=True)

# ========== Features -> Models arrows ==========
arrow(ax, xf + 2.6/2 + 0.05, ym1, xm - 2.4/2 - 0.05, ym1)
arrow(ax, xf + 2.6/2 + 0.05, ym2, xm - 2.4/2 - 0.05, ym2)

# ========== OUTPUT COLUMN ==========
rbox(ax, xo, ym1, 2.4, bh, c_out, "Atom-wise class\ndisloc. / GB / defect", bold_first_line=True)
rbox(ax, xo, ym2, 2.4, bh, c_out, "Event detection\nabsorb / transmit / emit", bold_first_line=True)

# ========== Models -> Outputs arrows ==========
arrow(ax, xm + 2.4/2 + 0.05, ym1, xo - 2.4/2 - 0.05, ym1)
arrow(ax, xm + 2.4/2 + 0.05, ym2, xo - 2.4/2 - 0.05, ym2)

# ========== TRANSFER BRACKET ==========
bx = xl + 2.3/2 + 0.22
by_top = y1 + bh/2 + 0.12
by_bot = y3 - bh/2 - 0.12
ax.plot([bx, bx+0.15, bx+0.15, bx],
        [by_top, by_top, by_bot, by_bot],
        color=c_transfer, linewidth=1.5, linestyle="--", clip_on=False)
ax.text(bx + 0.3, (by_top + by_bot)/2,
        "transfer learned\nrepresentations\n(strong → weak)",
        fontsize=6.5, color=c_transfer, va="center", ha="left",
        style="italic", linespacing=1.4)

# ========== DECREASING SUPERVISION arrow on left ==========
ax.annotate("", xy=(xs - bw/2 - 0.35, y4 - bh/2),
            xytext=(xs - bw/2 - 0.35, y1 + bh/2),
            arrowprops=dict(arrowstyle="-|>", color="#aaaaaa", lw=1.2))
ax.text(xs - bw/2 - 0.55, (y1 + y4)/2, "decreasing\nsupervision",
        ha="center", va="center", fontsize=6.5, color="#999999",
        rotation=90, family="sans-serif", linespacing=1.3)

plt.tight_layout(pad=0.3)
repo_root = Path(__file__).resolve().parents[1]
output_dir = repo_root / "graphs"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "pipeline_robust.pdf"
plt.savefig(output_path, bbox_inches="tight", dpi=300)
print(f"Saved {output_path}")
