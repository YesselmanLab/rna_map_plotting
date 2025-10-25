import matplotlib.lines as mlines
import matplotlib.pyplot as plt

def add_legend(ax, labels, loc="upper right"):
    handles = []
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for label, color in zip(labels, colors):
        patch = mlines.Line2D([], [], color=color, lw=0.75, label=label)
        handles.append(patch)
    arial_font = {"family": "Arial", "size": 6}

    legend = ax.legend(
        handles=handles,
        frameon=False,
        loc=loc,
        handlelength=1.0,
        handleheight=0.5,
        handletextpad=0.30,
        borderaxespad=-0.10,  # as close as possible to axes
        prop=arial_font,
        labelspacing=0.15,  # reduce space between lines in legend
    )

    return legend