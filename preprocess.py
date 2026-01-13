import pandas as pd


def basic_data_overview(df):
    print("=== BASIC DATA OVERVIEW ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(df.columns.tolist())
    print(df.head())
    print("\n")


def missing_values_overview(df):
    print("=== MISSING VALUES OVERVIEW ===")

    missing_count = df.isna().sum()
    missing_percent = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        "MissingCount": missing_count,
        "MissingPercent": missing_percent.round(2)
    }).sort_values(by="MissingCount", ascending=False)

    print(missing_df)
    print("\n")

    return missing_df


def basic_statistics(df):
    print("=== BASIC STATISTICS (NUMERICAL) ===")
    print(df.describe())
    print("\n")

    print("=== CATEGORICAL DISTRIBUTIONS ===")
    for col in ["Sex", "Pclass", "Embarked", "Survived"]:
        print(f"\n{col}:")
        print(df[col].value_counts(dropna=False))
    print("\n")


def preprocess_data(
    input_path="data.csv",
    output_path="processed_data.csv"
):
    # 1. Load data
    df = pd.read_csv(input_path)

    # 2. Initial data exploration
    basic_data_overview(df)
    missing_values_overview(df)
    basic_statistics(df)

    # 3. Handle missing values
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df = df.dropna(subset=["Embarked"])

    # 4. Feature engineering
    df["HasCabin"] = df["Cabin"].notna().astype(int)

    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "Young Adult", "Adult", "Senior"]
    )

    df["SurvivedLabel"] = df["Survived"].map(
        {0: "Did not survive", 1: "Survived"}
    )

    # 5. Drop unused columns
    df = df.drop(
        columns=["PassengerId", "Ticket", "Name", "Cabin"],
        errors="ignore"
    )

    # 6. Save processed data
    df.to_csv(output_path, index=False)

    print(f"Preprocessing finished. Output saved to: {output_path}")


if __name__ == "__main__":
    preprocess_data()
