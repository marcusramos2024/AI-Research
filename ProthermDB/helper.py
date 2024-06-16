import re
import csv
import pandas as pd
import os
import torch
import pathlib
import torch
from esm import FastaBatchedDataset, pretrained

def extract_uniprot_ids(csv_file_path):
    data = pd.read_csv(csv_file_path)
    
    uniprot_ids = data['UNIPROT_ID'].dropna()

    uniprot_ids_string = ' '.join(uniprot_ids)

    return uniprot_ids_string

def merge_excel_files(directory_path, output_file):
    all_data = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(directory_path, filename)
            data = pd.read_excel(file_path)
            all_data.append(data)

    merged_data = pd.concat(all_data, ignore_index=True)

    merged_data.to_excel(output_file, index=False)

# Creates a copy of @file removing all rows without @column value @value
def filter_column(file, column, value):
    df = pd.read_excel(file)

    filtered_df = df[df[column] == value]

    output_file = f'output-2.xlsx'
    filtered_df.to_excel(output_file, index=False)

# Updates "Sequence" column for given file
def insert_sequences(file):
    ids_file = 'IDs.xlsx'
    ids_df = pd.read_excel(ids_file)

    sequences = {}

    for index, row in ids_df.iterrows():
        sequences[row["UNIPROT_ID"]] = row["SEQUENCE"]


    df = pd.read_excel(file)
    for index, row in df.iterrows():
        df.at[index, 'Sequence'] = sequences.get(row["UNIPROT_ID"], "N\A")

    df.to_excel(file, index=False)

# Generates a fasta file from excell file
def generate_fasta(file):
    ids_df = pd.read_excel(file)

    fasta_file = file.replace("xlsx", "fasta")
    with open(fasta_file, "w") as file:    
            for row in ids_df.iterrows():
                string = ">" + row[1]["UNIPROT_ID"] + "\n" + row[1]["Sequence"] + "\n"
                file.write(string)

# Generates directory of embeddings from fasta
def extract_embeddings(model_name, fasta_file, tokens_per_batch=4096, seq_length=1022):
    repr_layers = []
    
    for i in range(1,34):
        repr_layers.append(i)

    
    model, alphabet = pretrained.load_model_and_alphabet(model_name)
    model.eval()

    if torch.cuda.is_available():
        model = model.cuda()
        
    dataset = FastaBatchedDataset.from_file(fasta_file)
    batches = dataset.get_batch_indices(tokens_per_batch, extra_toks_per_seq=1)

    data_loader = torch.utils.data.DataLoader(
        dataset, 
        collate_fn=alphabet.get_batch_converter(seq_length), 
        batch_sampler=batches
    )

    output_dir = pathlib.Path(model_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with torch.no_grad():
        for batch_idx, (labels, strs, toks) in enumerate(data_loader):

            print(f'Processing batch {batch_idx + 1} of {len(batches)}')

            if torch.cuda.is_available():
                toks = toks.to(device="cuda", non_blocking=True)

            out = model(toks, repr_layers=repr_layers, return_contacts=False)

            logits = out["logits"].to(device="cpu")
            representations = {layer: t.to(device="cpu") for layer, t in out["representations"].items()}
            
            for i, label in enumerate(labels):
                entry_id = label.split()[0]
                
                filename = output_dir / f"{entry_id}.pt"
                truncate_len = min(seq_length, len(strs[i]))

                result = {"entry_id": entry_id}
                result["mean_representations"] = {
                        layer: t[i, 1 : truncate_len + 1].mean(0).clone()
                        for layer, t in representations.items()
                    }

                torch.save(result, filename)

def read_embedding(directory, uniprotID, layer):
    embedding = torch.load(f'{directory}/{uniprotID}.pt')
    return embedding['mean_representations'][layer].numpy()

