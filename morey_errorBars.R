# http://www.cookbook-r.com/Graphs/Plotting_means_and_error_bars_(ggplot2)/   <- search "morey"

library(reshape2); library (ggplot2)
source("/Users/bauera/Dropbox/UofT/experiments/common-R-code/moreyFuncs")

setwd('/Users/bauera/Dropbox/UofT/experiments/event-seg_phase2/analysis')

# cartoon 1, acc data ====================================================================
df <- read.csv(file="df_aDat_byCs_1.csv", head=TRUE, sep=",")

df <- df[, c("X", "wi_acc", "ac_acc")]
df$X <- factor(df$X)

df_long <- melt(df,
                id.vars = "X",
                measure.vars = c("wi_acc","ac_acc"),
                variable.name = "condition")

df_a_acc_c1 <- summarySEwithin(df_long, measurevar="value", withinvars="condition",
                        idvar="X", na.rm=FALSE, conf.interval=.95)

# cartoon 2, acc data ====================================================================
df <- read.csv(file="df_aDat_byCs_2.csv", head=TRUE, sep=",")

df <- df[, c("X", "wi_acc", "ac_acc")]
df$X <- factor(df$X)

df_long <- melt(df,
                id.vars = "X",
                measure.vars = c("wi_acc","ac_acc"),
                variable.name = "condition")

df_a_acc_c2 <- summarySEwithin(df_long, measurevar="value", withinvars="condition",
                               idvar="X", na.rm=FALSE, conf.interval=.95)


# cartoon 1, RT data ====================================================================
df <- read.csv(file="df_aDat_byCs_1.csv", head=TRUE, sep=",")

df <- df[, c("X", "wi_RT", "ac_RT")]
df$X <- factor(df$X)

df_long <- melt(df,
                id.vars = "X",
                measure.vars = c("wi_RT","ac_RT"),
                variable.name = "condition")

df_a_RT_c1 <- summarySEwithin(df_long, measurevar="value", withinvars="condition",
                               idvar="X", na.rm=FALSE, conf.interval=.95)

# cartoon 2, RT data ====================================================================
df <- read.csv(file="df_aDat_byCs_2.csv", head=TRUE, sep=",")

df <- df[, c("X", "wi_RT", "ac_RT")]
df$X <- factor(df$X)

df_long <- melt(df,
                id.vars = "X",
                measure.vars = c("wi_RT","ac_RT"),
                variable.name = "condition")

df_a_RT_c2 <- summarySEwithin(df_long, measurevar="value", withinvars="condition",
                               idvar="X", na.rm=FALSE, conf.interval=.95)

# combine SEs, write to csv =============================================================

cartoon <- c(1, 2) 
accSE_byCs <- c(df_a_acc_c1['se']$se[1], df_a_acc_c2['se']$se[1])
RTSE_byCs <- c(df_a_RT_c1['se']$se[1], df_a_RT_c2['se']$se[1])
dfSE <- data.frame(cartoon, accSE_byCs, RTSE_byCs)
names(dfSE) <- c('cartoon', 'acc', 'RT')

write.csv(dfSE,'dfSEwi_byCs.csv', row.names=FALSE)