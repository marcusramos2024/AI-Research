*model.py*:
- Linear Regression model trained on embeddings generated from Facebook's ESM2 (https://github.com/facebookresearch/esm) looking to predict the corresponding melting temperature from ProthermDB (https://web.iitm.ac.in/bioinfo2/prothermdb/). 33 models are trained for each of the 33 layers of ESM2. 
- Steps:
	1. Extracted sequences from UNIPROT ID's from ProthermDB
	2. Cleaned data; removing duplicates and standardizing dataset to contain only the sequence and corresponding melting temperature
	3. Run sequences through ESM2 and output into "Embeddings" directory
	4. For each of ESM2 33 layers, train a linear regression model using the corresponding embedding layer to try and predict the melting temperature
	5. Plot results from each of the 33 layers; using Root mean squared error as the y axis and the layer as the x axis

*helper.py*:
- Contains all of the helper methods used in this research

*Results.png*: 
- Output from *model.py*
