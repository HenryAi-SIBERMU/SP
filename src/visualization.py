"""
Visualization Module

Functions untuk membuat visualisasi (charts, maps, infographics).
"""

import matplotlib.pyplot as plt
import seaborn as sns
import folium
import geopandas as gpd
from typing import Optional, Tuple, List

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_capacity_bar_chart(data: dict, 
                               title: str = "Solar Capacity Potential by Infrastructure Type",
                               xlabel: str = "Infrastructure Type",
                               ylabel: str = "Capacity (MWp)") -> plt.Figure:
    """
    Create bar chart for capacity comparison.
    
    Parameters:
    -----------
    data : dict
        Dictionary of {infrastructure_name: capacity_mwp}
    title, xlabel, ylabel : str
        Chart labels
        
    Returns:
    --------
    plt.Figure : Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    categories = list(data.keys())
    values = list(data.values())
    
    ax.bar(categories, values, color='#FF6B35')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def create_potential_map(gdf: gpd.GeoDataFrame,
                         capacity_column: str = 'capacity_kwp',
                         location_column: str = 'name',
                         center_coords: Tuple[float, float] = (-6.2088, 106.8456),  # Jakarta
                         zoom_start: int = 11) -> folium.Map:
    """
    Create interactive map showing solar potential locations.
    
    Parameters:
    -----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with location geometries and capacity data
    capacity_column : str
        Column name for capacity values
    location_column : str
        Column name for location names
    center_coords : Tuple[float, float]
        Map center coordinates (lat, lon)
    zoom_start : int
        Initial zoom level
        
    Returns:
    --------
    folium.Map : Interactive map object
    """
    # Create base map
    m = folium.Map(location=center_coords, zoom_start=zoom_start, tiles='OpenStreetMap')
    
    # Add markers for each location
    for idx, row in gdf.iterrows():
        capacity = row[capacity_column] if capacity_column in gdf.columns else 0
        name = row[location_column] if location_column in gdf.columns else f"Location {idx}"
        
        # Get coordinates
        if row.geometry.geom_type == 'Point':
            coords = [row.geometry.y, row.geometry.x]
        else:
            coords = [row.geometry.centroid.y, row.geometry.centroid.x]
        
        # Add marker
        folium.CircleMarker(
            location=coords,
            radius=min(capacity / 10, 20),  # Scale by capacity
            popup=f"{name}<br>Capacity: {capacity:.2f} kWp",
            color='#FF6B35',
            fill=True,
            fillColor='#FF6B35',
            fillOpacity=0.6
        ).add_to(m)
    
    return m

def create_financial_comparison(scenarios: dict,
                                 metrics: List[str] = ['npv', 'irr', 'payback_period_years'],
                                 title: str = "Financial Scenarios Comparison") -> plt.Figure:
    """
    Create comparison chart for different financial scenarios.
    
    Parameters:
    -----------
    scenarios : dict
        Dictionary of {scenario_name: {metric: value}}
    metrics : List[str]
        List of metrics to compare
    title : str
        Chart title
        
    Returns:
    --------
    plt.Figure : Matplotlib figure object
    """
    pass  # To be implemented

def save_figure(fig: plt.Figure, filepath: str, dpi: int = 300):
    """
    Save matplotlib figure to file.
    
    Parameters:
    -----------
    fig : plt.Figure
        Figure to save
    filepath : str
        Output file path
    dpi : int
        Resolution (default: 300)
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Figure saved to {filepath}")

# Add more visualization functions here
