import pandas as pd
from datetime import datetime, timedelta
import random

# adding comment and committing, testing github. 
# if I was to use this code much I would at a minimum create another .py to store all the functions so this main file would just contain the main() at the bottom.


# -----------------------
# Helper Data + Functions
# -----------------------

# -----------------------
# raw data.  the values are the universe of options, the weights are how likely it will generate that option.
col_data = {
    "firstname": {
        "values": [
            "Olivia", "Liam", "Emma", "Noah", "Ava", "Oliver", "Sophia", "Elijah", "Isabella", "Lucas",
            "Mia", "Mason", "Charlotte", "Logan", "Amelia", "Ethan", "Harper", "Aiden", "Evelyn", "James",
            "Abigail", "Benjamin", "Emily", "Henry", "Ella", "Sebastian", "Scarlett", "Jack", "Aria", "Daniel",
            "Luna", "Matthew", "Grace", "Joseph", "Chloe", "Samuel", "Camila", "David", "Penelope", "Carter"
        ]
    },
    "lastname": {
        "values": [
            "Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
            "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall",
            "Allen", "Young", "King", "Wright", "Scott"
        ]
    },
    "dept": {
        "values": ["HR", "Engineering", "Sales", "Support"],
        "weights": [0.2, 0.4, 0.2, 0.2]
    },
    "city": {
        "values": ["Austin", "Dallas", "Atlanta", "Seattle", "Phoenix"],
        "weights": [0.5, 0.16, 0.12, 0.12, 0.10]
    },
    "title": {
        "values": ["programmer", "hr", "sales", "test", "director"],
        "weights": [0.5, 0.1, 0.15, 0.15, 0.05]
    },
    "bool": {
        "values": ["y", "n"],
        "weights": [0.95, 0.05]
    }
}

# -----------------------
# this is for generating columns that either use input from other columns to create it or have some algo to create it
def add_col_special(num, df, types):
    if isinstance(types, str):
        types = [types]  # make it a list so we can loop over it

    for type in types:
        if type == "email":
            if "firstname" not in df.columns or "lastname" not in df.columns:
                raise ValueError("Email generation requires 'firstname' and 'lastname' columns in the DataFrame.")
            df["email"] = [
                f"{first.lower()}_{last.lower()}@example.com"
                for first, last in zip(df["firstname"], df["lastname"])
            ]
        elif type == "phonenumber":
            df["phonenumber"] = [
                f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
                for _ in range(len(df))
            ]
        elif type == "hiredate":
            start_date = datetime(2010, 1, 1)
            df["hiredate"] = [
                (start_date + timedelta(days=random.randint(0, 5000))).date()
                for _ in range(len(df))
            ]
        else:
            raise ValueError(f"Unknown column type: {type}")
        
# -----------------------
def gen_col(num, col):
    config = col_data.get(col)
    if not config:
        raise ValueError(f"No config found for column '{col}'")

    values = config["values"]
    weights = config.get("weights")
    return random.choices(values, weights=weights, k=num)

# -----------------------
# usage: cmp_cols(df1, "firstname", df2, "firstname") --- compares same column name in two diff files
#        cmp_cols(df, "firstname", col2="lastname") --- compares two diff columns in same file
def cmp_cols(df1, col1, df2=None, col2=None):
    # If df2 and col2 aren't provided, compare two columns in the same df
    if df2 is None:
        df2 = df1
    if col2 is None:
        col2 = col1

    diffs = df1[col1] != df2[col2]
    return pd.DataFrame({
        "row": df1.index[diffs],
        f"{col1}_df1": df1.loc[diffs, col1],
        f"{col2}_df2": df2.loc[diffs, col2]
    })

# -----------------------
def count_value(df, col, val):
    return (df[col] == val).sum()

# -----------------------
def bld_spreadsheet(num_rows, *columns):
    data = {}
    for col in columns:
        data[col] = gen_col(num_rows, col)
    return pd.DataFrame(data)


# -----------------------
# Main Program
# -----------------------

def main():
    ROWS = 40
    HSIZE = 40 # how much of the spreadsheet do we wanna print out

    print(("\n".join(["*"] * 5)))

    random.seed(42) # we want to play with the same random set
    df1 = bld_spreadsheet(ROWS, "firstname", "lastname", "city", "dept", "title", "bool")
    add_col_special(ROWS, df1, {"email", "phonenumber", "hiredate"}) #this is adding more columns to the existing df
    print(df1.head(HSIZE))

    print(("\n".join(["*"] * 2)))

    random.seed(88)
    df2 = bld_spreadsheet(ROWS, "firstname", "lastname", "city", "dept", "title", "bool")
    add_col_special(ROWS, df2, {"email", "phonenumber", "hiredate"}) #this is adding more columns to the existing df
    print(df2.head(HSIZE))

    print(cmp_cols(df1,"bool",df2,"bool"))
    print(f"Number of cities that are Austin = {count_value(df1, 'city', 'Austin')}")

# silly check for scope if people use this code in the future which i cant imagine will be the case
if __name__ == "__main__":
    main()
