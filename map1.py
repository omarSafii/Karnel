import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
import geopandas as gpd
import osmnx as ox
import folium
import numpy as np
from shapely.geometry import Polygon, LineString, box


# ==================== CONFIGURATION ====================
st.set_page_config(page_title="🌇 تقرير إعادة إعمار الخالدية", layout="wide", page_icon="🏗️")
ARABIC_FONT = "Tajawal, sans-serif"
COLOR_PALETTE = ["#2A9D8F", "#E76F51", "#264653", "#E9C46A", "#F4A261"]
GEOJSON_FILE = "khalidiya.geojson"

# ==================== CUSTOM STYLES ====================


st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700&display=swap');

* {{
    font-family: {ARABIC_FONT} !important;
}}

/* Vibrant header with animated gradient */
.header-container {{
    background: linear-gradient(135deg, 
        #2A9D8F 0%, 
        #264653 30%, 
        #E76F51 70%, 
        #E9C46A 100%);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    padding: 3rem;
    border-radius: 25px;
    box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    color: white;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}}

@keyframes gradientBG {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Modern stats cards with 3D effect */
.stats-card {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 5px solid {COLOR_PALETTE[0]};
}}

.stats-card:hover {{
    transform: translateY(-8px) rotateX(5deg) rotateY(-5deg);
    box-shadow: 0 15px 45px rgba(0,0,0,0.2);
}}

.stats-value {{
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(45deg, {COLOR_PALETTE[1]}, {COLOR_PALETTE[3]});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* Dynamic tabs styling */
[data-baseweb="tab-list"] {{
    gap: 15px;
    margin: 2rem 0;
}}

[data-baseweb="tab"] {{
    background: rgba(255,255,255,0.9) !important;
    border-radius: 15px !important;
    padding: 1rem 2rem !important;
    transition: all 0.3s ease !important;
    border: 2px solid {COLOR_PALETTE[2]} !important;
}}

[data-baseweb="tab"]:hover {{
    background: {COLOR_PALETTE[4]}15 !important;
}}

[aria-selected="true"] {{
    background: {COLOR_PALETTE[0]} !important;
    color: white !important;
    box-shadow: 0 4px 6px {COLOR_PALETTE[0]}40 !important;
}}

/* Enhanced map containers */
.map-container {{
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 2px solid {COLOR_PALETTE[3]};
    margin: 1.5rem 0;
}}

</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="header-container">
        <h1 style="text-align: center; margin:0; font-size: 2.8rem;">مشروع إعادة إعمار حي الخالدية</h1>
        <p style="text-align: center; margin:0.5rem 0 0; font-size: 1.2rem;">التقرير التفاعلي الشامل - تحديث 2024</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ تبويبات الصفحة -------------------
tab1, tab2, tab3 = st.tabs(["📊 الإحصاءات العامة", "🗺️ الخرائط التفاعلية", "📂 البيانات الخام"])

with tab1:
    metrics = [
        ("🏢 المباني المتضررة", "1,428", COLOR_PALETTE[1]),
        ("🚧 نسبة الدمار", "68%", COLOR_PALETTE[2]),
        ("👥 السكان المتأثرين", "4,820", COLOR_PALETTE[3]),
        ("💰 التكلفة التقديرية", "$24.5M", COLOR_PALETTE[4])
    ]
    # ------------------ بطاقات الإحصاءات -------------------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-value">1,248</div>
            <div class="stats-label">مبنى متضرر</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-value">63%</div>
            <div class="stats-label">نسبة الدمار</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-value">4.2k</div>
            <div class="stats-label">الكثافة السكانية</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-value">$18M</div>
            <div class="stats-label">تكلفة الإعمار</div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ مخطط بياني -------------------
    st.subheader("توزيع أنواع الأضرار")
    chart_data = {
        "النوع": ["كلي", "جزئي", "أساسيات", "هيكلي"],
        "النسبة": [38, 45, 12, 5]
    }
    st.bar_chart(chart_data, x="النوع", y="النسبة", use_container_width=True)

with tab2:
    # ------------------ خرائط Scribble -------------------
    with st.expander("خريطة Scribble المدمجة", expanded=True):
        components.html("""
        <iframe
            src="https://widgets.scribblemaps.com/sm/?id=7pmremiid2&z=17&type=hybrid"
            width="100%" height="600"
            frameborder="0"
            allowfullscreen
            loading="lazy">
        </iframe>
        """, height=600)

    # ------------------ خرائط Folium -------------------
    with st.expander("خريطة تحليلية متقدمة", expanded=True):
        try:
            gdf = gpd.read_file(GEOJSON_FILE).to_crs(epsg=4326)
            if not gdf.empty:
                geom = gdf.geometry.iloc[0]
                
                if isinstance(geom, LineString):
                    coords = list(geom.coords)
                    if coords[0] != coords[-1]: coords.append(coords[0])
                    geom = Polygon(coords)
                
                boundary = geom.buffer(0) if not geom.is_valid else geom
                cent = boundary.centroid
                
                m = folium.Map(location=[cent.y, cent.x], zoom_start=15, tiles="cartodbpositron")
                folium.GeoJson(
                    boundary,
                    style_function=lambda _: {"color": "red", "weight": 3}
                ).add_to(m)
                
                st_folium(m, width=1200, height=600)
                
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات: {str(e)}")

with tab3:
    # ------------------ قسم البيانات الخام -------------------
    with st.container():
        col_left, col_right = st.columns([2,1])
        
        with col_left:
            st.subheader("بيانات المباني")
            building_data = {
                "المساحة (م²)": np.random.randint(50, 300, 20),
                "الطوابق": np.random.randint(1, 6, 20),
                "حالة المبنى": np.random.choice(["مدمر", "متضرر", "سليم"], 20)
            }
            st.dataframe(building_data, use_container_width=True)
        
        with col_right:
            st.subheader("مرشحات البيانات")
            st.multiselect("حالة المبنى", options=["مدمر", "متضرر", "سليم"])
            st.slider("عدد الطوابق", 1, 5, (1,3))
            st.button("تطبيق الفلاتر")

# ------------------ تذييل الصفحة -------------------
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 1.5rem; background: #f8f9fa; border-radius: 15px;">
    <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
        <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="40">
        <img src="https://leafletjs.com/docs/images/logo.png" width="40">
        <img src="https://geopandas.org/en/stable/_images/geopandas_icon.png" width="40">
    </div>
    <p style="color: #666; margin:0;">تم تطوير النظام باستخدام أحدث التقنيات الجغرافية</p>
</div>
""", unsafe_allow_html=True)