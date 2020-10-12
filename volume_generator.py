import random
import numpy as np
import pdb
futures = ["HSI Futures", "HSCEI Futures", "SPX Futures", "SPX mini", "Nikkei Futures",
 "Nikkei mini", 'CAC Futures', "Valerie Futures", "Alan Futures", "Russell 2000 Futures", "SP Vangard Fund", "HK 700", "JP 9983" ]

for i in range(1000000):
    print(np.random.choice(futures),';', np.random.normal(1,0.4))


