from init_es2 import *
from analy_funs_es2 import *
sys.path.append('/Users/bauera/Dropbox/UofT/experiments/event-segmentation/analysis')
import init_es
sys.path.append('/Users/bauera/Dropbox/UofT/experiments/event-seg_phase2_normStimuliV3/analysis')
import analy_cmp_esnAllVers


# get boundary scores =========================================================
# adult data only
pGrp = 'aEventBounds'
eventBoundData = init_es.allDat[pGrp][1:3] # rugrats, busyWorld

forLMER_c1 = pd.read_csv('../designMaterials/forLMER_randEffectsVars_' + cartoonNames[0] + '_init.csv')
forLMER_c2 = pd.read_csv('../designMaterials/forLMER_randEffectsVars_' + cartoonNames[1] + '_init.csv')

def time2Sec(timestr): # should add to analy_funs_esX.py 
    ftr = [60,1] # does not permit hours
    return sum([i*j for i,j in zip(ftr, map(int,timestr.split(':')))])

# cartoon 1
eventBoundStart_c1 = [time2Sec(i) for i in forLMER_c1['lastOnScreen'].tolist()]
eventBoundEnd_c1 = [i+j for i,j in zip(eventBoundStart_c1, forLMER_c1['distanceSec'].tolist())]
eventBounds_c1 = pd.DataFrame({'start': eventBoundStart_c1,
                               'end' : eventBoundEnd_c1})

# cartoon 2
eventBoundStart_c2 = [time2Sec(i) for i in forLMER_c2['lastOnScreen'].tolist()]
eventBoundEnd_c2 = [i+j for i,j in zip(eventBoundStart_c2, forLMER_c2['distanceSec'].tolist())]
eventBounds_c2 = pd.DataFrame({'start': eventBoundStart_c2,
                               'end' : eventBoundEnd_c2})

eventBoundDesign = [eventBounds_c1, eventBounds_c2]

for i in range(len(eventBoundDesign)):
    boundaryScores = []
    
    for j in eventBoundDesign[i].index.tolist():
        startSlice = eventBoundDesign[i].loc[j, 'start']
        endSlice = eventBoundDesign[i].loc[j, 'end'] + 1
        boudaryScore = eventBoundData[i].sum(axis=1).iloc[startSlice:endSlice].sum()
        boundaryScores.append(boudaryScore)

    if i == 0:
        forLMER_c1['boundaryScore'] = boundaryScores
    else:
        forLMER_c2['boundaryScore'] = boundaryScores


# get norming difficulties ====================================================
df_esn1 = analy_cmp_esnAllVers.df_wi_esn.append(analy_cmp_esnAllVers.df_ac_esn, ignore_index=True)
df_esn1['itemID_mod'] = df_esn1['itemID']

df_esn2 = analy_cmp_esnAllVers.df_wi_esn2.append(analy_cmp_esnAllVers.df_ac_esn2, ignore_index=True)
remap = {1: 3, 4: 9, 5: 11, 6: 12, 7: 13, 2: 7, 3: 8, 9: 18}
df_esn2['itemID_mod'] = df_esn2['itemID'].map(remap)

df_esn3 = analy_cmp_esnAllVers.df_wi_esn3.append(analy_cmp_esnAllVers.df_ac_esn3, ignore_index=True)
remap = {1: 14, 2: 19}
df_esn3['itemID_mod'] = df_esn3['itemID'].map(remap)

df_esn_all = df_esn1.append(df_esn2) \
                    .append(df_esn3)

RT_esn_all = df_esn_all[(df_esn_all['correct'] == 1)].groupby('itemID_mod').agg({'latency': np.average})
RT_esn_all['itemID'] = RT_esn_all.index
acc_esn_all = df_esn_all.groupby('itemID_mod').agg({'correct': np.average})
acc_esn_all['itemID'] = acc_esn_all.index

forLMER_c1 = forLMER_c1.merge(RT_esn_all.loc[1:8,], on='itemID') \
                       .merge(acc_esn_all.loc[1:8,], on='itemID') \
                       .rename(columns={'latency': 'norm_RT', 'correct': 'norm_acc'})
forLMER_c2 = forLMER_c2.merge(RT_esn_all.loc[9:,], on='itemID') \
                       .merge(acc_esn_all.loc[9:,], on='itemID') \
                       .rename(columns={'latency': 'norm_RT', 'correct': 'norm_acc'})


# get phase 2 data and expand by subj =========================================
# adult data only
allDat_byTrial_RT_c1 = get_trial_data(aPs, cPs, paths)['aDat_RT_byCs'][0]
allDat_byTrial_acc_c1 = get_trial_data(aPs, cPs, paths)['aDat_acc_byCs'][0]
RT_c1 = pd.DataFrame()
acc_c1 = pd.DataFrame()
for i in range(len(aPs)):
    df_subjID = pd.DataFrame(data={'subjID': (np.ones([len(allDat_byTrial_RT_c1)])*(i+1)).astype(int)})
    RT_c1 = RT_c1.append( \
                 pd.concat([allDat_byTrial_RT_c1[['itemID', 'subj' + str(i+1)]] \
                 .rename(columns={'subj' + str(i+1): 'phase2_RT'}), df_subjID['subjID']],axis=1), ignore_index=True)
    acc_c1 = acc_c1.append(pd.concat([allDat_byTrial_acc_c1[['itemID', 'subj' + str(i+1)]] \
                 .rename(columns={'subj' + str(i+1): 'phase2_acc'}), df_subjID['subjID']],axis=1), ignore_index=True)
phase2_c1 = RT_c1.merge(acc_c1)

allDat_byTrial_RT_c2 = get_trial_data(aPs, cPs, paths)['aDat_RT_byCs'][1]
allDat_byTrial_acc_c2 = get_trial_data(aPs, cPs, paths)['aDat_acc_byCs'][1]
RT_c2 = pd.DataFrame()
acc_c2 = pd.DataFrame()
for i in range(len(aPs)):
    df_subjID = pd.DataFrame(data={'subjID': (np.ones([len(allDat_byTrial_RT_c2)])*(i+1)).astype(int)})
    RT_c2 = RT_c2.append( \
                 pd.concat([allDat_byTrial_RT_c2[['itemID', 'subj' + str(i+1)]] \
                 .rename(columns={'subj' + str(i+1): 'phase2_RT'}), df_subjID['subjID']],axis=1), ignore_index=True)
    acc_c2 = acc_c2.append(pd.concat([allDat_byTrial_acc_c2[['itemID', 'subj' + str(i+1)]] \
                 .rename(columns={'subj' + str(i+1): 'phase2_acc'}), df_subjID['subjID']],axis=1), ignore_index=True)
phase2_c2 = RT_c2.merge(acc_c2)


# Merge forLMER and phase2 ====================================================
# adult data only
forLMER_prepped_c1 = forLMER_c1.merge(phase2_c1, on='itemID')
forLMER_prepped_c2 = forLMER_c2.merge(phase2_c2, on='itemID')


# save for analy_LMER.R =======================================================
# adult data only
forLMER_prepped_c1.to_csv('./forLMER_randEffectsVars_' + cartoonNames[0] + '_prepped.csv', index=False)
forLMER_prepped_c2.to_csv('./forLMER_randEffectsVars_' + cartoonNames[1] + '_prepped.csv', index=False)
