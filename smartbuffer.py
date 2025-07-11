import streamlit as st
import math
import numpy as np
from typing import Optional, Dict, Tuple

# Inisialisasi konfigurasi halaman
def setup_page():
    """Konfigurasi awal halaman Streamlit"""
    st.set_page_config(
        page_title="SmartBuffer",
        page_icon="🧪",
        layout="wide"
    )
    
    # CSS styling
    st.markdown("""
    <style>
        .ph-scale {
            height: 30px;
            background: linear-gradient(to right, #e74c3c, #f39c12, #f1c40f, #2ecc71, #3498db);
            border-radius: 15px;
            margin: 20px 0;
            position: relative;
        }
        .ph-marker {
            position: absolute;
            top: -20px;
            transform: translateX(-50%);
            font-size: 12px;
        }
        .ph-indicator {
            position: absolute;
            top: -10px;
            width: 10px;
            height: 50px;
            background-color: #2c3e50;
            transform: translateX(-50%);
            border-radius: 5px;
        }
        .result-box {
            padding: 20px;
            background-color: #e8f4fc;
            border-radius: 10px;
            margin-top: 20px;
        }
        .warning-box {
            padding: 15px;
            background-color: #fff3cd;
            border-radius: 8px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Fungsi untuk memeriksa dan mengimpor matplotlib dengan aman
def safe_import_matplotlib() -> Optional[object]:
    """Mengimpor matplotlib dengan penanganan error yang baik"""
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Fitur Grafik Dinonaktifkan:</strong> Matplotlib tidak ditemukan.<br>
            Untuk mengaktifkan fitur grafik, jalankan: <code>pip install matplotlib</code>
        </div>
        """, unsafe_allow_html=True)
        return None

# Inisialisasi plt dengan penanganan error
plt = safe_import_matplotlib()

class PHCalculator:
    """Kelas utama untuk perhitungan pH"""
    
    SOLUTION_TYPES = [
        "Asam Kuat",
        "Asam Lemah",
        "Basa Kuat",
        "Basa Lemah",
        "Buffer Asam",
        "Buffer Basa"
    ]
    
    @staticmethod
    def calculate_ph(
        solution_type: str,
        concentration: float,
        ka: Optional[float] = None,
        kb: Optional[float] = None,
        salt_concentration: Optional[float] = None
    ) -> Dict[str, float]:
        """Menghitung pH berdasarkan jenis larutan"""
        result = {"ph": 7.0, "explanation": ""}
        
        try:
            if solution_type == "Asam Kuat":
                if concentration <= 0:
                    raise ValueError("Konsentrasi harus > 0")
                h_plus = concentration
                ph = -math.log10(h_plus)
                result["ph"] = ph
                result["explanation"] = (
                    f"pH larutan asam kuat dengan konsentrasi {concentration:.3f} M adalah {ph:.2f}. "
                    "Asam kuat terionisasi sempurna dalam air."
                )
            
            elif solution_type == "Asam Lemah":
                if not ka or ka <= 0:
                    raise ValueError("Ka harus > 0")
                if concentration <= 0:
                    raise ValueError("Konsentrasi harus > 0")
                h_plus = math.sqrt(ka * concentration)
                ph = -math.log10(h_plus)
                result["ph"] = ph
                result["explanation"] = (
                    f"pH larutan asam lemah dengan konsentrasi {concentration:.3f} M "
                    f"dan Ka = {ka:.2e} adalah {ph:.2f}."
                )
            
            # Implementasi serupa untuk jenis larutan lainnya...
            # (Basa Kuat, Basa Lemah, Buffer Asam, Buffer Basa)
            
        except ValueError as e:
            result["ph"] = 7.0
            result["explanation"] = f"Error: {str(e)}"
        except Exception as e:
            result["ph"] = 7.0
            result["explanation"] = "Terjadi kesalahan dalam perhitungan."
        
        return result

def display_ph_scale(ph_value: float) -> None:
    """Menampilkan visualisasi skala pH"""
    ph_percentage = max(0, min(100, (ph_value / 14) * 100))
    ph_color = "#2c3e50"  # Warna default
    
    if ph_value < 3:
        ph_color = "#e74c3c"
    elif ph_value < 6:
        ph_color = "#f39c12"
    elif ph_value < 8:
        ph_color = "#f1c40f"
    elif ph_value < 11:
        ph_color = "#2ecc71"
    else:
        ph_color = "#3498db"
    
    st.markdown(f"""
    <div class="ph-scale">
        <span class="ph-marker" style="left: 0%;">0</span>
        <span class="ph-marker" style="left: 16.66%;">2</span>
        <span class="ph-marker" style="left: 33.33%;">4</span>
        <span class="ph-marker" style="left: 50%;">7</span>
        <span class="ph-marker" style="left: 66.66%;">10</span>
        <span class="ph-marker" style="left: 83.33%;">12</span>
        <span class="ph-marker" style="left: 100%;">14</span>
        <div class="ph-indicator" style="left: {ph_percentage}%; background-color: {ph_color};"></div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Fungsi utama aplikasi"""
    setup_page()
    st.title("🧪 SmartBuffer - Kalkulator pH Asam Basa")
    st.markdown("Aplikasi untuk menghitung pH berbagai jenis larutan asam-basa dan buffer")
    
    with st.form("ph_calculation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            solution_type = st.selectbox(
                "Jenis Larutan:",
                options=PHCalculator.SOLUTION_TYPES,
                index=0
            )
            
            concentration = st.number_input(
                "Konsentrasi (M):",
                min_value=0.0,
                max_value=10.0,
                step=1e-3,
                format="%.3f",
                value=0.1
            )
            
            if solution_type in ["Asam Lemah", "Buffer Asam"]:
                ka = st.number_input(
                    "Konstanta Keasaman (Ka):",
                    min_value=0.0,
                    step=1e-10,
                    format="%.10f",
                    value=1.8e-5
                )
            
            if solution_type in ["Basa Lemah", "Buffer Basa"]:
                kb = st.number_input(
                    "Konstanta Kebasaan (Kb):",
                    min_value=0.0,
                    step=1e-10,
                    format="%.10f",
                    value=1.8e-5
                )
            
            if solution_type in ["Buffer Asam", "Buffer Basa"]:
                salt_concentration = st.number_input(
                    "Konsentrasi Garam (M):",
                    min_value=0.0,
                    step=1e-3,
                    format="%.3f",
                    value=0.1
                )
        
        submitted = st.form_submit_button("Hitung pH", use_container_width=True)
        
        if submitted:
            result = PHCalculator.calculate_ph(
                solution_type,
                concentration,
                ka if solution_type in ["Asam Lemah", "Buffer Asam"] else None,
                kb if solution_type in ["Basa Lemah", "Buffer Basa"] else None,
                salt_concentration if solution_type in ["Buffer Asam", "Buffer Basa"] else None
            )
            
            with col2:
                with st.expander("Hasil Perhitungan", expanded=True):
                    st.markdown(f"### pH = {result['ph']:.2f}")
                    display_ph_scale(result['ph'])
                    st.markdown(f"**Penjelasan:** {result['explanation']}")

if __name__ == "__main__":
    main()
