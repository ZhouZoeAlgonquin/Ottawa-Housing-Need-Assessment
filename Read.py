import pandas
import os
from pymongo import MongoClient

output_path = r"E:\output_csv"
os.makedirs(output_path, exist_ok=True)

#1. Reading and handling data of Immigrant Population.csv - Zoe Zhou
immigrantPopulation = pandas.read_csv('Immigrant Population.csv')
immigrantPopulation["Year"] = immigrantPopulation["Year"].astype(int)
immigrantPopulation["Population Group"] = immigrantPopulation["Population Group"].astype(str).str.replace(",", "").str.strip()
immigrantPopulation["Number"] = immigrantPopulation["Number"].astype(int)
immigrantPopulation["Percentage of Total Population"] = immigrantPopulation["Percentage of Total Population"].astype(float)
immigrantPopulation.to_csv(f"{output_path}/immigration_population.csv", index=False)
print("1. Immigration Population 文件清洁完成")


#2. Reading and handling data of Households.csv - Zoe Zhou
households = pandas.read_csv('Households.csv')
households["Number of Households"] = households["Number of Households"].astype(str).str.replace(",", "").str.strip()
households["Year"] = households["Year"].astype(int)
households["Population Percentage"] = households["Population Percentage"].astype(float)
households["Household Size"] = households["Household Size"].astype(str).str.replace(",", "").str.strip()
households["Dwelling Type"] = households["Dwelling Type"].astype(str).str.replace(",", "").str.strip()
households["Tenure"] = households["Tenure"].astype(str).str.replace(",", "").str.strip()

household_number_by_year = households.iloc[0:4]
household_number_by_year.columns = ["Year", "Number of Households", "Population Percentage", "Household Size",
                                    "Dwelling Type", "Tenure"]

household_size_by_year = households.iloc[4:19]
household_size_by_year.columns = ["Year", "Number of Households", "Population Percentage", "Household Size",
                                  "Dwelling Type", "Tenure"]

household_dwelling_type = households.iloc[19:33]
household_dwelling_type.columns = ["Year", "Number of Households", "Population Percentage", "Household Size", "Dwelling Type",
                         "Tenure"]
household_renter_owner = households.iloc[33:]


household_number_by_year.to_csv(f"{output_path}/household_number_by_year.csv", index=False)
household_size_by_year.to_csv(f"{output_path}/household_size_by_year.csv", index=False)
household_dwelling_type.to_csv(f"{output_path}/household_dwelling_type.csv", index=False)
household_renter_owner.to_csv(f"{output_path}/household_renter_owner.csv", index=False)

print("2. Households文件清洁完成")

#3. Reading and handling data of Housing Costs.csv - Zoe Zhou
housingCost = pandas.read_csv("Housing Costs.csv")

housingCost["Year"] = housingCost["Year"].astype(int)
housingCost["Rent Range"] = housingCost["Rent Range"].astype(str)
housingCost["Percentage of Households"]=housingCost["Percentage of Households"].astype(float)
housingCost["Rent Metric Type"] = housingCost["Rent Metric Type"].astype(str)
housingCost["Rent Amount"] = (housingCost["Rent Amount"].astype(str).str.replace("$", "", regex=False)
                              .str.replace(",", "", regex=False).str.strip().astype(float))
housingCost["Rent Amount"] = housingCost["Rent Amount"].apply(lambda x: f"${x:,.2f}")
housingCost["City"] = housingCost["City"].astype(str)
housingCost["Fiscal Quarter"] = housingCost["Fiscal Quarter"].astype(str)

rent_range_by_year = housingCost.iloc[1:21]
rent_range_by_year.columns = ["Year", "Rent Range", "Percentage of Households", "Rent Metric Type",
                              "Rent Amount", "City", "Fiscal Quarter"]
rent_range_by_year.to_csv(f"{output_path}/rent_range_by_year.csv", index=False)

ottawa_rent_amount_by_year = housingCost.iloc[21:42]
ottawa_rent_amount_by_year.columns = ["Year", "Rent Range", "Percentage of Households", "Rent Metric Type",
                                      "Rent Amount", "City", "Fiscal Quarter"]
ottawa_rent_amount_by_year.to_csv(f"{output_path}/ottawa_rent_amount_by_year.csv", index=False)

turnover_nonTurnover_unit_rent_2022 = housingCost.iloc[42:52]
turnover_nonTurnover_unit_rent_2022.columns = ["Year", "Rent Range", "Percentage of Households",
                                               "Rent Metric Type", "Rent Amount", "City", "Fiscal Quarter"]
turnover_nonTurnover_unit_rent_2022.to_csv(f"{output_path}/turnover_nonTurnover_unit_rent_2022.csv", index=False)

ottawa_urbanation_average_rent_by_fiscal_quarter = housingCost.iloc[52:60]
ottawa_urbanation_average_rent_by_fiscal_quarter.columns = ["Year", "Rent Range", "Percentage of Households",
                                                            "Rent Metric Type", "Rent Amount", "City", "Fiscal Quarter"]
ottawa_urbanation_average_rent_by_fiscal_quarter.to_csv(f"{output_path}/ottawa_urbanation_average_rent_by_fiscal_quarter.csv", index=False)

print("3. Housing Costs文件清洁完成")

#4. Reading and handling data of Housing Development.csv - Zoe Zhou
housingDevelopment = pandas.read_csv("Housing Development.csv")

rows_to_delete = [
    range(15, 19),
    range(34, 38),
    range(53, 57),
    range(72, 76),
    range(91, 95),
    range(110, 114),
    range(129, 133),
    range(148, 152),
    range(167, 171),
    range(186, 190),
    range(205, 209),
]

delete_idx = []
for r in rows_to_delete:
    delete_idx.extend(list(r))

housingDevelopment_cleaned = housingDevelopment.drop(delete_idx)
housingDevelopment_cleaned = housingDevelopment_cleaned.reset_index(drop=True)

housingDevelopment_cleaned.to_csv(f"{output_path}/housingDevelopment.csv", index=False)
print("4. housingDevelopment清洁完成")

#5. Reading and handling data of Housing Stock.csv - Zoe Zhou
housingStock = pandas.read_csv("Housing Stock.csv")

housingStock["Year"] = housingStock["Year"].astype(int)
housingStock["Dwelling Type"] = housingStock["Dwelling Type"].astype(str).str.replace(",", "").str.strip()
housingStock["Number of Occupied Dwellings"] = housingStock["Number of Occupied Dwellings"].str.replace(",", "").str.strip().astype(int)
housingStock["Percentage of Total Occupied Dwellings"] = housingStock["Percentage of Total Occupied Dwellings"].astype(float)

housingStock_2021_by_dwelling_type = housingStock.iloc[1:8]
housingStock_2021_by_dwelling_type.columns = ["Year", "Dwelling Type", "Number of Occupied Dwellings", "Period of Construction",
                                      "Percentage of Total Occupied Dwellings"]
housingStock_2021_by_dwelling_type.to_csv(f"{output_path}/housingStock_2021_by_dwelling_type.csv", index=False)

housingStock_2021_by_period_of_construction = housingStock.iloc[8:16]
housingStock_2021_by_period_of_construction.columns = ["Year", "Dwelling Type", "Number of Occupied Dwellings", "Period of Construction",
                                      "Percentage of Total Occupied Dwellings"]
housingStock_2021_by_period_of_construction.to_csv(f"{output_path}/housingStock_2021_by_period_of_construction.csv", index=False)

print("5. Housing Stock清洁完成")

#6. Reading and handling data of Income.csv - Zoe Zhou
income = pandas.read_csv("Income.csv")
income["Year"] = income["Year"].astype(int)
income["Median Income"] = (
    income["Median Income"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
income["Median Income"] = pandas.to_numeric(income["Median Income"], errors="coerce").fillna(0)
income["Median Income"] = income["Median Income"].astype(int)
income["Average Income"] = (
    income["Average Income"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
income["Average Income"] = pandas.to_numeric(income["Average Income"], errors="coerce").fillna(0)
income["Average Income"] = income["Average Income"].astype(int)
income["Very Low Income (20% or under of AMHI)"] = income["Very Low Income (20% or under of AMHI)"].astype(float)
income["Low Income (21% to 50% of AMHI)"] = income["Low Income (21% to 50% of AMHI)"].astype(float)
income["Moderate Income (51% to 80% of AMHI)"] = income["Moderate Income (51% to 80% of AMHI)"].astype(float)
income["Median Income (81% to 120% of AMHI)"] = income["Median Income (81% to 120% of AMHI)"].astype(float)
income["High Income (121% and more of AMHI)"] = income["High Income (121% and more of AMHI)"].astype(float)

income_by_number = income[
    [
        "Year",
        "Median Income",
        "Average Income",
    ]
]

income_by_number.to_csv(f"{output_path}/income_by_number.csv", index=False)

income_by_range = income[
    [
        "Year",
        "Very Low Income (20% or under of AMHI)",
        "Moderate Income (51% to 80% of AMHI)",
        "Median Income (81% to 120% of AMHI)",
        "High Income (121% and more of AMHI)",
    ]
]
income_by_range.to_csv(f"{output_path}/income_by_range.csv", index=False)

print("6. Income清洁完成")
#7. Reading and handling data of Population by Age Group.csv - Zoe Zhou
populationByAgeGroup = pandas.read_csv("Population by Age Group.csv")

populationByAgeGroup["Year"] = populationByAgeGroup["Year"].astype(int)
populationByAgeGroup["Age Group"] = populationByAgeGroup["Age Group"].astype(str)
populationByAgeGroup["Population Percentage"] = populationByAgeGroup["Population Percentage"].astype(float)
populationByAgeGroup["Gender"] = populationByAgeGroup["Gender"].astype(str)

populationByAgeGroup_all = populationByAgeGroup.iloc[1:12]
populationByAgeGroup_all.columns = ["Year", "Age Group", "Population Percentage", "Gender"]
populationByAgeGroup_all.to_csv(f"{output_path}/populationByAgeGroup_all.csv", index=False)

populationByAgeGroup_byGender = populationByAgeGroup.iloc[12:26]
populationByAgeGroup_byGender.columns = ["Year", "Age Group", "Population Percentage", "Gender"]
populationByAgeGroup_byGender.to_csv(f"{output_path}/populationByAgeGroup_byGender.csv", index=False)

print("7. Population by Age Group清洁完成")

#8. Reading and handling data of New Centralized Wait List Applications.csv - Zoe Zhou
new_centralized_waitlist = pandas.read_csv("New Centralized Wait List Applications.csv")

rows = [0, 6, 12, 18, 24, 30]

total_new_centralized_waitlist = new_centralized_waitlist.iloc[rows]
total_new_centralized_waitlist.columns = ["Year", "Number", "Percentage", "Percentage of Total Waitlist",
                                          "Chart Type", "Household Type"]
total_new_centralized_waitlist.to_csv(f"{output_path}/total_new_centralized_waitlist.csv", index=False)

new_centralized_waitlist_by_household = new_centralized_waitlist.drop(index=rows)
new_centralized_waitlist_by_household.columns = ["Year", "Number", "Percentage", "Percentage of Total Waitlist",
                                          "Chart Type", "Household Type"]
new_centralized_waitlist_by_household.to_csv(f"{output_path}/new_centralized_waitlist_by_household.csv", index=False)

print("8. New Centralized Wait List Applications清洁完成 ")

#9. Reading and handling data of Rent-Geared-to-Income and Housing Benefits.csv - Zoe Zhou
rent_geared_to_income = pandas.read_csv("Rent-Geared-to-Income and Housing Benefits.csv")
rent_geared_to_income["Year"] = rent_geared_to_income["Year"].astype(int)
rent_geared_to_income["Rent Supplements"] = rent_geared_to_income["Rent Supplements"].astype(int)
rent_geared_to_income["Housing Allowances"] = rent_geared_to_income["Housing Allowances"].fillna(0).astype(int)
rent_geared_to_income["Rent-Geared-to-Income"] = rent_geared_to_income["Rent-Geared-to-Income"].astype(int)

rent_geared_to_income.to_csv(f"{output_path}/rent_geared_to_income.csv", index=False)
print("9. Rent-Geared-to-Income and Housing Benefits清洁完成 ")


#10. Reading and handling data of Shelter Average Length of Stay.csv - Zoe Zhou
shelter_length_of_stay = pandas.read_csv("Shelter Average Length of Stay.csv")
row2 = [4,9,14,19,24,29]

shelter_length_of_stay["Year"] = shelter_length_of_stay["Year"].astype(int)
shelter_length_of_stay["Average Length of Stay (Days)"] = shelter_length_of_stay["Average Length of Stay (Days)"].astype(int)
shelter_length_of_stay["Population Group"] = shelter_length_of_stay["Population Group"].astype(str)

total_shelter_length_of_stay = shelter_length_of_stay.iloc[row2]
total_shelter_length_of_stay.columns = ["Year", "Average Length of Stay (Days)", "Population Group"]
total_shelter_length_of_stay.to_csv(f"{output_path}/total_shelter_length_of_stay.csv", index=False)

shelter_length_of_stay_by_population_group = shelter_length_of_stay.drop(index=row2)
shelter_length_of_stay_by_population_group.columns = ["Year", "Average Length of Stay (Days)", "Population Group"]
shelter_length_of_stay_by_population_group.to_csv(f"{output_path}/shelter_length_of_stay_by_population_group.csv", index=False)

print("10. Shelter Average Length of Stay 清洁完成")

#11. Reading and handling data of Shelter Demand and Capacity.csv - Zoe Zhou
shelter_demand = pandas.read_csv("Shelter Demand and Capacity.csv")

shelter_demand["Year"] = shelter_demand["Year"].astype(int)
shelter_demand["Number"] = shelter_demand["Number"].astype(int)
shelter_demand["Population Group"] = shelter_demand["Population Group"].astype(str)
shelter_demand["Shelter System Demand or Capacity?"] = shelter_demand["Shelter System Demand or Capacity?"].astype(str)

total_population_group_shelter_demand = shelter_demand.iloc[18:24]
total_population_group_shelter_demand.columns = ["Year", "Number","Population Group", "Shelter System Demand or Capacity?"]
total_population_group_shelter_demand.to_csv(f"{output_path}/total_population_group_shelter_demand.csv", index=False)

print("11. Shelter Demand and Capacity清洁完成")
#12. Reading and handling data of Vacancy Rate.csv - Zoe Zhou

vacancy = pandas.read_csv("Vacancy Rate.csv")

vacancy["Year"] = vacancy["Year"].astype(int)
vacancy["Unit Type"] = vacancy["Unit Type"].astype(str)
vacancy["Rent Range"] = vacancy["Rent Range"].astype(str)
vacancy["Vacancy Rate"] = vacancy["Vacancy Rate"].astype(float)
vacancy["Healthy Vacancy Rate"] = vacancy["Healthy Vacancy Rate"].astype(float)

vacancy_by_rent_range = vacancy.iloc[1:13].drop(index=6)
vacancy_by_rent_range.columns = ["Year", "Unit Type","Rent Range","Vacancy Rate", "Healthy Vacancy Rate"]
vacancy_by_rent_range.to_csv(f"{output_path}/vacancy_by_rent_range.csv", index=False)

vacancy_by_year = vacancy.iloc[13:33]
vacancy_by_year.columns = ["Year", "Unit Type","Rent Range","Vacancy Rate", "Healthy Vacancy Rate"]
vacancy_by_year.to_csv(f"{output_path}/vacancy_by_year.csv", index=False)

print("12. Vacancy Rate清洁完成")
#13. Reading and handling data of Affordable and Supportive Units Built.csv - Zoe Zhou

affordable_unit_built = pandas.read_csv("Affordable and Supportive Units Built.csv")

affordable_unit_built["Year"] = affordable_unit_built["Year"].astype(int)
affordable_unit_built["Affordable Units"] = affordable_unit_built["Affordable Units"].astype(int)
affordable_unit_built["Supportive Units"] = affordable_unit_built["Supportive Units"].astype(int)


affordable_unit_built_year = affordable_unit_built[
    [
        "Year",
        "Affordable Units",
        "Supportive Units",
    ]
]
affordable_unit_built_year.to_csv(f"{output_path}/affordable_unit_built_year.csv", index=False)
print("13. Affordable and Supportive Units Built清洁完成")


#14. Reading and handling data of Clients on Centralized Wait List.csv - Zoe Zhou
centralized_waitlist = pandas.read_csv("Clients on Centralized Wait List.csv")

centralized_waitlist["Year"] = centralized_waitlist["Year"].astype(int)
centralized_waitlist["Number"] = centralized_waitlist["Number"].str.replace(",", "").astype(int)
centralized_waitlist["Household Type"] = centralized_waitlist["Household Type"].astype(str)
centralized_waitlist["Indicator"] = centralized_waitlist["Indicator"].astype(str)

centralized_waitlist_total = centralized_waitlist.iloc[0:6]
centralized_waitlist_total.columns = ["Year", "Number", "Household Type", "Indicator"]
centralized_waitlist_total.to_csv(f"{output_path}/centralized_waitlist_total.csv", index=False)

centralized_waitlist_household_composition = centralized_waitlist.iloc[6:36]
centralized_waitlist_household_composition.columns = ["Year", "Number", "Household Type", "Indicator"]
centralized_waitlist_household_composition.to_csv(f"{output_path}/centralized_waitlist_household_composition.csv", index=False)

centralized_waitlist_unit_size = centralized_waitlist[36:72]
centralized_waitlist_unit_size.columns = ["Year", "Number", "Household Type", "Indicator"].copy()
centralized_waitlist_unit_size.to_csv(f"{output_path}/centralized_waitlist_unit_size.csv", index=False)

print("14. Clients on Centralized Wait List清洁完成")

#15. Reading and handling data of Consumer Price Index.csv - Zoe Zhou

cpi = pandas.read_csv("Consumer Price Index.csv")

cpi.columns = cpi.columns.astype(str).str.strip()

cpi["Date"] = pandas.to_datetime(cpi["Date"])
cpi["CPI All-items"] = cpi["CPI All-items"].astype(float).round(1)
cpi["CPI Food"] = pandas.to_numeric(cpi["CPI Food"], errors="coerce").round(1)
cpi["CPI Shelter"] = cpi["CPI Shelter"].astype(float).round(1)

cpi = cpi.dropna(subset=["CPI Food"])
cpi = cpi[cpi["CPI Food"] != 0]


cpi.to_csv(f"{output_path}/cpi.csv", index=False)
print("15. CPI清洁完成")

#16. Reading and handling data of Core Housing Need.csv - Zoe Zhou
housingNeed = pandas.read_csv("Core Housing Need.csv")

housingNeed["Year"] = housingNeed["Year"].astype(int)
housingNeed["Owner Percentage of Housing Need"] = housingNeed["Owner Percentage of Housing Need"].astype(float)
housingNeed["Renter Percentage of Housing Need"] = housingNeed["Renter Percentage of Housing Need"].astype(float)

housingNeed_owner_renter = housingNeed[
    [
    "Year",
    "Owner Percentage of Housing Need",
    "Renter Percentage of Housing Need"
    ]
]
housingNeed_owner_renter.to_csv(f"{output_path}/housingNeed_owner_renter.csv", index=False)

housingNeed_by_income = housingNeed[
    [
        "Year",
        "Very Low Income (20% or under of AMHI)",
        "Low Income (21% to 50% of AMHI)",
        "Moderate Income (51% to 80% of AMHI)",
        "Median Income (81% to 120% of AMHI)",
        "High Income (121% and more of AMHI)",
    ]
]
housingNeed_by_income.to_csv(f"{output_path}/housingNeed_by_income.csv", index=False)

housingNeed_by_age = housingNeed[
    [
        "Year",
        "0 to 17 years old in core housing need",
        "18 to 24 years old in core housing need",
        "25 to 54 years old in core housing need",
        "55 to 64 years old in core housing need",
        "65 years and older in core housing need"
    ]
]
housingNeed_by_age.to_csv(f"{output_path}/housingNeed_by_age.csv", index=False)

housingNeed_led_person = housingNeed[
    [
        "Year",
        "Single mother-led",
        "Women-led",
        "Indigenous",
        "Head member of racialized group",
        "Black-led",
        "New migrant-led",
        "Refugee claimant-led",
    ]
]
housingNeed_led_person.to_csv(f"{output_path}/housingNeed_led_person.csv", index=False)

housingNeed_minority = housingNeed[
    [
        "Year",
        "Head under 25",
        "Head over 65",
        "Head over 85",
        "Household with physical activity limitation",
        "Household with cognitive, mental, or substance use issue",
        "Transgender or non-binary",
    ]
]
housingNeed_minority.to_csv(f"{output_path}/housingNeed_minority.csv", index=False)

print("16. Core Housing Need清洁完成")

#17. Reading and handling data of Experiences of Homelessness.csv - Zoe Zhou

homelessness = pandas.read_csv("Experiences of Homelessness.csv")

homelessness["Year"] = homelessness["Year"].astype(int)
homelessness["Number"] = homelessness["Number"].str.replace(",", "").astype(int)
homelessness["Percentage of Total People Surveyed"] = homelessness["Percentage of Total People Surveyed"].astype(float)
homelessness["Population Group"] = homelessness["Population Group"].astype(str)
homelessness["Data Source"] = homelessness["Data Source"].astype(str)
homelessness["Type of Homelessness Experienced"] = homelessness["Type of Homelessness Experienced"].astype(str)

experience_of_Homelessness = homelessness.iloc[4:42]
experience_of_Homelessness.columns = ["Year", "Number", "Percentage of Total People Surveyed", "Population Group",
                                      "Data Source", "Type of Homelessness Experienced"]


experience_of_Homelessness.to_csv(f"{output_path}/experience_of_Homelessness.csv", index=False)

print("17. Experiences of Homelessness清洁完成")



#18. Reading and handling data of Housed from Centralized Wait List.csv - Zoe Zhou

house_centralized_waitlist = pandas.read_csv("Housed from Centralized Wait List.csv")

house_centralized_waitlist["Year"] = house_centralized_waitlist["Year"].astype(int)
house_centralized_waitlist["Number"] = house_centralized_waitlist["Number"].str.replace(",", "").astype(int)
house_centralized_waitlist["Percentage of Total Waitlist"] = house_centralized_waitlist["Percentage of Total Waitlist"].fillna(0).astype(float).round(2)
house_centralized_waitlist["Percentage of Annual Total Housed"] = house_centralized_waitlist["Percentage of Annual Total Housed"].fillna(0).astype(float).round(2)
house_centralized_waitlist["Chart Type"] = house_centralized_waitlist["Chart Type"].astype(str)
house_centralized_waitlist["Household Type"] = house_centralized_waitlist["Household Type"].astype(str)

row3 = [0,6,12,18,24,30]
house_centralized_waitlist_total = house_centralized_waitlist.iloc[row3]
house_centralized_waitlist_total.columns = ["Year", "Number", "Percentage of Total Waitlist","Percentage of Annual Total Housed","Chart Type", "Household Type"]
house_centralized_waitlist_total.to_csv(f"{output_path}/house_centralized_waitlist_total.csv", index=False)

house_centralized_waitlist_household = house_centralized_waitlist.drop(index=row3)
house_centralized_waitlist_household.columns = ["Year", "Number", "Percentage of Total Waitlist","Percentage of Annual Total Housed","Chart Type", "Household Type"]
house_centralized_waitlist_household.to_csv(f"{output_path}/house_centralized_waitlist_household.csv", index=False)

print("18. Housed from Centralized Wait List清洁完成")


#Connect to database
"""
client = MongoClient("mongodb://localhost:27017/")
db = client["test"]

print(db.list_collection_names())
"""
