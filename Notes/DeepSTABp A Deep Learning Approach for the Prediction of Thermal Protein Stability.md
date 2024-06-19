Datasets: https://git.nfdi4plants.org/f_jung/deepstabp/-/tree/main/runs/TransformerBasedTMPrediction

## DeepSTABp Architecture:
- **Embedding Layer 1**: Type of experimental condition used in the thermal proteome profiling experiment
- **Embedding Layer 2**: Protein amino acid sequence
- **Embedding Layer 3**: organism growth temperature

- Finally, the outputs of these 3 embeddings are concatenated and used as input for the 4th layer. The output of this 4th layer is the predicted melting temp (Tm)


##### ProTstab2s: Current state of the art temp predictor
- However, DeepSTABp beats it:
	- **DeepSTABp Prediction IQR**: 4.9 C
	- **ProTstab2s Prediction IQR**: 8.0 C
