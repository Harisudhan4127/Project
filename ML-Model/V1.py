import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from xgboost import plot_importance

df = pd.read_csv(r"data/providers_large_deterministic.csv")

X = df[[
    "service_cost",
    "CMS_quality_score",
    "patient_rating",
    "risk_rate",
    "experience_years",
    "capacity"
]]

cost_threshold = df["service_cost"].quantile(0.90)
quality_threshold = df["CMS_quality_score"].median()
df["target"] = ((df["service_cost"] < cost_threshold) | 
                (df["CMS_quality_score"] >= quality_threshold)).astype(int)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(eval_metric="logloss", use_label_encoder=False)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

plot_importance(model)
plt.show()

df["keep_prob"] = model.predict_proba(X)[:, 1]

baseline_cost = df["service_cost"].sum()
region_before = df["region"].nunique()

def evaluate_threshold(thresh):
    selected = df[df["keep_prob"] >= thresh]
    optimized_cost = selected["service_cost"].sum()
    savings_pct = (baseline_cost - optimized_cost) / baseline_cost * 100
    region_after = selected["region"].nunique()
    coverage_pct = (region_after / region_before) * 100
    return savings_pct, coverage_pct, selected


best_thresh = None
final_selected = None

for t in [i/100 for i in range(30, 90)]: 
    savings, coverage, selected = evaluate_threshold(t)
    if 8 <= savings <= 12 and coverage >= 95:
        best_thresh = t
        final_selected = selected
        break

if best_thresh:
    print(f"✅ Found optimal threshold: {best_thresh}")
    print(f"Savings: {savings:.2f}% | Coverage: {coverage:.2f}%")
    optimized_df = final_selected
else:
    print("⚠️ Could not hit exact 8–12% savings with ≥95% coverage. Consider adjusting rules.")
    optimized_df = df 

output_path = r"output/optimized_network_xgb.csv"
optimized_df.to_csv(output_path, index=False)
print("Optimized dataset saved at:", output_path)
