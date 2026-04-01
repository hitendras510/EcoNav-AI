import streamlit as st

def render_route_card(route_data: dict, is_best_route: bool = False):
    """
    Renders a premium glassmorphic route card using custom HTML/CSS.
    """
    path = route_data.get("path", [])
    distance = route_data.get("distance", 0)
    traffic = route_data.get("traffic", 0)
    score = route_data.get("score", route_data.get("eco_score", "N/A"))
    fuel = route_data.get("fuel", "N/A")
    
    # Build path string
    path_str = " → ".join(path) if path else "Unknown"
    
    # Traffic level badge
    if traffic <= 3:
        traffic_label = "Low"
        traffic_class = "green"
        traffic_icon = "🟢"
    elif traffic <= 6:
        traffic_label = "Medium"
        traffic_class = "amber"
        traffic_icon = "🟡"
    else:
        traffic_label = "High"
        traffic_class = "red"
        traffic_icon = "🔴"
    
    # Score formatting
    if isinstance(score, (int, float)):
        score_display = f"{score:.2f}"
    else:
        score_display = str(score)

    if is_best_route:
        card_html = f"""
        <div class="best-route-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
                <span style="font-size: 1.4rem;">🏆</span>
                <span style="font-weight: 700; color: #34d399; font-size: 1rem;">EcoNav Recommended Route</span>
            </div>
            <div style="margin-bottom: 14px;">
                <span class="stat-pill green">📏 {distance} km</span>
                <span class="stat-pill {traffic_class}">{traffic_icon} Traffic: {traffic_label}</span>
                <span class="stat-pill blue">⚡ Score: {score_display}</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem;">
                <strong style="color: #f1f5f9;">Path:</strong> {path_str}
            </div>
        </div>
        """
    else:
        card_html = f"""
        <div class="alt-route-card">
            <div style="margin-bottom: 12px;">
                <span class="stat-pill">📏 {distance} km</span>
                <span class="stat-pill {traffic_class}">{traffic_icon} Traffic: {traffic_label}</span>
                <span class="stat-pill">⚡ Score: {score_display}</span>
            </div>
            <div style="color: #64748b; font-size: 0.85rem;">
                <strong style="color: #94a3b8;">Path:</strong> {path_str}
            </div>
        </div>
        """
    
    st.markdown(card_html, unsafe_allow_html=True)
