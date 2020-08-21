import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')

htmltemp = """
	<div style="background-color:#00a4ba; border-radius:10px; width:100%; height:auto;">
	<h1 style="color:white; padding:10px;"><center> Data Analysing Tool </center></h1>
	</div>
	"""
st.markdown(htmltemp, unsafe_allow_html=True)


def main():
	def select_file(folder_path='./CSVfiles'):

		filenames = os.listdir(folder_path)
		selected_filename = st.selectbox("Select A CSV File", filenames)
		return os.path.join(folder_path, selected_filename)

	filename = select_file()
	st.success("Selected File is : {}".format(filename))

	# Reading data from CSV file.
	df = pd.read_csv(filename, encoding='iso8859_16', low_memory=False)

	# Displaying DataFrame
	if st.checkbox("Preview Dataframe"):
		html_temp2 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
			<h4 style="color:white;  padding:10px;"><center> Data Preview </center></h4>
			</div> """
		st.markdown(html_temp2, unsafe_allow_html=True)
		st.dataframe(df)

	# Display Column Names
	if st.checkbox("Column Names"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
			<h4 style="color:white;  padding:10px;"><center>Preview Of Column names</center></h4>
			</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		st.write(df.columns)

	# Display Shape Of DataFrame
	if st.checkbox("Shape of Dataset"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
			<h4 style="color:white;  padding:10px;"><center> Shape of DataFrame</center></h4>
			</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		data_dim = st.radio("Show Dimension By ", ("Rows", "Columns"))
		if data_dim == 'Rows':
			st.text("Number of Rows")
			st.write(df.shape[0])
		elif data_dim == 'Columns':
			st.text("Number of Columns")
			st.write(df.shape[1])
		else:
			st.write(df.shape)

	# Select Columns
	if st.checkbox("Select Multiple Columns To Preview"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
					<h4 style="color:white;  padding:10px;"><center> Select Multiple Columns To Preview  Of Data</center></h4>
					</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		all_columns = df.columns.tolist()
		selected_columns = st.multiselect("Select", all_columns)
		new_df = df[selected_columns]
		st.dataframe(new_df)

	# Displaying Datatypes
	if st.checkbox("Data Types"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
							<h4 style="color:white;  padding:10px;"><center> Displaying Datatyes Of All Columns</center></h4>
							</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		st.write(df.dtypes)

	# Summary Of DATAFRAME
	if st.checkbox("Summary"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
									<h4 style="color:white;  padding:10px;"><center> Summary Of A DataFrame</center></h4>
									</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		st.write(df.describe().T)

	# Plots and Visualizations
	html_temp3 = """ <div style="background-color:#f54281; width:100%; height:auto;">
										<h4 style="color:white;  padding:10px;"><center> DATA VISULIZATION </center></h4>
										</div> """
	st.markdown(html_temp3, unsafe_allow_html=True)
	# Correlation
	# Seaborn Plot
	if st.checkbox("Correlation Matrix"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
									<h4 style="color:white;  padding:10px;"><center> CORRELATION MATRIX </center></h4>
									</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		st.write(sns.heatmap(df.corr(), annot=True))
		st.pyplot()

	# Pie Chart
	if st.checkbox("Pie Plot"):
		all_columns_names = df.columns.tolist()
		if st.button("Click Here To Generate Pie Plot"):
			html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
										<h4 style="color:white;  padding:10px;"><center> PIE CHART </center></h4>
										</div> """
			st.markdown(html_temp3, unsafe_allow_html=True)
			st.success("Generating A Pie Plot")
			st.write(df.iloc[:, -1].value_counts().plot.pie(autopct="%1.1f%%"))
			st.pyplot()

	# Count Plot
	if st.checkbox("Bar Count Plot"):
		html_temp3 = """ <div style="background-color:#2e2e6b; width:100%; height:auto;">
									<h4 style="color:white;  padding:10px;"><center> Bar Count Plot </center></h4>
									</div> """
		st.markdown(html_temp3, unsafe_allow_html=True)
		st.text("Value Counts By Target")
		all_columns_names = df.columns.tolist()
		primary_col = st.selectbox("Primary Columm to GroupBy", all_columns_names)
		selected_columns_names = st.multiselect("Select Columns", all_columns_names)
		if st.button("Plot"):
			st.text("Generate Plot")
			if selected_columns_names:
				vc_plot = df.groupby(primary_col)[selected_columns_names].count()
			else:
				vc_plot = df.iloc[:, -1].value_counts()
			st.write(vc_plot.plot(kind="bar"))
			st.pyplot()

	# Customizable Plot
	html_temp3 = """ <div style="background-color:#00c943; width:100%; height:auto;">
								<h4 style="color:white;  padding:10px;"><center> SELECT YOUR OWN PLOT </center></h4>
								</div> """
	st.markdown(html_temp3, unsafe_allow_html=True)
	all_columns_names = df.columns.tolist()
	type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
	selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

	if st.button("Generate Plot"):
		st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

		# Plot By Streamlit
		if type_of_plot == 'area':
			cust_data = df[selected_columns_names]
			st.area_chart(cust_data)

		elif type_of_plot == 'bar':
			cust_data = df[selected_columns_names]
			st.bar_chart(cust_data)

		elif type_of_plot == 'line':
			cust_data = df[selected_columns_names]
			st.line_chart(cust_data)

		# Custom Plot
		elif type_of_plot:
			cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
			st.write(cust_plot)
			st.pyplot()

	if st.button("Thanks"):
		st.balloons()

	st.sidebar.header("About App")
	st.sidebar.info("Simple EDA Tool")

	st.sidebar.header("About")
	st.sidebar.text("Built with Streamlit")
	st.sidebar.warning("Maintained by Murali Krishna Mopidevi")


if __name__ == '__main__':
	main()
