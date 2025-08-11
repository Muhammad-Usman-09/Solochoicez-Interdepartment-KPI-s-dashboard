import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO
from utils.data_loader import DataLoader
from utils.charts import ChartGenerator
from config.settings import DEPARTMENTS, COLORS

# Page configuration
st.set_page_config(
    page_title="Solochoicez Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .department-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class SolochoicezDashboard:
    def __init__(self):
        self.data_loader = DataLoader()
        self.chart_generator = ChartGenerator()
        
    def run(self):
        st.markdown('<h1 class="main-header"> Solochoicez Pvt. Ltd. - Performance Dashboard</h1>', unsafe_allow_html=True)
        self.create_sidebar()
        
        if st.session_state.get('selected_view') == 'Overview':
            self.show_overview()
        elif st.session_state.get('selected_view') == 'Information Technology':
            self.show_it_solutions()
        elif st.session_state.get('selected_view') == 'HR Solutions and Services':
            self.show_hr_staffing()
        elif st.session_state.get('selected_view') == 'Business Consulting':
            self.show_business_consulting()
        elif st.session_state.get('selected_view') == 'Data Digitization':
            self.show_data_ai_services()

    def create_sidebar(self):
        st.sidebar.title("📋 Navigation")
        
        views = ['Overview', 'Information Technology', 'HR Solutions and Services', 'Business Consulting', 'Data Digitization']
        selected_view = st.sidebar.selectbox("Select View", views)
        st.session_state['selected_view'] = selected_view
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📅 Date Range")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("From", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("To", datetime.now())
        st.session_state['date_range'] = (start_date, end_date)

        st.sidebar.markdown("### 📊 Filters")
        max_rows = st.sidebar.slider("Number of records to display", min_value=10, max_value=300, value=100, step=10)
        st.session_state['max_rows'] = max_rows

        departments = ['IT Solutions', 'HR & Staffing', 'Business Consulting', 'Data & AI Services']
        selected_departments = st.sidebar.multiselect("Select Departments", departments, default=departments)
        st.session_state['selected_departments'] = selected_departments
        
        if st.sidebar.button("🔄 Refresh Data"):
            st.rerun()

    def filter_dataset(self, df):
        # Guard: if df is None or empty return empty df
        if df is None:
            return pd.DataFrame()
        if 'department' in df.columns and st.session_state.get('selected_departments'):
            df = df[df['department'].isin(st.session_state['selected_departments'])]
        max_rows = st.session_state.get('max_rows', len(df))
        if len(df) > max_rows:
            df = df.sample(max_rows, random_state=42)
        return df

    # ---------------- NEW UTILITY FUNCTIONS ----------------
    def _to_excel_bytes(self, df: pd.DataFrame) -> bytes:
        """Return Excel file as bytes for download."""
        output = BytesIO()
        # Use ExcelWriter with xlsxwriter or openpyxl (pandas will choose available engine)
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()

    def download_buttons(self, df, filename):
        """Show CSV and Excel download buttons for a dataframe."""
        if df is None or df.empty:
            st.info("No data to download.")
            return
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, file_name=f"{filename}.csv", mime="text/csv")
        try:
            excel_bytes = self._to_excel_bytes(df)
            st.download_button("📥 Download Excel", excel_bytes, file_name=f"{filename}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception:
            # Fallback: offer CSV only if excel writer missing
            pass

    def styled_dataframe(self, df):
        """Return a pandas Styler with conditional row background based on 'status' column.
           If 'status' not present or df empty, returns df as-is (DataFrame)."""
        if df is None or df.empty:
            return df  # empty DataFrame
        if 'status' in df.columns:
            def highlight_row(row):
                color_map = {
                    "On Hold": "#ffe6e6",
                    "Planning": "#fff4e6",
                    "Completed": "#e6ffe6",
                    "Active": "#e6f0ff"
                }
                bg = color_map.get(row["status"], "white")
                return [f'background-color: {bg}' for _ in row]
            try:
                sty = df.style.apply(highlight_row, axis=1)
                return sty
            except Exception:
                # If styler fails for any reason, return raw df
                return df
        return df

    def mini_kpi_chart(self, values, title):
        """Small trend chart below KPI. Accepts iterable of numeric values."""
        # Ensure there is at least one numeric point
        if not values:
            return
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=list(values), mode='lines+markers', line=dict(color="#1f77b4"), marker=dict(size=6)))
        fig.update_layout(
            height=100,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            title=dict(text=title, x=0.01, xanchor='left', yanchor='top', font=dict(size=10))
        )
        st.plotly_chart(fig, use_container_width=True)
    # --------------------------------------------------------

    def show_overview(self):
        st.markdown("## 📊 Company Overview")
        it_data = self.filter_dataset(self.data_loader.load_it_solutions_data())
        hr_data = self.filter_dataset(self.data_loader.load_hr_staffing_data())
        consulting_data = self.filter_dataset(self.data_loader.load_consulting_data())
        ai_data = self.filter_dataset(self.data_loader.load_ai_services_data())
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_projects = (0 if it_data is None else len(it_data)) + (0 if consulting_data is None else len(consulting_data)) + (0 if ai_data is None else len(ai_data))
            st.metric("Total Active Projects", total_projects, delta=5)
            # sample trend: last 3 months + current
            self.mini_kpi_chart([max(0, total_projects-3), max(0, total_projects-1), total_projects], "Projects Trend")
        with col2:
            total_employees = 0 if hr_data is None else len(hr_data)
            st.metric("Total Employees", total_employees, delta=12)
            self.mini_kpi_chart([max(0, total_employees-10), max(0, total_employees-5), total_employees], "Employees Trend")
        with col3:
            total_revenue = 2500000  # Sample data (kept as-is)
            st.metric("Monthly Revenue (PKR)", f"{total_revenue:,}", delta="15%")
            # revenue trend (sample numbers)
            self.mini_kpi_chart([int(total_revenue*0.85/1e5), int(total_revenue*0.9/1e5), int(total_revenue/1e5)], "Revenue Trend (×1e5)")
        with col4:
            client_satisfaction = 94.5
            st.metric("Client Satisfaction", f"{client_satisfaction}%", delta="2.1%")
            self.mini_kpi_chart([90, 92, client_satisfaction], "Satisfaction Trend")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            dept_revenue = {'IT Solutions': 1200000, 'HR & Staffing': 400000, 'Business Consulting': 600000, 'Data & AI Services': 300000}
            fig_revenue = px.pie(values=list(dept_revenue.values()), names=list(dept_revenue.keys()), title="Revenue Distribution by Department", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_revenue, use_container_width=True)
        with col2:
            project_status = {'Completed': 45, 'In Progress': 32, 'Planning': 18, 'On Hold': 5}
            fig_status = px.bar(x=list(project_status.keys()), y=list(project_status.values()), title="Project Status Overview", color=list(project_status.keys()), color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_status, use_container_width=True)

        # Provide overview-level raw data downloads (concatenate datasets if present)
        st.markdown("### 🔽 Download Overview Data")
        combined_frames = []
        for df in [it_data, hr_data, consulting_data, ai_data]:
            if isinstance(df, pd.DataFrame) and not df.empty:
                combined_frames.append(df.assign(source_df=df.__class__.__name__))
        if combined_frames:
            overview_df = pd.concat(combined_frames, ignore_index=True, sort=False)
            self.download_buttons(overview_df, "overview_data")
            st.dataframe(self.styled_dataframe(overview_df), use_container_width=True)
        else:
            st.info("No data available in overview to display or download.")

    def show_it_solutions(self):
        st.markdown('<div class="department-header">💻 Information Technology</div>', unsafe_allow_html=True)
        data = self.filter_dataset(self.data_loader.load_it_solutions_data() )

        # Safeguards for missing columns / empty data
        if data is None or data.empty:
            st.info("No IT data available.")
            return

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            active_projects = len(data[data['status'] == 'Active']) if 'status' in data.columns else 0
            st.metric("Active Projects", active_projects)
            self.mini_kpi_chart([max(0, active_projects-2), max(0, active_projects-1), active_projects], "Active Projects Trend")
        with col2:
            completed_projects = len(data[data['status'] == 'Completed']) if 'status' in data.columns else 0
            st.metric("Completed Projects", completed_projects)
            self.mini_kpi_chart([max(0, completed_projects-3), max(0, completed_projects-1), completed_projects], "Completed Trend")
        with col3:
            try:
                avg_completion = data['completion_percentage'].mean() if 'completion_percentage' in data.columns else 0
            except Exception:
                avg_completion = 0
            st.metric("Avg Completion", f"{avg_completion:.1f}%")
            self.mini_kpi_chart([max(0, avg_completion-5), max(0, avg_completion-2), avg_completion], "Avg Completion Trend")
        with col4:
            try:
                total_budget = data['budget'].sum() if 'budget' in data.columns else 0
            except Exception:
                total_budget = 0
            st.metric("Total Budget", f"PKR{total_budget:,.0f}")
            self.mini_kpi_chart([max(0, total_budget*0.9), total_budget, total_budget], "Budget Trend")

        col1, col2 = st.columns(2)
        with col1:
            fig_progress = px.bar(data, x='project_name', y='completion_percentage', title="Project Completion Progress", color='completion_percentage', color_continuous_scale='Viridis') if 'project_name' in data.columns and 'completion_percentage' in data.columns else None
            if fig_progress:
                fig_progress.update_layout(xaxis=dict(tickangle=45))
                st.plotly_chart(fig_progress, use_container_width=True)
            else:
                st.info("Not enough columns to plot 'Project Completion Progress'.")
        with col2:
            if 'technology' in data.columns:
                tech_counts = data['technology'].value_counts()
                fig_tech = px.pie(values=tech_counts.values, names=tech_counts.index, title="Technology Stack Distribution")
                st.plotly_chart(fig_tech, use_container_width=True)
            else:
                st.info("No 'technology' column available for Technology Stack Distribution.")

        st.markdown("### 📋 Project Details")
        self.download_buttons(data, "it_solutions")
        st.dataframe(self.styled_dataframe(data), use_container_width=True)


    def show_hr_staffing(self):
        st.markdown('<div class="department-header">👥 HR Solutions & Services</div>', unsafe_allow_html=True)
        
        data = self.filter_dataset(self.data_loader.load_hr_staffing_data())

        if data is None or data.empty:
            st.info("No HR data available.")
            return

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Employees", len(data))
            self.mini_kpi_chart([max(0, len(data)-10), max(0, len(data)-5), len(data)], "Employees Trend")
        with col2:
            try:
                avg_perf = data['performance_score'].mean() if 'performance_score' in data.columns else 0
            except Exception:
                avg_perf = 0
            st.metric("Avg Performance", f"{avg_perf:.1f}/10")
            self.mini_kpi_chart([max(0, avg_perf-1), avg_perf, avg_perf], "Performance Trend")
        with col3:
            active_employees = len(data[data['status'] == 'Active']) if 'status' in data.columns else 0
            st.metric("Active Employees", active_employees)
            self.mini_kpi_chart([max(0, active_employees-2), active_employees, active_employees], "Active Employees Trend")
        with col4:
            try:
                avg_salary = data['salary'].mean() if 'salary' in data.columns else 0
            except Exception:
                avg_salary = 0
            st.metric("Avg Salary", f"PKR{avg_salary:,.0f}")
            self.mini_kpi_chart([max(0, avg_salary*0.95), avg_salary, avg_salary], "Salary Trend")

        col1, col2 = st.columns(2)
        with col1:
            if 'department' in data.columns:
                dept_counts = data['department'].value_counts()
                fig_dept = px.bar(
                    x=dept_counts.index, y=dept_counts.values,
                    title="Employee Distribution by Department",
                    color=dept_counts.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_dept, use_container_width=True)
            else:
                st.info("No 'department' column available for Employee Distribution.")
        with col2:
            if 'performance_score' in data.columns and 'salary' in data.columns:
                if 'experience_years' in data.columns:
                    fig_perf = px.scatter(
                        data, x='performance_score', y='salary',
                        title="Performance vs Salary Analysis",
                        color='department' if 'department' in data.columns else None,
                        size='experience_years'
                    )
                else:
                    fig_perf = px.scatter(
                        data, x='performance_score', y='salary',
                        title="Performance vs Salary Analysis",
                        color='department' if 'department' in data.columns else None
                    )
                st.plotly_chart(fig_perf, use_container_width=True)
            else:
                st.info("Not enough columns to plot Performance vs Salary Analysis.")

        st.markdown("### 👤 Employee Details")
        self.download_buttons(data, "hr_staffing")
        st.dataframe(self.styled_dataframe(data), use_container_width=True)

    def show_business_consulting(self):
        st.markdown('<div class="department-header">📈 Business Consulting</div>', unsafe_allow_html=True)
        
        data = self.filter_dataset(self.data_loader.load_consulting_data())

        if data is None or data.empty:
            st.info("No Consulting data available.")
            return

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            active_cons = len(data[data['status'] == 'Active']) if 'status' in data.columns else 0
            st.metric("Active Consultations", active_cons)
            self.mini_kpi_chart([max(0, active_cons-2), active_cons, active_cons], "Active Consultations Trend")
        with col2:
            try:
                avg_duration = data['duration_months'].mean() if 'duration_months' in data.columns else 0
            except Exception:
                avg_duration = 0
            st.metric("Avg Duration", f"{avg_duration:.1f} months")
            self.mini_kpi_chart([max(0, avg_duration-2), avg_duration, avg_duration], "Duration Trend")
        with col3:
            try:
                total_value = data['project_value'].sum() if 'project_value' in data.columns else 0
            except Exception:
                total_value = 0
            st.metric("Total Value", f"PKR{total_value:,.0f}")
            self.mini_kpi_chart([max(0, total_value*0.9), total_value, total_value], "Project Value Trend")
        with col4:
            try:
                client_sat = data['client_satisfaction'].mean() if 'client_satisfaction' in data.columns else 0
            except Exception:
                client_sat = 0
            st.metric("Client Satisfaction", f"{client_sat:.1f}/10")
            self.mini_kpi_chart([max(0, client_sat-1), client_sat, client_sat], "Client Satisfaction Trend")

        col1, col2 = st.columns(2)
        with col1:
            if 'consulting_area' in data.columns:
                area_counts = data['consulting_area'].value_counts()
                fig_area = px.pie(
                    values=area_counts.values,
                    names=area_counts.index,
                    title="Consulting Areas Distribution"
                )
                st.plotly_chart(fig_area, use_container_width=True)
            else:
                st.info("No 'consulting_area' column available for Consulting Areas Distribution.")
        with col2:
            if all(c in data.columns for c in ['start_date', 'end_date', 'client_name']):
                fig_timeline = px.timeline(
                    data, x_start='start_date', x_end='end_date', y='client_name',
                    title="Project Timeline", color='status' if 'status' in data.columns else None
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            else:
                st.info("Not enough columns to plot Project Timeline (needs start_date, end_date, client_name).")

        st.markdown("### 📊 Consulting Projects")
        self.download_buttons(data, "business_consulting")
        st.dataframe(self.styled_dataframe(data), use_container_width=True)

    def show_data_ai_services(self):
        st.markdown('<div class="department-header">🤖 Data Digitization</div>', unsafe_allow_html=True)
        
        data = self.filter_dataset(self.data_loader.load_ai_services_data())

        if data is None or data.empty:
            st.info("No Data & AI Services data available.")
            return

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            active_ai = len(data[data['status'] == 'Active']) if 'status' in data.columns else 0
            st.metric("Active AI Projects", active_ai)
            self.mini_kpi_chart([max(0, active_ai-1), active_ai, active_ai], "Active AI Trend")
        with col2:
            try:
                avg_acc = data['model_accuracy'].mean() if 'model_accuracy' in data.columns else 0
            except Exception:
                avg_acc = 0
            st.metric("Avg Model Accuracy", f"{avg_acc:.1f}%")
            self.mini_kpi_chart([max(0, avg_acc-2), avg_acc, avg_acc], "Model Accuracy Trend")
        with col3:
            try:
                data_vol = data['data_volume_gb'].sum() if 'data_volume_gb' in data.columns else 0
            except Exception:
                data_vol = 0
            st.metric("Data Processed", f"{data_vol:.0f} GB")
            self.mini_kpi_chart([max(0, data_vol-50), data_vol, data_vol], "Data Volume Trend")
        with col4:
            try:
                auto_savings = data['automation_savings'].sum() if 'automation_savings' in data.columns else 0
            except Exception:
                auto_savings = 0
            st.metric("Automation Savings", f"PKR{auto_savings:,.0f}")
            self.mini_kpi_chart([max(0, auto_savings*0.9), auto_savings, auto_savings], "Automation Savings Trend")

        col1, col2 = st.columns(2)
        with col1:
            if 'service_type' in data.columns:
                service_counts = data['service_type'].value_counts()
                fig_service = px.bar(
                    x=service_counts.index, y=service_counts.values,
                    title="AI Service Types",
                    color=service_counts.values
                )
                st.plotly_chart(fig_service, use_container_width=True)
            else:
                st.info("No 'service_type' column available for AI Service Types.")
        with col2:
            if all(c in data.columns for c in ['data_volume_gb', 'model_accuracy']):
                fig_accuracy = px.scatter(
                    data, x='data_volume_gb', y='model_accuracy',
                    title="Data Volume vs Model Accuracy",
                    color='service_type' if 'service_type' in data.columns else None,
                    size='automation_savings' if 'automation_savings' in data.columns else None
                )
                st.plotly_chart(fig_accuracy, use_container_width=True)
            else:
                st.info("Not enough columns to plot Data Volume vs Model Accuracy.")

        st.markdown("### 🔬 AI Projects Details")
        self.download_buttons(data, "data_ai_services")
        st.dataframe(self.styled_dataframe(data), use_container_width=True)

if __name__ == "__main__":
    dashboard = SolochoicezDashboard()
    dashboard.run()