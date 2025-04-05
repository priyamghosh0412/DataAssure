import pandas as pd
import functools
import time
import re


def profile_step(
    expect_column_to_exist=None,
    expect_no_nulls=None,
    expect_column_values_to_be_in_set=None,
    expect_column_values_to_be_unique=None,
    expect_column_values_to_be_between=None,
    expect_column_dtype_to_be=None,
    expect_column_mean_to_be_between=None,
    expect_column_median_to_be_between=None,
    expect_column_max_to_be_between=None,
    expect_column_min_to_be_between=None,
    expect_column_std_to_be_less_than=None,
    expect_column_value_lengths_to_be_between=None,
    expect_table_row_count_to_be_between=None,
    expect_column_proportion_of_unique_values_to_be_between=None,
    expect_column_pair_values_to_be_unique=None,
    expect_column_values_to_not_match_regex=None,
    expect_column_values_to_match_regex=None,
    expect_column_values_to_not_be_in_set=None,
    expect_column_most_common_value_to_be=None,
    expect_table_columns_to_match_ordered_list=None,
    verbose=True
):
    def decorator(inner_func):
        @functools.wraps(inner_func)
        def wrapper(*args, **kwargs):
            with open("validation_report.txt", "w", encoding="utf-8") as report:
                def log(line, severity="INFO"):
                    formatted = f"[{severity}] {line}"
                    if verbose:
                        print(formatted)
                    report.write(formatted + "\n")

                log(f"📄 Validation Report for: {inner_func.__name__}")
                start = time.time()
                try:
                    df = inner_func(*args, **kwargs)
                except Exception as e:
                    log(f"❌ Failed to execute function: {e}", severity="CRITICAL")
                    raise
                end = time.time()
                log(f"⏱️ Function Execution Time: {round(end - start, 4)} seconds")

                def check_column_exists(col):
                    if col not in df.columns:
                        log(f"❌ Column '{col}' does not exist.", severity="CRITICAL")
                        return False
                    else:
                        log(f"✅ Column exists: {col}")
                        return True

                # Modular checks
                try:
                    if expect_column_to_exist:
                        for col in expect_column_to_exist:
                            check_column_exists(col)

                    if expect_no_nulls:
                        for col in expect_no_nulls:
                            if check_column_exists(col):
                                nulls = df[col].isnull().sum()
                                log(f"{'✅' if nulls == 0 else '❌'} Column '{col}' nulls: {nulls}",
                                    severity="WARNING" if nulls > 0 else "INFO")

                    if expect_column_values_to_be_in_set:
                        for col, valid_set in expect_column_values_to_be_in_set.items():
                            if check_column_exists(col):
                                invalid = ~df[col].isin(valid_set)
                                if invalid.any():
                                    log(f"❌ Column '{col}' has values outside {valid_set}",
                                        severity="WARNING")
                                else:
                                    log(f"✅ Column '{col}' values are in set {valid_set}")

                    if expect_column_values_to_be_unique:
                        for col in expect_column_values_to_be_unique:
                            if check_column_exists(col):
                                is_unique = df[col].is_unique
                                log(f"{'✅' if is_unique else '❌'} Column '{col}' uniqueness check",
                                    severity="WARNING" if not is_unique else "INFO")

                    if expect_column_values_to_be_between:
                        for col, (min_v, max_v) in expect_column_values_to_be_between.items():
                            if check_column_exists(col):
                                invalid = ~df[col].between(min_v, max_v)
                                if invalid.any():
                                    log(f"❌ Column '{col}' has values outside range [{min_v}, {max_v}]",
                                        severity="WARNING")
                                else:
                                    log(f"✅ Column '{col}' values are in range [{min_v}, {max_v}]")

                    if expect_column_dtype_to_be:
                        for col, dtype in expect_column_dtype_to_be.items():
                            if check_column_exists(col):
                                if str(df[col].dtype) != dtype:
                                    log(f"❌ Column '{col}' dtype is {df[col].dtype}, expected {dtype}",
                                        severity="WARNING")
                                else:
                                    log(f"✅ Column '{col}' dtype is {dtype}")

                    if expect_column_mean_to_be_between:
                        for col, (low, high) in expect_column_mean_to_be_between.items():
                            if check_column_exists(col):
                                mean_val = df[col].mean()
                                log(f"{'✅' if low <= mean_val <= high else '❌'} Mean of '{col}' is {mean_val}",
                                    severity="INFO" if low <= mean_val <= high else "WARNING")

                    if expect_column_median_to_be_between:
                        for col, (low, high) in expect_column_median_to_be_between.items():
                            if check_column_exists(col):
                                median_val = df[col].median()
                                log(f"{'✅' if low <= median_val <= high else '❌'} Median of '{col}' is {median_val}",
                                    severity="INFO" if low <= median_val <= high else "WARNING")

                    if expect_column_max_to_be_between:
                        for col, (low, high) in expect_column_max_to_be_between.items():
                            if check_column_exists(col):
                                max_val = df[col].max()
                                log(f"{'✅' if low <= max_val <= high else '❌'} Max of '{col}' is {max_val}",
                                    severity="INFO" if low <= max_val <= high else "WARNING")

                    if expect_column_min_to_be_between:
                        for col, (low, high) in expect_column_min_to_be_between.items():
                            if check_column_exists(col):
                                min_val = df[col].min()
                                log(f"{'✅' if low <= min_val <= high else '❌'} Min of '{col}' is {min_val}",
                                    severity="INFO" if low <= min_val <= high else "WARNING")

                    if expect_column_std_to_be_less_than:
                        for col, threshold in expect_column_std_to_be_less_than.items():
                            if check_column_exists(col):
                                std_val = df[col].std()
                                log(f"{'✅' if std_val <= threshold else '❌'} Std of '{col}' is {std_val}",
                                    severity="INFO" if std_val <= threshold else "WARNING")

                    if expect_column_value_lengths_to_be_between:
                        for col, (min_l, max_l) in expect_column_value_lengths_to_be_between.items():
                            if check_column_exists(col):
                                lengths = df[col].astype(str).apply(len)
                                valid = lengths.between(min_l, max_l).all()
                                log(f"{'✅' if valid else '❌'} Lengths of '{col}' are in range",
                                    severity="INFO" if valid else "WARNING")

                    if expect_table_row_count_to_be_between:
                        rows = df.shape[0]
                        low, high = expect_table_row_count_to_be_between
                        valid = low <= rows <= high
                        log(f"{'✅' if valid else '❌'} Row count: {rows}",
                            severity="INFO" if valid else "CRITICAL")

                    if expect_column_proportion_of_unique_values_to_be_between:
                        for col, (low, high) in expect_column_proportion_of_unique_values_to_be_between.items():
                            if check_column_exists(col):
                                ratio = df[col].nunique() / len(df[col])
                                valid = low <= ratio <= high
                                log(f"{'✅' if valid else '❌'} Unique ratio for '{col}': {round(ratio, 3)}",
                                    severity="INFO" if valid else "WARNING")

                    if expect_column_pair_values_to_be_unique:
                        for col1, col2 in expect_column_pair_values_to_be_unique:
                            valid = df.duplicated(subset=[col1, col2]).sum() == 0
                            log(f"{'✅' if valid else '❌'} Uniqueness of pair ({col1}, {col2})",
                                severity="WARNING" if not valid else "INFO")

                    if expect_column_values_to_not_match_regex:
                        for col, pattern in expect_column_values_to_not_match_regex.items():
                            if check_column_exists(col):
                                match = df[col].astype(str).str.contains(pattern, regex=True)
                                valid = not match.any()
                                log(f"{'✅' if valid else '❌'} Column '{col}' should not match regex '{pattern}'",
                                    severity="WARNING" if not valid else "INFO")

                    if expect_column_values_to_match_regex:
                        for col, pattern in expect_column_values_to_match_regex.items():
                            if check_column_exists(col):
                                match = df[col].astype(str).str.match(pattern)
                                valid = match.all()
                                log(f"{'✅' if valid else '❌'} Column '{col}' matches regex '{pattern}'",
                                    severity="WARNING" if not valid else "INFO")

                    if expect_column_values_to_not_be_in_set:
                        for col, bad_set in expect_column_values_to_not_be_in_set.items():
                            if check_column_exists(col):
                                match = df[col].isin(bad_set)
                                valid = not match.any()
                                log(f"{'✅' if valid else '❌'} Column '{col}' should not have values {bad_set}",
                                    severity="WARNING" if not valid else "INFO")

                    if expect_column_most_common_value_to_be:
                        for col, expected in expect_column_most_common_value_to_be.items():
                            if check_column_exists(col):
                                mode = df[col].mode().iloc[0]
                                valid = mode == expected
                                log(f"{'✅' if valid else '❌'} Most common value in '{col}' is '{mode}'",
                                    severity="INFO" if valid else "WARNING")

                    if expect_table_columns_to_match_ordered_list:
                        valid = list(df.columns) == expect_table_columns_to_match_ordered_list
                        log(f"{'✅' if valid else '❌'} Column order matches expected",
                            severity="CRITICAL" if not valid else "INFO")

                except Exception as e:
                    log(f"❌ Validation error: {e}", severity="CRITICAL")

                return df

        return wrapper
    return decorator
