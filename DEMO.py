import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="Enterprise Workplace Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# Corporate Banking Theme CSS - Fully Adaptive Light/Dark Mode
# --------------------------------
st.markdown("""
<style>
    /* Corporate Color Palette - Core colors stay consistent */
    :root {
        --primary-navy: #1e3a8a;
        --secondary-blue: #3b82f6;
        --accent-gold: #d97706;
        --success-green: #059669;
        --alert-red: #dc2626;
        --neutral-gray: #64748b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers - Use Streamlit's default text colors */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
    }
    
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Metric Cards - Always vibrant with white text */
    .metric-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 24px;
        border-radius: 8px;
        color: white !important;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.15);
        border-left: 4px solid #d97706;
    }
    
    .metric-card-success {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        border-left: 4px solid #10b981;
    }
    
    .metric-card-warning {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        border-left: 4px solid #f59e0b;
    }
    
    .metric-card-secondary {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-left: 4px solid #60a5fa;
    }
    
    .metric-card * {
        color: white !important;
    }
    
    .metric-card .metric-label {
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.95;
        margin-bottom: 8px;
    }
    
    .metric-card .metric-value {
        font-size: 36px;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .metric-card .metric-subtitle {
        font-size: 12px;
        opacity: 0.9;
    }
    
    /* Alert Boxes - Light mode optimized, dark mode adaptive */
    .alert-box {
        padding: 16px 20px;
        border-radius: 6px;
        margin: 16px 0;
        border-left: 4px solid;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .alert-critical {
        background-color: #fef2f2;
        border-left-color: #dc2626;
        color: #991b1b;
    }
    
    .alert-warning {
        background-color: #fffbeb;
        border-left-color: #d97706;
        color: #92400e;
    }
    
    .alert-info {
        background-color: #eff6ff;
        border-left-color: #3b82f6;
        color: #1e40af;
    }
    
    .alert-success {
        background-color: #f0fdf4;
        border-left-color: #059669;
        color: #065f46;
    }
    
    .alert-title {
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    /* Dark mode alert adjustments */
    @media (prefers-color-scheme: dark) {
        .alert-critical {
            background-color: rgba(254, 242, 242, 0.1);
            color: #fca5a5;
            border: 1px solid rgba(220, 38, 38, 0.3);
        }
        
        .alert-warning {
            background-color: rgba(255, 251, 235, 0.1);
            color: #fcd34d;
            border: 1px solid rgba(217, 119, 6, 0.3);
        }
        
        .alert-info {
            background-color: rgba(239, 246, 255, 0.1);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        .alert-success {
            background-color: rgba(240, 253, 244, 0.1);
            color: #6ee7b7;
            border: 1px solid rgba(5, 150, 105, 0.3);
        }
    }
    
    /* Insight Cards - Adapts to Streamlit theme */
    .insight-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    
    @media (prefers-color-scheme: dark) {
        .insight-card {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #334155;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
    }
    
    .insight-card-critical {
        border-left-color: #dc2626;
    }
    
    .insight-card-warning {
        border-left-color: #d97706;
    }
    
    .insight-card-success {
        border-left-color: #059669;
    }
    
    .insight-title {
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .insight-content {
        font-size: 14px;
        line-height: 1.6;
        opacity: 0.9;
    }
    
    /* Status Badges - Always visible */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .status-queued {
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
    }
    
    .status-preparing {
        background-color: #dbeafe;
        color: #1e40af;
        border: 1px solid #93c5fd;
    }
    
    .status-delivered {
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #6ee7b7;
    }
    
    .priority-high {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }
    
    .priority-normal {
        background-color: #e0e7ff;
        color: #3730a3;
        border: 1px solid #a5b4fc;
    }
    
    .priority-low {
        background-color: #f3f4f6;
        color: #374151;
        border: 1px solid #d1d5db;
    }
    
    /* Dark mode badge adjustments */
    @media (prefers-color-scheme: dark) {
        .status-queued {
            background-color: rgba(241, 245, 249, 0.15);
            color: #cbd5e1;
            border: 1px solid #475569;
        }
        
        .status-preparing {
            background-color: rgba(219, 234, 254, 0.15);
            color: #93c5fd;
            border: 1px solid #3b82f6;
        }
        
        .status-delivered {
            background-color: rgba(209, 250, 229, 0.15);
            color: #6ee7b7;
            border: 1px solid #059669;
        }
        
        .priority-high {
            background-color: rgba(254, 226, 226, 0.15);
            color: #fca5a5;
            border: 1px solid #dc2626;
        }
        
        .priority-normal {
            background-color: rgba(224, 231, 255, 0.15);
            color: #a5b4fc;
            border: 1px solid #6366f1;
        }
        
        .priority-low {
            background-color: rgba(243, 244, 246, 0.15);
            color: #d1d5db;
            border: 1px solid #6b7280;
        }
    }
    
    /* Inventory Cards */
    .inventory-card {
        background: white;
        padding: 16px;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
    }
    
    .inventory-critical {
        border-left: 4px solid #dc2626;
        background-color: #fef2f2;
    }
    
    .inventory-low {
        border-left: 4px solid #d97706;
        background-color: #fffbeb;
    }
    
    .inventory-stable {
        border-left: 4px solid #059669;
    }
    
    @media (prefers-color-scheme: dark) {
        .inventory-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid #334155;
        }
        
        .inventory-critical {
            background-color: rgba(254, 242, 242, 0.1);
        }
        
        .inventory-low {
            background-color: rgba(255, 251, 235, 0.1);
        }
    }
    
    /* Tables remain with Streamlit defaults for better compatibility */
    .dataframe {
        font-size: 13px;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Tabs - Always clear */
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 6px;
        font-weight: 500;
        padding: 0 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }
    
    /* Section dividers use Streamlit default */
    hr {
        margin: 24px 0;
    }
    
    /* Sidebar metrics */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        padding: 12px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Initialize Session State
# --------------------------------
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame({
        "Order ID": range(101, 111),
        "Item": ["Espresso", "Club Sandwich", "Green Tea", "Cappuccino", "Caesar Salad",
                 "Latte", "Burger Deluxe", "Matcha Latte", "Espresso", "Pasta Primavera"],
        "Employee": ["Sarah Chen", "Mike Ross", "Emma Stone", "John Doe", "Lisa Wang",
                     "Alex Kumar", "Tom Brady", "Sophie Turner", "James Wilson", "Maria Garcia"],
        "Status": ["delivered", "preparing", "queued", "queued", "preparing",
                   "queued", "queued", "delivered", "preparing", "queued"],
        "Priority": ["normal", "high", "normal", "normal", "normal",
                     "low", "high", "normal", "normal", "normal"],
        "ETA (min)": [0, 5, 12, 10, 7, 15, 20, 0, 6, 10],
        "Timestamp": ["09:15 AM", "09:30 AM", "09:45 AM", "10:00 AM", "10:15 AM",
                      "10:30 AM", "10:45 AM", "11:00 AM", "11:15 AM", "11:30 AM"],
        "Cost": [4.50, 8.99, 3.50, 5.00, 9.50, 4.75, 12.99, 5.50, 4.50, 11.99]
    })

if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Item": ["Coffee Beans", "Milk", "Bread", "Tea Leaves", "Vegetables"],
        "Stock Level": [20, 5, 12, 3, 15],
        "Unit": ["kg", "L", "loaves", "kg", "kg"],
        "Threshold": [10, 8, 6, 5, 10],
        "Status": ["stable", "low", "stable", "critical", "stable"],
        "Last Order": ["2 days ago", "1 day ago", "Today", "3 days ago", "Today"]
    })

if 'feedback' not in st.session_state:
    st.session_state.feedback = pd.DataFrame({
        "Employee": ["Aman Gupta", "Riya Patel", "Sara Williams", "David Lee"],
        "Staff Member": ["John Martinez", "Maria Santos", "John Martinez", "Chen Wei"],
        "Rating": [5, 4, 5, 5],
        "Comment": ["Exceptional service, very prompt delivery", "Quick response time, professional", 
                    "Very polite and helpful staff", "Perfect order accuracy every time"],
        "Date": ["Jan 24", "Jan 24", "Jan 23", "Jan 23"]
    })

# --------------------------------
# Helper Functions
# --------------------------------
def get_order_stats(orders_df):
    """Calculate order statistics"""
    return {
        'total': len(orders_df),
        'queued': len(orders_df[orders_df['Status'] == 'queued']),
        'preparing': len(orders_df[orders_df['Status'] == 'preparing']),
        'delivered': len(orders_df[orders_df['Status'] == 'delivered']),
        'revenue': orders_df['Cost'].sum(),
        'avg_eta': orders_df[orders_df['ETA (min)'] > 0]['ETA (min)'].mean()
    }

def create_metric_card(title, value, subtitle="", card_type="primary"):
    """Create a styled metric card"""
    return f"""
    <div class="metric-card metric-card-{card_type}">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """

def create_status_badge(status):
    """Create status badge"""
    return f'<span class="status-badge status-{status.lower()}">{status.upper()}</span>'

def create_priority_badge(priority):
    """Create priority badge"""
    return f'<span class="status-badge priority-{priority.lower()}">{priority.upper()}</span>'

# --------------------------------
# Header
# --------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Enterprise Workplace Platform")
    st.caption("Integrated Operations Management System | Real-time Analytics | AI-Driven Insights")
with col2:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 20px;">
        <div style="font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">System Status</div>
        <div style="font-size: 14px; color: #059669; font-weight: 600;">● OPERATIONAL</div>
    </div>
    """, unsafe_allow_html=True)

# Disclaimer Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
     padding: 12px 20px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 20px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 20px;">ℹ️</span>
        <div>
            <strong style="color: #1e40af;">DEMO MOCKUP NOTICE</strong>
            <div style="font-size: 13px; color: #1e3a8a; margin-top: 4px;">
                This is a demonstration mockup of the Enterprise Workplace Platform. All data displayed is simulated for illustrative purposes only. 
                The actual production system may include additional features, enhanced security protocols, and real-time data integration. 
                This mockup is subject to continuous improvement and iteration.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------
# Sidebar Controls
# --------------------------------
with st.sidebar:
    st.markdown("### SYSTEM CONTROLS")
    
    role = st.radio("Access Level", ["Administrative Dashboard", "Kitchen Operations"], index=0)
    
    st.markdown("---")
    
    ai_enabled = st.toggle("AI Advisory Module", value=True)
    
    st.markdown("---")
    
    time_range = st.selectbox("Reporting Period", ["Today", "This Week", "This Month", "This Quarter"])
    
    st.markdown("---")
    
    st.markdown("### OPERATIONAL METRICS")
    stats = get_order_stats(st.session_state.orders)
    
    st.metric("Active Orders", stats['total'], delta="+12 from yesterday")
    st.metric("Queue Depth", stats['queued'])
    st.metric("Daily Revenue", f"${stats['revenue']:.2f}", delta="+8.5%")
    
    st.markdown("---")
    
    st.markdown("### SYSTEM NOTIFICATIONS")
    st.info("3 pending alerts")
    
    st.markdown("---")
    
    if st.button("Refresh Dashboard", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# --------------------------------
# ADMINISTRATIVE DASHBOARD
# --------------------------------
if role == "Administrative Dashboard":
    
    # Tab Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Executive Overview", "AI Intelligence", "Performance Analytics", "Reports & Export"])
    
    # ===========================
    # TAB 1: EXECUTIVE OVERVIEW
    # ===========================
    with tab1:
        stats = get_order_stats(st.session_state.orders)
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Total Orders", 
                stats['total'],
                "Active transactions today",
                "primary"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Queue Status", 
                stats['queued'],
                f"{stats['preparing']} in preparation",
                "warning"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Revenue Generated", 
                f"${stats['revenue']:.2f}",
                "Average: $8.50 per order",
                "success"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Avg Processing Time", 
                f"{stats['avg_eta']:.1f} min",
                "Target: <10 minutes",
                "secondary"
            ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Hourly Order Distribution")
            hourly_data = pd.DataFrame({
                'Hour': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
                'Orders': [8, 15, 22, 35, 42, 38, 18, 12, 9]
            })
            fig = px.bar(hourly_data, x='Hour', y='Orders', 
                        color_discrete_sequence=['#1e3a8a'])
            fig.update_layout(
                height=320,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=12),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.subheader("Category Distribution")
            top_items = pd.DataFrame({
                'Category': ['Coffee', 'Sandwiches', 'Salads', 'Tea', 'Others'],
                'Orders': [145, 98, 76, 54, 32]
            })
            fig = px.pie(top_items, values='Orders', names='Category',
                        color_discrete_sequence=['#1e3a8a', '#3b82f6', '#059669', '#d97706', '#64748b'])
            fig.update_layout(
                height=320,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=12)
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        # Charts Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Inventory Management Status")
            
            for idx, row in st.session_state.inventory.iterrows():
                status_class = f"inventory-{row['Status']}"
                status_indicator = {
                    'critical': '● CRITICAL',
                    'low': '● LOW STOCK',
                    'stable': '● STABLE'
                }.get(row['Status'], '● STABLE')
                
                status_color = {
                    'critical': '#dc2626',
                    'low': '#d97706',
                    'stable': '#059669'
                }.get(row['Status'], '#059669')
                
                st.markdown(f"""
                <div class="inventory-card {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; margin-bottom: 4px;">{row['Item']}</div>
                            <div style="font-size: 11px; color: #64748b;">Last order: {row['Last Order']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 24px; font-weight: 700;">{row['Stock Level']} {row['Unit']}</div>
                            <div style="font-size: 11px; color: {status_color}; font-weight: 600;">{status_indicator}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Critical items alert
            critical_items = st.session_state.inventory[st.session_state.inventory['Status'].isin(['critical', 'low'])]
            if len(critical_items) > 0:
                st.markdown(f"""
                <div class="alert-box alert-warning">
                    <div class="alert-title">INVENTORY ALERT</div>
                    <div>{len(critical_items)} item(s) below threshold. Immediate reorder recommended: {', '.join(critical_items['Item'].tolist())}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Workspace Utilization")
            space_data = pd.DataFrame({
                'Area': ['Pantry', 'Seating Area', 'Meeting Rooms', 'Quiet Zones'],
                'Utilization': [75, 60, 40, 85],
                'Capacity': [20, 50, 10, 15]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=space_data['Area'],
                x=space_data['Utilization'],
                orientation='h',
                marker=dict(color='#1e3a8a'),
                text=space_data['Utilization'].apply(lambda x: f'{x}%'),
                textposition='inside',
                textfont=dict(color='white', size=12, family="Segoe UI")
            ))
            fig.update_layout(
                height=320,
                xaxis_title="Utilization Percentage",
                xaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(100,116,139,0.1)'),
                yaxis=dict(showgrid=False),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=12)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("### Utilization Insights")
            st.markdown("""
            <div class="alert-box alert-info">
                <div class="alert-title">CAPACITY ANALYSIS</div>
                <div>Quiet Zones at 85% capacity. Consider implementing reservation system during peak hours.</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Current Orders Table
        st.subheader("Active Order Registry")
        
        display_orders = st.session_state.orders[['Order ID', 'Item', 'Employee', 'Status', 'Priority', 'ETA (min)', 'Timestamp']].copy()
        
        # Use Streamlit's native dataframe without custom styling for theme compatibility
        st.dataframe(
            display_orders,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Order ID": st.column_config.NumberColumn("Order ID", format="%d"),
                "Item": st.column_config.TextColumn("Item"),
                "Employee": st.column_config.TextColumn("Employee"),
                "Status": st.column_config.TextColumn("Status"),
                "Priority": st.column_config.TextColumn("Priority"),
                "ETA (min)": st.column_config.NumberColumn("ETA (min)", format="%d"),
                "Timestamp": st.column_config.TextColumn("Timestamp")
            }
        )
    
    # ===========================
    # TAB 2: AI INTELLIGENCE
    # ===========================
    with tab2:
        if ai_enabled:
            st.markdown("""
            <div class="alert-box alert-info">
                <div class="alert-title">AI ADVISORY SYSTEM STATUS: ACTIVE</div>
                <div>Advanced analytics engine providing real-time operational intelligence and predictive insights based on historical data patterns and current operational metrics.</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("### Strategic Recommendations")
            
            # AI Insights Grid
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="insight-card insight-card-warning">
                    <div class="insight-title">DEMAND FORECAST ALERT</div>
                    <div class="insight-content">
                        Predictive models indicate significant demand surge expected between <strong>13:30-14:30</strong>. 
                        Recommend increasing kitchen staffing by one additional team member during this period to maintain service levels.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-card insight-card-success">
                    <div class="insight-title">PRODUCT OPTIMIZATION</div>
                    <div class="insight-content">
                        Coffee category showing <strong>23% increase</strong> in demand over previous period. 
                        Analysis suggests introducing premium coffee variants could capture additional revenue opportunity.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="insight-card">
                    <div class="insight-title">RESOURCE OPTIMIZATION</div>
                    <div class="insight-content">
                        Optimal staff break window identified: <strong>15:00-15:20</strong> based on historical traffic patterns. 
                        This timeframe shows consistently low order volume, minimizing operational impact.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-card insight-card-critical">
                    <div class="insight-title">SUPPLY CHAIN ALERT</div>
                    <div class="insight-content">
                        Critical inventory levels detected for Tea Leaves and Milk supplies. 
                        <strong>Immediate procurement action recommended</strong> within next 24 hours to prevent service disruption.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Demand Forecast
            st.subheader("Seven-Day Demand Projection Model")
            
            forecast_data = pd.DataFrame({
                'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                'Predicted Orders': [145, 158, 172, 165, 189, 95, 78],
                'Actual Orders': [142, 155, None, None, None, None, None],
                'Confidence Lower': [138, 150, 165, 158, 180, 88, 72],
                'Confidence Upper': [152, 166, 179, 172, 198, 102, 84]
            })
            
            fig = go.Figure()
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_data['Day'],
                y=forecast_data['Confidence Upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_data['Day'],
                y=forecast_data['Confidence Lower'],
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(30, 58, 138, 0.1)',
                fill='tonexty',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Predicted line
            fig.add_trace(go.Scatter(
                x=forecast_data['Day'], 
                y=forecast_data['Predicted Orders'],
                mode='lines+markers',
                name='AI Prediction',
                line=dict(color='#1e3a8a', width=3),
                marker=dict(size=8, color='#1e3a8a')
            ))
            
            # Actual line
            fig.add_trace(go.Scatter(
                x=forecast_data['Day'], 
                y=forecast_data['Actual Orders'],
                mode='lines+markers',
                name='Actual Performance',
                line=dict(color='#059669', width=3),
                marker=dict(size=8, color='#059669')
            ))
            
            fig.update_layout(
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=12),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)', title="Order Volume"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("---")
            
            # Analysis sections
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Operational Capacity Analysis")
                st.markdown("""
                <div class="alert-box alert-info">
                    <div class="alert-title">CURRENT STATUS</div>
                    <div>Kitchen capacity approaching operational limits during lunch period (12:00-14:00). Current throughput is 92% of maximum capacity.</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-card">
                    <div class="insight-title">RECOMMENDATION</div>
                    <div class="insight-content">
                        Implement staggered break scheduling or deploy temporary support personnel during identified peak periods to maintain service quality standards.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### Workspace Efficiency")
                st.markdown("""
                <div class="alert-box alert-warning">
                    <div class="alert-title">UTILIZATION METRICS</div>
                    <div>Pantry utilization at 75%, Quiet Zones at 85%. High-density periods creating potential service bottlenecks.</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-card">
                    <div class="insight-title">RECOMMENDATION</div>
                    <div class="insight-content">
                        Deploy staggered break schedules across departments to distribute workspace utilization more evenly throughout operational hours.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("""
            <div class="alert-box alert-info">
                <div class="alert-title">GOVERNANCE NOTICE</div>
                <div>All AI-generated insights are advisory in nature. Operational decisions require human authorization and oversight. System recommendations should be reviewed by appropriate management personnel before implementation.</div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="alert-box alert-warning">
                <div class="alert-title">AI ADVISORY MODULE: DISABLED</div>
                <div>The AI Intelligence system is currently inactive. Enable AI Advisory from the sidebar control panel to access predictive analytics and operational recommendations.</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===========================
    # TAB 3: PERFORMANCE ANALYTICS
    # ===========================
    with tab3:
        st.subheader("Revenue Performance Tracking")
        
        # Revenue trend
        revenue_data = pd.DataFrame({
            'Time': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
            'Revenue': [62, 135, 198, 315, 405, 342, 162, 108, 81]
        })
        
        fig = px.line(revenue_data, x='Time', y='Revenue', 
                     markers=True,
                     color_discrete_sequence=['#059669'])
        fig.update_layout(
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI", size=12),
            xaxis=dict(showgrid=False, title="Time Period"),
            yaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)', title="Revenue ($)")
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Service Quality Feedback")
            
            # Display feedback professionally
            for idx, row in st.session_state.feedback.iterrows():
                stars = "★" * row['Rating'] + "☆" * (5 - row['Rating'])
                st.markdown(f"""
                <div class="insight-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                        <div>
                            <div style="font-weight: 600;">{row['Employee']}</div>
                            <div style="font-size: 12px; color: #64748b;">Service Provider: {row['Staff Member']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #d97706; font-size: 14px;">{stars}</div>
                            <div style="font-size: 11px; color: #64748b;">{row['Date']}</div>
                        </div>
                    </div>
                    <div style="font-size: 13px; font-style: italic; opacity: 0.8;">"{row['Comment']}"</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Order Status Distribution")
            
            status_counts = st.session_state.orders['Status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        color_discrete_sequence=['#059669', '#3b82f6', '#64748b'])
            fig.update_layout(
                height=280,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=12)
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.subheader("Priority Classification")
            priority_counts = st.session_state.orders['Priority'].value_counts()
            
            fig = go.Figure(data=[go.Bar(
                x=priority_counts.index,
                y=priority_counts.values,
                marker_color=['#dc2626', '#1e3a8a', '#64748b'],
                text=priority_counts.values,
                textposition='outside'
            )])
            fig.update_layout(
                height=250,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Segoe UI", size=12),
                xaxis=dict(showgrid=False, title="Priority Level"),
                yaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)', title="Count")
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        # Performance Metrics Summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Service Rating", "4.75/5.00", delta="+0.15")
        with col2:
            st.metric("Order Accuracy", "98.5%", delta="+1.2%")
        with col3:
            st.metric("Avg Response Time", "2.3 min", delta="-0.4 min")
        with col4:
            st.metric("Customer Satisfaction", "96%", delta="+3%")
    
    # ===========================
    # TAB 4: REPORTS & EXPORT
    # ===========================
    with tab4:
        st.markdown("### Data Export & Reporting")
        st.write("Generate and download operational reports for compliance, analysis, and audit purposes.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Order Transaction Report")
            st.write("Complete order history with timestamps, status, and financial data.")
            csv_orders = st.session_state.orders.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Orders Data",
                data=csv_orders,
                file_name=f"orders_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### Inventory Management Report")
            st.write("Current stock levels, thresholds, and procurement history.")
            csv_inventory = st.session_state.inventory.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Inventory Data",
                data=csv_inventory,
                file_name=f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            st.markdown("#### Service Quality Report")
            st.write("Employee feedback, ratings, and service performance metrics.")
            csv_feedback = st.session_state.feedback.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Feedback Data",
                data=csv_feedback,
                file_name=f"feedback_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("---")
        
        st.subheader("Employee Recognition Data")
        st.caption("Confidential: Administrative access only. Service quality feedback for performance evaluation purposes.")
        
        # Use native Streamlit dataframe for theme compatibility
        st.dataframe(
            st.session_state.feedback,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Employee": st.column_config.TextColumn("Employee"),
                "Staff Member": st.column_config.TextColumn("Staff Member"),
                "Rating": st.column_config.NumberColumn("Rating", format="%d ⭐"),
                "Comment": st.column_config.TextColumn("Comment"),
                "Date": st.column_config.TextColumn("Date")
            }
        )
        
        st.markdown("---")
        
        st.markdown("### Report Generation Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_format = st.selectbox("Export Format", ["CSV", "Excel (XLSX)", "PDF"])
            include_charts = st.checkbox("Include visualization charts", value=True)
        
        with col2:
            date_range = st.date_input("Report Date Range", value=[datetime.now().date()])
            include_summary = st.checkbox("Include executive summary", value=True)

# --------------------------------
# KITCHEN OPERATIONS VIEW
# --------------------------------
else:
    tab1, tab2 = st.tabs(["Order Management", "Operational Controls"])
    
    # ===========================
    # KITCHEN TAB 1: ORDER MANAGEMENT
    # ===========================
    with tab1:
        stats = get_order_stats(st.session_state.orders)
        
        # High load warning
        if stats['queued'] > 3:
            st.markdown(f"""
            <div class="alert-box alert-warning">
                <div class="alert-title">HIGH VOLUME ALERT</div>
                <div><strong>{stats['queued']}</strong> orders currently in queue. Prioritize high-priority items to maintain service level agreements.</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Active Order Queue")
        
        # Filter options
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=['queued', 'preparing', 'delivered'],
                default=['queued', 'preparing']
            )
        with col2:
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=['high', 'normal', 'low'],
                default=['high', 'normal', 'low']
            )
        
        st.markdown("---")
        
        # Filter orders
        filtered_orders = st.session_state.orders[
            (st.session_state.orders['Status'].isin(status_filter)) &
            (st.session_state.orders['Priority'].isin(priority_filter))
        ].sort_values('Priority', ascending=False)
        
        # Display orders in professional format
        for idx, row in filtered_orders.iterrows():
            # Create card-like layout for each order
            st.markdown(f"""
            <div class="inventory-card" style="padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                            <span style="font-weight: 700; color: #1e3a8a; font-size: 16px;">Order #{row['Order ID']}</span>
                            {create_status_badge(row['Status'])}
                            {create_priority_badge(row['Priority'])}
                        </div>
                        <div style="font-size: 15px; font-weight: 600; margin-bottom: 4px;">{row['Item']}</div>
                        <div style="font-size: 13px; color: #64748b;">Employee: {row['Employee']} | Time: {row['Timestamp']}</div>
                    </div>
                    <div style="text-align: right; padding-left: 20px;">
                        <div style="color: #64748b; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">ETA</div>
                        <div style="font-size: 24px; font-weight: 700; color: #1e3a8a;">{row['ETA (min)']} min</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                if row['Status'] == 'queued':
                    if st.button("Start Preparation", key=f"start_{row['Order ID']}", use_container_width=True):
                        st.session_state.orders.loc[idx, 'Status'] = 'preparing'
                        st.rerun()
            
            with col2:
                if row['Status'] == 'preparing':
                    if st.button("Mark Complete", key=f"done_{row['Order ID']}", use_container_width=True):
                        st.session_state.orders.loc[idx, 'Status'] = 'delivered'
                        st.session_state.orders.loc[idx, 'ETA (min)'] = 0
                        st.rerun()
            
            st.markdown("---")
    
    # ===========================
    # KITCHEN TAB 2: OPERATIONAL CONTROLS
    # ===========================
    with tab2:
        st.markdown("### Quick Action Panel")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Update to Preparing", use_container_width=True, type="primary"):
                st.info("Select an order from Order Management tab")
        
        with col2:
            if st.button("Mark as Complete", use_container_width=True, type="primary"):
                st.success("Select an order from Order Management tab")
        
        with col3:
            if st.button("Assign Automated Delivery", use_container_width=True):
                st.info("Robot delivery system activated")
        
        st.markdown("""
        <div class="alert-box alert-info">
            <div class="alert-title">AUTOMATION NOTICE</div>
            <div>Automated delivery systems are optional. All delivery assignments remain under full kitchen staff control and discretion.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Communication
        st.markdown("### Internal Communication")
        
        col1, col2 = st.columns([5, 1])
        with col1:
            message = st.text_input("Send message to employee regarding order specifications or modifications...")
        with col2:
            st.write("")
            st.write("")
            if st.button("Send", use_container_width=True):
                if message:
                    st.success("Message transmitted successfully")
                else:
                    st.warning("Please enter a message")
        
        st.markdown("---")
        
        # Inventory Quick View
        st.markdown("### Inventory Status Monitor")
        
        col1, col2 = st.columns(2)
        
        for idx, row in st.session_state.inventory.iterrows():
            col = col1 if idx % 2 == 0 else col2
            
            with col:
                status_class = f"inventory-{row['Status']}"
                status_text = {
                    'critical': 'CRITICAL - REORDER REQUIRED',
                    'low': 'LOW STOCK - REORDER SOON',
                    'stable': 'ADEQUATE STOCK'
                }.get(row['Status'], 'ADEQUATE STOCK')
                
                status_color = {
                    'critical': '#dc2626',
                    'low': '#d97706',
                    'stable': '#059669'
                }.get(row['Status'], '#059669')
                
                st.markdown(f"""
                <div class="inventory-card {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-weight: 600; font-size: 15px;">{row['Item']}</span>
                        <span style="font-size: 22px; font-weight: 700;">{row['Stock Level']} {row['Unit']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 11px; color: #64748b;">Threshold: {row['Threshold']} {row['Unit']}</span>
                        <span style="font-size: 11px; color: {status_color}; font-weight: 600;">{status_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --------------------------------
# Footer
# --------------------------------
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px 0;">
    <div style="margin-bottom: 8px;">
        <strong>Enterprise Workplace Operations Platform</strong> | Version 2.0.1
    </div>
    <div>
        Confidential & Proprietary | For Authorized Personnel Only | {datetime.now().strftime('%B %d, %Y')}
    </div>
</div>
""", unsafe_allow_html=True)