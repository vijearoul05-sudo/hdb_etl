import pandas as pd

def profile_data():
    df = pd.read_csv("data/cleaned/master_dataset.csv")

    print("\n===== BASIC INFO =====")
    print(df.info())

    print("\n===== NULL VALUES =====")
    print(df.isnull().sum())

    print("\n===== UNIQUE VALUES =====")
    for col in df.columns:
        print(f"\n{col}: {df[col].nunique()} unique values")

    print("\n===== SAMPLE VALUES =====")
    for col in ["town", "flat_type", "flat_model"]:
        print(f"\n{col}:")
        print(df[col].value_counts().head(10))

    print("\n===== NUMERICAL STATS =====")
    print(df.describe())

if __name__ == "__main__":
    profile_data()