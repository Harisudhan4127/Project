import pandas as pd

# Load data
file_path = r"data/providers_large_deterministic.csv"
df = pd.read_csv(file_path)

# Step 1: Baseline network cost
baseline_cost = df["service_cost"].sum()

# Step 2: Define thresholds
# High-cost = above 90th percentile cost
cost_threshold = df["service_cost"].quantile(0.90)

# Low quality = CMS quality score below median
quality_threshold = df["CMS_quality_score"].median()

# Step 3: Flag providers for potential removal (high-cost & low-quality)
to_remove = df[(df["service_cost"] > cost_threshold) &
               (df["CMS_quality_score"] < quality_threshold)]

# Step 4: Optimize network by removing flagged providers
optimized_df = df.drop(to_remove.index)

# Step 5: Calculate new total cost and savings
optimized_cost = optimized_df["service_cost"].sum()
savings_pct = (baseline_cost - optimized_cost) / baseline_cost * 100

# Step 6: Check region coverage before vs after
region_before = df["region"].nunique()
region_after = optimized_df["region"].nunique()
coverage_pct = (region_after / region_before) * 100

# Step 7: Save optimized dataset for next model
output_path = "optimized_network.csv"
optimized_df.to_csv(output_path, index=False)

# Print results
print("Baseline Cost:", baseline_cost)
print("Optimized Cost:", optimized_cost)
print("Savings %:", savings_pct)
print("Regions before:", region_before)
print("Regions after:", region_after)
print("Coverage %:", coverage_pct)
print("Optimized dataset saved at:", output_path)
