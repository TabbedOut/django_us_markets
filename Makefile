data: data/geonames/us_zip_codes.csv data/department_of_labor/owcp_fee_schedule_by_zip_2011.csv data/us_census_bureau/zip_codes_2013/zip_codes_2013

data/geonames/US.zip:
	curl http://download.geonames.org/export/zip/US.zip > data/geonames/US.zip

data/geonames/us_zip_codes.csv: data/geonames/US.zip
	unzip data/geonames/US.zip US.txt
	mv US.txt data/geonames/us_zip_codes.txt
	in2csv -f csv data/geonames/us_zip_codes.txt > data/geonames/us_zip_codes.csv

data/department_of_labor/owcp_fee_schedule_by_zip_2011.xls:
	curl http://www.dol.gov/owcp/regs/feeschedule/fee/fee11/fs11_gpci_by_msa-ZIP.xls \
		> data/department_of_labor/owcp_fee_schedule_by_zip_2011.xls

data/department_of_labor/owcp_fee_schedule_by_zip_2011.csv: data/department_of_labor/owcp_fee_schedule_by_zip_2011.xls
	in2csv data/department_of_labor/owcp_fee_schedule_by_zip_2011.xls \
		| tail -n+11 \
		> data/department_of_labor/owcp_fee_schedule_by_zip_2011.csv

data/us_census_bureau/zip_codes_2013.zip:
	curl http://www2.census.gov/geo/tiger/TIGER2013/ZCTA5/tl_2013_us_zcta510.zip \
		> data/us_census_bureau/zip_codes_2013.zip

data/us_census_bureau/zip_codes_2013/zip_codes_2013:
	unzip data/us_census_bureau/zip_codes_2013.zip -d data/us_census_bureau/zip_codes_2013
