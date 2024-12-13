# styles.py

STYLES = {
    'modern': {
        'background': '#1a1a1a',
        'text': '#ffffff',
        'accent': '#00a8e8',
        'gradient': ['#00a8e8', '#00ff99'],
        'charts': ['#00a8e8', '#00ff99', '#ff0066', '#ffcc00'],
        'font': {
            'family': 'Arial, sans-serif',
            'size': {
                'title': 24,
                'header': 20,
                'body': 16,
                'caption': 14
            }
        },
        'spacing': {
            'padding': 20,
            'margin': 10
        }
    },
    'corporate': {
        'background': '#2c3e50',
        'text': '#ecf0f1',
        'accent': '#3498db',
        'gradient': ['#3498db', '#2ecc71'],
        'charts': ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f'],
        'font': {
            'family': 'Helvetica, Arial, sans-serif',
            'size': {
                'title': 22,
                'header': 18,
                'body': 14,
                'caption': 12
            }
        },
        'spacing': {
            'padding': 16,
            'margin': 8
        }
    },
    'dark': {
        'background': '#000000',
        'text': '#ffffff',
        'accent': '#ff0066',
        'gradient': ['#ff0066', '#00ff99'],
        'charts': ['#ff0066', '#00ff99', '#00ccff', '#ffcc00'],
        'font': {
            'family': 'Roboto, sans-serif',
            'size': {
                'title': 26,
                'header': 22,
                'body': 16,
                'caption': 14
            }
        },
        'spacing': {
            'padding': 24,
            'margin': 12
        }
    },
    'light': {
        'background': '#ffffff',
        'text': '#2c3e50',
        'accent': '#3498db',
        'gradient': ['#3498db', '#2ecc71'],
        'charts': ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f'],
        'font': {
            'family': 'Open Sans, sans-serif',
            'size': {
                'title': 24,
                'header': 20,
                'body': 16,
                'caption': 14
            }
        },
        'spacing': {
            'padding': 20,
            'margin': 10
        }
    }
}

# Chart-specific styles
CHART_STYLES = {
    'line': {
        'line_width': 2,
        'marker_size': 6,
        'opacity': 0.8
    },
    'bar': {
        'opacity': 0.7,
        'bar_width': 0.8
    },
    'scatter': {
        'marker_size': 8,
        'opacity': 0.7
    },
    'pie': {
        'opacity': 0.8,
        'hole': 0
    },
    'area': {
        'opacity': 0.6,
        'line_width': 1
    }
}

# Animation styles
ANIMATION_STYLES = {
    'transition_duration': 500,
    'frame_duration': 100,
    'easing': 'cubic-in-out'
}

# Custom color palettes
COLOR_PALETTES = {
    'modern': [
        '#00a8e8', '#00ff99', '#ff0066', '#ffcc00',
        '#00ccff', '#33ff99', '#ff3366', '#ffdd33'
    ],
    'corporate': [
        '#3498db', '#2ecc71', '#e74c3c', '#f1c40f',
        '#9b59b6', '#1abc9c', '#e67e22', '#34495e'
    ],
    'dark': [
        '#ff0066', '#00ff99', '#00ccff', '#ffcc00',
        '#ff3366', '#33ff99', '#33ccff', '#ffdd33'
    ],
    'light': [
        '#3498db', '#2ecc71', '#e74c3c', '#f1c40f',
        '#9b59b6', '#1abc9c', '#e67e22', '#34495e'
    ]
}

def get_style(style_name: str) -> dict:
    """Get complete style configuration"""
    if style_name not in STYLES:
        raise ValueError(f"Unknown style: {style_name}")
    
    return {
        **STYLES[style_name],
        'chart_styles': CHART_STYLES,
        'animation_styles': ANIMATION_STYLES,
        'color_palette': COLOR_PALETTES[style_name]
    }

def apply_style_to_figure(fig, style_name: str):
    """Apply style to a plotly figure"""
    style = get_style(style_name)
    
    fig.update_layout(
        template='plotly_dark' if style['background'] == '#000000' else 'plotly_white',
        paper_bgcolor=style['background'],
        plot_bgcolor=style['background'],
        font=dict(
            family=style['font']['family'],
            size=style['font']['size']['body'],
            color=style['text']
        ),
        title_font=dict(
            family=style['font']['family'],
            size=style['font']['size']['title'],
            color=style['text']
        ),
        margin=dict(
            l=style['spacing']['margin'],
            r=style['spacing']['margin'],
            t=style['spacing']['margin'],
            b=style['spacing']['margin'],
            pad=style['spacing']['padding']
        )
    )
    
    return fig