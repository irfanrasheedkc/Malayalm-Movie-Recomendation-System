# Malayalm-Movie-Recomendation-System

### 1. Data Collection

Data is collected from IMDB website using the python program full_scraping.py and the data is saved as full_details.csv.

### 2. Model Training

We builid a similarity matrix and could recommend movies based on cosine similarity.<br>
Adjust the combined features to change the recommendation criteria.<br>
Malayalam_Movie_Recommendation.ipynb will save the similarity.npy and index_to_title_mapping.npy.

### 3. Start fastapi server

    uvicorn app:app

### 4. Open home.html

    ./home.html

#### home page
<img src="Assets\home.png" alt="home" >

#### Example based on genre-cast recommendation
<img src="Assets\example1.png" alt="home" >
<img src="Assets\example2.png" alt="home" >