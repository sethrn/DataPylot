COLORS = [
    "blue", "green", "red", "purple", "orange",
    "brown", "pink", "gray", "olive", "cyan"
]

COLOR_PALETTES = [
    "tab10", "civdis", "viridis", "deep", "muted", "pastel", "bright", "dark", "colorblind",
    "Set1", "Set2", "Set3", "husl", "hls", "Paired", "Accent",
]

STYLES = [
    "whitegrid", "darkgrid", "white", "ticks"
]

MARKERS = [
    "o", ".", "s", "^", "v", "D", "*", "X", "P", "+" 
]

LINE_STYLES = [
    "-", "--", "-.", ":"    
]

UNIVARIATE_CONFIG = {
    "Count Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "X Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Grid Lines", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "Label Rotation", "entry": "entry", "entry_type": "int", "required": False, "default": 0},
        ]
    },
    "Box Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Grid Lines", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
        ]
    },
    "Histogram": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Bins", "entry": "entry", "entry_type": "int", "required": False, "default": 10},
            {"label": "Density", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "KDE Overlay", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None}
        ]
    },
    "KDE Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Shade Area", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True},
            {"label": "Line Style", "entry": "dropdown", "entry_type": LINE_STYLES, "required": False, "default": "-"},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Bandwidth", "entry": "entry", "entry_type": "float", "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""}
        ]
    },
    "Pie Chart": {
        "library": "matplotlib",
        "import": "import matplotlib.pyplot as plt",
        "options": [
            {"label": "Feature", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Explode Largest", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "Display Percentage", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True},
            {"label": "Start Angle", "entry": "entry", "entry_type": "int", "required": False, "default": 90},
            {"label": "Color Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""}
        ]
    }
}

BIVARIATE_CONFIG = {
    "Grouped Count Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "X Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Label Rotation", "entry": "entry", "entry_type": "int", "required": False, "default": 0},
        ]
    },
    "Grouped Box Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
        ]
    },
    "Violin Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "X Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Grid Lines", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
        ]
    },
    "Scatter Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "X Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Point Size", "entry": "entry", "entry_type": "int", "required": False, "default": 40},
            {"label": "Marker Style", "entry": "dropdown", "entry_type": MARKERS, "required": False, "default": "o"},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},

        ]
    },
    "Swarm Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Point Size", "entry": "entry", "entry_type": "int", "required": False, "default": 5},
            {"label": "Marker Style", "entry": "dropdown", "entry_type": MARKERS, "required": False, "default": "o"},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
        ]
    },
    "Line Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "X Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Color", "entry": "dropdown", "entry_type": COLORS, "required": False, "default": None},
            {"label": "Marker Style", "entry": "dropdown", "entry_type": MARKERS, "required": False, "default": "o"},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
        ]
    }
}

MULTIVARIATE_CONFIG = {
    "Grouped Violin Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Y Axis Label", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Grid Lines", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "Show Legend", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True}
        ]
    },

    "Grouped Swarm Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Point Size", "entry": "entry", "entry_type": "int", "required": False, "default": 5},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Marker Style", "entry": "dropdown", "entry_type": MARKERS, "required": False, "default": "o"},
            {"label": "Grid Lines", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "Show Legend", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True}
        ]
    },

    "Grouped Scatter Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Marker Style", "entry": "dropdown", "entry_type": MARKERS, "required": False, "default": "o"},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Grid Lines", "entry": "checkbox", "entry_type": "bool", "required": False, "default": False},
            {"label": "Show Legend", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True}
        ]
    },

    "Grouped Line Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "X Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Y Axis", "entry": "dropdown", "entry_type": "numeric", "required": True, "default": None},
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": True, "default": None},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""},
            {"label": "Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Marker Style", "entry": "dropdown", "entry_type": MARKERS, "required": False, "default": "o"},
            {"label": "Line Style", "entry": "dropdown", "entry_type": LINE_STYLES, "required": False, "default": "-"},
            {"label": "Plot Style", "entry": "dropdown", "entry_type": STYLES, "required": False, "default": None},
            {"label": "Show Legend", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True}
        ]
    },

    "Heatmap": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "Correlation Method", "entry": "dropdown", "entry_type": ["pearson", "spearman", "kendall"], "required": True, "default": "pearson"},
            {"label": "Annotate Values", "entry": "checkbox", "entry_type": "bool", "required": False, "default": True},
            {"label": "Color Map", "entry": "dropdown", "entry_type": ["coolwarm", "viridis", "magma", "cividis", "YlGnBu", "inferno"], "required": False, "default": "coolwarm"},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""}
        ]
    },

    "Pair Plot": {
        "library": "seaborn",
        "import": "import seaborn as sns",
        "options": [
            {"label": "Hue", "entry": "dropdown", "entry_type": "any", "required": False, "default": None},
            {"label": "Palette", "entry": "dropdown", "entry_type": COLOR_PALETTES, "required": False, "default": None},
            {"label": "Kind", "entry": "dropdown", "entry_type": ["scatter", "kde"], "required": False, "default": "scatter"},
            {"label": "Plot Title", "entry": "text", "entry_type": "str", "required": False, "default": ""}
        ]
    }
}
