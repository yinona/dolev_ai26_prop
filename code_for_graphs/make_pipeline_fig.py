import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

fig, ax = plt.subplots(figsize=(12.8, 4.9))
ax.set_xlim(0, 13)
ax.set_ylim(-4.1, 2.3)
ax.axis("off")

# Rounded, light style (similar to earlier versions)
COL = {
    "data": "#dbeafe",
    "cnn": "#e9d5ff",
    "dxa": "#fef3c7",
    "loss": "#fee2e2",
    "out": "#dcfce7",
    "edge": "#64748b",
    "arr": "#334155",
    "warn": "#b91c1c",
    "transfer": "#7c3aed",
}

BH = 0.86
GAP = 0.42
PAD = 0.06


def box(x, y, w, title, subtitle, color):
    patch = FancyBboxPatch(
        (x, y - BH / 2),
        w,
        BH,
        boxstyle="round,pad=0.06",
        linewidth=1.0,
        edgecolor=COL["edge"],
        facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + 0.12, title, ha="center", va="center", fontsize=8.8, fontweight="bold")
    ax.text(x + w / 2, y - 0.15, subtitle, ha="center", va="center", fontsize=7, color="#334155")
    return x + w


def harrow(x1, y, x2, color=COL["arr"], lw=1.2, ls="-"):
    ax.annotate(
        "",
        xy=(x2, y),
        xytext=(x1, y),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls),
    )


def varrow(x, y1, y2, color=COL["arr"], lw=1.2, ls="-"):
    ax.annotate(
        "",
        xy=(x, y2),
        xytext=(x, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls),
    )


# ---------------- TRAINING ----------------
y_top = 0.95
y_bottom = -1.10
ax.text(0.35, 1.9, "TRAINING (grain interior, DXA available)", fontsize=10, fontweight="bold", color="#1e293b")

w_md = 2.3
w_feat = 2.6
w_cnn = 2.0
w_out = 2.2

x = 0.5
x_md_l = x
x_md_r = box(x, y_top, w_md, "MD simulation", "LAMMPS, FCC Cu", COL["data"])
x = x_md_r + GAP
x_feat_l = x
x_feat_r = box(x, y_top, w_feat, "Feature extraction", "stress, velocity, energy", COL["data"])
x = x_feat_r + GAP
x_cnn_l = x
x_cnn_r = box(x, y_top, w_cnn, "CNN", "predict dislocations", COL["cnn"])
x = x_cnn_r + GAP
x_out_top_l = x
x_out_top_r = box(x, y_top, w_out, "Output", "CNN prediction", COL["out"])

# Lower training blocks: DXA under MD, Loss under CNN
dxa_w = w_md
loss_w = w_cnn
dxa_l = x_md_l + (2.3 - dxa_w) / 2
loss_l = x_cnn_l + (2.0 - loss_w) / 2
box(dxa_l, y_bottom, dxa_w, "DXA labels", "ground truth", COL["dxa"])
box(loss_l, y_bottom, loss_w, "Loss", "CNN vs DXA", COL["loss"])

# Top-row arrows
harrow(x_md_r + PAD, y_top, x_feat_l - PAD)
harrow(x_feat_r + PAD, y_top, x_cnn_l - PAD)
harrow(x_cnn_r + PAD, y_top, x_out_top_l - PAD)

# Vertical arrows to lower blocks
varrow(x_md_l + 2.3 / 2, y_top - BH / 2 - 0.03, y_bottom + BH / 2 + 0.03)

# Output feeds Loss, and DXA also feeds Loss
ax.annotate(
    "",
    xy=(loss_l + loss_w * 1.05, y_bottom + 0.02),
    xytext=(x_out_top_l + w_out / 2, y_top - BH / 2 - 0.12),
    arrowprops=dict(arrowstyle="-|>", color=COL["arr"], lw=1.2, connectionstyle="angle3,angleA=-90,angleB=180"),
)
harrow(dxa_l + dxa_w + PAD, y_bottom, loss_l - PAD)

# Backprop: Loss -> CNN (centered on block midline)
loss_center_x = loss_l + loss_w / 2
varrow(loss_center_x, y_bottom + BH / 2 + 0.10, y_top - BH / 2 - 0.10, color=COL["warn"], lw=1.1, ls="dashed")
ax.text(loss_center_x + 0.22, (y_top + y_bottom) / 2, "back\npropagation", fontsize=7, color=COL["warn"], rotation=90, va="center", ha="center")

# ---------------- APPLICATION ----------------
y_a = -3.00
ax.text(0.35, -2.10, "APPLICATION (grain boundary, DXA fails)", fontsize=10, fontweight="bold", color="#1e293b")

x = 0.5
x2_md_l = x
x2_md_r = box(x, y_a, w_md, "MD simulation", "bicrystal / high-angle GB", COL["data"])
x = x2_md_r + GAP
x2_feat_l = x
x2_feat_r = box(x, y_a, w_feat, "Feature extraction", "same features", COL["data"])
x = x2_feat_r + GAP
x2_cnn_l = x
x2_cnn_r = box(x, y_a, w_cnn, "Trained CNN", "predict GB activity", COL["cnn"])
x = x2_cnn_r + GAP
x2_out_l = x
x2_out_r = box(x, y_a, w_out, "Output", "GB defect/activity map", COL["out"])

# Arrow between every application block
harrow(x2_md_r + PAD, y_a, x2_feat_l - PAD)
harrow(x2_feat_r + PAD, y_a, x2_cnn_l - PAD)
harrow(x2_cnn_r + PAD, y_a, x2_out_l - PAD)

plt.tight_layout(pad=0.15)
repo_root = Path(__file__).resolve().parents[1]
output_dir = repo_root / "graphs"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "pipeline.pdf"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Saved {output_path}")
