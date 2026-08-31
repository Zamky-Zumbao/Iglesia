import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ===== CONFIGURACIÓN =====
st.set_page_config(
    page_title="Bodega Iglesia",
    page_icon="🏪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== COLORES =====
COLOR_LOGO = "#1a237e"
COLOR_FONDO = "#0d47a1"
COLOR_PRIMARIO = "#1E3A8A"
COLOR_SECUNDARIO = "#3B82F6"
COLOR_ACENTO = "#06B6D4"
COLOR_EXITO = "#10B981"
COLOR_ALERTA = "#F59E0B"
COLOR_PELIGRO = "#EF4444"
COLOR_TEXTO = "#1E293B"

# ===== CSS =====
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fredoka:wght@600;700&display=swap');

    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    :root {{
        --primario: {COLOR_PRIMARIO};
        --secundario: {COLOR_SECUNDARIO};
        --acento: {COLOR_ACENTO};
        --exito: {COLOR_EXITO};
        --alerta: {COLOR_ALERTA};
        --peligro: {COLOR_PELIGRO};
        --texto: {COLOR_TEXTO};
        --durazno: #F4A97F;
        --radio: 16px;
        --sombra: 0 8px 24px rgba(15, 23, 42, 0.10);
        --sombra-hover: 0 12px 32px rgba(15, 23, 42, 0.18);
    }}

    /* ===== FONDO GENERAL ===== */
    .stApp {{
        background:
            radial-gradient(circle at 15% 0%, rgba(59,130,246,0.35), transparent 45%),
            radial-gradient(circle at 90% 10%, rgba(6,182,212,0.25), transparent 40%),
            linear-gradient(160deg, #0B1E4D 0%, {COLOR_PRIMARIO} 45%, #0d47a1 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }}

    /* Limita el ancho en pantallas grandes para que no se vea "estirado" en tablet/desktop */
    .block-container {{
        max-width: 720px;
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1rem;
        padding-right: 1rem;
        margin: 0 auto;
    }}

    #MainMenu, footer[data-testid="stFooter"], header[data-testid="stHeader"] {{
        background: transparent;
    }}

    /* ===== BOTONES ===== */
    .stButton > button {{
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.2px;
        padding: 16px 14px !important;
        min-height: 56px;
        line-height: 1.25 !important;
        white-space: pre-line !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
        box-shadow: var(--sombra) !important;
        width: 100% !important;
        background: rgba(255, 255, 255, 0.97) !important;
        color: var(--primario) !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: var(--sombra-hover) !important;
        background: linear-gradient(135deg, var(--primario), var(--secundario)) !important;
        color: white !important;
        border-color: transparent !important;
    }}
    .stButton > button:active {{
        transform: translateY(0) scale(0.98) !important;
    }}
    /* Botones de acción principal (Registrar / Guardar) resaltados */
    .stButton > button:has(div p:first-child:only-child) {{}}

    /* ===== BOTONES MENÚ PRINCIPAL (compactos, 1 fila) ===== */
    .st-key-home-menu .stButton > button {{
        min-height: 40px !important;
        padding: 8px 4px !important;
        font-size: clamp(11px, 3.4vw, 14px) !important;
        white-space: nowrap !important;
        gap: 4px;
    }}
    .st-key-home-menu div[data-testid="column"] {{
        padding: 0 3px !important;
    }}

    /* ===== HEADER ===== */
    .app-header {{
        text-align: center;
        padding: 6px 0 2px 0;
    }}
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        flex-wrap: wrap;
    }}
    .header-container img {{
        width: clamp(48px, 12vw, 68px);
        height: clamp(48px, 12vw, 68px);
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }}
    .header-title {{
        font-family: 'Fredoka', 'Inter', sans-serif;
        font-size: clamp(24px, 7vw, 38px);
        font-weight: 700;
        color: var(--durazno) !important;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.35);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}

    hr {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.18) !important;
        margin: 1.1rem 0 !important;
    }}

    /* ===== TITULOS DE SECCIÓN ===== */
    h1, h2, h3, h4 {{
        color: white !important;
        font-weight: 800 !important;
    }}
    h3 {{
        font-size: clamp(18px, 4.5vw, 22px) !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    h4 {{
        font-size: clamp(15px, 4vw, 17px) !important;
        color: rgba(255,255,255,0.95) !important;
        margin-top: 0.6rem !important;
    }}

    /* ===== TARJETAS DE MÉTRICAS ===== */
    .metric-card {{
        background: rgba(255, 255, 255, 0.97) !important;
        border-radius: var(--radio);
        padding: 16px 10px;
        text-align: center;
        box-shadow: var(--sombra);
        border-top: 4px solid var(--primario);
        margin-bottom: 12px;
        transition: transform 0.15s ease;
    }}
    .metric-card:hover {{ transform: translateY(-3px); }}
    .metric-card.green {{ border-top-color: var(--exito); }}
    .metric-card.blue {{ border-top-color: var(--acento); }}
    .metric-card.orange {{ border-top-color: var(--alerta); }}

    .metric-value {{
        font-size: clamp(22px, 6vw, 30px);
        font-weight: 800;
        margin: 4px 0 2px 0;
        color: var(--texto);
    }}
    .metric-label {{
        font-size: 11.5px;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* ===== TARJETA DE MOVIMIENTO / REGISTRO ===== */
    .item-card {{
        background: rgba(255,255,255,0.97);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 8px;
        border-left: 4px solid var(--secundario);
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }}
    .item-card .hora {{
        color: var(--primario);
        font-weight: 700;
    }}
    .item-card .motivo {{
        color: #64748B;
        font-size: 12.5px;
    }}
    .success-box {{
        background: rgba(220, 252, 231, 0.97) !important;
        border-radius: var(--radio);
        padding: 16px;
        border-left: 5px solid var(--exito);
        box-shadow: var(--sombra);
        color: var(--texto);
    }}

    /* ===== FOOTER ===== */
    .footer {{
        text-align: center;
        color: rgba(255,255,255,0.85);
        font-size: 12.5px;
        font-weight: 500;
        margin-top: 20px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: var(--radio);
        padding: 14px;
        backdrop-filter: blur(6px);
        line-height: 1.7;
    }}

    /* ===== INPUTS ===== */
    .stSelectbox > div > div, .stNumberInput > div > div, .stTextInput > div > div {{
        background: rgba(255,255,255,0.97) !important;
        border-radius: 12px !important;
        box-shadow: var(--sombra);
    }}
    label, .stMarkdown p {{
        color: white !important;
        font-weight: 600 !important;
    }}
    .stSelectbox label, .stNumberInput label, .stTextInput label {{
        font-size: 13.5px !important;
    }}

    /* ===== ALERTAS / MENSAJES ===== */
    .stAlert {{
        background: rgba(255,255,255,0.97) !important;
        backdrop-filter: blur(6px);
        border-radius: var(--radio) !important;
        box-shadow: var(--sombra);
    }}
    .stAlert p {{ color: var(--texto) !important; font-weight: 500 !important; }}

    /* ===== TABLA / DATAFRAME ===== */
    [data-testid="stDataFrame"] {{
        border-radius: var(--radio);
        overflow: hidden;
        box-shadow: var(--sombra);
    }}

    /* ===== RESPONSIVE: CELULARES ===== */
    @media (max-width: 480px) {{
        .block-container {{
            padding-left: 0.6rem;
            padding-right: 0.6rem;
            padding-top: 0.8rem !important;
        }}
        .stButton > button {{
            font-size: 14px !important;
            padding: 14px 8px !important;
            min-height: 52px;
        }}
        .header-container img {{
            width: 46px;
            height: 46px;
        }}
        div[data-testid="column"] {{
            padding: 0 4px !important;
        }}
    }}

    /* ===== RESPONSIVE: TABLETS ===== */
    @media (min-width: 481px) and (max-width: 1024px) {{
        .block-container {{
            max-width: 680px;
        }}
    }}

    /* ===== PANTALLAS GRANDES ===== */
    @media (min-width: 1025px) {{
        .block-container {{
            max-width: 760px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ===== HEADER CON LOGO + TÍTULO =====
LOGO_URL = "https://i.ibb.co/d4NTj1CV/logo.png"

st.markdown(f"""
<div class="app-header">
    <div class="header-container">
        <img src="{LOGO_URL}" alt="Logo Iglesia">
        <span class="header-title">Control Inventario</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== BASE DE DATOS =====
DB_NAME = "inventario.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        stock_actual INTEGER DEFAULT 0,
        stock_minimo INTEGER DEFAULT 4,
        unidad TEXT DEFAULT 'unidades'
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        tipo TEXT,
        cantidad INTEGER,
        stock_anterior INTEGER,
        stock_nuevo INTEGER,
        motivo TEXT,
        documento TEXT,
        usuario TEXT,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute("SELECT COUNT(*) FROM productos")
    if c.fetchone()[0] == 0:
        productos_excel = [
            # ===== ASEO (26 artículos) =====
            ('Bolsa Basura 50x70', 'ASEO', 50, 4, 'unidades'),
            ('Bolsa Basura 70x90', 'ASEO', 50, 4, 'unidades'),
            ('Bolsa Basura 90x120', 'ASEO', 50, 4, 'unidades'),
            ('Bolsa Camiseta', 'ASEO', 50, 4, 'unidades'),
            ('Cloro Gel', 'ASEO', 50, 4, 'unidades'),
            ('Desengrasante', 'ASEO', 50, 4, 'unidades'),
            ('Desinfectante Baño', 'ASEO', 50, 4, 'unidades'),
            ('Desodorante Ambiental', 'ASEO', 50, 4, 'unidades'),
            ('Detergente Polvo', 'ASEO', 50, 4, 'unidades'),
            ('Escobas Pisos', 'ASEO', 50, 4, 'unidades'),
            ('Esponjas Lavaplatos', 'ASEO', 50, 4, 'unidades'),
            ('Guantes Latex', 'ASEO', 50, 4, 'unidades'),
            ('Insecticiada', 'ASEO', 50, 4, 'unidades'),
            ('Jabón', 'ASEO', 50, 4, 'unidades'),
            ('Lava Lozas', 'ASEO', 50, 4, 'unidades'),
            ('Limpia Piso Poet', 'ASEO', 50, 4, 'unidades'),
            ('Limpia Vidrio', 'ASEO', 50, 4, 'unidades'),
            ('Limpiador en Crema', 'ASEO', 50, 4, 'unidades'),
            ('Lustra Muebles', 'ASEO', 50, 4, 'unidades'),
            ('Palas Aseo', 'ASEO', 50, 4, 'unidades'),
            ('Paños Amarillos', 'ASEO', 50, 4, 'unidades'),
            ('Removedor de Sarro', 'ASEO', 50, 4, 'unidades'),
            ('Toalla Desinfectante', 'ASEO', 50, 4, 'unidades'),
            ('Trapero Micro Fibra', 'ASEO', 50, 4, 'unidades'),
            ('Traperos Húmedos', 'ASEO', 50, 4, 'unidades'),
            ('Virutillas', 'ASEO', 50, 4, 'unidades'),
            
            # ===== BAÑO (3 artículos) =====
            ('Papel Higiénico', 'BAÑO', 50, 4, 'unidades'),
            ('Toalla Papel 100 Mts', 'BAÑO', 50, 4, 'unidades'),
            ('Toalla Papel Rollo Baño', 'BAÑO', 50, 4, 'unidades'),
            
            # ===== CONSUMIBLES (15 artículos) =====
            ('Aceite', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Agua Mineral con Gas', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Agua Mineral sin Gas', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Azúcar', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Café', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Dulces Bienvenida', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Endulzante', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Galletas Mini', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Galletas Variedades Bienvenida', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Jugo Instantáneo', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Jugos en Caja Individual', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Latas de Bebida', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Pan', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Sal', 'CONSUMIBLES', 50, 4, 'unidades'),
            ('Té Caja 100 Bolsas', 'CONSUMIBLES', 50, 4, 'unidades'),
            
            # ===== DESECHABLES (8 artículos) =====
            ('Cucharas Chicas Plásticas', 'DESECHABLES', 50, 4, 'unidades'),
            ('Platos Cartón', 'DESECHABLES', 50, 4, 'unidades'),
            ('Revolvedores', 'DESECHABLES', 50, 4, 'unidades'),
            ('Servilletas 100 Unidades', 'DESECHABLES', 50, 4, 'unidades'),
            ('Vasos Plásticos Desechables', 'DESECHABLES', 50, 4, 'unidades'),
            ('Vasos Térmicos', 'DESECHABLES', 50, 4, 'unidades'),
            ('Plato Grande Plásticos', 'DESECHABLES', 50, 4, 'unidades'),
            ('Bandejas de Cartón', 'DESECHABLES', 50, 4, 'unidades'),
            
            # ===== OTROS (1 artículo) =====
            ('Gas de 11 Kilos', 'OTROS', 50, 4, 'unidades'),
        ]
        
        c.executemany('''INSERT INTO productos 
            (nombre, categoria, stock_actual, stock_minimo, unidad) 
            VALUES (?,?,?,?,?)''', productos_excel)
    
    conn.commit()
    conn.close()

def get_productos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, nombre, stock_actual, stock_minimo, unidad, categoria FROM productos ORDER BY categoria, nombre")
    productos = c.fetchall()
    conn.close()
    return [(int(p[0]), str(p[1]), int(p[2]), int(p[3]), str(p[4]), str(p[5])) for p in productos]

def registrar_entrada(producto_id, cantidad, documento, usuario):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT stock_actual FROM productos WHERE id=?", (producto_id,))
    stock_actual = int(c.fetchone()[0])
    nuevo_stock = stock_actual + cantidad
    c.execute("UPDATE productos SET stock_actual=? WHERE id=?", (nuevo_stock, producto_id))
    c.execute('''INSERT INTO movimientos 
        (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo, documento, usuario) 
        VALUES (?, 'ENTRADA', ?, ?, ?, ?, ?, ?)''', 
        (producto_id, cantidad, stock_actual, nuevo_stock, "Ingreso por compra", documento, usuario))
    conn.commit()
    conn.close()

def registrar_salida(producto_id, cantidad, motivo, usuario):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT stock_actual FROM productos WHERE id=?", (producto_id,))
    stock_actual = int(c.fetchone()[0])
    nuevo_stock = stock_actual - cantidad
    c.execute("UPDATE productos SET stock_actual=? WHERE id=?", (nuevo_stock, producto_id))
    c.execute('''INSERT INTO movimientos 
        (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo, usuario) 
        VALUES (?, 'SALIDA', ?, ?, ?, ?, ?)''', 
        (producto_id, cantidad, stock_actual, nuevo_stock, motivo, usuario))
    conn.commit()
    conn.close()

def registrar_ajuste(producto_id, nuevo_stock, motivo, usuario):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT stock_actual FROM productos WHERE id=?", (producto_id,))
    stock_actual = int(c.fetchone()[0])
    c.execute("UPDATE productos SET stock_actual=? WHERE id=?", (nuevo_stock, producto_id))
    c.execute('''INSERT INTO movimientos 
        (producto_id, tipo, cantidad, stock_anterior, stock_nuevo, motivo, usuario) 
        VALUES (?, 'AJUSTE', ?, ?, ?, ?, ?)''', 
        (producto_id, nuevo_stock - stock_actual, stock_actual, nuevo_stock, motivo, usuario))
    conn.commit()
    conn.close()

def get_salidas_hoy():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    c.execute('''SELECT m.fecha_hora, p.nombre, m.cantidad, p.unidad, m.motivo
        FROM movimientos m JOIN productos p ON m.producto_id = p.id
        WHERE m.tipo = 'SALIDA' AND DATE(m.fecha_hora) = ?
        ORDER BY m.fecha_hora DESC''', (hoy,))
    return c.fetchall()

def get_entradas_hoy():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    c.execute('''SELECT m.fecha_hora, p.nombre, m.cantidad, p.unidad, m.documento
        FROM movimientos m JOIN productos p ON m.producto_id = p.id
        WHERE m.tipo = 'ENTRADA' AND DATE(m.fecha_hora) = ?
        ORDER BY m.fecha_hora DESC''', (hoy,))
    return c.fetchall()

def get_stock_critico():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''SELECT nombre, stock_actual, stock_minimo, unidad, categoria
        FROM productos WHERE stock_actual < stock_minimo ORDER BY stock_actual''')
    return c.fetchall()

def get_todos_movimientos(limit=50):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''SELECT m.fecha_hora, p.nombre, m.tipo, m.cantidad, p.unidad, m.motivo, m.usuario
        FROM movimientos m JOIN productos p ON m.producto_id = p.id
        ORDER BY m.fecha_hora DESC LIMIT ?''', (limit,))
    return c.fetchall()

def get_resumen():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    c.execute("SELECT COUNT(*) FROM productos")
    total_productos = c.fetchone()[0] or 0
    
    c.execute("SELECT SUM(stock_actual) FROM productos")
    total_stock = c.fetchone()[0] or 0
    
    c.execute("SELECT COUNT(*) FROM productos WHERE stock_actual < stock_minimo")
    criticos = c.fetchone()[0] or 0
    
    c.execute("SELECT SUM(cantidad) FROM movimientos WHERE tipo='SALIDA' AND DATE(fecha_hora)=?", (hoy,))
    salidas_hoy = c.fetchone()[0] or 0
    
    c.execute("SELECT SUM(cantidad) FROM movimientos WHERE tipo='ENTRADA' AND DATE(fecha_hora)=?", (hoy,))
    entradas_hoy = c.fetchone()[0] or 0
    
    c.execute("SELECT COUNT(*) FROM movimientos WHERE tipo='AJUSTE' AND DATE(fecha_hora)=?", (hoy,))
    ajustes_hoy = c.fetchone()[0] or 0
    
    conn.close()
    return {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'criticos': criticos,
        'salidas_hoy': salidas_hoy,
        'entradas_hoy': entradas_hoy,
        'ajustes_hoy': ajustes_hoy
    }

# ===== INICIALIZAR =====
init_db()

# ===== SESIÓN =====
if 'usuario' not in st.session_state:
    st.session_state.usuario = "Juan Pérez"
    st.session_state.rol = "ENCARGADO"
if 'pagina' not in st.session_state:
    st.session_state.pagina = "menu_principal"
if 'menu_anterior' not in st.session_state:
    st.session_state.menu_anterior = ""
if 'salida_registrada' not in st.session_state:
    st.session_state.salida_registrada = False
if 'ultimo_registro' not in st.session_state:
    st.session_state.ultimo_registro = {}

# ============================================
# ===== MENÚ PRINCIPAL =====
# ============================================
def menu_principal():
    st.markdown("### 📋 Selecciona una opción:")
    
    with st.container(key="home-menu"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Salida", use_container_width=True):
                st.session_state.pagina = "submenu_salida"
                st.session_state.menu_anterior = "principal"
                st.session_state.salida_registrada = False
                st.rerun()
        
        with col2:
            if st.button("📦 Stock", use_container_width=True):
                st.session_state.pagina = "submenu_stock"
                st.session_state.menu_anterior = "principal"
                st.rerun()
        
        with col3:
            if st.button("📋 Hoy", use_container_width=True):
                st.session_state.pagina = "submenu_hoy"
                st.session_state.menu_anterior = "principal"
                st.rerun()
    
    st.markdown("---")
    st.markdown(f"""
    <div class="footer">
        👤 {st.session_state.usuario} | Rol: {st.session_state.rol}<br>
        📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
    """, unsafe_allow_html=True)

# ===== SUBMENÚ: SALIDA DE PRODUCTOS =====
def submenu_salida():
    st.markdown("### 📤 SALIDA DE PRODUCTOS")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        st.session_state.pagina = "menu_principal"
        st.session_state.salida_registrada = False
        st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ REGISTRAR SALIDA", use_container_width=True):
            st.session_state.pagina = "registrar_salida"
            st.session_state.salida_registrada = False
            st.rerun()
        
        if st.button("⚠️ STOCK CRÍTICO", use_container_width=True):
            st.session_state.pagina = "ver_criticos"
            st.rerun()
    
    with col2:
        if st.button("📦 VER STOCK DISPONIBLE", use_container_width=True):
            st.session_state.pagina = "ver_stock_completo"
            st.rerun()
        
        if st.button("✏️ AJUSTAR STOCK", use_container_width=True):
            st.session_state.pagina = "ajustar_stock"
            st.rerun()

# ===== SUBMENÚ: VER STOCK =====
def submenu_stock():
    st.markdown("### 📦 VER STOCK")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    st.markdown("---")
    
    resumen = get_resumen()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-label">📦 Productos</div>
            <div class="metric-value">{resumen['total_productos']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card blue">
            <div class="metric-label">📊 Stock Total</div>
            <div class="metric-value">{resumen['total_stock']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        color = "orange" if resumen['criticos'] > 0 else "green"
        st.markdown(f"""
        <div class="metric-card {color}">
            <div class="metric-label">⚠️ Críticos</div>
            <div class="metric-value">{resumen['criticos']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 VER STOCK COMPLETO", use_container_width=True):
            st.session_state.pagina = "ver_stock_completo"
            st.rerun()
        
        if st.button("✏️ AJUSTAR STOCK", use_container_width=True):
            st.session_state.pagina = "ajustar_stock"
            st.rerun()
    
    with col2:
        if st.button("⚠️ STOCK CRÍTICO", use_container_width=True):
            st.session_state.pagina = "ver_criticos"
            st.rerun()
        
        if st.button("📋 SALIDA DE HOY", use_container_width=True):
            st.session_state.pagina = "ver_salidas_hoy"
            st.rerun()

# ===== SUBMENÚ: SALIDA DE HOY =====
def submenu_hoy():
    st.markdown("### 📋 SALIDA DE HOY")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    resumen = get_resumen()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📤 Salidas", resumen['salidas_hoy'])
    with col2:
        st.metric("📥 Entradas", resumen['entradas_hoy'])
    with col3:
        st.metric("✏️ Ajustes", resumen['ajustes_hoy'])
    
    st.markdown("---")
    
    salidas = get_salidas_hoy()
    if salidas:
        st.markdown("#### 📤 Salidas registradas hoy:")
        for s in salidas:
            st.markdown(f"""
            <div class="item-card">
                <span class="hora">🕐 {s[0][11:16]}</span> | {s[1]} | <b>-{s[2]}</b> {s[3]}<br>
                <span class="motivo">Motivo: {s[4]}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No hay salidas registradas hoy")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 REGISTRAR SALIDA", use_container_width=True):
            st.session_state.pagina = "registrar_salida"
            st.rerun()
    with col2:
        if st.button("⚠️ STOCK CRÍTICO", use_container_width=True):
            st.session_state.pagina = "ver_criticos"
            st.rerun()

# ============================================
# ===== ACCIONES =====
# ============================================

# --- REGISTRAR SALIDA ---
def registrar_salida_accion():
    st.markdown("### ✏️ REGISTRAR SALIDA")
    
    if st.button("🔙 VOLVER AL SUBMENÚ", use_container_width=True):
        st.session_state.pagina = "submenu_salida"
        st.session_state.salida_registrada = False
        st.rerun()
    
    st.markdown("---")
    
    productos = get_productos()
    if not productos:
        st.warning("No hay productos registrados")
        return
    
    opciones = {p[1]: p for p in productos}
    seleccion = st.selectbox("Seleccionar producto:", list(opciones.keys()))
    producto = opciones[seleccion]
    
    producto_id = producto[0]
    nombre = producto[1]
    stock_actual = producto[2]
    unidad = producto[4]
    
    st.info(f"📦 Stock actual: **{stock_actual} {unidad}**")
    
    if stock_actual == 0:
        st.error("⚠️ Este producto no tiene stock disponible")
        return
    
    cantidad = st.number_input("Cantidad a retirar:", min_value=1, max_value=stock_actual, value=1, step=1)
    
    motivo = st.selectbox("Motivo:", [
        "Bienvenida",
        "Limpieza General",
        "Desayuno",
        "Cena",
        "La Casa Ora",
        "Mujeres",
        "Hombres",
        "Kids"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ REGISTRAR SALIDA", use_container_width=True):
            try:
                registrar_salida(producto_id, cantidad, motivo, st.session_state.usuario)
                st.session_state.salida_registrada = True
                st.session_state.ultimo_registro = {
                    'producto': nombre,
                    'cantidad': cantidad,
                    'unidad': unidad,
                    'motivo': motivo,
                    'stock_restante': stock_actual - cantidad
                }
                st.success(f"✅ ¡Salida registrada con éxito!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error al registrar: {e}")
    
    with col2:
        if st.button("🔙 VOLVER AL MENÚ", use_container_width=True):
            st.session_state.pagina = "menu_principal"
            st.session_state.salida_registrada = False
            st.rerun()
    
    if st.session_state.salida_registrada and st.session_state.ultimo_registro:
        ult = st.session_state.ultimo_registro
        st.markdown("---")
        st.markdown(f"""
        <div class="success-box">
            <b>✅ Última salida registrada:</b><br>
            📦 {ult['producto']} | <b>-{ult['cantidad']}</b> {ult['unidad']}<br>
            📝 Motivo: {ult['motivo']}<br>
            📊 Stock restante: <b>{ult['stock_restante']}</b> {ult['unidad']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 REGISTRAR OTRA SALIDA", use_container_width=True):
            st.session_state.salida_registrada = False
            st.rerun()

# --- VER STOCK COMPLETO ---
def ver_stock_completo():
    st.markdown("### 📦 STOCK COMPLETO")
    
    if st.button("🔙 VOLVER", use_container_width=True):
        if st.session_state.menu_anterior == "principal":
            st.session_state.pagina = "menu_principal"
        else:
            st.session_state.pagina = "submenu_salida"
        st.rerun()
    
    st.markdown("---")
    
    productos = get_productos()
    if productos:
        categorias = {}
        for p in productos:
            cat = p[5]
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(p)
        
        for categoria, items in categorias.items():
            st.markdown(f"#### 📂 {categoria}")
            data = []
            for p in items:
                estado = "✅ OK" if p[2] > p[3] else "⚠️ CRÍTICO"
                data.append({
                    "Producto": p[1],
                    "Stock": f"{p[2]} {p[4]}",
                    "Mínimo": f"{p[3]} {p[4]}",
                    "Estado": estado
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# --- STOCK CRÍTICO ---
def ver_criticos():
    st.markdown("### ⚠️ STOCK CRÍTICO")
    
    if st.button("🔙 VOLVER", use_container_width=True):
        st.session_state.pagina = "submenu_salida"
        st.rerun()
    
    st.markdown("---")
    
    criticos = get_stock_critico()
    if criticos:
        for c in criticos:
            st.error(f"""
            **{c[0]}** ({c[4]})
            📦 Stock: {c[1]} {c[3]} | Mínimo: {c[2]} {c[3]}
            → **FALTAN {c[2]-c[1]} {c[3]}** 🔴
            """)
    else:
        st.success("✅ ¡Todos los productos están en niveles adecuados!")

# --- SALIDAS DE HOY ---
def ver_salidas_hoy():
    st.markdown("### 📋 SALIDAS DE HOY")
    
    if st.button("🔙 VOLVER", use_container_width=True):
        st.session_state.pagina = "submenu_stock"
        st.rerun()
    
    st.markdown("---")
    
    salidas = get_salidas_hoy()
    if salidas:
        total = 0
        for s in salidas:
            st.markdown(f"""
            <div class="item-card">
                <span class="hora">🕐 {s[0][11:16]}</span> | {s[1]} | <b>-{s[2]}</b> {s[3]}<br>
                <span class="motivo">Motivo: {s[4]}</span>
            </div>
            """, unsafe_allow_html=True)
            total += s[2]
        st.info(f"📊 TOTAL SALIDAS: **{total} unidades**")
    else:
        st.success("✅ No hay salidas registradas hoy")

# --- AJUSTAR STOCK ---
def ajustar_stock():
    st.markdown("### ✏️ AJUSTAR STOCK")
    st.warning("⚠️ Este cambio quedará registrado para auditoría")
    
    if st.button("🔙 VOLVER", use_container_width=True):
        st.session_state.pagina = "submenu_salida"
        st.rerun()
    
    st.markdown("---")
    
    productos = get_productos()
    if not productos:
        st.warning("No hay productos")
        return
    
    opciones = {p[1]: p for p in productos}
    seleccion = st.selectbox("Seleccionar producto:", list(opciones.keys()))
    producto = opciones[seleccion]
    
    nuevo_stock = st.number_input(f"Nuevo stock (actual: {producto[2]}):", 0, value=producto[2])
    motivo = st.text_input("Motivo del ajuste:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 GUARDAR AJUSTE", use_container_width=True):
            if motivo:
                registrar_ajuste(producto[0], nuevo_stock, motivo, st.session_state.usuario)
                st.success(f"✅ Ajuste: {producto[2]} → {nuevo_stock} {producto[4]}")
                st.rerun()
            else:
                st.error("⚠️ Ingresa un motivo")
    with col2:
        if st.button("🔙 VOLVER", use_container_width=True):
            st.session_state.pagina = "submenu_salida"
            st.rerun()

# ============================================
# ===== CONTROLADOR DE PÁGINAS ===============
# ============================================

if st.session_state.pagina == "menu_principal":
    menu_principal()

elif st.session_state.pagina == "submenu_salida":
    submenu_salida()

elif st.session_state.pagina == "submenu_stock":
    submenu_stock()

elif st.session_state.pagina == "submenu_hoy":
    submenu_hoy()

elif st.session_state.pagina == "registrar_salida":
    registrar_salida_accion()

elif st.session_state.pagina == "ver_stock_completo":
    ver_stock_completo()

elif st.session_state.pagina == "ver_criticos":
    ver_criticos()

elif st.session_state.pagina == "ver_salidas_hoy":
    ver_salidas_hoy()

elif st.session_state.pagina == "ajustar_stock":
    ajustar_stock()

else:
    st.session_state.pagina = "menu_principal"
    st.rerun()