import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CARREGAMENTO E LIMPEZA (Mantendo a lógica que funcionou) ---
df_custo = pd.read_csv('custo_moradia.csv', sep=';', encoding='utf-8', skiprows=1)
df_custo.columns = df_custo.columns.str.strip()
df_custo = df_custo[['Unidade Geográfica', 'Custo médio m² - moeda corrente-Reais']]
df_custo.columns = ['UF', 'Custo_m2']

df_pobreza = pd.read_csv('pobreza_ibge.csv', skiprows=4)
df_pobreza = df_pobreza.iloc[:, [0, 2, 3, 7]]
df_pobreza.columns = ['UF', 'IPM_Geral', 'Pobreza_Moradia', 'Pobreza_Financeira']

df_pobreza['UF'] = df_pobreza['UF'].str.strip()
for col in ['IPM_Geral', 'Pobreza_Moradia', 'Pobreza_Financeira']:
    df_pobreza[col] = df_pobreza[col].astype(str).str.replace(',', '.').str.strip()
    df_pobreza[col] = pd.to_numeric(df_pobreza[col], errors='coerce')

df_pobreza = df_pobreza.dropna(subset=['IPM_Geral'])
df_pobreza = df_pobreza[df_pobreza['UF'] != 'Brasil']

df_final = pd.merge(df_custo, df_pobreza, on='UF')

mapa_regioes = {
    'Acre': 'Norte', 'Amazonas': 'Norte', 'Amapá': 'Norte', 'Pará': 'Norte', 'Rondônia': 'Norte', 'Roraima': 'Norte', 'Tocantins': 'Norte',
    'Alagoas': 'Nordeste', 'Bahia': 'Nordeste', 'Ceará': 'Nordeste', 'Maranhão': 'Nordeste', 'Paraíba': 'Nordeste', 'Pernambuco': 'Nordeste', 'Piauí': 'Nordeste', 'Rio Grande do Norte': 'Nordeste', 'Sergipe': 'Nordeste',
    'Espírito Santo': 'Sudeste', 'Minas Gerais': 'Sudeste', 'Rio de Janeiro': 'Sudeste', 'São Paulo': 'Sudeste',
    'Paraná': 'Sul', 'Rio Grande do Sul': 'Sul', 'Santa Catarina': 'Sul',
    'Distrito Federal': 'Centro-Oeste', 'Goiás': 'Centro-Oeste', 'Mato Grosso': 'Centro-Oeste', 'Mato Grosso do Sul': 'Centro-Oeste'
}
df_final['Regiao'] = df_final['UF'].map(mapa_regioes)

# --- 2. CRIAÇÃO DOS GRÁFICOS (Lado a Lado) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))
sns.set_theme(style="whitegrid")

# Gráfico 1: Custo m2 vs Impacto Financeiro
sns.scatterplot(data=df_final, x='Custo_m2', y='Pobreza_Financeira', hue='Regiao', 
                size='IPM_Geral', sizes=(100, 1000), alpha=0.7, palette='viridis', ax=ax1)

# Gráfico 2: Custo m2 vs Impacto Moradia
sns.scatterplot(data=df_final, x='Custo_m2', y='Pobreza_Moradia', hue='Regiao', 
                size='IPM_Geral', sizes=(100, 1000), alpha=0.7, palette='magma', ax=ax2)

# Função para adicionar nomes sem muita sobreposição (ajuste simples de offset)
def label_points(df, x_col, y_col, ax):
    for i in range(df.shape[0]):
        # Adiciona um pequeno deslocamento alternado para evitar sobreposição vertical
        offset = 0.2 if i % 2 == 0 else -0.4 
        ax.text(df[x_col][i]+5, df[y_col][i] + offset, df.UF[i], fontsize=9, alpha=0.8)

label_points(df_final, 'Custo_m2', 'Pobreza_Financeira', ax1)
label_points(df_final, 'Custo_m2', 'Pobreza_Moradia', ax2)

# Customização Ax1
ax1.set_title('Custo do m² vs. Impacto Financeiro na Pobreza', fontsize=15, fontweight='bold')
ax1.set_xlabel('Custo Médio do m² (R$)', fontsize=12)
ax1.set_ylabel('Impacto Financeiro no IPM-CR (%)', fontsize=12)
ax1.legend(title='Regiões', bbox_to_anchor=(1, 1))

# Customização Ax2
ax2.set_title('Custo do m² vs. Impacto da Moradia na Pobreza', fontsize=15, fontweight='bold')
ax2.set_xlabel('Custo Médio do m² (R$)', fontsize=12)
ax2.set_ylabel('Impacto de Moradia no IPM-CR (%)', fontsize=12)
ax2.legend(title='Regiões', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.savefig('analise_comparativa_ibge.png', dpi=300)
print("Sucesso! O gráfico comparativo foi gerado.")