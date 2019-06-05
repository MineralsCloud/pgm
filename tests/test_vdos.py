from pgm.vdos import *
import pandas as pd
if __name__ == "__main__":
    df = pd.read_csv('data/vdos/science2005/1100.dos', names= ['f', 'i'])
    f, i = normalize(df['f']*8.0656, df['i'])
    s = vdos_entropy(f, i, 1100, N=2)
    print(ry_to_kb(s))