from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")


#find your right key here
table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table=simple hisotry-data'})
table_body = table.find_all('tr')

row_length = len(table_body)

List_of_USDIDR = [] #initiating a tuple

for table_rows in table_body.find_all('tr'):
    columns = table_rows.find_all('td')
    periode = columns[0].text
    fx_rate = columns[2].text.replace("IDR", "").replace(",", "").strip()
    
    List_of_USDIDR.append((periode,fx_rate))
List_of_USDIDR

#change into dataframe
df_USDIDR = pd.DataFrame(List_of_USDIDR, columns = ('Periode','USDIDR'))#, 'description'))
df_USDIDR['Periode'] = df_USDIDR['Periode'].astype('datetime64')
df_USDIDR['USDIDR'] = df_USDIDR['USDIDR'].astype('float64')
df_USDIDR.head()


#insert data wrangling here
df_USDIDR = df_USDIDR.set_index('Periode')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df_USDIDR["fx_rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df_USDIDR.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)