import os
xvg=os.listdir('/home/new/Documents/Nigel/new/MD_results/rmsf_files/')
for i in xvg:
    if ".xvg" in i:
        xvg_name=i[:-4]
        os.system("cat "+i+" | tail -n+18 | awk '{print $2}' > "+xvg_name+".csv")
    else:
        pass
