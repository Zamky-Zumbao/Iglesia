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
COLOR_DURAZNO = "#F4A97F"

# ===== CSS =====
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Fredoka:wght@600;700&display=swap');

    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 15% 0%, rgba(59,130,246,0.35), transparent 45%),
            radial-gradient(circle at 90% 10%, rgba(6,182,212,0.25), transparent 40%),
            linear-gradient(160deg, #0B1E4D 0%, {COLOR_PRIMARIO} 45%, #0d47a1 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }}

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
        transition: all 0.15s ease !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10) !important;
        width: 100% !important;
        background: rgba(255, 255, 255, 0.97) !important;
        color: {COLOR_PRIMARIO} !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.18) !important;
        background: linear-gradient(135deg, {COLOR_PRIMARIO}, {COLOR_SECUNDARIO}) !important;
        color: white !important;
        border-color: transparent !important;
    }}

    /* Botones de filtro */
    .st-key-filtro_todos .stButton > button,
    .st-key-filtro_aseo .stButton > button,
    .st-key-filtro_consumibles .stButton > button,
    .st-key-filtro_desechables .stButton > button,
    .st-key-filtro_stock_aseo .stButton > button,
    .st-key-filtro_stock_consumibles .stButton > button,
    .st-key-filtro_stock_desechables .stButton > button {{
        min-height: 40px !important;
        padding: 8px 4px !important;
        font-size: clamp(11px, 2.5vw, 13px) !important;
        white-space: nowrap !important;
        border-radius: 10px !important;
    }}
    .st-key-filtro_todos div[data-testid="column"],
    .st-key-filtro_aseo div[data-testid="column"],
    .st-key-filtro_consumibles div[data-testid="column"],
    .st-key-filtro_desechables div[data-testid="column"],
    .st-key-filtro_stock_aseo div[data-testid="column"],
    .st-key-filtro_stock_consumibles div[data-testid="column"],
    .st-key-filtro_stock_desechables div[data-testid="column"] {{
        padding: 0 3px !important;
    }}

    .st-key-home-menu .stButton > button {{
        min-height: 40px !important;
        padding: 8px 4px !important;
        font-size: clamp(11px, 3.4vw, 14px) !important;
        white-space: nowrap !important;
    }}
    .st-key-home-menu div[data-testid="column"] {{
        padding: 0 3px !important;
    }}

    /* Botón AGREGAR mismo alto que inputs */
    .st-key-btn_agregar_carrito .stButton > button {{
        min-height: 56px !important;
        height: 56px !important;
        padding: 8px 14px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 14px !important;
    }}

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
        color: {COLOR_DURAZNO} !important;
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

    .metric-card {{
        background: rgba(255, 255, 255, 0.97) !important;
        border-radius: 16px;
        padding: 16px 10px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
        border-top: 4px solid {COLOR_PRIMARIO};
        margin-bottom: 12px;
        transition: transform 0.15s ease;
    }}
    .metric-card:hover {{ transform: translateY(-3px); }}
    .metric-card.green {{ border-top-color: {COLOR_EXITO}; }}
    .metric-card.blue {{ border-top-color: {COLOR_ACENTO}; }}
    .metric-card.orange {{ border-top-color: {COLOR_ALERTA}; }}

    .metric-value {{
        font-size: clamp(22px, 6vw, 30px);
        font-weight: 800;
        margin: 4px 0 2px 0;
        color: {COLOR_TEXTO};
    }}
    .metric-label {{
        font-size: 11.5px;
        color: #64748B;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .item-card {{
        background: rgba(255,255,255,0.97);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 8px;
        border-left: 4px solid {COLOR_SECUNDARIO};
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }}
    .item-card .hora {{
        color: {COLOR_PRIMARIO};
        font-weight: 700;
    }}
    .item-card .motivo {{
        color: #64748B;
        font-size: 12.5px;
    }}

    .success-box {{
        background: rgba(220, 252, 231, 0.97) !important;
        border-radius: 16px;
        padding: 16px;
        border-left: 5px solid {COLOR_EXITO};
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
        color: {COLOR_TEXTO};
    }}

    .footer {{
        text-align: center;
        color: rgba(255,255,255,0.85);
        font-size: 12.5px;
        font-weight: 500;
        margin-top: 20px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 14px;
        backdrop-filter: blur(6px);
        line-height: 1.7;
    }}

    /* Créditos - casi invisibles */
    .creditos {{
        text-align: center;
        color: rgba(255,255,255,0.12) !important;
        font-size: 9px !important;
        font-weight: 300 !important;
        margin-top: 5px !important;
        letter-spacing: 1px !important;
    }}
    .creditos:hover {{
        color: rgba(255,255,255,0.3) !important;
        transition: color 0.3s ease;
    }}

    .stSelectbox > div > div, .stNumberInput > div > div, .stTextInput > div > div {{
        background: rgba(255,255,255,0.97) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
    }}
    label, .stMarkdown p {{
        color: white !important;
        font-weight: 600 !important;
    }}

    /* Instrucciones en color blanco */
    .instrucciones {{
        color: white !important;
        font-weight: 400 !important;
        line-height: 1.8 !important;
    }}
    .instrucciones strong {{
        color: {COLOR_DURAZNO} !important;
        font-weight: 700 !important;
    }}

    .stAlert {{
        background: rgba(255,255,255,0.97) !important;
        backdrop-filter: blur(6px);
        border-radius: 16px !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
    }}
    .stAlert p {{ color: {COLOR_TEXTO} !important; font-weight: 500 !important; }}

    [data-testid="stDataFrame"] {{
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
    }}

    .filtro-activo {{
        background: rgba(255,255,255,0.15) !important;
        border-radius: 10px;
        padding: 4px 12px;
        display: inline-block;
        color: rgba(255,255,255,0.9);
        font-size: 13px;
        font-weight: 600;
    }}

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
        .st-key-filtro_todos .stButton > button,
        .st-key-filtro_aseo .stButton > button,
        .st-key-filtro_consumibles .stButton > button,
        .st-key-filtro_desechables .stButton > button,
        .st-key-filtro_stock_aseo .stButton > button,
        .st-key-filtro_stock_consumibles .stButton > button,
        .st-key-filtro_stock_desechables .stButton > button {{
            font-size: clamp(9px, 2vw, 11px) !important;
            padding: 6px 2px !important;
            min-height: 32px !important;
        }}
        .st-key-btn_agregar_carrito .stButton > button {{
            min-height: 46px !important;
            height: 46px !important;
            font-size: 12px !important;
        }}
    }}

    @media (min-width: 481px) and (max-width: 1024px) {{
        .block-container {{
            max-width: 680px;
        }}
    }}

    @media (min-width: 1025px) {{
        .block-container {{
            max-width: 760px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
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
    
    # ===== LISTA COMPLETA DE ARTÍCULOS (58 artículos) =====
    productos_excel = [
        # ===== ASEO (29 artículos) =====
        ('Bolsa Basura 50x70', 'ASEO', 50, 4, 'unidades'),
        ('Bolsa Basura 70x90', 'ASEO', 50, 4, 'unidades'),
        ('Bolsa Basura 90x120', 'ASEO', 50, 4, 'unidades'),
        ('Bolsa Camiseta', 'ASEO', 50, 4, 'unidades'),
        ('Escobas Pisos', 'ASEO', 50, 4, 'unidades'),
        ('Esponjas Lavaplatos', 'ASEO', 50, 4, 'unidades'),
        ('Palas Aseo', 'ASEO', 50, 4, 'unidades'),
        ('Trapero Micro Fibra', 'ASEO', 50, 4, 'unidades'),
        ('Traperos Húmedos', 'ASEO', 50, 4, 'unidades'),
        ('Guantes Latex', 'ASEO', 50, 4, 'unidades'),
        ('Papel Higiénico', 'ASEO', 50, 4, 'unidades'),
        ('Toalla Papel 100 Mts', 'ASEO', 50, 4, 'unidades'),
        ('Toalla Papel Rollo Baño', 'ASEO', 50, 4, 'unidades'),
        ('Cloro Gel', 'ASEO', 50, 4, 'unidades'),
        ('Desengrasante', 'ASEO', 50, 4, 'unidades'),
        ('Desinfectante Baño', 'ASEO', 50, 4, 'unidades'),
        ('Desodorante Ambiental', 'ASEO', 50, 4, 'unidades'),
        ('Detergente Polvo', 'ASEO', 50, 4, 'unidades'),
        ('Lava Lozas', 'ASEO', 50, 4, 'unidades'),
        ('Limpia Piso Poet', 'ASEO', 50, 4, 'unidades'),
        ('Limpia Vidrio', 'ASEO', 50, 4, 'unidades'),
        ('Limpiador en Crema', 'ASEO', 50, 4, 'unidades'),
        ('Insecticida', 'ASEO', 50, 4, 'unidades'),
        ('Jabón', 'ASEO', 50, 4, 'unidades'),
        ('Lustra Muebles', 'ASEO', 50, 4, 'unidades'),
        ('Removedor de Sarro', 'ASEO', 50, 4, 'unidades'),
        ('Virutillas', 'ASEO', 50, 4, 'unidades'),
        ('Paños Amarillos', 'ASEO', 50, 4, 'unidades'),
        ('Toalla Desinfectante', 'ASEO', 50, 4, 'unidades'),
        
        # ===== CONSUMIBLES (21 artículos) =====
        ('Aceite', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Agua Mineral con Gas', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Agua Mineral sin Gas', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Azúcar', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Café', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Dulces Bienvenida', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Endulzante', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Mini', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Jugo Instantáneo', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Jugos en Caja Individual', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Latas de Bebida', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Pan', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Sal', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Té Caja 100 Bolsas', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Costa', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Frac', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Gretel', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Donuts', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Obsesion', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Kuky', 'CONSUMIBLES', 50, 4, 'unidades'),
        ('Galletas Triton', 'CONSUMIBLES', 50, 4, 'unidades'),
        
        # ===== DESECHABLES (8 artículos) =====
        ('Cucharas Chicas Plásticas', 'DESECHABLES', 50, 4, 'unidades'),
        ('Platos Cartón', 'DESECHABLES', 50, 4, 'unidades'),
        ('Revolvedores', 'DESECHABLES', 50, 4, 'unidades'),
        ('Servilletas 100 Unidades', 'DESECHABLES', 50, 4, 'unidades'),
        ('Vasos Plásticos Desechables', 'DESECHABLES', 50, 4, 'unidades'),
        ('Vasos Térmicos', 'DESECHABLES', 50, 4, 'unidades'),
        ('Plato Grande Plásticos', 'DESECHABLES', 50, 4, 'unidades'),
        ('Bandejas de Cartón', 'DESECHABLES', 50, 4, 'unidades'),
    ]
    
    for producto in productos_excel:
        nombre = producto[0]
        c.execute("SELECT COUNT(*) FROM productos WHERE nombre = ?", (nombre,))
        if c.fetchone()[0] == 0:
            c.execute('''INSERT INTO productos 
                (nombre, categoria, stock_actual, stock_minimo, unidad) 
                VALUES (?,?,?,?,?)''', producto)
    
    conn.commit()
    conn.close()

def get_productos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, nombre, stock_actual, stock_minimo, unidad, categoria FROM productos ORDER BY nombre")
    productos = c.fetchall()
    conn.close()
    return [(int(p[0]), str(p[1]), int(p[2]), int(p[3]), str(p[4]), str(p[5])) for p in productos]

def get_productos_por_categoria(categoria=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    if categoria and categoria != "TODOS":
        c.execute("SELECT id, nombre, stock_actual, stock_minimo, unidad, categoria FROM productos WHERE categoria = ? ORDER BY nombre", (categoria,))
    else:
        c.execute("SELECT id, nombre, stock_actual, stock_minimo, unidad, categoria FROM productos ORDER BY nombre")
    
    productos = c.fetchall()
    conn.close()
    return [(int(p[0]), str(p[1]), int(p[2]), int(p[3]), str(p[4]), str(p[5])) for p in productos]

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

def get_movimientos_por_motivo(motivo=None, fecha=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    query = '''SELECT m.fecha_hora, p.nombre, m.cantidad, p.unidad, m.motivo, m.usuario
        FROM movimientos m JOIN productos p ON m.producto_id = p.id
        WHERE m.tipo = 'SALIDA' '''
    params = []
    
    if motivo and motivo != "Todos":
        query += " AND m.motivo = ?"
        params.append(motivo)
    
    if fecha:
        query += " AND DATE(m.fecha_hora) = ?"
        params.append(fecha)
    
    query += " ORDER BY m.fecha_hora DESC"
    
    c.execute(query, params)
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
    
    c.execute("SELECT DISTINCT motivo FROM movimientos WHERE tipo='SALIDA' AND motivo IS NOT NULL AND motivo != ''")
    motivos = [row[0] for row in c.fetchall()]
    
    conn.close()
    return {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'criticos': criticos,
        'salidas_hoy': salidas_hoy,
        'entradas_hoy': entradas_hoy,
        'ajustes_hoy': ajustes_hoy,
        'motivos': motivos
    }

# ===== INICIALIZAR =====
init_db()

# ===== SESIÓN =====
if 'usuario' not in st.session_state:
    st.session_state.usuario = "Carlos Collao"
if 'rol' not in st.session_state:
    st.session_state.rol = "ENCARGADO"  # <-- AGREGAR ESTA LÍNEA
if 'pagina' not in st.session_state:
    st.session_state.pagina = "menu_principal"
if 'menu_anterior' not in st.session_state:
    st.session_state.menu_anterior = ""
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'filtro_categoria' not in st.session_state:
    st.session_state.filtro_categoria = "ASEO"
if 'filtro_stock' not in st.session_state:
    st.session_state.filtro_stock = "ASEO"

# ============================================
# ===== MENÚ PRINCIPAL =====
# ============================================
def menu_principal():
    st.markdown("### 📋 Selecciona una opción:")
    
    with st.container(key="home-menu"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Salida", use_container_width=True, key="btn_menu_salida"):
                st.session_state.pagina = "submenu_salida"
                st.session_state.menu_anterior = "principal"
                st.rerun()
        
        with col2:
            if st.button("📦 Stock", use_container_width=True, key="btn_menu_stock"):
                st.session_state.pagina = "submenu_stock"
                st.session_state.menu_anterior = "principal"
                st.rerun()
        
        with col3:
            if st.button("📋 Hoy", use_container_width=True, key="btn_menu_hoy"):
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

# ============================================
# ===== SUBMENÚ: SALIDA =====
# ============================================
def submenu_salida():
    st.markdown("### 📤 SALIDA DE PRODUCTOS")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True, key="btn_volver_salida"):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ SALIDA MÚLTIPLE", use_container_width=True, key="btn_salida_multiple"):
            st.session_state.pagina = "salida_multiple"
            st.rerun()
        
        if st.button("⚠️ STOCK CRÍTICO", use_container_width=True, key="btn_criticos_salida"):
            st.session_state.pagina = "ver_criticos"
            st.rerun()
    
    with col2:
        if st.button("📦 VER STOCK", use_container_width=True, key="btn_ver_stock_salida"):
            st.session_state.pagina = "ver_stock_completo"
            st.rerun()
        
        if st.button("✏️ AJUSTAR STOCK", use_container_width=True, key="btn_ajustar_salida"):
            st.session_state.pagina = "ajustar_stock"
            st.rerun()

# ============================================
# ===== SUBMENÚ: STOCK =====
# ============================================
def submenu_stock():
    st.markdown("### 📦 VER STOCK")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True, key="btn_volver_stock"):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    st.markdown("---")
    
    # ===== MÉTRICAS =====
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
    
    # ===== BOTONES =====
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 VER STOCK COMPLETO", use_container_width=True, key="btn_stock_completo"):
            st.session_state.pagina = "ver_stock_completo"
            st.rerun()
        
        if st.button("📋 REPORTES POR MOTIVO", use_container_width=True, key="btn_reportes_motivo"):
            st.session_state.pagina = "reportes_motivo"
            st.rerun()
    
    with col2:
        if st.button("✏️ AJUSTAR STOCK", use_container_width=True, key="btn_ajustar_stock_sub"):
            st.session_state.pagina = "ajustar_stock"
            st.rerun()
        
        if st.button("⚠️ STOCK CRÍTICO", use_container_width=True, key="btn_criticos_stock_sub"):
            st.session_state.pagina = "ver_criticos"
            st.rerun()

# ============================================
# ===== SUBMENÚ: HOY =====
# ============================================
def submenu_hoy():
    st.markdown("### 📋 SALIDAS DE HOY")
    st.markdown(f"📅 {datetime.now().strftime('%A, %d de %B de %Y')}")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True, key="btn_volver_hoy"):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    st.markdown("---")
    
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
        st.markdown("#### 📤 Productos retirados hoy:")
        total = 0
        for s in salidas:
            st.markdown(f"""
            <div class="item-card">
                <span class="hora">🕐 {s[0][11:16]}</span> | 
                <b>{s[1]}</b> | 
                <span style="color: #EF4444; font-weight: 700;">-{s[2]}</span> {s[3]}<br>
                <span class="motivo">📝 Motivo: {s[4]}</span>
            </div>
            """, unsafe_allow_html=True)
            total += s[2]
        
        st.markdown("---")
        st.info(f"📊 **TOTAL UNIDADES RETIRADAS HOY: {total}**")
    else:
        st.success("✅ No hay salidas registradas hoy")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 REGISTRAR SALIDA", use_container_width=True, key="btn_registrar_hoy"):
            st.session_state.pagina = "salida_multiple"
            st.rerun()
    with col2:
        if st.button("🔙 VOLVER AL MENÚ", use_container_width=True, key="btn_volver_menu_hoy"):
            st.session_state.pagina = "menu_principal"
            st.rerun()

# ============================================
# ===== SALIDA MÚLTIPLE (CARRITO) =====
# ============================================
def salida_multiple():
    st.markdown("### ✏️ SALIDA MÚLTIPLE")
    st.markdown("Agrega productos uno por uno al carrito de salida")
    st.markdown("---")
    
    if st.button("🔙 VOLVER", use_container_width=True, key="btn_volver_carrito"):
        st.session_state.pagina = "submenu_salida"
        st.rerun()
    
    st.markdown("---")
    
    # ===== FILTROS POR FAMILIA =====
    st.markdown("#### 🔍 Filtrar por categoría:")
    
    col_filtros = st.columns(3)  # <-- SOLO 3 FAMILIAS
    
    with col_filtros[0]:
        if st.button("🧹 ASEO", use_container_width=True, key="filtro_aseo"):
            st.session_state.filtro_categoria = "ASEO"
            st.rerun()
    
    with col_filtros[1]:
        if st.button("🍽️ CONSUMIBLES", use_container_width=True, key="filtro_consumibles"):
            st.session_state.filtro_categoria = "CONSUMIBLES"
            st.rerun()
    
    with col_filtros[2]:
        if st.button("🥡 DESECHABLES", use_container_width=True, key="filtro_desechables"):
            st.session_state.filtro_categoria = "DESECHABLES"
            st.rerun()
    
    # Mostrar filtro activo
    st.caption(f"🔍 Mostrando: **{st.session_state.filtro_categoria}**")
    
    st.markdown("---")
    
    # ===== OBTENER PRODUCTOS SEGÚN FILTRO =====
    productos = get_productos_por_categoria(st.session_state.filtro_categoria)
    
    if not productos:
        st.warning("No hay productos en esta categoría")
        return
    
    # ===== AGREGAR PRODUCTO AL CARRITO =====
    st.markdown("#### ➕ Agregar producto al carrito")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        opciones = {p[1]: p for p in productos}
        seleccion = st.selectbox(
            "Producto:",
            list(opciones.keys()),
            index=None,
            placeholder="🔽 Selecciona un producto...",
            key="select_producto_carrito"
        )
        
        if seleccion is None:
            st.info("👆 Selecciona un producto para agregarlo al carrito")
            return
        
        producto = opciones[seleccion]
        stock_actual = producto[2]
        unidad = producto[4]
    
    with col2:
        cantidad = st.number_input(
            "Cantidad:",
            min_value=1,
            max_value=stock_actual,
            value=1,
            step=1,
            key="cantidad_carrito"
        )
    
    with col3:
        st.markdown(" ")
        if st.button("➕ AGREGAR", use_container_width=True, key="btn_agregar_carrito"):
            if cantidad > 0 and cantidad <= stock_actual:
                encontrado = False
                for item in st.session_state.carrito:
                    if item['id'] == producto[0]:
                        item['cantidad'] += cantidad
                        encontrado = True
                        break
                
                if not encontrado:
                    st.session_state.carrito.append({
                        'id': producto[0],
                        'nombre': producto[1],
                        'cantidad': cantidad,
                        'unidad': producto[4],
                        'stock_actual': producto[2]
                    })
                
                st.success(f"✅ Agregado: {producto[1]} x{cantidad} {producto[4]}")
                st.rerun()
            else:
                st.error(f"⚠️ Stock insuficiente. Disponible: {stock_actual} {producto[4]}")
    
    st.markdown("---")
    
    # ===== MOSTRAR CARRITO =====
    if st.session_state.carrito:
        st.markdown("#### 🛒 Carrito de salida")
        
        data = []
        carrito_ordenado = sorted(st.session_state.carrito, key=lambda x: x['nombre'])
        for idx, item in enumerate(carrito_ordenado):
            data.append({
                "#": idx + 1,
                "Producto": item['nombre'],
                "Cantidad": f"{item['cantidad']} {item['unidad']}",
                "Stock disponible": f"{item['stock_actual']} {item['unidad']}"
            })
        
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("#### 🗑️ Eliminar productos")
        cols = st.columns(min(len(st.session_state.carrito), 4))
        for idx, item in enumerate(carrito_ordenado):
            with cols[idx % 4]:
                if st.button(f"❌ {item['nombre'][:12]}", key=f"del_{idx}"):
                    for i, car_item in enumerate(st.session_state.carrito):
                        if car_item['nombre'] == item['nombre']:
                            st.session_state.carrito.pop(i)
                            break
                    st.rerun()
        
        st.markdown("---")
        
        # ===== CONFIRMAR SALIDA =====
        st.markdown("#### 📝 Confirmar salida")
        
        motivo = st.selectbox("Motivo de la salida:", [
            "Bienvenida",
            "Limpieza General",
            "Desayuno",
            "Cena",
            "La Casa Ora",
            "Mujeres",
            "Hombres",
            "Kids"
        ], key="motivo_carrito")
        
        total_productos = len(st.session_state.carrito)
        total_unidades = sum(item['cantidad'] for item in st.session_state.carrito)
        
        st.warning(f"⚠️ Vas a registrar la salida de **{total_productos} productos** ({total_unidades} unidades en total). Esta acción no se puede deshacer.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ CONFIRMAR SALIDA", use_container_width=True, key="btn_confirmar_carrito"):
                try:
                    for item in st.session_state.carrito:
                        registrar_salida(
                            item['id'],
                            item['cantidad'],
                            motivo,
                            st.session_state.usuario
                        )
                    
                    st.success(f"✅ ¡Salida múltiple registrada con éxito!")
                    st.info(f"📦 {total_productos} productos | 📊 {total_unidades} unidades | 📝 Motivo: {motivo}")
                    st.balloons()
                    
                    st.markdown("---")
                    st.markdown("#### 📋 Detalle de la salida:")
                    for item in sorted(st.session_state.carrito, key=lambda x: x['nombre']):
                        st.markdown(f"• {item['nombre']}: **-{item['cantidad']}** {item['unidad']}")
                    
                    st.session_state.carrito = []
                    
                    if st.button("🔄 NUEVA SALIDA", use_container_width=True, key="btn_nueva_salida"):
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al registrar: {e}")
        
        with col2:
            if st.button("🧹 VACIAR CARRITO", use_container_width=True, key="btn_vaciar_carrito"):
                st.session_state.carrito = []
                st.rerun()
        
        with col3:
            if st.button("🔙 VOLVER AL MENÚ", use_container_width=True, key="btn_volver_menu_carrito"):
                st.session_state.carrito = []
                st.session_state.pagina = "menu_principal"
                st.rerun()
    
    else:
        st.info("🛒 El carrito está vacío. Agrega productos arriba.")
        
        st.markdown("---")
        st.markdown("""
        <div class="instrucciones">
        <strong>📝 Instrucciones:</strong><br>
        1. Selecciona un producto<br>
        2. Ingresa la cantidad<br>
        3. Presiona <strong>AGREGAR</strong><br>
        4. Repite hasta tener todos los productos<br>
        5. Confirma la salida con el botón <strong>CONFIRMAR SALIDA</strong>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# ===== VER STOCK COMPLETO =====
# ============================================
def ver_stock_completo():
    st.markdown("### 📦 STOCK COMPLETO")
    
    if st.button("🔙 VOLVER", use_container_width=True, key="btn_volver_stock_completo"):
        if st.session_state.menu_anterior == "principal":
            st.session_state.pagina = "menu_principal"
        else:
            st.session_state.pagina = "submenu_salida"
        st.rerun()
    
    st.markdown("---")
    
    # ===== FILTROS POR FAMILIA (SOLO 3) =====
    st.markdown("#### 🔍 Filtrar por categoría:")
    
    col_filtros = st.columns(3)
    
    with col_filtros[0]:
        if st.button("🧹 ASEO", use_container_width=True, key="filtro_stock_aseo"):
            st.session_state.filtro_stock = "ASEO"
            st.rerun()
    
    with col_filtros[1]:
        if st.button("🍽️ CONSUMIBLES", use_container_width=True, key="filtro_stock_consumibles"):
            st.session_state.filtro_stock = "CONSUMIBLES"
            st.rerun()
    
    with col_filtros[2]:
        if st.button("🥡 DESECHABLES", use_container_width=True, key="filtro_stock_desechables"):
            st.session_state.filtro_stock = "DESECHABLES"
            st.rerun()
    
    # Mostrar filtro activo
    st.caption(f"🔍 Mostrando: **{st.session_state.filtro_stock}**")
    
    st.markdown("---")
    
    # ===== OBTENER PRODUCTOS SEGÚN FILTRO =====
    productos = get_productos_por_categoria(st.session_state.filtro_stock)
    
    if not productos:
        st.warning("No hay productos en esta categoría")
        return
    
    # ===== MOSTRAR STOCK =====
    categorias = {}
    for p in productos:
        cat = p[5]
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(p)
    
    for categoria in sorted(categorias.keys()):
        items = categorias[categoria]
        st.markdown(f"#### 📂 {categoria}")
        data = []
        for p in sorted(items, key=lambda x: x[1]):
            estado = "✅ OK" if p[2] > p[3] else "⚠️ CRÍTICO"
            data.append({
                "Producto": p[1],
                "Stock": f"{p[2]} {p[4]}",
                "Mínimo": f"{p[3]} {p[4]}",
                "Estado": estado
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ============================================
# ===== STOCK CRÍTICO =====
# ============================================
def ver_criticos():
    st.markdown("### ⚠️ STOCK CRÍTICO")
    
    if st.button("🔙 VOLVER", use_container_width=True, key="btn_volver_criticos"):
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

# ============================================
# ===== AJUSTAR STOCK =====
# ============================================
def ajustar_stock():
    st.markdown("### ✏️ AJUSTAR STOCK")
    st.warning("⚠️ Este cambio quedará registrado para auditoría")
    
    if st.button("🔙 VOLVER", use_container_width=True, key="btn_volver_ajustar"):
        st.session_state.pagina = "submenu_salida"
        st.rerun()
    
    st.markdown("---")
    
    productos = get_productos()
    if not productos:
        st.warning("No hay productos")
        return
    
    productos_ordenados = sorted(productos, key=lambda x: x[1])
    opciones = {p[1]: p for p in productos_ordenados}
    seleccion = st.selectbox("Seleccionar producto:", list(opciones.keys()), key="select_ajustar")
    producto = opciones[seleccion]
    
    nuevo_stock = st.number_input(f"Nuevo stock (actual: {producto[2]}):", 0, value=producto[2], key="num_ajustar")
    motivo = st.text_input("Motivo del ajuste:", key="text_ajustar")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 GUARDAR AJUSTE", use_container_width=True, key="btn_guardar_ajustar"):
            if motivo:
                registrar_ajuste(producto[0], nuevo_stock, motivo, st.session_state.usuario)
                st.success(f"✅ Ajuste: {producto[2]} → {nuevo_stock} {producto[4]}")
                st.rerun()
            else:
                st.error("⚠️ Ingresa un motivo")
    with col2:
        if st.button("🔙 VOLVER", use_container_width=True, key="btn_volver_ajustar2"):
            st.session_state.pagina = "submenu_salida"
            st.rerun()

# ============================================
# ===== REPORTES POR MOTIVO =====
# ============================================
def reportes_motivo():
    st.markdown("### 📋 REPORTES POR MOTIVO")
    st.markdown("Filtra las salidas por motivo")
    st.markdown("---")
    
    if st.button("🔙 VOLVER", use_container_width=True, key="btn_volver_reportes"):
        st.session_state.pagina = "submenu_stock"
        st.rerun()
    
    st.markdown("---")
    
    resumen = get_resumen()
    motivos = resumen['motivos']
    
    col1, col2 = st.columns(2)
    with col1:
        motivo_filtro = st.selectbox("Motivo:", ["Todos"] + motivos if motivos else ["Todos"], key="select_motivo_filtro")
    with col2:
        fecha_filtro = st.date_input("Fecha:", value=datetime.now().date(), key="date_filtro")
    
    fecha_str = fecha_filtro.strftime('%Y-%m-%d')
    datos = get_movimientos_por_motivo(motivo_filtro if motivo_filtro != "Todos" else None, fecha_str)
    
    if datos:
        data = []
        for d in datos:
            data.append({
                "Fecha": d[0][:16],
                "Producto": d[1],
                "Cantidad": f"{d[2]} {d[3]}",
                "Motivo": d[4],
                "Usuario": d[5]
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total = sum(d[2] for d in datos)
        st.info(f"📊 Total de unidades entregadas: **{total}**")
    else:
        st.info("No hay movimientos para los filtros seleccionados")

# ============================================
# ===== CONTROLADOR =====
# ============================================

if st.session_state.pagina == "menu_principal":
    menu_principal()

elif st.session_state.pagina == "submenu_salida":
    submenu_salida()

elif st.session_state.pagina == "submenu_stock":
    submenu_stock()

elif st.session_state.pagina == "submenu_hoy":
    submenu_hoy()

elif st.session_state.pagina == "salida_multiple":
    salida_multiple()

elif st.session_state.pagina == "ver_stock_completo":
    ver_stock_completo()

elif st.session_state.pagina == "ver_criticos":
    ver_criticos()

elif st.session_state.pagina == "ajustar_stock":
    ajustar_stock()

elif st.session_state.pagina == "reportes_motivo":
    reportes_motivo()

else:
    st.session_state.pagina = "menu_principal"
    st.rerun()

# ===== CRÉDITOS (casi invisibles) =====
st.markdown("""
<div class="creditos">
    ⚡ Desarrollado por Zamky Zumbao ⚡
</div>
""", unsafe_allow_html=True)