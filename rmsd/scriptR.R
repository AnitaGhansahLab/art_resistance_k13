rm(list = ls())
options(stringsAsFactors = FALSE)
wt = read.table('wild_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
A675V = read.table('A675V_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
C580Y = read.table('C580Y_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
M476I = read.table('M476I_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
P553L = read.table('P553L_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
P574L = read.table('P574L_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
R561H = read.table('R561H_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
A557S = read.table('A557S_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
A578S = read.table('A578S_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)
Y493H_C580Y = read.table('Y493H_C580Y_rmsf.csv', sep = '', header = FALSE, quote = "'", stringsAsFactors = FALSE, fill = TRUE)

gyrate_frame = list(Apo = wt$V1,
                    A675V = A675V$V1,
                    C580Y = C580Y$V1,
                    M476I = M476I$V1,
                    P553L = P553L$V1,
                    P574L = P574L$V1,
                    R561H = R561H$V1,
                    A557S = A557S$V1,
                    A578S = A578S$V1,
                    Y493H_C580Y = Y493H_C580Y$V1)

a_WT <- gyrate_frame$Apo
a_A675V <- gyrate_frame$A675V
a_C580Y <- gyrate_frame$C580Y
a_M476I <- gyrate_frame$M476I
a_P553L <- gyrate_frame$P553L
a_P574L <- gyrate_frame$P574L
a_R561H <- gyrate_frame$R561H
a_A557S <- gyrate_frame$A557S
a_A578S <- gyrate_frame$A578S
a_Y493H_C580Y <- gyrate_frame$Y493H_C580Y

#wild = mean(a_WT)
#A675V = mean(a_A675V)
#C580Y = mean(a_C580Y)
#M476I = mean(a_M476I)
#P553L = mean(a_P553L)
#P574L = mean(a_P574L)
#R561H = mean(a_R561H)

#a=rbind(Apo, A675V, C580Y, M476I, P553L, P574L, R561H)
#write.csv(a, file="./rmsd_mean_all.csv")

gyrate_data_1 = cbind(a_WT, a_A675V, a_C580Y, a_M476I, a_P553L, a_P574L, a_R561H, a_A557S, a_A578S, a_Y493H_C580Y)


write.csv(gyrate_data_1, file = "./rmsf_line.csv")

library("tidyverse")
library("ggplot2")
library("ggpubr")
library("data.table")
#library("xlsx")

gyrate_wt <- rep("Apo", length(wt$V1))
gyrate_A675V <- rep("A675V", length(A675V$V1))
gyrate_C580Y <- rep("C580Y", length(C580Y$V1))
gyrate_M476I <- rep("M476I", length(M476I$V1))
gyrate_P553L <- rep("P553L", length(P553L$V1))
gyrate_P574L <- rep("P574L", length(P574L$V1))
gyrate_R561H <- rep("R561H", length(R561H$V1))
gyrate_A557S <- rep("A557S", length(A557S$V1)) 
gyrate_A578S <- rep("A578S", length(A578S$V1))
gyrate_Y493H_C580Y <- rep("Y493H_C580Y", length(Y493H_C580Y$V1))

a_WT = cbind(rmsd = gyrate_frame$Apo, gyrate_wt)
a_A675V = cbind(rmsd = gyrate_frame$A675V, gyrate_A675V)
a_C580Y = cbind(rmsd = gyrate_frame$C580Y, gyrate_C580Y)
a_M476I = cbind(rmsd = gyrate_frame$M476I, gyrate_M476I)
a_P553L = cbind(rmsd = gyrate_frame$P553L, gyrate_P553L)
a_P574L = cbind(rmsd = gyrate_frame$P574L, gyrate_P574L)
a_R561H = cbind(rmsd = gyrate_frame$R561H, gyrate_R561H)
a_A557S = cbind(rmsd = gyrate_frame$A557S, gyrate_A557S)
a_A578S = cbind(rmsd = gyrate_frame$A578S, gyrate_A578S)
a_Y493H_C580Y = cbind(rmsd = gyrate_frame$Y493H_C580Y, gyrate_Y493H_C580Y)

gyrate_data_1 = rbind(a_WT, a_A675V, a_C580Y, a_M476I, a_P553L, a_P574L, a_R561H, a_A557S, a_A578S, a_Y493H_C580Y)

colnames(gyrate_data_1) = c("rmsd (nm)", "Systems")

write.csv(gyrate_data_1, file = "./rmsf_new.csv")
gyrate_data_1 = rbind(a_WT, a_A675V, a_C580Y, a_P553L, a_P574L, a_R561H, a_A557S, a_A578S, a_Y493H_C580Y)





