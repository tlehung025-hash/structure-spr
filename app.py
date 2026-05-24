import streamlit as st
import pandas as pd

# Cấu hình trang hiển thị
st.set_page_config(
    page_title="SPR GLOBAL - Tính Toán Kết Cấu Móng & Đà Kiềng",
    page_icon="🏗️",
    layout="wide"
)

# Giao diện Tiêu đề chính
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>SPR GLOBAL - CÔNG CỤ TÍNH TOÁN KẾT CẤU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B5563;'>Tính Toán Móng Đơn & Đà Kiềng</h3>", unsafe_allow_html=True)
st.write("---")

# Tạo 2 cột nhập liệu: Móng đơn và Đà kiềng
col1, col2 = st.columns(2)

with col1:
    st.header("🏗️ 1. Thông Số Móng Đơn")
    tải_trọng = st.number_input("Tải trọng đứng N (kN):", min_value=0.0, value=150.0, step=10.0)
    momen_x = st.number_input("Mô-men Mx (kNm):", min_value=0.0, value=25.0, step=5.0)
    momen_y = st.number_input("Mô-men My (kNm):", min_value=0.0, value=15.0, step=5.0)
    
    st.markdown("**Kích thước móng dự kiến:**")
    b_mong = st.number_input("Chiều rộng móng B (m):", min_value=0.5, value=1.5, step=0.1)
    l_mong = st.number_input("Chiều dài móng L (m):", min_value=0.5, value=1.8, step=0.1)
    h_mong = st.number_input("Chiều cao móng H (m):", min_value=0.2, value=0.6, step=0.05)
    
    R_tc = st.number_input("Cường độ tiêu chuẩn của đất nền R_tc (kPa):", min_value=50.0, value=180.0, step=10.0)

with col2:
    st.header("🪵 2. Thông Số Đà Kiềng (Giằng Móng)")
    b_dk = st.number_input("Chiều rộng đà kiềng b (m):", min_value=0.1, value=0.22, step=0.01)
    h_dk = st.number_input("Chiều cao đà kiềng h (m):", min_value=0.2, value=0.4, step=0.05)
    l_dk = st.number_input("Chiều dài nhịp đà kiềng L_dk (m):", min_value=1.0, value=4.0, step=0.1)
    q_dk = st.number_input("Tải trọng phân bố đều trên đà kiềng q (kN/m):", min_value=0.0, value=12.0, step=1.0)

# --- PHẦN TÍNH TOÁN KẾT QUẢ ---
st.write("---")
st.header("📊 Kết Quả Kiểm Tra Đột Phá & Chịu Lực")

# 1. Tính toán móng đơn
diện_tích = b_mong * l_mong
thể_tích_móng = diện_tích * h_mong
trọng_lượng_bản_thân = thể_tích_móng * 25.0  # Khối lượng riêng bê tông cốt thép 25 kN/m3

# Ứng suất dưới đáy móng
sigma_tb = (tải_trọng + trọng_lượng_bản_thân) / diện_tích
w_x = (l_mong * (b_mong**2)) / 6
w_y = (b_mong * (l_mong**2)) / 6
sigma_max = sigma_tb + (momen_x / w_x) + (momen_y / w_y)

# 2. Tính toán đà kiềng
momen_dk_max = (q_dk * (l_dk**2)) / 8  # Sơ đồ khớp đơn giản làm ví dụ đại diện

# Hiển thị bảng so sánh đất nền móng đơn
st.subheader("Kiểm tra áp lực nền đất dưới đáy móng:")
đạt_áp_lực = sigma_max <= 1.2 * R_tc and sigma_tb <= R_tc

data_mong = {
    "Thông số kiểm tra": ["Áp lực trung bình đáy móng (σ_tb)", "Áp lực lớn nhất đáy móng (σ_max)", "Cường độ chịu tải của đất (R_tc)"],
    "Giá trị tính toán (kPa)": [f"{sigma_tb:.2f}", f"{sigma_max:.2f}", f"{R_tc:.2f}"],
    "Điều kiện kiểm tra": [f"≤ {R_tc:.2f}", f"≤ {1.2 * R_tc:.2f}", "Tiêu chuẩn thiết kế"]
}
df_mong = pd.DataFrame(data_mong)
st.table(df_mong)

if đạt_áp_lực:
    st.success("✅ Kích thước móng ĐẠT yêu cầu chịu lực của nền đất!")
else:
    st.error("❌ Kích thước móng KHÔNG ĐẠT! Vui lòng tăng bề rộng B hoặc chiều dài L của móng.")

# Hiển thị kết quả đà kiềng
st.write("---")
st.subheader("Thông số nội lực đà kiềng dự kiến:")
st.info(f"Mô-men uốn lớn nhất trong đà kiềng: **{momen_dk_max:.2f} kNm**")

# Bản quyền chân trang
st.write("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>© 2026 SPR GLOBAL Jsc. Toàn quyền bảo lưu.</p>", unsafe_allow_html=True)
