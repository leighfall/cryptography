# Cryptography
A repo for all programs written in my Cryptography class.

## Hash Attack
The program executes with no inputs and conducts a Collision Attack and a Pre-Image Attack using bit sizes of 8, 10, 12, 14, 16, 18, 20, and 22 and runs 50 samples on each of those sizes (for a total of 800 runs).

It gathers results and saves them to an Excel spreadsheet where analysis can be performed.

Roadmap: Build graphs in matplotlib instead of Excel.

## RSA

A program for executing encryption and decryption using RSA values. 

The program will generate p and q values, phi and n values based off of those p and q values, check that their GCD is 1, and then generate a secret d exponent. Values after that were used for passoff of the project; Thus values generated during the passoff were hardcoded in.
