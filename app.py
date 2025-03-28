import streamlit as st

# ================== CONFIGURACIÓN DE IDIOMAS =====================
LANG_ES = {
    "title": "Safe Manager - Nivel Óptimo",
    "header": "CONTROL DE SAFE Y CAMBIO",
    "registers": "Cajas con $200 cada una:",
    "calculate": "¿Cuánto cambio debo ordenar?",
    "result_header": "Resultado",
    "suggestions": "🔁 Sugerencias de cambio:",
    "iou_warning": "El total es menor a $2300. ¿El resto está en IOU?",
    "iou_confirm": "IOU registrado por ${} para alcanzar $2300.",
    "insufficient": "⚠️ Cambio insuficiente: debes tener al menos $1200 en billetes pequeños y monedas.",
    "incomplete_registers": "🔔 Solo {} de 4 cajas están completas."
}

LANG_EN = {
    "title": "Safe Manager - Optimal Level",
    "header": "SAFE AND CHANGE CONTROL",
    "registers": "Registers with $200 each:",
    "calculate": "How much change should I order?",
    "result_header": "Result",
    "suggestions": "🔁 Change Order Suggestions:",
    "iou_warning": "Total is below $2300. Is the rest in IOU?",
    "iou_confirm": "IOU registered for ${} to reach $2300.",
    "insufficient": "⚠️ Insufficient change: you need at least $1200 in small bills and coins.",
    "incomplete_registers": "🔔 Only {} of 4 registers are complete."
}

OPTIMAL = {
    "$1":  {"pack_size": 25,  "target_packs": 14},
    "$5":  {"pack_size": 100, "target_packs": 8},
    "¢25": {"pack_size": 10,  "target_packs": 20},
    "¢10": {"pack_size": 5,   "target_packs": 20},
    "¢5":  {"pack_size": 2,   "target_packs": 10, "max_packs": 10},
    "¢1":  {"pack_size": 0.5, "target_packs": 60, "max_packs": 60}
}

# ================== APP STREAMLIT =====================
st.set_page_config(page_title="Safe Manager", layout="centered")

lang = st.sidebar.selectbox("🌐 Idioma / Language", ["ES", "EN"])
L = LANG_ES if lang == "ES" else LANG_EN

st.title(L["header"])

st.markdown(f"### {L['registers']}")
cols = st.columns(4)
register_check = [cols[i].checkbox(f"Caja {i+1}" if lang == "ES" else f"Register {i+1}") for i in range(4)]

st.markdown("---")
st.subheader("💵 Ingreso por denominación")

denoms = ["$1", "$5", "$10", "$20", "$50", "$100", "¢25", "¢10", "¢5", "¢1"]
amounts = {}

for d in denoms:
    amounts[d] = st.number_input(f"{d} (en $)", min_value=0.0, step=0.01, value=0.0)

if st.button(L["calculate"]):
    total = sum(amounts.values()) + sum(register_check) * 200
    small_change = sum(amounts[d] for d in ["$1", "$5", "¢25", "¢10", "¢5", "¢1"])
    packs = {}
    suggestions = []
    warnings = []

    for k, v in amounts.items():
        if k in OPTIMAL:
            cfg = OPTIMAL[k]
            size = cfg["pack_size"]
            n_packs = v / size
            packs[k] = n_packs
            if n_packs < cfg["target_packs"]:
                falta = cfg["target_packs"] - n_packs
                total_faltante = round(falta * size, 2)
                suggestions.append(f"🔹 {'Ordenar' if lang == 'ES' else 'Order'} {int(round(falta))} paquetes de {k} (≈ ${total_faltante})")
            if 'max_packs' in cfg and n_packs > cfg['max_packs']:
                warnings.append(f"⚠️ {'Demasiados paquetes' if lang == 'ES' else 'Too many packs'} de {k}. Máx: {cfg['max_packs']}, tienes: {n_packs:.1f}")
        if k in ["$10", "$20", "$50", "$100"] and v > 0:
            suggestions.append(f"🔁 {'Cambiar' if lang == 'ES' else 'Exchange'} ${v:.2f} de {k} por billetes pequeños.")

    st.markdown(f"### 💰 {L['result_header']}")
    st.write(f"**Total (safe + cajas):** ${total:.2f}")

    if small_change < 1200:
        st.warning(L["insufficient"])
    if sum(register_check) < 4:
        st.warning(L["incomplete_registers"].format(sum(register_check)))

    st.markdown("---")
    if suggestions:
        st.subheader(L["suggestions"])
        for s in suggestions:
            st.write(s)

    if total < 2300:
        st.info(L["iou_warning"])
        if st.checkbox("✔️ IOU registrado"):
            st.success(L["iou_confirm"].format(round(2300 - total, 2)))

    if warnings:
        st.error("⚠️ " + "\n".join(warnings))

st.markdown("---")
st.caption("By Juan Morillo")
