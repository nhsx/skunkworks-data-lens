
This script scrapes the NHS Database data and inserts it into Elastic search.

Script starts at https://data.england.nhs.uk/ncdr/database/

NHS store data in the following structure Database -> Tables -> Columns. 

The script works by getting a list of databases then following the links it creates an object for each table, it then
collects the columns and adds them to the object, once all columns have been collected it sends it to elastic search.

An example of JSON data sent to elastic search ...

`{
        "_index" : "com205-nhs-england-databases",
        "_type" : "_doc",
        "_id" : "fiTDUXYBBq4JYfWNOEXe",
        "_score" : 1.0,
        "_source" : {
          "db_title" : "Admitted patient care, accident & emergency and outpatient data",
          "db_url_path" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/",
          "source" : "NHS England NCDR Reference Library",
          "source_url" : "https://data.england.nhs.uk/ncdr/database/",
          "ingest.timestamp" : "2020-12-11T12:25:12.437",
          "db_description" : "The SUS+ data. This includes data for admitted patient care, accident & emergency and outpatients.",
          "table_name" : "tbl_Data_SEM_AEA",
          "table_url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/table/9924/",
          "title" : "Admitted patient care, accident & emergency and outpatient data / tbl_Data_SEM_AEA",
          "table_description" : "The A&E data, taken from SUS SEM from 2008/09 until 2014/15 and from SUS+ for 2015/16 onwards.",
          "columns" : [
            {
              "name" : "AEA_Arrival_Mode",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176221/"
            },
            {
              "name" : "AEA_Assessment_Wait_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176229/"
            },
            {
              "name" : "AEA_Attendance_Category",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176233/"
            },
            {
              "name" : "AEA_Attendance_Conclusion_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176262/"
            },
            {
              "name" : "AEA_Attendance_Conclusion_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176268/"
            },
            {
              "name" : "AEA_Attendance_Disposal",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176249/"
            },
            {
              "name" : "AEA_Attendance_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176256/"
            },
            {
              "name" : "AEA_Conclusion_Wait_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176275/"
            },
            {
              "name" : "AEA_DSCRO_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/180559/"
            },
            {
              "name" : "AEA_Department_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176277/"
            },
            {
              "name" : "AEA_Departure_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176293/"
            },
            {
              "name" : "AEA_Departure_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176300/"
            },
            {
              "name" : "AEA_Diagnosis_01",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181089/"
            },
            {
              "name" : "AEA_Diagnosis_02",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181096/"
            },
            {
              "name" : "AEA_Diagnosis_03",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181103/"
            },
            {
              "name" : "AEA_Diagnosis_04",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181110/"
            },
            {
              "name" : "AEA_Diagnosis_05",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181117/"
            },
            {
              "name" : "AEA_Diagnosis_06",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181124/"
            },
            {
              "name" : "AEA_Diagnosis_07",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181131/"
            },
            {
              "name" : "AEA_Diagnosis_08",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181138/"
            },
            {
              "name" : "AEA_Diagnosis_09",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181145/"
            },
            {
              "name" : "AEA_Diagnosis_10",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181152/"
            },
            {
              "name" : "AEA_Diagnosis_11",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181159/"
            },
            {
              "name" : "AEA_Diagnosis_12",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181166/"
            },
            {
              "name" : "AEA_Diagnosis_13",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181173/"
            },
            {
              "name" : "AEA_Diagnosis_14",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181180/"
            },
            {
              "name" : "AEA_Diagnosis_15",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181187/"
            },
            {
              "name" : "AEA_Diagnosis_16",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181194/"
            },
            {
              "name" : "AEA_Diagnosis_17",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181201/"
            },
            {
              "name" : "AEA_Diagnosis_18",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181208/"
            },
            {
              "name" : "AEA_Diagnosis_19",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181215/"
            },
            {
              "name" : "AEA_Diagnosis_20",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181222/"
            },
            {
              "name" : "AEA_Diagnosis_21",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181229/"
            },
            {
              "name" : "AEA_Diagnosis_22",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181236/"
            },
            {
              "name" : "AEA_Diagnosis_23",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181243/"
            },
            {
              "name" : "AEA_Diagnosis_24",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181250/"
            },
            {
              "name" : "AEA_Duration",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176307/"
            },
            {
              "name" : "AEA_File_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176313/"
            },
            {
              "name" : "AEA_Ident",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176318/"
            },
            {
              "name" : "AEA_Incident_Location_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176347/"
            },
            {
              "name" : "AEA_Initial_Assessment_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176355/"
            },
            {
              "name" : "AEA_Initial_Assessment_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176362/"
            },
            {
              "name" : "AEA_Investigation_01",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176370/"
            },
            {
              "name" : "AEA_Investigation_02",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176377/"
            },
            {
              "name" : "AEA_Investigation_03",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176384/"
            },
            {
              "name" : "AEA_Investigation_04",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176391/"
            },
            {
              "name" : "AEA_Investigation_05",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176398/"
            },
            {
              "name" : "AEA_Investigation_06",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176405/"
            },
            {
              "name" : "AEA_Investigation_07",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176412/"
            },
            {
              "name" : "AEA_Investigation_08",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176419/"
            },
            {
              "name" : "AEA_Investigation_09",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176426/"
            },
            {
              "name" : "AEA_Investigation_10",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176433/"
            },
            {
              "name" : "AEA_Investigation_11",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176440/"
            },
            {
              "name" : "AEA_Investigation_12",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176447/"
            },
            {
              "name" : "AEA_Investigation_13",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176454/"
            },
            {
              "name" : "AEA_Investigation_14",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176461/"
            },
            {
              "name" : "AEA_Investigation_15",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176468/"
            },
            {
              "name" : "AEA_Investigation_16",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176475/"
            },
            {
              "name" : "AEA_Investigation_17",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176482/"
            },
            {
              "name" : "AEA_Investigation_18",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176489/"
            },
            {
              "name" : "AEA_Investigation_19",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176496/"
            },
            {
              "name" : "AEA_Investigation_20",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176503/"
            },
            {
              "name" : "AEA_Investigation_21",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176510/"
            },
            {
              "name" : "AEA_Investigation_22",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176517/"
            },
            {
              "name" : "AEA_Investigation_23",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176524/"
            },
            {
              "name" : "AEA_Investigation_24",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176531/"
            },
            {
              "name" : "AEA_Load_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176542/"
            },
            {
              "name" : "AEA_PCD_Indicator",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188834/"
            },
            {
              "name" : "AEA_Patient_Group",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176562/"
            },
            {
              "name" : "AEA_Raw_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176570/"
            },
            {
              "name" : "AEA_Referral_Source",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176590/"
            },
            {
              "name" : "AEA_Staff_Member_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176607/"
            },
            {
              "name" : "AEA_Time_Seen_For_Treatment",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176792/"
            },
            {
              "name" : "AEA_Treatment_01",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176616/"
            },
            {
              "name" : "AEA_Treatment_02",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176623/"
            },
            {
              "name" : "AEA_Treatment_03",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176630/"
            },
            {
              "name" : "AEA_Treatment_04",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176637/"
            },
            {
              "name" : "AEA_Treatment_05",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176644/"
            },
            {
              "name" : "AEA_Treatment_06",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176651/"
            },
            {
              "name" : "AEA_Treatment_07",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176658/"
            },
            {
              "name" : "AEA_Treatment_08",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176665/"
            },
            {
              "name" : "AEA_Treatment_09",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176672/"
            },
            {
              "name" : "AEA_Treatment_10",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176679/"
            },
            {
              "name" : "AEA_Treatment_11",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176686/"
            },
            {
              "name" : "AEA_Treatment_12",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176693/"
            },
            {
              "name" : "AEA_Treatment_13",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176700/"
            },
            {
              "name" : "AEA_Treatment_14",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176707/"
            },
            {
              "name" : "AEA_Treatment_15",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176714/"
            },
            {
              "name" : "AEA_Treatment_16",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176721/"
            },
            {
              "name" : "AEA_Treatment_17",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176728/"
            },
            {
              "name" : "AEA_Treatment_18",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176735/"
            },
            {
              "name" : "AEA_Treatment_19",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176742/"
            },
            {
              "name" : "AEA_Treatment_20",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176749/"
            },
            {
              "name" : "AEA_Treatment_21",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176756/"
            },
            {
              "name" : "AEA_Treatment_22",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176763/"
            },
            {
              "name" : "AEA_Treatment_23",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176770/"
            },
            {
              "name" : "AEA_Treatment_24",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176777/"
            },
            {
              "name" : "AEA_Treatment_Wait",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176796/"
            },
            {
              "name" : "Address_Format_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177054/"
            },
            {
              "name" : "Age_Range_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177401/"
            },
            {
              "name" : "Age_at_CDS_Activity_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177181/"
            },
            {
              "name" : "Age_at_End_of_Episode",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177248/"
            },
            {
              "name" : "Age_at_Start_of_Episode",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177307/"
            },
            {
              "name" : "Agreement_Line_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187232/"
            },
            {
              "name" : "Ambulance_Incident_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177473/"
            },
            {
              "name" : "Applicable_Date_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178956/"
            },
            {
              "name" : "Area_Code_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189360/"
            },
            {
              "name" : "Area_code_from_Provider_Postcode_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189347/"
            },
            {
              "name" : "Arrival_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177781/"
            },
            {
              "name" : "Arrival_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177793/"
            },
            {
              "name" : "Bulk_Replacement_CDS_Group",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178964/"
            },
            {
              "name" : "CDS_Activity_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176835/"
            },
            {
              "name" : "CDS_Group",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178983/"
            },
            {
              "name" : "CDS_Interchange_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178993/"
            },
            {
              "name" : "CDS_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179032/"
            },
            {
              "name" : "Carer_Support_Indicator",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178909/"
            },
            {
              "name" : "Census_Area_2001_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176215/"
            },
            {
              "name" : "Census_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178972/"
            },
            {
              "name" : "Census_ED_1991",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182929/"
            },
            {
              "name" : "Commissioner_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187870/"
            },
            {
              "name" : "Commissioner_Code_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188477/"
            },
            {
              "name" : "Commissioner_Reference_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179624/"
            },
            {
              "name" : "Commissioning_Serial_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179695/"
            },
            {
              "name" : "Confidentiality_Category_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179789/"
            },
            {
              "name" : "Country",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/180024/"
            },
            {
              "name" : "County_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/180045/"
            },
            {
              "name" : "Der_AEA_Duration",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176310/"
            },
            {
              "name" : "Der_Activity_Month",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176915/"
            },
            {
              "name" : "Der_Age_At_CDS_Activity_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/177190/"
            },
            {
              "name" : "Der_Commissioner_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187893/"
            },
            {
              "name" : "Der_DataSource",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/180582/"
            },
            {
              "name" : "Der_Diagnosis_All",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181263/"
            },
            {
              "name" : "Der_Financial_Year",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/183466/"
            },
            {
              "name" : "Der_Investigation_All",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176539/"
            },
            {
              "name" : "Der_Number_Diagnosis",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187383/"
            },
            {
              "name" : "Der_Number_Investigation",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187408/"
            },
            {
              "name" : "Der_Number_Treatment",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187617/"
            },
            {
              "name" : "Der_PostCode_Sector",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189404/"
            },
            {
              "name" : "Der_Postcode_CCG_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179444/"
            },
            {
              "name" : "Der_Postcode_Constituency_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179799/"
            },
            {
              "name" : "Der_Postcode_Dist_Unitary_Auth",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/195377/"
            },
            {
              "name" : "Der_Postcode_Electoral_Ward",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182740/"
            },
            {
              "name" : "Der_Postcode_Grid_Easting",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184188/"
            },
            {
              "name" : "Der_Postcode_Grid_Northing",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184205/"
            },
            {
              "name" : "Der_Postcode_LSOA_2011_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/186059/"
            },
            {
              "name" : "Der_Postcode_LSOA_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/186076/"
            },
            {
              "name" : "Der_Postcode_Local_Auth",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185844/"
            },
            {
              "name" : "Der_Postcode_MSOA_2011_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/186423/"
            },
            {
              "name" : "Der_Postcode_MSOA_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/186437/"
            },
            {
              "name" : "Der_Postcode_PCT_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189608/"
            },
            {
              "name" : "Der_Practice_Patient_Distance_Miles",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182455/"
            },
            {
              "name" : "Der_Practice_Provider_Distance_Miles",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182435/"
            },
            {
              "name" : "Der_Provider_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187991/"
            },
            {
              "name" : "Der_Provider_Patient_Distance_Miles",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182471/"
            },
            {
              "name" : "Der_Provider_Site_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/192693/"
            },
            {
              "name" : "Der_Pseudo_NHS_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/190640/"
            },
            {
              "name" : "Der_Pseudo_Patient_Pathway_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188904/"
            },
            {
              "name" : "Der_Treatment_All",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/176785/"
            },
            {
              "name" : "Diagnosis_Scheme_In_Use",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/181782/"
            },
            {
              "name" : "Dominant_Grouping_Variable_Procedure",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189842/"
            },
            {
              "name" : "ED_District_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182724/"
            },
            {
              "name" : "Electoral_Area_1998",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182712/"
            },
            {
              "name" : "Electoral_Ward_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182761/"
            },
            {
              "name" : "Electoral_Ward_from_postcode",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/182773/"
            },
            {
              "name" : "Ethnic_Category",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/183008/"
            },
            {
              "name" : "Extract_Date_Time",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178977/"
            },
            {
              "name" : "FCE_HRG",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184474/"
            },
            {
              "name" : "Finished_Indicator",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/183832/"
            },
            {
              "name" : "GOR_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184061/"
            },
            {
              "name" : "GP_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/183930/"
            },
            {
              "name" : "GP_Practice_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184115/"
            },
            {
              "name" : "GP_Practice_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184138/"
            },
            {
              "name" : "Generated_Record_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/183968/"
            },
            {
              "name" : "HRG_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184493/"
            },
            {
              "name" : "HRG_Version_No",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185005/"
            },
            {
              "name" : "Investigation_Scheme_In_Use",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185598/"
            },
            {
              "name" : "Lead_Care_Activity_Indicator",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185717/"
            },
            {
              "name" : "Local_Patient_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185872/"
            },
            {
              "name" : "Local_Unitary_Authority",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/195398/"
            },
            {
              "name" : "Month_of_Birth",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/186847/"
            },
            {
              "name" : "NHS_Number_Trace_Status",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187209/"
            },
            {
              "name" : "Name_Format_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/186890/"
            },
            {
              "name" : "OSV_Class_at_CDS_Activity_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188771/"
            },
            {
              "name" : "Old_SHA_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/193461/"
            },
            {
              "name" : "Org_Code_Ambulance_Trust",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188405/"
            },
            {
              "name" : "Org_Code_Local_Patient_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188425/"
            },
            {
              "name" : "Org_Code_Patient_Pathway_ID_Issuer",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188458/"
            },
            {
              "name" : "Org_Code_Residence_Responsibility",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179464/"
            },
            {
              "name" : "Org_Code_Sender_of_Transaction",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188395/"
            },
            {
              "name" : "Org_Code_Type_GP",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188484/"
            },
            {
              "name" : "Org_Code_Type_Local_Patient_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188488/"
            },
            {
              "name" : "Org_Code_Type_PCT_of_Residence",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188517/"
            },
            {
              "name" : "Org_Code_Type_of_Sender",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188512/"
            },
            {
              "name" : "PBR_Generated_Core_HRG_Version_for_Information",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185009/"
            },
            {
              "name" : "PBR_Generated_Core_HRG_for_Information",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/184580/"
            },
            {
              "name" : "PCT_Derived_from_GP_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189640/"
            },
            {
              "name" : "PCT_Derived_from_SUS_GP_Practice",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189648/"
            },
            {
              "name" : "PCT_Type_Derived_from_GP_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189654/"
            },
            {
              "name" : "PCT_Type_from_Postcode_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188695/"
            },
            {
              "name" : "PCT_from_Postcode_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189619/"
            },
            {
              "name" : "PCT_of_Residence",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189630/"
            },
            {
              "name" : "Patient_Pathway_ID",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188911/"
            },
            {
              "name" : "Person_Title",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/189200/"
            },
            {
              "name" : "Procedure_Scheme_In_Use",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/190196/"
            },
            {
              "name" : "Protocol_Identifier",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179008/"
            },
            {
              "name" : "Provider_Code",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188325/"
            },
            {
              "name" : "Provider_Code_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188581/"
            },
            {
              "name" : "Provider_Reference_Number",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/190604/"
            },
            {
              "name" : "RTT_Length_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/191295/"
            },
            {
              "name" : "RTT_Period_End_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/191276/"
            },
            {
              "name" : "RTT_Period_Start_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/191339/"
            },
            {
              "name" : "RTT_Period_Status",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/191313/"
            },
            {
              "name" : "Reason_For_Access",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/190859/"
            },
            {
              "name" : "Report_period_End_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179021/"
            },
            {
              "name" : "Report_period_Start_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179026/"
            },
            {
              "name" : "SHA_Type_from_GP_Practice_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188588/"
            },
            {
              "name" : "SHA_Type_from_Postcode_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/188592/"
            },
            {
              "name" : "SHA_from_GP_Practice_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/193468/"
            },
            {
              "name" : "SHA_from_Postcode_SUS",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/193472/"
            },
            {
              "name" : "Service_Agreement_Change_Date",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/187227/"
            },
            {
              "name" : "Sex",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/192540/"
            },
            {
              "name" : "Site_Code_of_Treatment",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/192739/"
            },
            {
              "name" : "Spell_Core_HRG_Version_No",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/185011/"
            },
            {
              "name" : "Test_Indicator",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/178998/"
            },
            {
              "name" : "Treatment_Scheme_In_Use",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/194791/"
            },
            {
              "name" : "Unique_Booking_Reference_Number_Converted",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/195009/"
            },
            {
              "name" : "Unique_CDS_Identifier",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179037/"
            },
            {
              "name" : "Update_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179042/"
            },
            {
              "name" : "Wait_Time_Measurement_Type",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/195433/"
            },
            {
              "name" : "Withheld_Identity_Reason",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/195817/"
            },
            {
              "name" : "XML_Version",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/179003/"
            },
            {
              "name" : "Year_of_Birth",
              "url" : "https://data.england.nhs.uk/ncdr/database/NHSE_SUSPlus_Live/column/195908/"
            }
          ]
        }
      }`


