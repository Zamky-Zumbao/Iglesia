import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ===== CONFIGURACIÓN =====
st.set_page_config(
    page_title="Bodega Iglesia",
    page_icon="🏪",
    layout="centered"
)

# ===== CSS =====
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 15px;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .stButton > button {
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    .main-title {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 14px;
        font-weight: 400;
    }
    
    .footer {
        text-align: center;
        color: #999;
        font-size: 12px;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #FF4B4B;
        margin-bottom: 10px;
    }
    .metric-card.green { border-left-color: #00C853; }
    .metric-card.blue { border-left-color: #2979FF; }
    .metric-card.orange { border-left-color: #FF9100; }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        margin: 3px 0;
    }
    .metric-label {
        font-size: 12px;
        color: #666;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

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
        productos_ejemplo = [
            ('Azúcar 1kg', 'Despensa', 50, 4, 'unidades'),
            ('Café 500gr', 'Despensa', 50, 4, 'unidades'),
            ('Té caja 100 bolsas', 'Despensa', 50, 4, 'cajas'),
            ('Endulzante botella', 'Despensa', 50, 4, 'botellas'),
            ('Servilletas 100un', 'Limpieza', 50, 4, 'paquetes'),
            ('Galletas Mini', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Costa', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Frac', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Gretel', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Donuts', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Obsesion', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Kuky', 'Galletas', 50, 4, 'paquetes'),
            ('Galletas Triton', 'Galletas', 50, 4, 'paquetes'),
            ('Confort', 'Limpieza', 50, 4, 'rollos'),
            ('Toalla Nova', 'Limpieza', 50, 4, 'paquetes'),
            ('Bolsa B 70x50', 'Bolsas', 50, 4, 'unidades'),
            ('Bolsa B 70x80', 'Bolsas', 50, 4, 'unidades'),
            ('Paños Des. Multiuso', 'Limpieza', 50, 4, 'paquetes'),
        ]
        c.executemany('''INSERT INTO productos 
            (nombre, categoria, stock_actual, stock_minimo, unidad) 
            VALUES (?,?,?,?,?)''', productos_ejemplo)
    
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
# ===== MENÚ PRINCIPAL (WIZARD NIVEL 1) =====
# ============================================
def menu_principal():
    st.markdown('<div class="main-title">🏪 BODEGA IGLESIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Administración Simple</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # ===== 3 OPCIONES PRINCIPALES =====
    st.markdown("### 📋 Selecciona una opción:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤\n1. SALIDA DE\nPRODUCTOS", use_container_width=True):
            st.session_state.pagina = "submenu_salida"
            st.session_state.menu_anterior = "principal"
            st.session_state.salida_registrada = False
            st.rerun()
    
    with col2:
        if st.button("📦\n2. VER\nSTOCK", use_container_width=True):
            st.session_state.pagina = "submenu_stock"
            st.session_state.menu_anterior = "principal"
            st.rerun()
    
    with col3:
        if st.button("📋\n3. SALIDA\nDE HOY", use_container_width=True):
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
# ===== SUBMENÚ: SALIDA DE PRODUCTOS ========
# ============================================
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

# ============================================
# ===== SUBMENÚ: VER STOCK ==================
# ============================================
def submenu_stock():
    st.markdown("### 📦 VER STOCK")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    st.markdown("---")
    
    # ===== MÉTRICAS DENTRO DE VER STOCK =====
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

# ============================================
# ===== SUBMENÚ: SALIDA DE HOY ==============
# ============================================
def submenu_hoy():
    st.markdown("### 📋 SALIDA DE HOY")
    st.markdown("---")
    
    if st.button("🔙 VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        st.session_state.pagina = "menu_principal"
        st.rerun()
    
    # Mostrar resumen del día
    resumen = get_resumen()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📤 Salidas", resumen['salidas_hoy'])
    with col2:
        st.metric("📥 Entradas", resumen['entradas_hoy'])
    with col3:
        st.metric("✏️ Ajustes", resumen['ajustes_hoy'])
    
    st.markdown("---")
    
    # Mostrar salidas del día
    salidas = get_salidas_hoy()
    if salidas:
        st.markdown("#### 📤 Salidas registradas hoy:")
        for s in salidas:
            st.markdown(f"""
            <div style="background: white; border-radius: 10px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #FF6B6B;">
                <b>🕐 {s[0][11:16]}</b> | {s[1]} | <b>-{s[2]}</b> {s[3]}<br>
                <span style="color: #666; font-size: 13px;">Motivo: {s[4]}</span>
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
# ===== ACCIONES =============================
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
    
    opciones = {f"{p[1]} ({p[2]} {p[4]})": p for p in productos}
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
    
    # Mostrar último registro si existe
    if st.session_state.salida_registrada and st.session_state.ultimo_registro:
        ult = st.session_state.ultimo_registro
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #e8f5e9; border-radius: 12px; padding: 15px; border-left: 4px solid #00C853;">
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

# --- SALIDAS DE HOY (vista detallada) ---
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
            <div style="background: white; border-radius: 10px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #FF6B6B;">
                <b>🕐 {s[0][11:16]}</b> | {s[1]} | <b>-{s[2]}</b> {s[3]}<br>
                <span style="color: #666; font-size: 13px;">Motivo: {s[4]}</span>
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
    
    opciones = {f"{p[1]} ({p[2]} {p[4]})": p for p in productos}
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