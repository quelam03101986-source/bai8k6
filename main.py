import sqlite3
import requests
import streamlit as st


# database
def create_table():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS favorite_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL UNIQUE,
            added_date TEXT,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()


# weather api

API_KEY = "1386194825985e3fa8d19f01c3819826"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name):
    try:
        url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric&lang=vi" # tạo URL
        response = requests.get(url) # tao y/c len server

        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }
        return None
    except Exception:
        return None


# giao diện

def setup_page():
    st.set_page_config(
        page_title="Dự Báo Thời Tiết",
        page_icon="⛅",
        layout="centered"
    )

    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #87CEEB, #E0F7FA);
        }
        </style>
    """, unsafe_allow_html=True)


def show_header():
    st.title("⛅ App Thời Tiết Thông Minh")
    st.markdown("Nhập tên thành phố để xem nhiệt độ hiện tại.")
    st.markdown("---")


# code chính

create_table() # ham tao CSDL
setup_page() # ham cai giao dien
show_header() # ham tao tieu de

st.subheader("🔍 Tra cứu")
col1, col2 = st.columns([3, 1])

with col1:
    city_input = st.text_input(
        "Nhập tên thành phố",
        placeholder="Hanoi, Hong Kong, New York..."
    )

with col2:
    st.write("")
    st.write("")
    search_btn = st.button("Xem")

if search_btn and city_input:
    with st.spinner('Đang tải...'):
        data = get_weather(city_input)

    if data:
        st.success(f"{data['city']}")

        col_a, col_b = st.columns(2) # chia 2 cot = nhau

        with col_a:
            icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@4x.png"
            st.image(icon_url, width=120)
            st.caption(data['description'].capitalize())

        with col_b:
            st.metric("Nhiệt độ", f"{data['temp']} °C")
            st.metric("Độ ẩm", f"{data['humidity']} %")

    else:
        st.error("Không tìm thấy thành phố!")

st.markdown("---")
st.caption("Tip: dùng 'Ho Chi Minh' hoặc 'Saigon'")
