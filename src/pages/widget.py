import streamlit as st
import pandas as pd

def main():
    st.title("Zoho Widget Examples")
    # --- Customer Overview (Summary Cards) ---
    st.markdown("## 💼 Customer Overview")
    cols = st.columns(4)
    with cols[0]:
        st.metric(label="Account Value", value="$45,230", delta=None, help="Annual Contract Value")
        st.caption("Annual Contract Value")
    with cols[1]:
        st.metric(label="Risk Score", value="Low")
        st.caption("Based on payment history")
    with cols[2]:
        st.metric(label="Support Tier", value="Premium")
        st.caption("Response: 2 hours")
    with cols[3]:
        st.metric(label="Last Contact", value="3 days ago")
        st.caption("Email - Product inquiry")

    st.markdown("---")

    # --- Recent Support History (Data Table) ---
    st.markdown("## 🎫 Recent Support History")
    support_data = [
        ["2025-09-15", "Technical Issue", "High", "Resolved", "4.2 hours"],
        ["2025-09-10", "Billing Question", "Medium", "Resolved", "1.8 hours"],
        ["2025-09-05", "Feature Request", "Low", "In Progress", "-"]
    ]
    support_status = {
        "Resolved": ("active", "#d4edda", "#155724"),
        "In Progress": ("warning", "#fff3cd", "#856404")
    }
    df = pd.DataFrame(support_data, columns=["Date", "Issue Type", "Priority", "Status", "Resolution Time"])
    def status_badge(status):
        style, bg, fg = support_status.get(status, ("inactive", "#f8d7da", "#721c24"))
        return f'<span style="background-color:{bg};color:{fg};padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600;text-transform:uppercase;">{status}</span>'
    df["Status"] = df["Status"].apply(status_badge)
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown("---")

    # --- Account Information (Key-Value Grid) ---
    st.markdown("## 📊 Account Information")
    info = [
        ("Account Manager", "Sarah Johnson"),
        ("Implementation Date", "March 15, 2023"),
        ("License Count", "125 users"),
        ("Contract End Date", "March 15, 2026"),
        ("Payment Method", "Auto-pay (Credit Card)"),
        ("Renewal Probability", "95%")
    ]
    cols = st.columns(3)
    for i, (label, value) in enumerate(info):
        with cols[i % 3]:
            st.caption(label)
            st.write(f"**{value}**")

    st.markdown("---")

    # --- Recent Activity Timeline ---
    st.markdown("## ⏰ Recent Activity Timeline")
    timeline = [
        ("September 16, 2025", "Support ticket created", "Customer reported login issues affecting 12 users"),
        ("September 14, 2025", "Payment processed", "Monthly subscription payment of $2,450 completed"),
        ("September 10, 2025", "Feature usage spike", "API calls increased by 150% - potential upgrade opportunity")
    ]
    for date, title, desc in timeline:
        st.markdown(f"**{date}**")
        st.info(f"**{title}**<br>{desc}", icon="🕒")

    st.markdown("---")

    # --- Action Buttons ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("View Full History")
    with col2:
        st.button("Export Report")
    with col3:
        st.button("Set Alert")

    st.markdown("---")

    # --- Loading & Error States ---
    st.markdown("## ⚠️ Loading & Error States")
    st.info("🔄 Loading customer data...", icon="🔄")
    st.error("Error: Unable to fetch data from internal API. Please check your connection and try again.")

if __name__ == "__main__":
    main()
