
global input "/Users/a_king/Documents/D3/Sac_Budget/input data/"
global output "/Users/a_king/Documents/D3/Sac_Budget/data/prep_data/temp/"
global temp "/Users/a_king/Documents/temp/"


import excel using "$input/Sac_Budget_1415.xlsx", clear firstr
renvars, lower
save "$temp/t1.dta", replace

use "$temp/t1.dta", clear
keep if inlist(time, "2015", "2016")
rename time year
destring budgetamount, replace

replace departmentdescription="Current Planning" if departmentdescription=="Planning" & division=="Planning Division"
replace division="Maintenance Services Division" if division=="Urban Forestry Division" & departmentdescription=="Urban Forestry"
replace division="Public Improvement Finance Division" if division=="Accounting Division" & departmentdescription=="Public Improvement Finance"
replace departmentdescription="Employee Services - HR" if departmentdescription=="Employment & Compensation"

keep if exprev=="Expenses"

collapse(sum) amount=budgetamount, by(groupsection department division departmentdescription year) fast
reshape wide amount, i(groupsection department division departmentdescription) j(year) string
format amount* %15.0fc
gen change=(amount2016/amount2015)-1
export excel using "$output/sac_budget_t1.xlsx", replace firstr(var)
