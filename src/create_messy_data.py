import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


def augment_dataset(df, target_size=5000):
    """
    Augment dataset to target size with realistic data patterns
    """
    current_size = len(df)
    additional_needed = target_size - current_size

    if additional_needed <= 0:
        return df

    new_rows = []

    # Define realistic data distributions
    regions = [
        "North America",
        "Europe",
        "Asia",
        "South America",
        "Africa",
        "Australia",
        "Middle East",
    ]
    industries = [
        "Technology",
        "Finance",
        "Healthcare",
        "Education",
        "Manufacturing",
        "Retail",
        "Consulting",
        "Media",
        "Government",
        "Non-profit",
    ]
    job_roles = [
        "Software Developer",
        "Data Analyst",
        "Project Manager",
        "Marketing Manager",
        "Sales Representative",
        "Designer",
        "Customer Support",
        "HR Manager",
        "Financial Analyst",
        "Content Writer",
        "Product Manager",
        "Consultant",
    ]
    work_arrangements = ["Remote", "Hybrid", "Office"]
    mental_health_statuses = ["Good", "Fair", "Poor", "Excellent", "Very Poor"]
    burnout_levels = ["Low", "Moderate", "High", "Very High", "None"]
    physical_health_issues = [
        "None",
        "Back Pain",
        "Eye Strain",
        "Neck Pain",
        "Headaches",
        "Carpal Tunnel",
        "Fatigue",
        "Multiple Issues",
    ]
    salary_ranges = [
        "$30k-$50k",
        "$50k-$70k",
        "$70k-$100k",
        "$100k-$150k",
        "$150k-$200k",
        "$200k+",
        "Under $30k",
    ]

    for i in range(additional_needed):
        new_row = {}

        # Survey_Date - Generate realistic dates in 2025
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 6, 30)
        days_diff = (end_date - start_date).days
        random_date = start_date + timedelta(days=np.random.randint(0, days_diff))
        new_row["Survey_Date"] = random_date.strftime("%Y-%m-%d")

        # Age - Realistic age distribution (22-65)
        age_weights = np.array([0.01] * 44)  # Base weight for all ages
        age_weights[3:14] = 0.03  # Ages 25-35 (peak)
        age_weights[14:24] = 0.025  # Ages 36-45
        age_weights[24:34] = 0.02  # Ages 46-55
        age_weights = age_weights / age_weights.sum()
        new_row["Age"] = np.random.choice(range(22, 66), p=age_weights)

        # Gender - Realistic distribution
        new_row["Gender"] = np.random.choice(
            ["Male", "Female", "Other"], p=[0.48, 0.5, 0.02]
        )

        # Region - Global distribution
        new_row["Region"] = np.random.choice(
            regions, p=[0.3, 0.25, 0.2, 0.1, 0.05, 0.05, 0.05]
        )

        # Industry - Common remote work industries
        new_row["Industry"] = np.random.choice(
            industries, p=[0.2, 0.15, 0.12, 0.1, 0.08, 0.08, 0.07, 0.05, 0.05, 0.1]
        )

        # Job_Role - Remote-friendly roles
        new_row["Job_Role"] = np.random.choice(job_roles)

        # Work_Arrangement - Remote work distribution
        work_arrangement = np.random.choice(work_arrangements, p=[0.4, 0.35, 0.25])
        new_row["Work_Arrangement"] = work_arrangement

        # Hours_Per_Week - Realistic work hours
        hours_weights = np.zeros(41)  # 20-60 hours
        hours_weights[20] = 0.3  # 40 hours (standard)
        hours_weights[15:26] = 0.15  # 35-45 hours
        hours_weights[5:15] = 0.1  # 25-34 hours (part-time)
        hours_weights[26:36] = 0.08  # 46-55 hours (overtime)
        hours_weights[0:5] = 0.02  # 20-24 hours
        hours_weights[36:41] = 0.02  # 56-60 hours
        hours_weights = hours_weights / hours_weights.sum()
        new_row["Hours_Per_Week"] = np.random.choice(range(20, 61), p=hours_weights)

        # Mental_Health_Status - Distribution based on work arrangement
        if work_arrangement == "Remote":
            new_row["Mental_Health_Status"] = np.random.choice(
                mental_health_statuses, p=[0.3, 0.3, 0.25, 0.1, 0.05]
            )
        elif work_arrangement == "Hybrid":
            new_row["Mental_Health_Status"] = np.random.choice(
                mental_health_statuses, p=[0.35, 0.25, 0.2, 0.15, 0.05]
            )
        else:  # Office
            new_row["Mental_Health_Status"] = np.random.choice(
                mental_health_statuses, p=[0.4, 0.25, 0.15, 0.15, 0.05]
            )

        # Burnout_Level - Correlated with work arrangement
        if work_arrangement == "Remote":
            new_row["Burnout_Level"] = np.random.choice(
                burnout_levels, p=[0.2, 0.35, 0.25, 0.15, 0.05]
            )
        elif work_arrangement == "Hybrid":
            new_row["Burnout_Level"] = np.random.choice(
                burnout_levels, p=[0.25, 0.3, 0.2, 0.1, 0.15]
            )
        else:  # Office
            new_row["Burnout_Level"] = np.random.choice(
                burnout_levels, p=[0.3, 0.25, 0.15, 0.05, 0.25]
            )

        # Work_Life_Balance_Score - 1-10 scale (higher for remote/hybrid)
        if work_arrangement == "Remote":
            new_row["Work_Life_Balance_Score"] = np.random.randint(4, 11)
        elif work_arrangement == "Hybrid":
            new_row["Work_Life_Balance_Score"] = np.random.randint(5, 11)
        else:  # Office
            new_row["Work_Life_Balance_Score"] = np.random.randint(3, 9)

        # Physical_Health_Issues - Common remote work issues
        if work_arrangement == "Remote":
            new_row["Physical_Health_Issues"] = np.random.choice(
                physical_health_issues, p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.05, 0.03, 0.02]
            )
        elif work_arrangement == "Hybrid":
            new_row["Physical_Health_Issues"] = np.random.choice(
                physical_health_issues, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
            )
        else:  # Office
            new_row["Physical_Health_Issues"] = np.random.choice(
                physical_health_issues, p=[0.4, 0.15, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
            )

        # Social_Isolation_Score - 1-10 scale (higher for remote)
        if work_arrangement == "Remote":
            new_row["Social_Isolation_Score"] = np.random.randint(4, 11)
        elif work_arrangement == "Hybrid":
            new_row["Social_Isolation_Score"] = np.random.randint(2, 8)
        else:  # Office
            new_row["Social_Isolation_Score"] = np.random.randint(1, 6)

        # Salary_Range - Realistic distribution
        new_row["Salary_Range"] = np.random.choice(
            salary_ranges, p=[0.2, 0.25, 0.25, 0.15, 0.08, 0.05, 0.02]
        )

        new_rows.append(new_row)

    # Create DataFrame and combine with original
    new_df = pd.DataFrame(new_rows)

    # Ensure column order matches original
    new_df = new_df[df.columns]

    # Combine datasets
    result_df = pd.concat([df, new_df], ignore_index=True)

    return result_df


def add_realistic_messiness(df):
    """
    Add realistic data quality issues to the dataset
    """
    df_messy = df.copy()
    n_rows = len(df_messy)

    print(f"Adding messiness to {n_rows} rows...")

    # 1. MISSING VALUES - Strategic patterns
    # Work_Life_Balance_Score missing (sensitive topic)
    missing_wlb = np.random.choice(
        df_messy.index, size=int(0.12 * n_rows), replace=False
    )
    df_messy.loc[missing_wlb, "Work_Life_Balance_Score"] = np.nan

    # Age missing (privacy concerns)
    missing_age = np.random.choice(
        df_messy.index, size=int(0.05 * n_rows), replace=False
    )
    df_messy.loc[missing_age, "Age"] = np.nan

    # Social_Isolation_Score missing
    missing_social = np.random.choice(
        df_messy.index, size=int(0.08 * n_rows), replace=False
    )
    df_messy.loc[missing_social, "Social_Isolation_Score"] = np.nan

    # Mental_Health_Status missing (sensitive topic)
    missing_mental = np.random.choice(
        df_messy.index, size=int(0.15 * n_rows), replace=False
    )
    df_messy.loc[missing_mental, "Mental_Health_Status"] = np.nan

    # Hours_Per_Week missing (incomplete surveys)
    missing_hours = np.random.choice(
        df_messy.index, size=int(0.06 * n_rows), replace=False
    )
    df_messy.loc[missing_hours, "Hours_Per_Week"] = np.nan

    # 2. INCONSISTENT FORMATTING
    # Work_Arrangement variations
    work_variations = {
        "Remote": [
            "remote",
            "REMOTE",
            "Remote Work",
            "Work from Home",
            "WFH",
            "Remote ",
            "  Remote",
        ],
        "Hybrid": [
            "hybrid",
            "HYBRID",
            "Hybrid Work",
            "Mixed",
            "Flexible",
            "Hybrid ",
            "  Hybrid",
        ],
        "Office": [
            "office",
            "OFFICE",
            "On-site",
            "In-person",
            "Office Work",
            "Office ",
            "  Office",
        ],
    }

    for original, variations in work_variations.items():
        mask = df_messy["Work_Arrangement"] == original
        indices = df_messy[mask].index
        change_indices = np.random.choice(
            indices, size=int(0.15 * len(indices)), replace=False
        )
        for idx in change_indices:
            df_messy.loc[idx, "Work_Arrangement"] = np.random.choice(variations)

    # Gender variations
    gender_variations = {
        "Male": ["male", "MALE", "M", "Man", "Male ", "  Male"],
        "Female": ["female", "FEMALE", "F", "Woman", "Female ", "  Female"],
        "Other": [
            "other",
            "OTHER",
            "Non-binary",
            "Prefer not to say",
            "Other ",
            "  Other",
        ],
    }

    for original, variations in gender_variations.items():
        mask = df_messy["Gender"] == original
        indices = df_messy[mask].index
        if len(indices) > 0:
            change_indices = np.random.choice(
                indices, size=int(0.08 * len(indices)), replace=False
            )
            for idx in change_indices:
                df_messy.loc[idx, "Gender"] = np.random.choice(variations)

    # Industry variations
    industry_variations = {
        "Technology": [
            "Tech",
            "IT",
            "Software",
            "Technology ",
            "tech",
            "TECHNOLOGY",
            "  Technology",
        ],
        "Finance": [
            "Financial Services",
            "Banking",
            "Fintech",
            "Finance ",
            "finance",
            "FINANCE",
            "  Finance",
        ],
        "Healthcare": [
            "Health Care",
            "Medical",
            "Healthcare ",
            "healthcare",
            "HEALTHCARE",
            "  Healthcare",
        ],
        "Education": [
            "Educational",
            "Academic",
            "Education ",
            "education",
            "EDUCATION",
            "  Education",
        ],
        "Manufacturing": [
            "Manufacturing ",
            "Production",
            "Industrial",
            "manufacturing",
            "MANUFACTURING",
            "  Manufacturing",
        ],
    }

    for original, variations in industry_variations.items():
        mask = df_messy["Industry"] == original
        indices = df_messy[mask].index
        if len(indices) > 0:
            change_indices = np.random.choice(
                indices, size=int(0.1 * len(indices)), replace=False
            )
            for idx in change_indices:
                df_messy.loc[idx, "Industry"] = np.random.choice(variations)

    # 3. OUTLIERS AND IMPOSSIBLE VALUES
    # Age outliers
    outlier_age = np.random.choice(
        df_messy.index, size=int(0.01 * n_rows), replace=False
    )
    for idx in outlier_age:
        df_messy.loc[idx, "Age"] = np.random.choice([15, 16, 17, 85, 90, 150, 1995, 0])

    # Work_Life_Balance_Score outliers (should be 1-10)
    outlier_wlb = np.random.choice(
        df_messy.index, size=int(0.02 * n_rows), replace=False
    )
    for idx in outlier_wlb:
        df_messy.loc[idx, "Work_Life_Balance_Score"] = np.random.choice(
            [0, 11, 12, 15, 99, -1]
        )

    # Social_Isolation_Score outliers (should be 1-10)
    outlier_social = np.random.choice(
        df_messy.index, size=int(0.015 * n_rows), replace=False
    )
    for idx in outlier_social:
        df_messy.loc[idx, "Social_Isolation_Score"] = np.random.choice(
            [0, 11, 12, 15, 99, -1]
        )

    # Hours_Per_Week outliers
    outlier_hours = np.random.choice(
        df_messy.index, size=int(0.01 * n_rows), replace=False
    )
    for idx in outlier_hours:
        df_messy.loc[idx, "Hours_Per_Week"] = np.random.choice(
            [0, 1, 100, 168, 999, -5]
        )

    # 4. DUPLICATES
    # Create exact duplicates
    duplicate_indices = np.random.choice(
        df_messy.index, size=int(0.03 * n_rows), replace=False
    )
    duplicate_rows = df_messy.loc[duplicate_indices].copy()
    df_messy = pd.concat([df_messy, duplicate_rows], ignore_index=True)

    # 5. WHITESPACE AND FORMATTING ISSUES
    text_columns = [
        "Gender",
        "Region",
        "Industry",
        "Job_Role",
        "Work_Arrangement",
        "Mental_Health_Status",
        "Burnout_Level",
        "Physical_Health_Issues",
        "Salary_Range",
    ]

    for col in text_columns:
        if col in df_messy.columns:
            # Add random whitespace
            mask = df_messy[col].notna()
            indices = df_messy[mask].index
            whitespace_indices = np.random.choice(
                indices, size=int(0.1 * len(indices)), replace=False
            )
            for idx in whitespace_indices:
                original = str(df_messy.loc[idx, col])
                variations = [
                    f"  {original}  ",
                    f" {original}",
                    f"{original} ",
                    f"\t{original}",
                    f"{original}\n",
                ]
                df_messy.loc[idx, col] = np.random.choice(variations)

    # 6. DATE FORMAT INCONSISTENCIES
    date_indices = df_messy["Survey_Date"].notna()
    indices = df_messy[date_indices].index
    change_indices = np.random.choice(
        indices, size=int(0.15 * len(indices)), replace=False
    )

    for idx in change_indices:
        try:
            original_date = pd.to_datetime(df_messy.loc[idx, "Survey_Date"])
            formats = [
                original_date.strftime("%m/%d/%Y"),
                original_date.strftime("%d-%m-%Y"),
                original_date.strftime("%Y/%m/%d"),
                original_date.strftime("%b %d, %Y"),
                original_date.strftime("%d %B %Y"),
                original_date.strftime("%Y-%m-%d %H:%M:%S"),
                original_date.strftime("%m-%d-%Y"),
            ]
            df_messy.loc[idx, "Survey_Date"] = np.random.choice(formats)
        except:
            pass

    # 7. TYPOS AND SPELLING ERRORS
    # Mental Health Status typos
    mental_health_typos = {
        "Good": ["good", "GOOD", "Good ", "Goo", "god", "Goood"],
        "Fair": ["fair", "FAIR", "Fair ", "Fiar", "fare", "Faire"],
        "Poor": ["poor", "POOR", "Poor ", "Por", "pore", "Pooor"],
        "Excellent": [
            "excellent",
            "EXCELLENT",
            "Excelent",
            "Excellnt",
            "Excellent ",
            "Exellent",
        ],
        "Very Poor": [
            "very poor",
            "VERY POOR",
            "Very por",
            "Very Poor ",
            "verypoor",
            "Very Pooor",
        ],
    }

    for original, typos in mental_health_typos.items():
        mask = df_messy["Mental_Health_Status"] == original
        indices = df_messy[mask].index
        if len(indices) > 0:
            change_indices = np.random.choice(
                indices, size=int(0.05 * len(indices)), replace=False
            )
            for idx in change_indices:
                df_messy.loc[idx, "Mental_Health_Status"] = np.random.choice(typos)

    # Burnout Level typos
    burnout_typos = {
        "Low": ["low", "LOW", "Low ", "Lw", "lo"],
        "Moderate": ["moderate", "MODERATE", "Moderat", "Moderate ", "Moderete"],
        "High": ["high", "HIGH", "High ", "Hgh", "hi"],
        "Very High": ["very high", "VERY HIGH", "Very Hgh", "Very High ", "veryhigh"],
        "None": ["none", "NONE", "None ", "non", "N/A", "nil"],
    }

    for original, typos in burnout_typos.items():
        mask = df_messy["Burnout_Level"] == original
        indices = df_messy[mask].index
        if len(indices) > 0:
            change_indices = np.random.choice(
                indices, size=int(0.05 * len(indices)), replace=False
            )
            for idx in change_indices:
                df_messy.loc[idx, "Burnout_Level"] = np.random.choice(typos)

    # 8. MIXED DATA TYPES
    # Convert some numeric fields to strings with various formats
    numeric_cols = [
        "Age",
        "Hours_Per_Week",
        "Work_Life_Balance_Score",
        "Social_Isolation_Score",
    ]

    for col in numeric_cols:
        mask = df_messy[col].notna()
        indices = df_messy[mask].index
        if len(indices) > 0:
            change_indices = np.random.choice(
                indices, size=int(0.02 * len(indices)), replace=False
            )
            for idx in change_indices:
                original = df_messy.loc[idx, col]
                if pd.notna(original):
                    string_variations = [
                        f"{original}.0",
                        f"{original}.00",
                        f" {original} ",
                        f"{original}hrs" if "Hours" in col else f"{original}pts",
                        f"Level {original}"
                        if "Score" in col
                        else f"Age {original}"
                        if col == "Age"
                        else f"{original}",
                        f"({original})",
                        f"{original}+",
                    ]
                    df_messy.loc[idx, col] = np.random.choice(string_variations)

    print(f"Messiness added! Final dataset shape: {df_messy.shape}")
    return df_messy


def main():
    """
    Main function to create messy dataset
    """
    # Check current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    # Try different possible paths
    possible_paths = [
        "data/post_pandemic_remote_work_health_impact_2025_raw.csv",
        "../data/post_pandemic_remote_work_health_impact_2025_raw.csv",
        "./data/post_pandemic_remote_work_health_impact_2025_raw.csv",
    ]

    df_original = None
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df_original = pd.read_csv(path)
                print(f"✅ Loaded original dataset from: {path}")
                print(f"Original dataset shape: {df_original.shape}")
                break
        except Exception:
            continue

    if df_original is None:
        print("❌ Original dataset not found. Creating a sample dataset...")
        # Create sample dataset with your exact columns
        df_original = pd.DataFrame(
            {
                "Survey_Date": ["2025-01-15", "2025-01-16", "2025-01-17"],
                "Age": [25, 30, 35],
                "Gender": ["Male", "Female", "Other"],
                "Region": ["North America", "Europe", "Asia"],
                "Industry": ["Technology", "Finance", "Healthcare"],
                "Job_Role": ["Software Developer", "Data Analyst", "Project Manager"],
                "Work_Arrangement": ["Remote", "Hybrid", "Office"],
                "Hours_Per_Week": [40, 35, 45],
                "Mental_Health_Status": ["Good", "Fair", "Poor"],
                "Burnout_Level": ["Low", "Moderate", "High"],
                "Work_Life_Balance_Score": [7, 6, 5],
                "Physical_Health_Issues": ["None", "Back Pain", "Eye Strain"],
                "Social_Isolation_Score": [3, 5, 2],
                "Salary_Range": ["$50k-$70k", "$70k-$100k", "$100k-$150k"],
            }
        )
        print(f"Sample dataset created with shape: {df_original.shape}")

    # Augment dataset
    print("Augmenting dataset...")
    df_augmented = augment_dataset(df_original, target_size=5000)
    print(f"Augmented dataset shape: {df_augmented.shape}")

    # Add messiness
    print("Adding messiness...")
    df_messy = add_realistic_messiness(df_augmented)

    # Save dataset
    output_path = "../data/remote_work_health_dataset_augmented_raw.csv"

    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_messy.to_csv(output_path, index=False)
        print(f"✅ Messy dataset saved to: {output_path}")
    except Exception as e:
        print(f"❌ Could not save to {output_path}: {e}")
        return None

    print("\n🎯 Dataset creation complete!")
    print(f"Final shape: {df_messy.shape}")
    print(f"Missing values: {df_messy.isnull().sum().sum()}")
    print(f"Duplicates: {df_messy.duplicated().sum()}")

    return df_messy


if __name__ == "__main__":
    df_final = main()
