import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Cargar datos
df = pd.read_csv('ia_project_golden_clean.csv')

print("=" * 80)
print("ANÁLISIS Y VISUALIZACIÓN DE DATOS - IA PROJECT GOLDEN CLEAN")
print("=" * 80)

# Estadísticas básicas
print(f"\nDimensiones del dataset: {df.shape[0]} registros x {df.shape[1]} columnas")
print(f"\nColumnas disponibles:\n{df.columns.tolist()}")
print(f"\nTipos de datos:\n{df.dtypes}")
print(f"\nValores faltantes:\n{df.isnull().sum()}")

# Crear figura con múltiples subplots
fig = plt.figure(figsize=(18, 14))

# 1. Distribución de estado del cliente
ax1 = plt.subplot(3, 3, 1)
customer_status = df['customer_status'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#f39c12']
customer_status.plot(kind='bar', ax=ax1, color=colors[:len(customer_status)])
ax1.set_title('Distribución de Estado del Cliente', fontsize=12, fontweight='bold')
ax1.set_xlabel('Estado')
ax1.set_ylabel('Cantidad')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(customer_status.values):
    ax1.text(i, v + 5, str(v), ha='center', fontweight='bold')

# 2. Distribución de planes
ax2 = plt.subplot(3, 3, 2)
plan_counts = df['plan'].value_counts()
colors_plan = ['#3498db', '#9b59b6', '#e67e22']
plan_counts.plot(kind='bar', ax=ax2, color=colors_plan[:len(plan_counts)])
ax2.set_title('Distribución de Planes de Suscripción', fontsize=12, fontweight='bold')
ax2.set_xlabel('Plan')
ax2.set_ylabel('Cantidad')
ax2.tick_params(axis='x', rotation=45)
for i, v in enumerate(plan_counts.values):
    ax2.text(i, v + 5, str(v), ha='center', fontweight='bold')

# 3. Distribución de países
ax3 = plt.subplot(3, 3, 3)
country_counts = df['country'].value_counts().head(8)
country_counts.plot(kind='barh', ax=ax3, color='#16a085')
ax3.set_title('Top 8 Países por Cantidad de Usuarios', fontsize=12, fontweight='bold')
ax3.set_xlabel('Cantidad')
for i, v in enumerate(country_counts.values):
    ax3.text(v + 5, i, str(v), va='center', fontweight='bold')

# 4. Distribución de altura
ax4 = plt.subplot(3, 3, 4)
ax4.hist(df['height_cm'].dropna(), bins=30, color='#3498db', edgecolor='black', alpha=0.7)
ax4.set_title('Distribución de Altura (cm)', fontsize=12, fontweight='bold')
ax4.set_xlabel('Altura (cm)')
ax4.set_ylabel('Frecuencia')
ax4.axvline(df['height_cm'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df["height_cm"].mean():.1f}')
ax4.axvline(df['height_cm'].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df["height_cm"].median():.1f}')
ax4.legend()

# 5. Distribución de peso
ax5 = plt.subplot(3, 3, 5)
ax5.hist(df['weight_kg'].dropna(), bins=30, color='#e74c3c', edgecolor='black', alpha=0.7)
ax5.set_title('Distribución de Peso (kg)', fontsize=12, fontweight='bold')
ax5.set_xlabel('Peso (kg)')
ax5.set_ylabel('Frecuencia')
ax5.axvline(df['weight_kg'].mean(), color='blue', linestyle='--', linewidth=2, label=f'Media: {df["weight_kg"].mean():.1f}')
ax5.axvline(df['weight_kg'].median(), color='orange', linestyle='--', linewidth=2, label=f'Mediana: {df["weight_kg"].median():.1f}')
ax5.legend()

# 6. Gasto por plan
ax6 = plt.subplot(3, 3, 6)
plan_spending = df.groupby('plan')['amount_spent_mxn'].mean().sort_values(ascending=False)
plan_spending.plot(kind='bar', ax=ax6, color=['#9b59b6', '#3498db', '#e67e22'])
ax6.set_title('Gasto Promedio por Plan (MXN)', fontsize=12, fontweight='bold')
ax6.set_xlabel('Plan')
ax6.set_ylabel('Gasto Promedio (MXN)')
ax6.tick_params(axis='x', rotation=45)
for i, v in enumerate(plan_spending.values):
    ax6.text(i, v + 100, f'${v:.2f}', ha='center', fontweight='bold')

# 7. Scatter: Altura vs Peso
ax7 = plt.subplot(3, 3, 7)
scatter = ax7.scatter(df['height_cm'], df['weight_kg'], alpha=0.5, c=df['amount_spent_mxn'], 
                     cmap='viridis', s=30, edgecolors='black', linewidth=0.5)
ax7.set_title('Relación Altura vs Peso (coloreado por gasto)', fontsize=12, fontweight='bold')
ax7.set_xlabel('Altura (cm)')
ax7.set_ylabel('Peso (kg)')
cbar = plt.colorbar(scatter, ax=ax7)
cbar.set_label('Gasto (MXN)', fontweight='bold')

# 8. Distribución de idioma preferido
ax8 = plt.subplot(3, 3, 8)
language_counts = df['preferred_language'].value_counts()
colors_lang = ['#16a085', '#c0392b', '#8e44ad']
ax8.pie(language_counts.values, labels=language_counts.index, autopct='%1.1f%%', 
        colors=colors_lang[:len(language_counts)], startangle=90, textprops={'fontweight': 'bold'})
ax8.set_title('Distribución de Idioma Preferido', fontsize=12, fontweight='bold')

# 9. Gasto por estado del cliente
ax9 = plt.subplot(3, 3, 9)
status_spending = df.groupby('customer_status')['amount_spent_mxn'].agg(['mean', 'count'])
status_spending['mean'].plot(kind='bar', ax=ax9, color=['#2ecc71', '#e74c3c', '#f39c12'])
ax9.set_title('Gasto Promedio por Estado del Cliente', fontsize=12, fontweight='bold')
ax9.set_xlabel('Estado')
ax9.set_ylabel('Gasto Promedio (MXN)')
ax9.tick_params(axis='x', rotation=45)
for i, v in enumerate(status_spending['mean'].values):
    ax9.text(i, v + 100, f'${v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizacion_datos.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: visualizacion_datos.png")

# ANÁLISIS DETALLADO
print("\n" + "=" * 80)
print("ANÁLISIS DETALLADO")
print("=" * 80)

print("\n1. ESTADO DEL CLIENTE:")
print(df['customer_status'].value_counts())
print(f"\nPorcentajes:\n{df['customer_status'].value_counts(normalize=True) * 100}")

print("\n2. ANÁLISIS POR PLAN:")
for plan in df['plan'].unique():
    plan_data = df[df['plan'] == plan]
    print(f"\n{plan}:")
    print(f"  - Cantidad: {len(plan_data)}")
    print(f"  - Gasto promedio: ${plan_data['amount_spent_mxn'].mean():.2f}")
    print(f"  - Gasto total: ${plan_data['amount_spent_mxn'].sum():.2f}")
    print(f"  - Rango de gasto: ${plan_data['amount_spent_mxn'].min():.2f} - ${plan_data['amount_spent_mxn'].max():.2f}")

print("\n3. ESTADÍSTICAS FÍSICAS:")
print(f"Altura (cm):")
print(f"  - Media: {df['height_cm'].mean():.2f}")
print(f"  - Mediana: {df['height_cm'].median():.2f}")
print(f"  - Desv. Est: {df['height_cm'].std():.2f}")
print(f"  - Rango: {df['height_cm'].min():.2f} - {df['height_cm'].max():.2f}")

print(f"\nPeso (kg):")
print(f"  - Media: {df['weight_kg'].mean():.2f}")
print(f"  - Mediana: {df['weight_kg'].median():.2f}")
print(f"  - Desv. Est: {df['weight_kg'].std():.2f}")
print(f"  - Rango: {df['weight_kg'].min():.2f} - {df['weight_kg'].max():.2f}")

print("\n4. DISTRIBUCIÓN GEOGRÁFICA (TOP 10):")
print(df['country'].value_counts().head(10))

print("\n5. VALIDEZ DE EMAIL:")
email_validity = df['email_valid'].value_counts()
print(email_validity)
print(f"Porcentaje de emails válidos: {(email_validity.get(True, 0) / len(df) * 100):.2f}%")

print("\n6. CONSENTIMIENTO MARKETING:")
marketing_consent = df['marketing_consent'].value_counts()
print(marketing_consent)

print("\n7. ANÁLISIS DE GASTO:")
print(f"  - Gasto total: ${df['amount_spent_mxn'].sum():.2f}")
print(f"  - Gasto promedio: ${df['amount_spent_mxn'].mean():.2f}")
print(f"  - Gasto mediano: ${df['amount_spent_mxn'].median():.2f}")
print(f"  - Desv. Est: ${df['amount_spent_mxn'].std():.2f}")

# Crear figura adicional: Análisis de correlaciones
fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

# Correlación: Altura-Peso
ax = axes[0, 0]
correlation_hw = df['height_cm'].corr(df['weight_kg'])
ax.scatter(df['height_cm'], df['weight_kg'], alpha=0.3, color='#3498db')
z = np.polyfit(df['height_cm'].dropna(), df['weight_kg'].dropna(), 1)
p = np.poly1d(z)
ax.plot(df['height_cm'].sort_values(), p(df['height_cm'].sort_values()), "r--", linewidth=2, label=f'Correlación: {correlation_hw:.3f}')
ax.set_xlabel('Altura (cm)')
ax.set_ylabel('Peso (kg)')
ax.set_title('Correlación Altura vs Peso', fontweight='bold')
ax.legend()

# Gasto por idioma
ax = axes[0, 1]
lang_spending = df.groupby('preferred_language')['amount_spent_mxn'].mean().sort_values(ascending=False)
lang_spending.plot(kind='barh', ax=ax, color='#16a085')
ax.set_xlabel('Gasto Promedio (MXN)')
ax.set_title('Gasto Promedio por Idioma Preferido', fontweight='bold')

# Validez de email por país (Top 5)
ax = axes[1, 0]
top_countries = df['country'].value_counts().head(5).index
email_validity_by_country = df[df['country'].isin(top_countries)].groupby('country')['email_valid'].apply(lambda x: (x == True).sum() / len(x) * 100)
email_validity_by_country.sort_values(ascending=False).plot(kind='bar', ax=ax, color='#e74c3c')
ax.set_ylabel('% Emails Válidos')
ax.set_title('Validez de Email por País (Top 5)', fontweight='bold')
ax.tick_params(axis='x', rotation=45)

# Gasto por consentimiento marketing
ax = axes[1, 1]
consent_mapping = {True: 'Sí', False: 'No', 'True': 'Sí', 'False': 'No', 'YES': 'Sí', 'NO': 'No', 'Y': 'Sí', 'N': 'No', 'Sí': 'Sí', '0': 'No', '1': 'Sí'}
df['marketing_consent_clean'] = df['marketing_consent'].astype(str).map(lambda x: consent_mapping.get(x, 'Desconocido'))
consent_spending = df.groupby('marketing_consent_clean')['amount_spent_mxn'].mean().sort_values(ascending=False)
consent_spending.plot(kind='bar', ax=ax, color=['#2ecc71', '#e74c3c'])
ax.set_ylabel('Gasto Promedio (MXN)')
ax.set_xlabel('Consentimiento Marketing')
ax.set_title('Gasto Promedio por Consentimiento Marketing', fontweight='bold')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('analisis_correlaciones.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: analisis_correlaciones.png")

print("\n" + "=" * 80)
print("VISUALIZACIONES COMPLETADAS")
print("=" * 80)
print("\nArchivos generados:")
print("  ✓ visualizacion_datos.png - Dashboard principal con 9 visualizaciones")
print("  ✓ analisis_correlaciones.png - Análisis de correlaciones y relaciones")
print("\n")
