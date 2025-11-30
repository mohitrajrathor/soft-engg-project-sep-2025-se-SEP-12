"""
Chart generation utility using matplotlib.
Generates deterministic, context-aware chart images for slide decks.
"""

import io
import base64
import logging
from typing import List, Tuple, Optional
import re

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None
    np = None

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generates chart images as base64 Data URIs."""
    
    def __init__(self):
        if not MATPLOTLIB_AVAILABLE:
            logger.warning("Matplotlib not available. Chart generation disabled.")
    
    def generate_synthetic_data(
        self, 
        slide_title: str, 
        chart_type: str, 
        slide_index: int,
        num_points: Optional[int] = None
    ) -> Tuple[List[str], List[float]]:
        """
        Generate contextual synthetic data based on slide title and chart type.
        
        Args:
            slide_title: Title of the slide (used for context)
            chart_type: Type of chart (bar, line, pie, scatter)
            slide_index: Index of slide (for deterministic randomness)
            num_points: Optional number of data points
        
        Returns:
            Tuple of (labels, values)
        """
        # Create deterministic seed from title and index
        seed = abs(hash(slide_title)) % 10000 + slide_index * 100
        np.random.seed(seed)
        
        title_lower = slide_title.lower()
        
        # Detect context from keywords
        is_growth = any(kw in title_lower for kw in ['growth', 'increase', 'rising', 'trend'])
        is_decline = any(kw in title_lower for kw in ['decline', 'decrease', 'falling', 'drop'])
        is_comparison = any(kw in title_lower for kw in ['compare', 'comparison', 'versus', 'vs'])
        is_distribution = any(kw in title_lower for kw in ['distribution', 'breakdown', 'share', 'composition'])
        is_performance = any(kw in title_lower for kw in ['performance', 'metrics', 'kpi', 'score'])
        
        if chart_type == "bar":
            n = num_points or np.random.randint(5, 9)
            labels = self._generate_category_labels(n, title_lower)
            
            if is_comparison:
                # Varied values for comparison
                values = np.random.uniform(40, 95, n).tolist()
            elif is_performance:
                # Performance scores (higher better)
                values = np.random.uniform(60, 98, n).tolist()
            else:
                # General data
                values = np.random.uniform(30, 100, n).tolist()
        
        elif chart_type == "line":
            n = num_points or np.random.randint(6, 11)
            labels = self._generate_time_labels(n)
            
            base = np.random.uniform(40, 60)
            if is_growth:
                # Increasing trend with noise
                values = [base + i * np.random.uniform(3, 8) + np.random.uniform(-5, 5) for i in range(n)]
            elif is_decline:
                # Decreasing trend with noise
                values = [base + 50 - i * np.random.uniform(3, 8) + np.random.uniform(-5, 5) for i in range(n)]
            else:
                # Stable with fluctuation
                values = [base + np.random.uniform(-10, 10) for _ in range(n)]
            
            # Ensure positive values
            values = [max(10, v) for v in values]
        
        elif chart_type == "pie":
            n = num_points or np.random.randint(4, 7)
            labels = self._generate_category_labels(n, title_lower)
            
            if is_distribution:
                # More varied distribution
                values = np.random.dirichlet(np.ones(n)) * 100
            else:
                # Somewhat balanced distribution
                values = np.random.dirichlet(np.ones(n) * 2) * 100
            
            values = values.tolist()
        
        elif chart_type == "scatter":
            n = num_points or np.random.randint(15, 25)
            # For scatter, labels are just point indices
            labels = [str(i) for i in range(n)]
            
            # Generate correlated data (x and y values)
            x_vals = np.random.uniform(10, 100, n)
            
            if 'correlation' in title_lower or 'relationship' in title_lower:
                # Positive correlation with noise
                y_vals = x_vals * np.random.uniform(0.7, 1.2) + np.random.normal(0, 10, n)
            else:
                # Random scatter
                y_vals = np.random.uniform(10, 100, n)
            
            # For scatter, return as list of tuples (x, y)
            values = list(zip(x_vals.tolist(), y_vals.tolist()))
            return labels, values
        
        else:
            # Default bar chart
            n = 6
            labels = [f"Item {i+1}" for i in range(n)]
            values = np.random.uniform(30, 90, n).tolist()
        
        return labels, values
    
    def _generate_category_labels(self, n: int, context: str = "") -> List[str]:
        """Generate contextual category labels."""
        if 'quarter' in context or 'q1' in context:
            return [f"Q{i+1}" for i in range(min(n, 4))]
        elif 'month' in context:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            return months[:n]
        elif 'product' in context or 'item' in context:
            return [f"Product {chr(65+i)}" for i in range(n)]
        elif 'category' in context or 'segment' in context:
            return [f"Category {chr(65+i)}" for i in range(n)]
        elif 'region' in context or 'location' in context:
            regions = ["North", "South", "East", "West", "Central", "Northeast", "Southeast", "Northwest"]
            return regions[:n]
        else:
            return [f"Item {i+1}" for i in range(n)]
    
    def _generate_time_labels(self, n: int) -> List[str]:
        """Generate time-series labels."""
        if n <= 4:
            return [f"Q{i+1}" for i in range(n)]
        elif n <= 12:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            return months[:n]
        else:
            return [f"Week {i+1}" for i in range(n)]
    
    def _truncate_label(self, label: str, max_len: int = 18) -> str:
        """Truncate label if too long."""
        if len(label) > max_len:
            return label[:max_len-2] + ".."
        return label
    
    def generate_chart_image(
        self,
        chart_type: str,
        title: str,
        labels: List[str],
        values: List,
        slide_title: str = "",
        slide_index: int = 0
    ) -> Optional[str]:
        """
        Generate a chart image and return as base64 Data URI.
        
        Args:
            chart_type: Type of chart (bar, line, pie, scatter)
            title: Chart title
            labels: Data labels
            values: Data values
            slide_title: Slide title for context
            slide_index: Slide index
        
        Returns:
            Base64 Data URI string or None if generation fails
        """
        if not MATPLOTLIB_AVAILABLE:
            logger.warning("Matplotlib not available. Cannot generate chart.")
            return None
        
        try:
            # Create figure with appropriate size
            fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
            
            # Truncate labels
            truncated_labels = [self._truncate_label(str(l)) for l in labels]
            
            if chart_type == "bar":
                bars = ax.bar(truncated_labels, values, color='#4F46E5', alpha=0.8, edgecolor='white')
                ax.set_ylabel('Values', fontsize=10)
                # Rotate x-labels if many categories
                if len(labels) > 6:
                    plt.xticks(rotation=30, ha='right', fontsize=9)
                else:
                    plt.xticks(fontsize=9)
                ax.grid(axis='y', alpha=0.3)
            
            elif chart_type == "line":
                ax.plot(truncated_labels, values, marker='o', linewidth=2.5, 
                       color='#4F46E5', markersize=6, markerfacecolor='white', 
                       markeredgewidth=2, markeredgecolor='#4F46E5')
                ax.set_ylabel('Values', fontsize=10)
                if len(labels) > 8:
                    plt.xticks(rotation=30, ha='right', fontsize=9)
                else:
                    plt.xticks(fontsize=9)
                ax.grid(alpha=0.3)
            
            elif chart_type == "pie":
                colors = plt.cm.Set3(np.linspace(0, 1, len(values)))
                wedges, texts, autotexts = ax.pie(
                    values, 
                    labels=truncated_labels, 
                    autopct='%1.1f%%',
                    colors=colors,
                    startangle=90,
                    textprops={'fontsize': 9}
                )
                # Make percentage text more visible
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_weight('bold')
                    autotext.set_fontsize(8)
            
            elif chart_type == "scatter":
                # Values are list of (x, y) tuples
                if values and isinstance(values[0], (list, tuple)):
                    x_vals, y_vals = zip(*values)
                    ax.scatter(x_vals, y_vals, s=50, alpha=0.6, color='#4F46E5', edgecolors='white')
                    ax.set_xlabel('X Values', fontsize=10)
                    ax.set_ylabel('Y Values', fontsize=10)
                    ax.grid(alpha=0.3)
            
            # Set title
            ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
            
            # Tight layout to prevent clipping
            plt.tight_layout()
            
            # Save to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Encode as base64
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            data_uri = f"data:image/png;base64,{image_base64}"
            
            # Clean up
            plt.close(fig)
            buf.close()
            
            logger.info(f"Successfully generated {chart_type} chart: {title}")
            return data_uri
        
        except Exception as e:
            logger.error(f"Failed to generate chart: {e}")
            plt.close('all')  # Clean up any open figures
            return None


# Global instance
chart_generator = ChartGenerator()
