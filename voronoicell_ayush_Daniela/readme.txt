For details and example on the applicability of AVO, see: Chem. Eur. J. 2020, 26, 2080–2093.

1. Run a densf calculations (.run file) for each fragment to generate the values of FMO in a user-defined grid
  a. Note that the sample input file is for ADF2017
  b. Check ADF manual for information on the input keywords
  c. Use the same grid details for both fragment calculations and make sure that the entire system,
     that is, fragments 1 and 2 as well as the molecular orbitals, fits inside the grid.

2.	Use the python script (.py) to run the AVO code:
  a. Make sure that python3, plams and numpy modules are loaded in your machine
  b. For those that are not familiar with python, there is a version of the AVO code with prompt added
    i.	To run the AVO code just use the command in your terminal: python densitydevide2.py
    ii. You will be prompted to provide the following information:
      - The KFFile of fragment 1, that is, the output file from the densf calculation for fragment 1
      - The KFFile of fragment 2, that is, the output file from the densf calculation for fragment 2
      - The .xyz file with the coordinates of the complex
      - The symmetry of the fragment orbitals you want to calculate the AVO
      - The number of the orbitals of fragment 1 and 2
  c. Otherwise, you will have to input the above information inside AVO code (in densitydevide.py) by yourself before running it
  d. Once the calculation is finished, the output will be printed in your terminal
