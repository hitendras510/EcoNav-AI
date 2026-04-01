import streamlit as st

def render_ai_engine():
    """
    Renders the AI Engine Control Panel tab with model status,
    manual training trigger, and a live training log area.
    """
    st.markdown('<div class="section-header">🤖 AI Engine Control Panel</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color: #94a3b8; margin-bottom: 24px;">'
        'Monitor and control the EcoNav AI model. Trigger retraining cycles on demand '
        'and view real-time model performance metrics.'
        '</p>',
        unsafe_allow_html=True,
    )

    # ---- Model Status ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">🧠</div>
                <div style="color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Model Status</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #34d399; margin-top: 4px;">
                    <span class="status-dot online"></span> Active
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">⚡</div>
                <div style="color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Architecture</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #f1f5f9; margin-top: 4px;">
                    PyTorch MLP
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">🔄</div>
                <div style="color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Hot-Reload</div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #34d399; margin-top: 4px;">
                    Enabled
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Model Architecture Diagram ----
    st.markdown('<div class="section-header">🏗️ Model Architecture</div>', unsafe_allow_html=True)
    
    arch_dot = """
    digraph Model {
        rankdir=LR;
        bgcolor="transparent";
        node [shape=record, style="rounded,filled", fontname="Inter", fontsize=10,
              fillcolor="#1e293b", fontcolor="#e2e8f0", color="#334155", penwidth=1.5];
        edge [color="#475569", penwidth=1.2, arrowsize=0.8];

        input [label="{Input Layer|distance, traffic, fuel}", fillcolor="#064e3b", color="#10b981", fontcolor="#34d399"];
        h1 [label="{Hidden Layer 1|16 neurons + ReLU}"];
        h2 [label="{Hidden Layer 2|8 neurons + ReLU}"];
        output [label="{Output|Eco Score}", fillcolor="#1e1b4b", color="#6366f1", fontcolor="#a5b4fc"];

        input -> h1 -> h2 -> output;
    }
    """
    st.graphviz_chart(arch_dot, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Manual Training Trigger ----
    st.markdown('<div class="section-header">🎯 Manual Training</div>', unsafe_allow_html=True)

    # Initialize training log
    if "training_log" not in st.session_state:
        st.session_state.training_log = []

    if st.button("🚀 Trigger Model Retraining", key="btn_train", use_container_width=True):
        with st.spinner("Running ML training pipeline & hot-reloading weights…"):
            from services.api_client import trigger_training
            result = trigger_training()

            if result.get("status") == "success":
                st.session_state.training_log.append("✅ " + result.get("message", "Training completed."))
                st.success(result["message"])
            else:
                st.session_state.training_log.append("❌ " + result.get("message", "Unknown error."))
                st.error(result.get("message", "Training failed."))

    # Show training log
    if st.session_state.training_log:
        st.markdown('<div class="section-header">📋 Training Log</div>', unsafe_allow_html=True)
        log_html = "<div class='training-log'>"
        for entry in st.session_state.training_log:
            log_html += f"<div>{entry}</div>"
        log_html += "</div>"
        st.markdown(log_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Feature Info ----
    st.markdown('<div class="section-header">📊 Feature Pipeline</div>', unsafe_allow_html=True)

    features_html = """
    <div class="glass-card">
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);">
                    <th style="text-align: left; padding: 10px; color: #94a3b8; font-weight: 600; font-size: 0.8rem; text-transform: uppercase;">Feature</th>
                    <th style="text-align: left; padding: 10px; color: #94a3b8; font-weight: 600; font-size: 0.8rem; text-transform: uppercase;">Type</th>
                    <th style="text-align: left; padding: 10px; color: #94a3b8; font-weight: 600; font-size: 0.8rem; text-transform: uppercase;">Description</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 10px; color: #34d399; font-weight: 500;">distance</td>
                    <td style="padding: 10px; color: #94a3b8;">float</td>
                    <td style="padding: 10px; color: #94a3b8;">Route length in kilometers</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <td style="padding: 10px; color: #3b82f6; font-weight: 500;">traffic</td>
                    <td style="padding: 10px; color: #94a3b8;">int</td>
                    <td style="padding: 10px; color: #94a3b8;">Traffic congestion level (1-10)</td>
                </tr>
                <tr>
                    <td style="padding: 10px; color: #f59e0b; font-weight: 500;">fuel</td>
                    <td style="padding: 10px; color: #94a3b8;">float</td>
                    <td style="padding: 10px; color: #94a3b8;">Estimated fuel consumption</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    st.markdown(features_html, unsafe_allow_html=True)
