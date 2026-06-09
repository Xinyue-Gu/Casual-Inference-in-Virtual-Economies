import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# 假设 df 是清洗好的面板数据
# 包含列: ['skin_id', 'date', 'price', 'is_treatment', 'is_post', 'player_count']

# 1. 创建交互项 (Treatment Effect)
df['did_interaction'] = df['is_treatment'] * df['is_post']
df['log_price'] = np.log(df['price'])

# 2. 基础 DiD 跑法 (使用聚类稳健标准误 Clustered Standard Errors)
# 在面板数据中，同一个皮肤在不同时间的价格误差项是自相关的，必须聚类到 skin_id 级别
formula_basic = 'log_price ~ is_treatment + is_post + did_interaction + np.log(player_count)'
model_basic = smf.ols(formula_basic, data=df).fit(
    cov_type='cluster', 
    cov_kwds={'groups': df['skin_id']}
)
print(model_basic.summary())

# 3. 进阶：双向固定效应 (TWFE)
# 注意：在包含个体和时间固定效应后，is_treatment 和 is_post 的主效应会被共线性吸收，只留下交互项
formula_twfe = 'log_price ~ did_interaction + np.log(player_count) + C(skin_id) + C(date)'
model_twfe = smf.ols(formula_twfe, data=df).fit(
    cov_type='cluster', 
    cov_kwds={'groups': df['skin_id']}
)
# print(model_twfe.summary()) # 隐藏长输出，重点关注 did_interaction 的 p-value 和系数


# 1. 计算相对时间 (Relative Time)
# 假设 event_date 是更新日期
df['relative_week'] = ((df['date'] - event_date).dt.days // 7)

# 2. 生成哑变量并与 is_treatment 交互
# 排除 relative_week == -1 作为基准组 (Baseline)
weeks = sorted(df['relative_week'].unique())
weeks.remove(-1) 

for w in weeks:
    df[f'treat_x_week_{w}'] = df['is_treatment'] * (df['relative_week'] == w).astype(int)

# 3. 构建公式并运行 OLS
interaction_terms = ' + '.join([f'treat_x_week_{w}' for w in weeks])
formula_event = f'log_price ~ {interaction_terms} + np.log(player_count) + C(skin_id) + C(relative_week)'
model_event = smf.ols(formula_event, data=df).fit(cov_type='cluster', cov_kwds={'groups': df['skin_id']})

# 4. 提取系数和置信区间用于画图
coefs = []
errors = []
plot_weeks = []

for w in weeks:
    var_name = f'treat_x_week_{w}'
    coefs.append(model_event.params[var_name])
    # 95% CI
    conf_int = model_event.conf_int().loc[var_name]
    errors.append(coefs[-1] - conf_int[0])
    plot_weeks.append(w)

# 插入基准组 (-1周, 系数为0)
plot_weeks.append(-1)
coefs.append(0)
errors.append(0)

# 排序以便画图
plot_df = pd.DataFrame({'week': plot_weeks, 'coef': coefs, 'err': errors}).sort_values('week')

# 5. 绘制平行趋势图 (Institutional-Grade Plot)
plt.figure(figsize=(10, 6))
plt.errorbar(plot_df['week'], plot_df['coef'], yerr=plot_df['err'], 
             fmt='-o', capsize=5, color='#1f77b4', markersize=6)
plt.axhline(0, color='black', linestyle='--', linewidth=1.2) # 0效应线
plt.axvline(0, color='red', linestyle='--', linewidth=1.5, label='CS2 Engine Update') # 事件发生日
plt.xlabel('Weeks Relative to Update', fontsize=12)
plt.ylabel('Treatment Effect on Log Price', fontsize=12)
plt.title('Event Study: Parallel Trends Assumption', fontsize=14, weight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()