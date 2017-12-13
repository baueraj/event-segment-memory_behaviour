def get_participant_data_plt(aPs, cPs, paths, rt_thresh_fl):
    """
    read participant data stored as csv files

    Parameters
    ----------
    aPs : vector array
        adult participant IDs
    cPs : vector array
        children participant IDs   
    paths : list of strings
        paths to files
    rt_thresh_fl : int (==0 or 1)
        flag to further threshold RT (apart from outliers)    
        
    Returns
    -------
    allDat : dictionary (of data)

    Notes
    -----
    Includes code handling of >rt_threshold data (PsychoPy missed these catches)
    """
    
    import pdb
    import numpy as np
    import pandas as pd
    
    rm_outliers_std = 2.5
    if rt_thresh_fl:
        rt_threshold = 5000
    else:
        rt_threshold = 99999
    
    dPath = paths[0]

    # read adult data first, then child data
    for p in ('a', 'c'):
        if p == 'a':
            iPs = aPs
        else:
            iPs = cPs
            #cDat = [] # dummy code when no children data
            #allDat = {'aDat_byCs': aDat, 'cDat_byCs': cDat, 'aPs': aPs, 'cPs': cPs} # dummy code when no children data
            #return allDat # dummy code when no children data

        dat_c1 = pd.DataFrame()
        dat_c2 = pd.DataFrame()
        ps_c1 = []
        ps_c2 = []
            
        for idx, i in enumerate(iPs):
            if i % 2 == 0:
                iCartoonOrder = ['1', '2']
            else:
                iCartoonOrder = ['2', '1']
    
            for s, c in enumerate(iCartoonOrder):
                
                try:
                    iDat = pd.read_csv(dPath + '/' + p + '_p' + str(i) + '_s' + str(s + 1) + '_c' + c + '.csv')
                except:
                    print('{}{} missing data for c{}'.format(p, str(i), c))
                    continue
                
                # label >rt_threshold trials as 'timeout' (where PsychoPy missed)
                great_thresh_ind = np.where(iDat[' RT (ms)'] >= rt_threshold)
                iDat.loc[great_thresh_ind[0], 'correct'] = 0
                iDat.loc[great_thresh_ind[0], ' RT (ms)'] = 0
                iDat.loc[great_thresh_ind[0], ' response'] = 'timeout'
                
                # remove data with RT beyond x * std of mean (rm_outliers_std defined above)
                def drop(group):
                    mean, std = group.mean(), group.std()
                    inliers = (group - mean).abs() <= rm_outliers_std * std
                    return inliers

                # Remove outliers ONLY for CORRECT trials
                #maskRT = iDat.groupby(' condition')[' RT (ms)'].apply(drop)
                #iDat = iDat[maskRT]
                maskRT = iDat[(iDat['correct'] == 1)].groupby(' condition')[' RT (ms)'].apply(drop) # returns the inliers mask
                iDat.drop(maskRT[maskRT == False].index, inplace=True)
                
                # accuracy
                iDat_acc = iDat[iDat[' response'] != 'timeout'].groupby(' condition').agg({'correct': np.average})
                iDat_timeout = iDat.groupby(' condition').agg({' response': lambda x: (x == 'timeout').mean()})

                # RT w/ removal of incorrect trials
                iDat_corrTrials = iDat.copy()
                iDat_corrTrials = iDat[(iDat['correct'] == 1)]
                iDat_corrTri_RT = iDat_corrTrials.groupby(' condition').agg({' RT (ms)': np.average})
                
                if c == '1':
                    
                    if 1 in iDat_corrTri_RT.index:
                        wi_RT_add = iDat_corrTri_RT.loc[1, ' RT (ms)']
                    else:
                        # consider changing to nan or somehow indicating this cond's data doesn't exist for this subj
                        wi_RT_add = 0
                        
                    if 2 in iDat_corrTri_RT.index:
                        ac_RT_add = iDat_corrTri_RT.loc[2, ' RT (ms)']
                    else:
                        ac_RT_add = 0    
                        
                    dat_c1 = dat_c1.append({'wi_acc': iDat_acc.loc[1, 'correct'], 
                                            'ac_acc': iDat_acc.loc[2, 'correct'],
                                            'wi_tout': iDat_timeout.loc[1, ' response'], 
                                            'ac_tout': iDat_timeout.loc[2, ' response'],                      
                                            'wi_RT': wi_RT_add,
                                            'ac_RT': ac_RT_add},
                                ignore_index=True)
                    ps_c1.append(i)

                else:
                    
                    if 3 in iDat_corrTri_RT.index:
                        wi_RT_add = iDat_corrTri_RT.loc[3, ' RT (ms)']
                    else:
                        wi_RT_add = 0
                        
                    if 4 in iDat_corrTri_RT.index:
                        ac_RT_add = iDat_corrTri_RT.loc[4, ' RT (ms)']
                    else:
                        ac_RT_add = 0   
                    
                    dat_c2 = dat_c2.append({'wi_acc': iDat_acc.loc[3, 'correct'], 
                                            'ac_acc': iDat_acc.loc[4, 'correct'],
                                            'wi_tout': iDat_timeout.loc[3, ' response'], 
                                            'ac_tout': iDat_timeout.loc[4, ' response'],                     
                                            'wi_RT': wi_RT_add,
                                            'ac_RT': ac_RT_add},
                                ignore_index=True)
                    ps_c2.append(i)
                    
        #reorder columns
        dat_c1 = dat_c1[['wi_acc', 'ac_acc', 'wi_tout', 'ac_tout', 'wi_RT', 'ac_RT']]
        dat_c2 = dat_c2[['wi_acc', 'ac_acc', 'wi_tout', 'ac_tout', 'wi_RT', 'ac_RT']]
       
        if p == 'a':
            dat_c1.set_index(np.array(ps_c1), inplace=True)
            dat_c2.set_index(np.array(ps_c2), inplace=True)
            aDat = [dat_c1, dat_c2]
        else:
            dat_c1.set_index(np.array(ps_c1), inplace=True)
            dat_c2.set_index(np.array(ps_c2), inplace=True)
            cDat = [dat_c1, dat_c2]
                
    allDat = {'aDat_byCs': aDat, 'cDat_byCs': cDat, 'aPs': aPs, 'cPs': cPs}
    
    return allDat



def get_trial_data_plt(aPs, cPs, paths, rt_thresh_fl):
    """
    read participant data stored as csv files and return trial data avg'd over subjects

    Parameters
    ----------
    aPs : vector array
        adult participant IDs
    cPs : vector array
        children participant IDs   
    paths : list of strings
        paths to files
    rt_thresh_fl : int (==0 or 1)
        flag to further threshold RT    
        
    Returns
    -------
    allDat_byTrial : dictionary (of trial data avg'd over subjects)

    Notes
    -----
    Not currently assessing 'timeout' as its own response
    Not currently removing outlier data per subject
    Includes code handling of >rt_threshold data (PsychoPy missed these catches)
    """

    import pdb
    import numpy as np
    import pandas as pd
    
    dPath = paths[0]
    otherPath1 = paths[1]
    cartoonNames = ['rugrats', 'busyWorld']
    
    if rt_thresh_fl:
        rt_threshold = 5000
    else:
        rt_threshold = 99999

    # read adult data first, then child data
    for p in ('a', 'c'):
        if p == 'a':
            iPs = aPs
        else:
            iPs = cPs
            #allDat_byTrial = {'aDat_acc_byCs': aDat_acc, 'aDat_RT_byCs': aDat_RT, 'aPs': aPs, 'cPs': cPs} # dummy code when no children data
            #return allDat_byTrial # dummy code when no children data
            
        dat_acc_c1 = pd.DataFrame()
        dat_RT_c1 = pd.DataFrame()
        dat_acc_c2 = pd.DataFrame()
        dat_RT_c2 = pd.DataFrame()
            
        for idx, i in enumerate(iPs):
            if i % 2 == 0:
                iCartoonOrder = ['1', '2']
            else:
                iCartoonOrder = ['2', '1']
    
            for s, c in enumerate(iCartoonOrder):
                
                try:
                    iDat_nonSort = pd.read_csv(dPath + '/' + p + '_p' + str(i) + '_s' + str(s + 1) + '_c' + c + '.csv')
                except:
                    print('{}{} missing data for c{}'.format(p, str(i), c))
                    continue
                
                iDat_nonSort['trialNo'] = iDat_nonSort.index
                            
                getItemIDs = pd.read_csv(otherPath1 + '/' + 'forLMER_randEffectsVars_' + cartoonNames[int(c)-1] + '_init.csv')
                iDat_nonSort['itemID'] = getItemIDs['itemID']
                
                iDat = iDat_nonSort.copy()
                iDat = iDat.sort_values([' condition', 'trialNo'])
                
                # label >rt_threshold trials as 'timeout' (where PsychoPy missed)
                great_thresh_ind = np.where(iDat[' RT (ms)'] >= rt_threshold)
                iDat.loc[great_thresh_ind[0], 'correct'] = 0
                iDat.loc[great_thresh_ind[0], ' RT (ms)'] = 0
                iDat.loc[great_thresh_ind[0], ' response'] = 'timeout'
                
                # replace RT with nan for incorrect trials
                iDat.loc[(iDat['correct'] == 0), ' RT (ms)'] = np.nan
                         
                # replace acc with nan for timeout trials
                iDat.loc[(iDat[' response'] == 'timeout'), 'correct'] = np.nan
                
                if c == '1':
                    if len(dat_acc_c1) == 0:
                        dat_acc_c1 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_acc_c1[' condition'] = iDat[' condition'].copy()
                        dat_acc_c1['itemID'] = iDat['itemID'].copy()
                        dat_tout_c1 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_tout_c1[' condition'] = iDat[' condition'].copy()
                        dat_tout_c1['itemID'] = iDat['itemID'].copy()
                        dat_RT_c1 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_RT_c1[' condition'] = iDat[' condition'].copy()
                        dat_RT_c1['itemID'] = iDat['itemID'].copy()
                        
                    dat_acc_c1['subj' + str(i)] = iDat['correct'].copy()
                    dat_tout_c1['subj' + str(i)] = (iDat[' response'] == 'timeout').astype(int)
                    dat_RT_c1['subj' + str(i)] = iDat[' RT (ms)'].copy()
                else:
                    if len(dat_acc_c2) == 0:
                        dat_acc_c2 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_acc_c2[' condition'] = iDat[' condition'].copy()
                        dat_acc_c2['itemID'] = iDat['itemID'].copy()
                        dat_tout_c2 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_tout_c2[' condition'] = iDat[' condition'].copy()
                        dat_tout_c2['itemID'] = iDat['itemID'].copy()
                        dat_RT_c2 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_RT_c2[' condition'] = iDat[' condition'].copy()
                        dat_RT_c2['itemID'] = iDat['itemID'].copy()
                        
                    dat_acc_c2['subj' + str(i)] = iDat['correct'].copy()
                    dat_tout_c2['subj' + str(i)] = (iDat[' response'] == 'timeout').astype(int)
                    dat_RT_c2['subj' + str(i)] = iDat[' RT (ms)'].copy()
                
        if p == 'a':
            aDat_acc = [dat_acc_c1, dat_acc_c2]
            aDat_tout = [dat_tout_c1, dat_tout_c2]
            aDat_RT = [dat_RT_c1, dat_RT_c2]
        else:
            cDat_acc = [dat_acc_c1, dat_acc_c2]
            cDat_tout = [dat_tout_c1, dat_tout_c2]
            cDat_RT = [dat_RT_c1, dat_RT_c2]
                
    allDat_byTrial = {'aDat_acc_byCs': aDat_acc, 'aDat_tout_byCs': aDat_tout, 'aDat_RT_byCs': aDat_RT,
              'cDat_acc_byCs': cDat_acc, 'cDat_tout_byCs': cDat_tout, 'cDat_RT_byCs': cDat_RT,
              'aPs': aPs, 'cPs': cPs}

    return allDat_byTrial



"""
def rm_outliers(df, std_frm_mean, col_name):
    ""
    drops rows in df if latency falls above high threshold
    
    Parameters
    ----------
    df : pandas data frame
        contains the data
    std_frm_mean : int
        specifies how many stds from mean to be removed
    col_name : string
        specifies df column name to access for thresholding

    Returns
    -------
    df_thresh : pandas data frame
        contains the data with outlier data rows 
        
    Notes
    -----
    NA
    ""

    import numpy as np
    import pandas as pd

    thresh = np.std(df[col_name]) * std_frm_mean
    grt_thresh_ind = np.where(df[col_name] > thresh)
    less_thresh_ind = np.where(df[col_name] < thresh)
    df_thresh = df.copy()
    df_thresh.drop(df_thresh.index[[grt_thresh_ind, less_thresh_ind]], inplace=True)
    df_thresh.reset_index(drop=True, inplace=True)
    
    return df_thresh
"""
