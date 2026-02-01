import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="Enterprise Workplace Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# Corporate Banking Theme CSS
# --------------------------------
st.markdown("""
<style>
    :root {
        --primary-navy: #1e3a8a;
        --secondary-blue: #3b82f6;
        --accent-gold: #d97706;
        --success-green: #059669;
        --alert-red: #dc2626;
        --neutral-gray: #64748b;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    h1, h2, h3, h4, h5, h6 {font-weight: 600;}
    h1 {font-weight: 700; letter-spacing: -0.5px;}
    
    .metric-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 24px; border-radius: 8px; color: white !important;
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
    .metric-card * {color: white !important;}
    .metric-card .metric-label {
        font-size: 13px; font-weight: 500; text-transform: uppercase;
        letter-spacing: 0.5px; opacity: 0.95; margin-bottom: 8px;
    }
    .metric-card .metric-value {
        font-size: 36px; font-weight: 700; line-height: 1; margin-bottom: 8px;
    }
    .metric-card .metric-subtitle {font-size: 12px; opacity: 0.9;}
    
    .alert-box {
        padding: 16px 20px; border-radius: 6px; margin: 16px 0;
        border-left: 4px solid; font-size: 14px; line-height: 1.6;
    }
    .alert-critical {background-color: #fef2f2; border-left-color: #dc2626; color: #991b1b;}
    .alert-warning {background-color: #fffbeb; border-left-color: #d97706; color: #92400e;}
    .alert-info {background-color: #eff6ff; border-left-color: #3b82f6; color: #1e40af;}
    .alert-success {background-color: #f0fdf4; border-left-color: #059669; color: #065f46;}
    .alert-title {font-weight: 600; margin-bottom: 4px;}
    
    @media (prefers-color-scheme: dark) {
        .alert-critical {background-color: rgba(254, 242, 242, 0.1); color: #fca5a5; border: 1px solid rgba(220, 38, 38, 0.3);}
        .alert-warning {background-color: rgba(255, 251, 235, 0.1); color: #fcd34d; border: 1px solid rgba(217, 119, 6, 0.3);}
        .alert-info {background-color: rgba(239, 246, 255, 0.1); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3);}
        .alert-success {background-color: rgba(240, 253, 244, 0.1); color: #6ee7b7; border: 1px solid rgba(5, 150, 105, 0.3);}
    }
    
    .insight-card {
        background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 8px;
        border: 1px solid #e2e8f0; border-left: 4px solid #3b82f6;
        margin: 12px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    @media (prefers-color-scheme: dark) {
        .insight-card {background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; box-shadow: 0 1px 3px rgba(0,0,0,0.3);}
    }
    .insight-card-critical {border-left-color: #dc2626;}
    .insight-card-warning {border-left-color: #d97706;}
    .insight-card-success {border-left-color: #059669;}
    .insight-title {font-size: 15px; font-weight: 600; margin-bottom: 8px;}
    .insight-content {font-size: 14px; line-height: 1.6; opacity: 0.9;}
    
    .status-badge {
        display: inline-block; padding: 4px 12px; border-radius: 4px;
        font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px;
    }
    .status-queued {background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;}
    .status-preparing {background-color: #dbeafe; color: #1e40af; border: 1px solid #93c5fd;}
    .status-delivered {background-color: #d1fae5; color: #065f46; border: 1px solid #6ee7b7;}
    .status-active {background-color: #d1fae5; color: #065f46; border: 1px solid #6ee7b7;}
    .status-vacation {background-color: #fef3c7; color: #92400e; border: 1px solid #fcd34d;}
    .priority-high {background-color: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;}
    .priority-normal {background-color: #e0e7ff; color: #3730a3; border: 1px solid #a5b4fc;}
    .priority-low {background-color: #f3f4f6; color: #374151; border: 1px solid #d1d5db;}
    
    @media (prefers-color-scheme: dark) {
        .status-queued {background-color: rgba(241, 245, 249, 0.15); color: #cbd5e1; border: 1px solid #475569;}
        .status-preparing {background-color: rgba(219, 234, 254, 0.15); color: #93c5fd; border: 1px solid #3b82f6;}
        .status-delivered, .status-active {background-color: rgba(209, 250, 229, 0.15); color: #6ee7b7; border: 1px solid #059669;}
        .status-vacation {background-color: rgba(254, 243, 199, 0.15); color: #fcd34d; border: 1px solid #d97706;}
        .priority-high {background-color: rgba(254, 226, 226, 0.15); color: #fca5a5; border: 1px solid #dc2626;}
        .priority-normal {background-color: rgba(224, 231, 255, 0.15); color: #a5b4fc; border: 1px solid #6366f1;}
        .priority-low {background-color: rgba(243, 244, 246, 0.15); color: #d1d5db; border: 1px solid #6b7280;}
    }
    
    .inventory-card {
        background: white; padding: 16px; border-radius: 6px;
        border: 1px solid #e2e8f0; margin-bottom: 12px;
    }
    .inventory-critical {border-left: 4px solid #dc2626; background-color: #fef2f2;}
    .inventory-low {border-left: 4px solid #d97706; background-color: #fffbeb;}
    .inventory-stable {border-left: 4px solid #059669;}
    
    @media (prefers-color-scheme: dark) {
        .inventory-card {background: rgba(30, 41, 59, 0.6); border: 1px solid #334155;}
        .inventory-critical {background-color: rgba(254, 242, 242, 0.1);}
        .inventory-low {background-color: rgba(255, 251, 235, 0.1);}
    }
    
    .stButton>button {
        border-radius: 6px; font-weight: 600; letter-spacing: 0.3px; transition: all 0.2s;
    }
    .stButton>button:hover {transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15);}
    .stTabs [data-baseweb="tab"] {height: 48px; border-radius: 6px; font-weight: 500; padding: 0 24px;}
    .stTabs [aria-selected="true"] {background-color: #1e3a8a !important; color: white !important;}
    hr {margin: 24px 0;}
    [data-testid="stSidebar"] [data-testid="stMetric"] {padding: 12px; border-radius: 6px;}
    
    .login-container {
        max-width: 400px; margin: 100px auto; padding: 40px;
        background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    @media (prefers-color-scheme: dark) {
        .login-container {background: rgba(30, 41, 59, 0.8);}
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Authentication System
# --------------------------------
USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "System Administrator"},
    "kitchen": {"password": "kitchen123", "role": "kitchen", "name": "Kitchen Staff"},
    "employee": {"password": "emp123", "role": "employee", "name": "John Doe"}
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.username = None

# --------------------------------
# Initialize Data with Dynamic Capabilities
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
        "Cost": [4.50, 8.99, 3.50, 5.00, 9.50, 4.75, 12.99, 5.50, 4.50, 11.99],
        "Assigned Staff": ["Maria Santos", "John Martinez", "Chen Wei", "Maria Santos", "John Martinez",
                           "Chen Wei", "Maria Santos", "John Martinez", "Chen Wei", "Maria Santos"],
        "Message": ["", "", "", "", "", "", "", "", "", ""],
        "Rating": [5, 0, 0, 0, 0, 0, 0, 4, 0, 0],
        "Delivery Method": ["Staff", "Staff", "Staff", "Staff", "Staff", "Staff", "Staff", "Staff", "Staff", "Staff"]
    })
    st.session_state.next_order_id = 111

if 'employees' not in st.session_state:
    st.session_state.employees = pd.DataFrame({
        "Employee ID": ["E001", "E002", "E003", "E004", "E005", "E006", "E007", "E008"],
        "Name": ["Sarah Chen", "Mike Ross", "Emma Stone", "John Doe", "Lisa Wang", "Alex Kumar", "Tom Brady", "Sophie Turner"],
        "Department": ["Engineering", "Sales", "Marketing", "Finance", "HR", "Operations", "IT", "Customer Success"],
        "Position": ["Senior Engineer", "Sales Manager", "Marketing Lead", "Financial Analyst", "HR Manager", "Operations Coordinator", "IT Specialist", "CS Manager"],
        "Priority Level": ["normal", "high", "high", "normal", "high", "normal", "normal", "high"],  # Based on position
        "Status": ["Active", "Active", "Vacation", "Active", "Active", "Vacation", "Active", "Active"],
        "Vacation Start": [None, None, "2026-01-28", None, None, "2026-01-30", None, None],
        "Vacation End": [None, None, "2026-02-05", None, None, "2026-02-03", None, None],
        "Replacement": [None, None, "Mike Ross", None, None, "Sarah Chen", None, None],
        "Email": ["sarah.chen@company.com", "mike.ross@company.com", "emma.stone@company.com", "john.doe@company.com", 
                  "lisa.wang@company.com", "alex.kumar@company.com", "tom.brady@company.com", "sophie.turner@company.com"],
        "Phone": ["+971-50-123-4567", "+971-50-234-5678", "+971-50-345-6789", "+971-50-456-7890",
                  "+971-50-567-8901", "+971-50-678-9012", "+971-50-789-0123", "+971-50-890-1234"],
        "Join Date": ["2023-01-15", "2022-06-10", "2023-03-20", "2021-11-05", "2022-09-12", "2023-07-01", "2022-02-28", "2023-05-18"]
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

if 'time_filter' not in st.session_state:
    st.session_state.time_filter = "Today"

# Kitchen staff list
KITCHEN_STAFF = ["Maria Santos", "John Martinez", "Chen Wei", "Alex Rodriguez"]

# --------------------------------
# Helper Functions
# --------------------------------
def get_order_stats(orders_df):
    return {
        'total': len(orders_df),
        'queued': len(orders_df[orders_df['Status'] == 'queued']),
        'preparing': len(orders_df[orders_df['Status'] == 'preparing']),
        'delivered': len(orders_df[orders_df['Status'] == 'delivered']),
        'revenue': orders_df['Cost'].sum(),
        'avg_eta': orders_df[orders_df['ETA (min)'] > 0]['ETA (min)'].mean() if len(orders_df[orders_df['ETA (min)'] > 0]) > 0 else 0
    }

def create_metric_card(title, value, subtitle="", card_type="primary"):
    return f"""
    <div class="metric-card metric-card-{card_type}">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """

def create_status_badge(status):
    return f'<span class="status-badge status-{status.lower()}">{status.upper()}</span>'

def create_priority_badge(priority):
    return f'<span class="status-badge priority-{priority.lower()}">{priority.upper()}</span>'

def get_employee_priority(employee_name):
    """Get priority level based on employee's position"""
    employee_data = st.session_state.employees[st.session_state.employees['Name'] == employee_name]
    if len(employee_data) > 0:
        return employee_data.iloc[0]['Priority Level']
    return 'normal'  # Default priority

def logout():
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.username = None
    st.rerun()

def filter_orders_by_time(orders_df, time_filter):
    """Filter orders based on time period - simulates different data"""
    if time_filter == "Today":
        return orders_df
    elif time_filter == "This Week":
        # Simulate more orders for the week
        multiplier = 5
        new_orders = []
        for i in range(multiplier):
            temp_df = orders_df.copy()
            temp_df['Order ID'] = temp_df['Order ID'] + (i * 100)
            new_orders.append(temp_df)
        return pd.concat(new_orders, ignore_index=True)
    elif time_filter == "This Month":
        # Simulate even more orders for the month
        multiplier = 20
        new_orders = []
        for i in range(multiplier):
            temp_df = orders_df.copy()
            temp_df['Order ID'] = temp_df['Order ID'] + (i * 100)
            new_orders.append(temp_df)
        return pd.concat(new_orders, ignore_index=True)
    else:  # This Quarter
        multiplier = 60
        new_orders = []
        for i in range(multiplier):
            temp_df = orders_df.copy()
            temp_df['Order ID'] = temp_df['Order ID'] + (i * 100)
            new_orders.append(temp_df)
        return pd.concat(new_orders, ignore_index=True)

# --------------------------------
# Login Page
# --------------------------------
if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-container">
        <h1 style="text-align: center; color: #1e3a8a; margin-bottom: 10px;">Enterprise Platform</h1>
        <p style="text-align: center; color: #64748b; margin-bottom: 30px;">Secure Access Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Sign In")
        
        # Use session state to track credentials
        if 'login_username' not in st.session_state:
            st.session_state.login_username = ""
        if 'login_password' not in st.session_state:
            st.session_state.login_password = ""
        if 'login_error' not in st.session_state:
            st.session_state.login_error = False
        
        username = st.text_input("Username", placeholder="Enter your username", key="username_input", 
                                value=st.session_state.login_username)
        password = st.text_input("Password", type="password", placeholder="Enter your password", 
                                key="password_input", value=st.session_state.login_password)
        
        # Update session state
        if username != st.session_state.login_username:
            st.session_state.login_username = username
            st.session_state.login_error = False
        if password != st.session_state.login_password:
            st.session_state.login_password = password
            st.session_state.login_error = False
        
        # Function to handle login
        def attempt_login(user, pwd):
            if user in USERS and USERS[user]["password"] == pwd:
                st.session_state.authenticated = True
                st.session_state.user_role = USERS[user]["role"]
                st.session_state.user_name = USERS[user]["name"]
                st.session_state.username = user
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.session_state.login_error = False
                return True
            else:
                st.session_state.login_error = True
                return False
        
        # Sign In Button
        if st.button("Sign In", use_container_width=True, type="primary"):
            if username and password:
                if attempt_login(username, password):
                    st.success(f"Welcome, {USERS[username]['name']}!")
                    st.rerun()
            else:
                st.warning("Please enter both username and password.")
        
        # Auto-login when both fields are filled (works alongside button)
        if username and password and not st.session_state.login_error:
            if username in USERS and USERS[username]["password"] == password:
                if attempt_login(username, password):
                    st.success(f"Welcome, {USERS[username]['name']}!")
                    st.rerun()
        
        # Show error if login failed
        if st.session_state.login_error:
            st.error("❌ Invalid credentials. Please check your username and password.")
        
        st.markdown("---")
        st.markdown("""
        <div style="background: #eff6ff; padding: 12px; border-radius: 6px; border-left: 3px solid #3b82f6;">
            <strong style="color: #1e40af;">Demo Credentials:</strong><br>
            <small style="color: #1e3a8a;">
            • Admin: <code>admin</code> / <code>admin123</code><br>
            • Kitchen: <code>kitchen</code> / <code>kitchen123</code><br>
            • Employee: <code>employee</code> / <code>emp123</code>
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# --------------------------------
# Main Application (After Authentication)
# --------------------------------

# Header
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.title("Enterprise Workplace Platform")
    st.caption("Integrated Operations Management System")
with col2:
    st.markdown(f"""
    <div style="padding-top: 20px;">
        <div style="font-size: 13px; color: #64748b;">Logged in as</div>
        <div style="font-size: 16px; font-weight: 600; color: #1e3a8a;">{st.session_state.user_name}</div>
        <div style="font-size: 12px; color: #64748b;">Role: {st.session_state.user_role.title()}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.write("")
    st.write("")
    if st.button("Logout", use_container_width=True):
        logout()

# Demo Disclaimer
st.markdown("""
<div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
     padding: 16px 24px; border-radius: 8px; border-left: 4px solid #3b82f6; 
     margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
    <div style="display: flex; align-items: start; gap: 12px;">
        <div style="font-size: 24px; line-height: 1;">ℹ️</div>
        <div style="flex: 1;">
            <div style="font-weight: 700; color: #1e40af; font-size: 15px; margin-bottom: 6px;">
                DEMONSTRATION MOCKUP - NOT PRODUCTION DATA
            </div>
            <div style="font-size: 13px; color: #1e3a8a; line-height: 1.5;">
                This is a visual demonstration mockup. All data is simulated. Production system will include enhanced security and real-time integration.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================
# EMPLOYEE VIEW
# ===================================
if st.session_state.user_role == "employee":
    
    with st.sidebar:
        st.header("Employee Portal")
        my_orders_count = len(st.session_state.orders[st.session_state.orders['Employee'] == st.session_state.user_name])
        my_pending = len(st.session_state.orders[(st.session_state.orders['Employee'] == st.session_state.user_name) & 
                                                  (st.session_state.orders['Status'].isin(['queued', 'preparing']))])
        st.metric("My Orders Today", my_orders_count)
        st.metric("Pending", my_pending)
    
    tab1, tab2, tab3 = st.tabs(["My Orders", "Place Order", "My Profile"])
    
    # MY ORDERS TAB
    with tab1:
        st.subheader("My Order History")
        
        my_orders = st.session_state.orders[st.session_state.orders['Employee'] == st.session_state.user_name]
        
        if len(my_orders) > 0:
            for idx, order in my_orders.iterrows():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    status_html = create_status_badge(order['Status'])
                    st.markdown(f"""
                    **Order #{order['Order ID']}** {status_html}  
                    **{order['Item']}** - ${order['Cost']:.2f}  
                    Ordered: {order['Timestamp']} | Staff: {order['Assigned Staff']}  
                    {f'📨 Message: {order["Message"]}' if order['Message'] else ''}
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("ETA", f"{order['ETA (min)']} min")
                
                # Rating option for delivered orders
                if order['Status'] == 'delivered' and order['Rating'] == 0:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        rating = st.selectbox(f"Rate Service", [1, 2, 3, 4, 5], key=f"rating_{order['Order ID']}")
                    with col2:
                        comment = st.text_input(f"Comment", key=f"comment_{order['Order ID']}", placeholder="Optional feedback")
                    with col3:
                        st.write("")
                        st.write("")
                        if st.button("Submit", key=f"submit_{order['Order ID']}"):
                            st.session_state.orders.loc[idx, 'Rating'] = rating
                            # Add to feedback
                            new_feedback = pd.DataFrame({
                                "Employee": [st.session_state.user_name],
                                "Staff Member": [order['Assigned Staff']],
                                "Rating": [rating],
                                "Comment": [comment if comment else "No comment"],
                                "Date": [datetime.now().strftime("%b %d")]
                            })
                            st.session_state.feedback = pd.concat([st.session_state.feedback, new_feedback], ignore_index=True)
                            st.success("Thank you for your feedback!")
                            st.rerun()
                elif order['Status'] == 'delivered' and order['Rating'] > 0:
                    st.success(f"✅ You rated this order: {'⭐' * order['Rating']}")
                
                st.divider()
        else:
            st.info("You have no orders yet. Place your first order!")
    
    # PLACE ORDER TAB
    with tab2:
        st.subheader("Place New Order")
        
        # Get current employee's priority level
        employee_data = st.session_state.employees[st.session_state.employees['Name'] == st.session_state.user_name]
        if len(employee_data) > 0:
            emp_priority = employee_data.iloc[0]['Priority Level']
            emp_position = employee_data.iloc[0]['Position']
        else:
            emp_priority = 'normal'
            emp_position = 'Employee'
        
        # Show employee's priority level info
        priority_color = {'high': '🔴', 'normal': '🟡', 'low': '🟢'}
        st.info(f"{priority_color.get(emp_priority, '🟡')} Your order priority: **{emp_priority.upper()}** (Based on position: {emp_position})")
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category", ["Beverages", "Main Course", "Snacks", "Desserts"])
            
            items = {
                "Beverages": [("Espresso", 4.50), ("Cappuccino", 5.00), ("Latte", 4.75), ("Green Tea", 3.50), ("Matcha Latte", 5.50)],
                "Main Course": [("Club Sandwich", 8.99), ("Burger Deluxe", 12.99), ("Pasta Primavera", 11.99), ("Caesar Salad", 9.50)],
                "Snacks": [("French Fries", 4.00), ("Nachos", 6.50), ("Spring Rolls", 7.00)],
                "Desserts": [("Chocolate Cake", 6.00), ("Ice Cream", 4.50), ("Fruit Salad", 5.50)]
            }
            
            item_selection = st.selectbox("Select Item", [f"{item[0]} - ${item[1]:.2f}" for item in items[category]])
            selected_item = item_selection.split(" - ")[0]
            selected_price = float(item_selection.split("$")[1])
        
        with col2:
            special_instructions = st.text_area("Special Instructions", 
                                               placeholder="Any dietary requirements or preferences...",
                                               help="Add any special requests for your order")
        
        if st.button("Place Order", type="primary", use_container_width=True):
            # Add new order with auto-assigned priority based on employee position
            new_order = pd.DataFrame({
                "Order ID": [st.session_state.next_order_id],
                "Item": [selected_item],
                "Employee": [st.session_state.user_name],
                "Status": ["queued"],
                "Priority": [emp_priority],  # Auto-assigned based on position
                "ETA (min)": [random.randint(8, 15)],
                "Timestamp": [datetime.now().strftime("%I:%M %p")],
                "Cost": [selected_price],
                "Assigned Staff": [random.choice(KITCHEN_STAFF)],
                "Message": [special_instructions if special_instructions else ""],
                "Rating": [0],
                "Delivery Method": ["Staff"]
            })
            st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)
            st.session_state.next_order_id += 1
            st.success(f"✅ Order placed successfully for {selected_item}! Your order ID is #{st.session_state.next_order_id - 1}")
            st.info(f"Priority assigned: **{emp_priority.upper()}** based on your position as {emp_position}")
            st.rerun()
    
    # MY PROFILE TAB
    with tab3:
        st.subheader("My Profile")
        
        employee_data = st.session_state.employees[st.session_state.employees['Name'] == st.session_state.user_name]
        
        if len(employee_data) > 0:
            emp = employee_data.iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="insight-card">
                    <h4>Personal Information</h4>
                    <p><strong>Employee ID:</strong> {emp['Employee ID']}</p>
                    <p><strong>Name:</strong> {emp['Name']}</p>
                    <p><strong>Email:</strong> {emp['Email']}</p>
                    <p><strong>Phone:</strong> {emp['Phone']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                priority_badge = create_priority_badge(emp['Priority Level'])
                st.markdown(f"""
                <div class="insight-card">
                    <h4>Employment Details</h4>
                    <p><strong>Department:</strong> {emp['Department']}</p>
                    <p><strong>Position:</strong> {emp['Position']}</p>
                    <p><strong>Join Date:</strong> {emp['Join Date']}</p>
                    <p><strong>Status:</strong> {create_status_badge(emp['Status'])}</p>
                    <p><strong>Order Priority:</strong> {priority_badge}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.subheader("Request Vacation")
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                end_date = st.date_input("End Date")
            
            replacement = st.selectbox("Suggested Replacement", st.session_state.employees['Name'].tolist())
            reason = st.text_area("Reason for Leave")
            
            if st.button("Submit Vacation Request", type="primary"):
                st.success("Vacation request submitted successfully! Your manager will review it.")

# ===================================
# KITCHEN STAFF VIEW
# ===================================
elif st.session_state.user_role == "kitchen":
    
    with st.sidebar:
        st.header("Kitchen Operations")
        stats = get_order_stats(st.session_state.orders)
        st.metric("Active Orders", stats['total'])
        st.metric("In Queue", stats['queued'])
        st.metric("Preparing", stats['preparing'])
        st.divider()
        
        st.subheader("Inventory Status")
        for _, row in st.session_state.inventory.iterrows():
            status_color = {'critical': '🔴', 'low': '🟡', 'stable': '🟢'}.get(row['Status'], '🟢')
            st.metric(f"{status_color} {row['Item']}", f"{row['Stock Level']} {row['Unit']}")
    
    tab1, tab2 = st.tabs(["Order Management", "Inventory Management"])
    
    # ORDER MANAGEMENT TAB
    with tab1:
        stats = get_order_stats(st.session_state.orders)
        
        if stats['queued'] > 3:
            st.markdown(f"""
            <div class="alert-box alert-warning">
                <div class="alert-title">HIGH VOLUME ALERT</div>
                <div><strong>{stats['queued']}</strong> orders in queue. Prioritize high-priority items.</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.subheader("Active Order Queue")
        
        col1, col2 = st.columns([2, 2])
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
        
        filtered_orders = st.session_state.orders[
            (st.session_state.orders['Status'].isin(status_filter)) &
            (st.session_state.orders['Priority'].isin(priority_filter))
        ].sort_values('Priority', ascending=False)
        
        for idx, row in filtered_orders.iterrows():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                status_html = create_status_badge(row['Status'])
                priority_html = create_priority_badge(row['Priority'])
                delivery_icon = "🤖" if row['Delivery Method'] == 'Robot' else "👤"
                st.markdown(f"""
                **Order #{row['Order ID']}** {status_html} {priority_html} {delivery_icon}  
                **{row['Item']}**  
                Employee: {row['Employee']} | Time: {row['Timestamp']} | Staff: {row['Assigned Staff']}  
                Delivery: {row['Delivery Method']}  
                {f'📨 Special Instructions: {row["Message"]}' if row['Message'] else ''}
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("ETA", f"{row['ETA (min)']} min")
            
            col1, col2, col3, col4 = st.columns([1.5, 1.5, 2, 2])
            
            with col1:
                if row['Status'] == 'queued':
                    if st.button("▶️ Start Prep", key=f"start_{row['Order ID']}", use_container_width=True):
                        st.session_state.orders.loc[idx, 'Status'] = 'preparing'
                        st.rerun()
            
            with col2:
                if row['Status'] == 'preparing':
                    # Create a unique key for the popover state
                    if f"show_delivery_{row['Order ID']}" not in st.session_state:
                        st.session_state[f"show_delivery_{row['Order ID']}"] = False
                    
                    if st.button("✅ Complete", key=f"done_{row['Order ID']}", use_container_width=True):
                        st.session_state[f"show_delivery_{row['Order ID']}"] = True
                        st.rerun()
                    
                    # Show delivery method selection
                    if st.session_state.get(f"show_delivery_{row['Order ID']}", False):
                        st.markdown("**Select Delivery:**")
                        delivery_col1, delivery_col2 = st.columns(2)
                        
                        with delivery_col1:
                            if st.button("👤 Staff", key=f"staff_delivery_{row['Order ID']}", use_container_width=True):
                                st.session_state.orders.loc[idx, 'Status'] = 'delivered'
                                st.session_state.orders.loc[idx, 'ETA (min)'] = 0
                                st.session_state.orders.loc[idx, 'Delivery Method'] = 'Staff'
                                st.session_state[f"show_delivery_{row['Order ID']}"] = False
                                st.success("Order completed! Staff will deliver.")
                                st.rerun()
                        
                        with delivery_col2:
                            if st.button("🤖 Robot", key=f"robot_delivery_{row['Order ID']}", use_container_width=True):
                                st.session_state.orders.loc[idx, 'Status'] = 'delivered'
                                st.session_state.orders.loc[idx, 'ETA (min)'] = 0
                                st.session_state.orders.loc[idx, 'Delivery Method'] = 'Robot'
                                st.session_state[f"show_delivery_{row['Order ID']}"] = False
                                st.success("Order completed! Robot will deliver.")
                                st.rerun()
            
            with col3:
                if row['Status'] in ['queued', 'preparing']:
                    new_staff = st.selectbox("Reassign to", KITCHEN_STAFF, 
                                             index=KITCHEN_STAFF.index(row['Assigned Staff']),
                                             key=f"staff_{row['Order ID']}")
                    if new_staff != row['Assigned Staff']:
                        if st.button("Update Staff", key=f"update_staff_{row['Order ID']}"):
                            st.session_state.orders.loc[idx, 'Assigned Staff'] = new_staff
                            st.success(f"Reassigned to {new_staff}")
                            st.rerun()
            
            with col4:
                if row['Status'] in ['queued', 'preparing']:
                    message = st.text_input("Message to employee", key=f"msg_{row['Order ID']}", 
                                           value=row['Message'], placeholder="Add notes...")
                    if message != row['Message']:
                        if st.button("Send", key=f"send_{row['Order ID']}"):
                            st.session_state.orders.loc[idx, 'Message'] = message
                            st.success("Message sent!")
                            st.rerun()
            
            st.divider()
    
    # INVENTORY MANAGEMENT TAB
    with tab2:
        st.subheader("Inventory Management")
        
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
                
                # Quick update stock
                new_stock = st.number_input(f"Update {row['Item']}", 
                                            min_value=0, 
                                            value=int(row['Stock Level']),
                                            key=f"inv_{idx}")
                if new_stock != row['Stock Level']:
                    if st.button(f"Update Stock", key=f"update_inv_{idx}"):
                        st.session_state.inventory.loc[idx, 'Stock Level'] = new_stock
                        # Update status
                        if new_stock < row['Threshold'] / 2:
                            st.session_state.inventory.loc[idx, 'Status'] = 'critical'
                        elif new_stock < row['Threshold']:
                            st.session_state.inventory.loc[idx, 'Status'] = 'low'
                        else:
                            st.session_state.inventory.loc[idx, 'Status'] = 'stable'
                        st.success(f"Updated {row['Item']} stock!")
                        st.rerun()

# ===================================
# ADMIN VIEW
# ===================================
else:
    
    with st.sidebar:
        st.header("Admin Controls")
        
        st.subheader("Reporting Period")
        time_filter = st.selectbox("Select Period", ["Today", "This Week", "This Month", "This Quarter"])
        if time_filter != st.session_state.time_filter:
            st.session_state.time_filter = time_filter
            st.rerun()
        
        st.divider()
        
        # Get filtered data based on time selection
        filtered_orders_data = filter_orders_by_time(st.session_state.orders, st.session_state.time_filter)
        stats = get_order_stats(filtered_orders_data)
        
        st.metric("Active Orders", stats['total'], delta=f"+{int(stats['total']*0.12)} from previous period")
        st.metric("Queue Depth", stats['queued'])
        st.metric(f"{st.session_state.time_filter} Revenue", f"${stats['revenue']:.2f}", delta="+8.5%")
        
        st.divider()
        
        st.subheader("Inventory Overview")
        for _, row in st.session_state.inventory.iterrows():
            status_color = {'critical': '🔴', 'low': '🟡', 'stable': '🟢'}.get(row['Status'], '🟢')
            st.metric(f"{status_color} {row['Item']}", f"{row['Stock Level']} {row['Unit']}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Executive Overview", "Employee Management", "Inventory Management", "Performance Analytics", "Reports & Export"])
    
    # TAB 1: EXECUTIVE OVERVIEW
    with tab1:
        filtered_orders_data = filter_orders_by_time(st.session_state.orders, st.session_state.time_filter)
        stats = get_order_stats(filtered_orders_data)
        
        st.info(f"📊 Showing data for: **{st.session_state.time_filter}** | Total Orders: {stats['total']}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Total Orders", 
                stats['total'],
                f"Period: {st.session_state.time_filter}",
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
                f"Avg: ${stats['revenue']/stats['total'] if stats['total'] > 0 else 0:.2f}/order",
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
        
        # AI Insights (Always On)
        st.subheader("AI-Powered Strategic Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-card insight-card-warning">
                <div class="insight-title">DEMAND FORECAST ALERT</div>
                <div class="insight-content">
                    Expected demand surge between <strong>13:30-14:30</strong>. 
                    Recommend +1 kitchen staff during peak period.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-card insight-card-success">
                <div class="insight-title">PRODUCT OPTIMIZATION</div>
                <div class="insight-content">
                    Coffee demand up <strong>23%</strong>. Consider premium coffee variants for revenue opportunity.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-card">
                <div class="insight-title">RESOURCE OPTIMIZATION</div>
                <div class="insight-content">
                    Optimal staff break: <strong>15:00-15:20</strong> based on historical low traffic.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-card insight-card-critical">
                <div class="insight-title">SUPPLY CHAIN ALERT</div>
                <div class="insight-content">
                    Critical inventory for Tea Leaves and Milk. <strong>Immediate procurement recommended</strong> within 24 hours.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Hourly Order Distribution")
            # Adjust data based on time filter
            multiplier = {"Today": 1, "This Week": 5, "This Month": 20, "This Quarter": 60}[st.session_state.time_filter]
            hourly_data = pd.DataFrame({
                'Hour': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
                'Orders': [int(x * multiplier) for x in [8, 15, 22, 35, 42, 38, 18, 12, 9]]
            })
            fig = px.bar(hourly_data, x='Hour', y='Orders', color_discrete_sequence=['#1e3a8a'])
            fig.update_layout(
                height=320, showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
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
            fig.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(family="Segoe UI", size=12))
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("---")
        
        st.subheader("Active Order Registry")
        display_orders = st.session_state.orders[['Order ID', 'Item', 'Employee', 'Status', 'Priority', 'ETA (min)', 'Timestamp', 'Assigned Staff']].copy()
        st.dataframe(display_orders, use_container_width=True, hide_index=True)
    
    # TAB 2: EMPLOYEE MANAGEMENT
    with tab2:
        st.subheader("Employee Directory & Management")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_employees = len(st.session_state.employees)
        active_employees = len(st.session_state.employees[st.session_state.employees['Status'] == 'Active'])
        on_vacation = len(st.session_state.employees[st.session_state.employees['Status'] == 'Vacation'])
        
        with col1:
            st.metric("Total Employees", total_employees)
        with col2:
            st.metric("Active", active_employees, delta=f"{(active_employees/total_employees*100):.0f}%")
        with col3:
            st.metric("On Vacation", on_vacation)
        with col4:
            st.metric("Departments", st.session_state.employees['Department'].nunique())
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dept_filter = st.multiselect(
                "Filter by Department",
                options=st.session_state.employees['Department'].unique(),
                default=st.session_state.employees['Department'].unique()
            )
        
        with col2:
            status_filter_emp = st.multiselect(
                "Filter by Status",
                options=['Active', 'Vacation'],
                default=['Active', 'Vacation']
            )
        
        with col3:
            search = st.text_input("Search by Name", placeholder="Enter employee name...")
        
        filtered_employees = st.session_state.employees[
            (st.session_state.employees['Department'].isin(dept_filter)) &
            (st.session_state.employees['Status'].isin(status_filter_emp))
        ]
        
        if search:
            filtered_employees = filtered_employees[filtered_employees['Name'].str.contains(search, case=False)]
        
        st.markdown("---")
        
        for idx, emp in filtered_employees.iterrows():
            with st.expander(f"👤 {emp['Name']} - {emp['Position']} | {create_status_badge(emp['Status'])}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    **Employee ID:** {emp['Employee ID']}  
                    **Department:** {emp['Department']}  
                    **Position:** {emp['Position']}  
                    **Join Date:** {emp['Join Date']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Email:** {emp['Email']}  
                    **Phone:** {emp['Phone']}  
                    **Status:** {emp['Status']}
                    """)
                
                with col3:
                    if emp['Status'] == 'Vacation':
                        st.markdown(f"""
                        <div class="alert-box alert-warning" style="margin: 0;">
                            <div class="alert-title">ON VACATION</div>
                            <div>
                            <strong>From:</strong> {emp['Vacation Start']}<br>
                            <strong>Until:</strong> {emp['Vacation End']}<br>
                            <strong>Replacement:</strong> {emp['Replacement']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        days_left = (pd.to_datetime(emp['Vacation End']) - pd.to_datetime(datetime.now().date())).days
                        st.info(f"Returns in {days_left} days")
                    else:
                        st.success("Currently Active")
        
        st.markdown("---")
        
        st.subheader("Vacation Calendar & Coverage Planning")
        
        vacation_employees = st.session_state.employees[st.session_state.employees['Status'] == 'Vacation']
        
        if len(vacation_employees) > 0:
            vacation_data = []
            for _, emp in vacation_employees.iterrows():
                vacation_data.append({
                    'Employee': emp['Name'],
                    'Department': emp['Department'],
                    'Start': emp['Vacation Start'],
                    'End': emp['Vacation End'],
                    'Replacement': emp['Replacement'],
                    'Days': (pd.to_datetime(emp['Vacation End']) - pd.to_datetime(emp['Vacation Start'])).days
                })
            
            vacation_df = pd.DataFrame(vacation_data)
            st.dataframe(vacation_df, use_container_width=True, hide_index=True)
        else:
            st.info("No employees currently on vacation.")
    
    # TAB 3: INVENTORY MANAGEMENT
    with tab3:
        st.subheader("Inventory Management & Control")
        
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
                        <span style="font-size: 11px; color: #64748b;">Threshold: {row['Threshold']} {row['Unit']} | Last Order: {row['Last Order']}</span>
                        <span style="font-size: 11px; color: {status_color}; font-weight: 600;">{status_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                subcol1, subcol2 = st.columns([2, 1])
                with subcol1:
                    new_stock = st.number_input(f"Update {row['Item']}", 
                                                min_value=0, 
                                                value=int(row['Stock Level']),
                                                key=f"admin_inv_{idx}")
                with subcol2:
                    st.write("")
                    st.write("")
                    if st.button(f"Update", key=f"admin_update_inv_{idx}"):
                        st.session_state.inventory.loc[idx, 'Stock Level'] = new_stock
                        if new_stock < row['Threshold'] / 2:
                            st.session_state.inventory.loc[idx, 'Status'] = 'critical'
                        elif new_stock < row['Threshold']:
                            st.session_state.inventory.loc[idx, 'Status'] = 'low'
                        else:
                            st.session_state.inventory.loc[idx, 'Status'] = 'stable'
                        st.success(f"Updated!")
                        st.rerun()
    
    # TAB 4: PERFORMANCE ANALYTICS
    with tab4:
        st.subheader("Revenue Performance Tracking")
        
        filtered_orders_data = filter_orders_by_time(st.session_state.orders, st.session_state.time_filter)
        
        revenue_multiplier = {"Today": 1, "This Week": 7, "This Month": 30, "This Quarter": 90}[st.session_state.time_filter]
        revenue_data = pd.DataFrame({
            'Time': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
            'Revenue': [int(x * revenue_multiplier) for x in [62, 135, 198, 315, 405, 342, 162, 108, 81]]
        })
        
        fig = px.line(revenue_data, x='Time', y='Revenue', markers=True, color_discrete_sequence=['#059669'])
        fig.update_layout(
            height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI", size=12),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(100,116,139,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Service Rating", "4.75/5.00", delta="+0.15")
        with col2:
            st.metric("Order Accuracy", "98.5%", delta="+1.2%")
        with col3:
            st.metric("Avg Response Time", "2.3 min", delta="-0.4 min")
        with col4:
            st.metric("Satisfaction", "96%", delta="+3%")
        
        st.markdown("---")
        
        st.subheader("Employee Feedback Overview")
        st.dataframe(st.session_state.feedback, use_container_width=True, hide_index=True)
    
    # TAB 5: REPORTS
    with tab5:
        st.subheader("Data Export & Reporting")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Order Transaction Report")
            csv_orders = st.session_state.orders.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Orders Data",
                data=csv_orders,
                file_name=f"orders_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### Employee Directory")
            csv_emp = st.session_state.employees.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Employee Data",
                data=csv_emp,
                file_name=f"employees_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            st.markdown("#### Service Feedback")
            csv_feedback = st.session_state.feedback.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Feedback Data",
                data=csv_feedback,
                file_name=f"feedback_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv", use_container_width=True
            )
# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px 0;">
    <div style="margin-bottom: 8px;">
        <strong>Enterprise Workplace Operations Platform</strong> | Version 2.1.0 | Fully Integrated System
    </div>
    <div>
        Confidential & Proprietary | For Authorized Personnel Only | {datetime.now().strftime('%B %d, %Y')}
    </div>
</div>
""", unsafe_allow_html=True)