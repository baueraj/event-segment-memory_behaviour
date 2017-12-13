setwd('/Users/bauera/Dropbox/UofT/experiments/event-seg_phase2/analysis')

library(lme4); library(lmerTest); library(reshape)

df_c1 <- read.csv(file="forLMER_randEffectsVars_busyWorld_prepped.csv", head=TRUE, sep=",")
df_c2 <- read.csv(file="forLMER_randEffectsVars_rugrats_prepped.csv", head=TRUE, sep=",")

# combine data
df_c1$cartoon<-1
df_c2$cartoon<-2
df<-rbind(df_c1,df_c2)

# transform data -- RT not normally distributed
df$log_phase2_RT<-log(df$phase2_RT)

# calculate proportion score and compute some bins (note -- HARD-CODED)
df$boundaryScoreProp<-df$boundaryScore/22 #<------------ NOTE: HARD-CODED NO. OF SUBJECTS
df$boundaryScoreProp<-df$boundaryScore/22 #<------------ NOTE: HARD-CODED NO. OF SUBJECTS
df$boundaryScoreBin4<-round(df$boundaryScoreProp*3.6)
df$boundaryScoreBin<-1*(df$boundaryScoreProp>median(df$boundaryScoreProp))

# center and rescale some data
df<-ddply(df,c('subjID'),transform,distanceSecCent=(distanceSec-mean(distanceSec)))
df<-ddply(df,c('subjID'),transform,norm_RTCent=scale(norm_RT))
df<-ddply(df,c('itemID'),transform,ave_acc=(mean(phase2_acc)))

# run LMER models on RT and accuracy, for cartoons combined and separatelys
RT_model_1 <- lmer(log_phase2_RT ~ boundaryScoreProp + distanceSecCent + norm_RTCent + norm_acc + cartoon + (boundaryScoreProp + distanceSecCent + norm_RTCent + norm_acc + cartoon || subjID), data=df)
summary(RT_model_1)

RT_model_2 <- lmer((phase2_RT) ~ boundaryScoreProp * distanceSecCent + norm_RTCent + norm_acc + cartoon + (boundaryScoreProp * distanceSecCent + norm_RTCent + norm_acc + cartoon || subjID), data=df)
summary(RT_model_2)

RT_model_c1 <- lmer(log_phase2_RT ~ boundaryScoreProp + distanceSecCent + norm_RTCent + norm_acc + (boundaryScoreProp + distanceSecCent + norm_RTCent + norm_acc || subjID), data=df, subset = (cartoon==1))
RT_model_c2 <- lmer(log_phase2_RT ~ boundaryScoreProp + distanceSecCent + norm_RTCent + norm_acc + (boundaryScoreProp + distanceSecCent + norm_RTCent + norm_acc || subjID), data=df, subset = (cartoon==2))
summary(RT_model_c1)
summary(RT_model_c2)

acc_model <- glmer(phase2_acc ~ boundaryScoreProp + norm_acc + distanceSecCent + norm_RTCent+ cartoon + (boundaryScoreProp+norm_acc + distanceSecCent + norm_RTCent + cartoon || subjID), data=df, family="binomial")#subset=(ave_acc<1&ave_acc>.5))#, subset=(norm_acc<.92))
summary(acc_model)

# other analysis
RT.bound <- cast(df, subjID ~ boundaryScoreBin4, mean, value=('phase2_RT'), na.rm=T)
colMeans(RT.bound, na.rm=T)

item_acc <- cast(df, itemID~., mean, value=('phase2_acc'), na.rm=T)

