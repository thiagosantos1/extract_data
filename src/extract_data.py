import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import fire

"""
	Install dependecies by running: pip3 install -r requirements.txt

	Running command example:
	python3 extract_data.py --path_to_excell /Users/thiago/test_stanford.xlsx --report_column_name report --path_to_data_output /Users/thiago/extracted_stanford.xlsx
"""

def extract_diagnosis(path_to_excell:str, report_column_name:str, path_to_data_output:str,
					  keywords_de_identiy = ['i have reviewed', 'i have review', 'i have signed', 'i have sign',
										'i have checked', 'i have check',  'i reviewed', 'i review', 'i signed', 'i sign',
										'i checked', 'i check', 'dr.', 'dr', 'md', 'm.d','reviewed', 'review', 'signed', 'sign',]):
	"""
		This program takes an excell sheet and extract the diagnosis of a pathology report

		Required inputs:
			1) path_to_excell - Original excell with the full pathology report
			2) report_column_name - Which column has the pathology report
			3) path_to_data_output - Where to save the report
			4) keywords_de_identiy - A list of potential keywords to de identify the data ( break the diagnosis section)
	"""

	data = pd.read_excel(path_to_excell)[report_column_name]
	out_reports = []
	for i in tqdm(range(data.shape[0]),desc ="Extracting Data"):
		txt = data.iloc[i].lower()
		if "diagnosis" in txt:
			txt = re.sub(' +', ' ', txt)
			txt = re.sub('diagnosis :', 'diagnosis:', txt)
			subs = "diagnosis: " + txt.split("diagnosis:")[-1]
			
			for flag in keywords_de_identiy:
				if flag in subs:
					out_reports.append(subs.split(flag)[0])
					break

	df = pd.DataFrame(out_reports,columns =[report_column_name])

	df.to_excel(path_to_data_output) 


def run():
	fire.Fire(extract_diagnosis)

if __name__ == '__main__':
	run()