# Automated Pipeline for MHC Class II Peptide Binding Predictions
## 1. Overview
This pipeline automates the analysis of **MHC Class II peptide binding predictions** using  
a **VCF file** as input. The pipeline needs to run on **Linux systems**. The pipeline performs the following tasks:

- **Variant annotation** using ANNOVAR  
- **Peptide extraction** from mutated proteins  
- **MHC binding predictions** using NetMHCIIpan & MixMHC2pred  
- **Integration with gene expression data**  
- **Clustering peptides** to identify potential target sequences  

---

## 2. Workflow

### Step 1: Start the Main Script
Run the following command to start the pipeline:

```bash
python3 script/main_script.py
```
The script will **prompt for the required inputs** step by step.

### **Step 2: Input VCF File**
- The script will ask for the **VCF file path**.
- This file contains genetic variants used for analysis.

### **Step 3: Run ANNOVAR**
- The pipeline automatically searches for ANNOVAR in the project directory.
- If not found, the user is prompted to enter the path.

### **Step 4: Generate Mutated Peptides**
- Peptides (12-25 amino acids) are extracted from mutated proteins.
- Frameshift mutations are handled using a **sampling strategy** to reduce redundancy.

### **Step 5: Run MHC Binding Predictions**
- **NetMHCIIpan** and **MixMHC2pred** are executed automatically.
- The pipeline dynamically selects **HLA alleles** from `alleleList_net.txt` and `alleleList_mix.txt`.

### **Step 6: Post-processing**
- **Filter peptides** based on binding affinity (`Rank ≤ 5`).
- **Map peptides to genes** based on their transcript association.
- **Integrate gene expression data** to filter out low-expression peptides.
- **Cluster similar peptides** to identify representative sequences.

---

## **3. Folder Structure**
The project follows this directory structure, make sure yours is exactly the same:

**(Important: Rename the parent folder to 'script' after cloning)**

```
project_root/
│── annovar/                  # ANNOVAR software (user provided)
│── annovar_outputs/          # ANNOVAR results
│── netMHCIIpan_outputs/      # NetMHCIIpan results
│── netMHCIIpan-4.3/          # NetMHCIIpan software (user provided)
│── MixMHC2pred_outputs/      # MixMHC2pred results
│── MixMHC2pred-2.0.2.2/      # MixMHC2pred software (user provided)
│── gene_expression_data.csv  # Gene expression files, can be at anywhere
│── script/                   # Python scripts (rename needed here)
│   ├── main_script.py        # Main pipeline script
│   ├── annovar_related/      # ANNOVAR related scripts
│   ├── netMHCIIpan_related/  # NetMHCIIpan related scripts
│   ├── MixMHC2pred_related/  # MixMHC2pred related scripts
│   │── alleleList_net.txt    # HLA alleles for NetMHCIIpan
│   │── alleleList_mix.txt    # HLA alleles for MixMHC2pred
│── bs6206.vcf/               # vcf file, can be at any place
```

---

## **4. Expected Outputs**
Each **CSV file** (one per allele) will contain the following columns, depending on the software, there might be extra columns:

| Peptide | Gene Name | Gene Expression | Considered Target | Cluster | Rank |
|---------|----------|----------------|------------------|--------|------|
| XXXXXX  | GENE1    | 12.5           | 1                | XXXXXXYYYY | 1.2 |
| YYYYYY  | GENE1    | 15.3           | 1                | XXXXXXYYYY | 2.1 |

- **Considered Target** → `1` if TPM >= threshold, otherwise `0`
- **Cluster** → Merged peptide sequences from overlapping segments

---

## **5. Installation & Setup**
### **Step 1: Install Required Dependencies**
Ensure you have **Python 3.8+** installed, then run:
```bash
pip install numpy pandas
```
The Linux system also requires to run:
```bash
sudo apt update
sudo apt install perl tcsh
```

### **Step 2: Extract Required Software**
Download and extract `netMHCIIpan` and `MixMHC2pred` (Recommended to use the same version of the tools):
```bash
tar -xvzf netMHCIIpan-4.3e.Linux.tar.gz
tar -xvzf MixMHC2pred-2.0.2.2.tar.gz
```
If you are using **MixMHC2pred** for the first time, you may need to download the wished alleles' definition files from the page:
http://mixmhc2pred.gfellerlab.org/PWMdef. We are using **'PWMdef_Human.zip'**, what you need to do is simply download the zip and 
extract the folder under MixMHC2pred path, and rename it to **'PWMdef'**.

If you are using **netMHCIIpan** for the first time, please follow the documentation to set up the software successfully
before executing the script, details can be found at https://services.healthtech.dtu.dk/services/NetMHCIIpan-4.3/

**Make sure the software can run (manually) before using the script!!!**

### **Step 3: Set Up Execution Permissions**
Ensure the executables have proper permissions:
```bash
chmod +x netMHCIIpan-4.3/netMHCIIpan
chmod +x MixMHC2pred-2.0.2.2/MixMHC2pred_unix
```
---

## **6. Configuration & Customization**
### **Modifying Allele Lists**
- **NetMHCIIpan alleles**: Edit `alleleList_net.txt`
- **MixMHC2pred alleles**: Edit `alleleList_mix.txt`

### **Adjusting TPM Threshold**
- The script will prompt for a **TPM threshold** during execution.
- To set a **default threshold**, modify `main_script.py` accordingly.

---

## **7. Troubleshooting**
### **1. NetMHCIIpan or MixMHC2pred Not Found**
**Error:**  
```bash
NetMHCIIpan executable not found in folder: netMHCIIpan-4.3
```
**Solution:**  
Ensure you extracted the files correctly and set execution permissions.

### **2. Missing Required Input Files**
If you see:
```bash
FileNotFoundError: No file named 'mutated_peptide_sequences.pep'
```
Ensure you have run the **VCF processing steps correctly**.

### **3. Results Contain "Unknown" Gene Names**
This may occur if a peptide **does not map** to any known gene.  
**Solution:** Ensure correct **gene expression data** is provided.

---

## **8. Contact**
For issues, please contact:  
📧 **Boyu Zhang** - BOYU003@e.ntu.edu.sg  
📍 **Nanyang Technological University**  
📌 **Last Updated: 2025-02-06**
