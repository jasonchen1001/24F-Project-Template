import streamlit as st
import requests
import pandas as pd
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API URL
API_BASE_URL = "http://web-api:4000/maintenance_staff"

def fetch_alerts():
    """获取 Alert 数据"""
    try:
        with st.spinner("Loading alerts..."):
            response = requests.get(f"{API_BASE_URL}/alerts")
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data
                else:
                    st.info("No alerts available.")
                    return None
            else:
                st.error(f"Failed to fetch alerts. Status Code: {response.status_code}")
                logger.error(f"API Error: {response.text}")
                return None
    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to the server.")
        logger.error(f"Connection Error: {str(e)}")
        return None


def update_alert(alert_id, metrics, alerts, severity):
    """更新 Alert 数据"""
    try:
        with st.spinner("Updating alert..."):
            # 确保 URL 正确拼接
            url = f"{API_BASE_URL}/alerts/{alert_id}"
            
            # 构建请求数据
            data = {
                "metrics": metrics,
                "alerts": alerts,
                "severity": severity
            }
            
            # 发送 PUT 请求
            response = requests.put(url, json=data)
            
            if response.status_code == 200:
                st.success("Alert updated successfully!")
                st.rerun()
            else:
                st.error(f"Failed to update alert. Status Code: {response.status_code}")
                if response.status_code == 404:
                    st.error("Alert ID not found.")
                st.error(f"Error details: {response.text}")
    except Exception as e:
        st.error(f"Error updating alert: {str(e)}")

def main():
    st.title("Alert History Management")
    st.write("Manage alert history for databases.")

    # 获取告警数据
    with st.spinner("Loading alerts..."):
        response = requests.get(f"{API_BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()
            if alerts:
                # 转换为 DataFrame 并显示
                df = pd.DataFrame(alerts)
                st.subheader("Current Alerts")
                
                # 显示当前告警列表
                st.dataframe(
                    df,
                    hide_index=True,
                    use_container_width=True
                )

                # 编辑部分
                st.subheader("Edit Alert")
                
                # 使用 database_id 作为选项
                selected_alert = st.selectbox(
                    "Select Alert to Edit",
                    options=df["database_id"].tolist(),
                    format_func=lambda x: f"Database: {df[df['database_id']==x]['database_name'].iloc[0]} ({x})"
                )

                if selected_alert:
                    alert_data = df[df["database_id"] == selected_alert].iloc[0]
                    
                    with st.form("edit_alert_form"):
                        metrics = st.text_input("Metrics", value=alert_data["metrics"])
                        alerts_text = st.text_area("Alerts", value=alert_data["alerts"])
                        severity = st.selectbox(
                            "Severity",
                            options=["Low", "Medium", "High"],
                            index=["Low", "Medium", "High"].index(alert_data["severity"])
                        )
                        
                        if st.form_submit_button("Update Alert"):
                            update_alert(selected_alert, metrics, alerts_text, severity)
            else:
                st.info("No alerts available.")
        else:
            st.error(f"Failed to fetch alerts. Status Code: {response.status_code}")

if __name__ == "__main__":
    main()