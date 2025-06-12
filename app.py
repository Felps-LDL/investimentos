import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador de Investimento", layout="centered")

st.title("💰 Simulador de Investimento com Juros Compostos")

desejado = st.number_input("🎯 Valor desejado (meta)", min_value=0.0, step=100.0)
patrimonio = st.number_input("📈 Patrimônio atual (R$)", min_value=0.0, step=100.0)
salario = st.number_input("💼 Seu salário atual (R$)", min_value=0.0, step=100.0)
projecao = st.slider("⏳ Meses para projeção", 1, 240, 60)

sem_investimento = 0
investimento = patrimonio
aumento = 12
x, y = [], []
a, b = [], []
lucros = []

for i in range(projecao):
    if i > aumento:
        salario += salario * 0.05
        aumento += 12

    investimento += salario * 0.3
    
    x.append(i + 1)
    y.append(investimento)
    a.append(i + 1)
    b.append(sem_investimento)

    lucro = investimento * 0.01
    investimento += lucro
    sem_investimento += salario * 0.3

    lucros.append(lucro)

df = pd.DataFrame({'Mês': x, 'Investimento': y, 'Lucro': lucros})
dg = pd.DataFrame({'Mês': a, 'Aporte Mensal': b})

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Mês'], y=df['Investimento'],
                         mode='lines+markers',
                         name='Investimento',
                         line=dict(color='lime', width=3),
                         marker=dict(size=6)))

fig.add_trace(go.Scatter(
    x=dg['Mês'], y=dg['Aporte Mensal'],
    mode='lines+markers',
    name='Aporte Mensal',
    line=dict(color='orange', width=2, dash='dot'),
    marker=dict(size=5)
))

fig.add_hline(y=desejado, line_dash="dash", line_color="red",
              annotation_text=f"Meta: R${desejado:,.2f}",
              annotation_position="top right")

fig.add_annotation(x=df['Mês'].iloc[-1], y=df['Investimento'].iloc[-1],
                   text=f"R$ {df['Investimento'].iloc[-1]:,.2f}",
                   showarrow=True, arrowhead=1)

fig.add_annotation(x=dg['Mês'].iloc[-1], y=dg['Aporte Mensal'].iloc[-1],
                   text=f"R$ {dg['Aporte Mensal'].iloc[-1]:,.2f}",
                   showarrow=True, arrowhead=1)

fig.update_layout(title='Projeção de Investimento',
                  xaxis_title='Meses',
                  yaxis_title='Valor Investido (R$)',
                  template='plotly_dark',
                  height=500)

st.plotly_chart(fig, use_container_width=True)

st.success(f"📈 Patrimônio acumulado: R$ {investimento:,.2f}")

st.dataframe(df.style.format({"Investimento": "R$ {:,.2f}", "Lucro": "R$ {:,.2f}"}))

st.download_button("📥 Baixar gráfico", fig.to_image(format="png"), file_name="investimento.png")

if investimento >= desejado:
    st.balloons()
    st.info("Parabéns! Você atingiu sua meta. 🎉")
else:
    st.warning("Você ainda não atingiu a meta. Continue investindo!")