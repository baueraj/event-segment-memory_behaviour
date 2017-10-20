def get_participant_data(aPs, cPs, paths):
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
        
    Returns
    -------
    allDat : dictionary (of data)

    Notes
    -----
    NA
    """
    
    import pdb
    import numpy as np
    import pandas as pd
    
    rm_outliers_std = 2.5
    
    dPath = paths[0]

    # read adult data first, then child data
    for p in ('a', 'c'):
        if p == 'a':
            iPs = aPs
        else:
            iPs = cPs
            cDat = [] # dummy code when no children data
            allDat = {'aDat_byCs': aDat, 'cDat_byCs': cDat, 'aPs': aPs, 'cPs': cPs} # dummy code when no children data
            return allDat # dummy code when no children data
            
        dat_c1 = pd.DataFrame()
        dat_c2 = pd.DataFrame()
            
        for idx, i in enumerate(iPs):
            if i % 2 == 0:
                iCartoonOrder = ['1', '2']
            else:
                iCartoonOrder = ['2', '1']
    
            for s, c in enumerate(iCartoonOrder):
                iDat = pd.read_csv(dPath + '/' + p + '_p' + str(i) + '_s' + str(s + 1) + '_c' + c + '.csv')
                
                # remove data with RT beyond x * std of mean (rm_outliers_std defined at beginning of function)
                def drop(group):
                    mean, std = group.mean(), group.std()
                    inliers = (group - mean).abs() <= rm_outliers_std * std
                    return inliers
                
                maskRT = iDat.groupby(' condition')[' RT (ms)'].apply(drop)
                iDat = iDat[maskRT]           
                
                # accuracy
                iDat_acc = iDat.groupby(' condition').agg({'correct': np.average})
                
                # RT w/ removal of incorrect trials
                iDat_corrTrials = iDat.copy()
                iDat_corrTrials = iDat[(iDat['correct'] == 1)]
                iDat_corrTri_RT = iDat_corrTrials.groupby(' condition').agg({' RT (ms)': np.average})
                
                if c == '1':
                    dat_c1 = dat_c1.append({'wi_acc': iDat_acc.loc[1, 'correct'], 
                                            'ac_acc': iDat_acc.loc[2, 'correct'],
                                            'wi_RT': iDat_corrTri_RT.loc[1, ' RT (ms)'],
                                            'ac_RT': iDat_corrTri_RT.loc[2, ' RT (ms)']},
                                ignore_index=True)
                else:
                    dat_c2 = dat_c2.append({'wi_acc': iDat_acc.loc[3, 'correct'], 
                                            'ac_acc': iDat_acc.loc[4, 'correct'],
                                            'wi_RT': iDat_corrTri_RT.loc[3, ' RT (ms)'],
                                            'ac_RT': iDat_corrTri_RT.loc[4, ' RT (ms)']},
                                ignore_index=True)
                    
        dat_c1 = dat_c1[['wi_acc', 'ac_acc', 'wi_RT', 'ac_RT']]
        dat_c2 = dat_c2[['wi_acc', 'ac_acc', 'wi_RT', 'ac_RT']]
        
        if p == 'a':
            dat_c1.set_index(aPs, inplace=True)
            dat_c2.set_index(aPs, inplace=True)
            aDat = [dat_c1, dat_c2]
        else:
            dat_c1.set_index(cPs, inplace=True)
            dat_c2.set_index(cPs, inplace=True)
            cDat = [dat_c1, dat_c2]
                
    allDat = {'aDat_byCs': aDat, 'cDat_byCs': cDat, 'aPs': aPs, 'cPs': cPs}
    
    return allDat



def get_trial_data(aPs, cPs, paths):
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
        
    Returns
    -------
    allDat_byTrial : dictionary (of trial data avg'd over subjects)

    Notes
    -----
    NA
    """
    import pdb
    import numpy as np
    import pandas as pd
    
    dPath = paths[0]
    otherPath1 = paths[1]
    cartoonNames = ['rugrats', 'busyWorld']

    # read adult data first, then child data
    for p in ('a', 'c'):
        if p == 'a':
            iPs = aPs
        else:
            iPs = cPs
            allDat_byTrial = {'aDat_acc_byCs': aDat_acc, 'aDat_RT_byCs': aDat_RT, 'aPs': aPs, 'cPs': cPs} # dummy code when no children data
            return allDat_byTrial # dummy code when no children data
            
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
                iDat_nonSort = pd.read_csv(dPath + '/' + p + '_p' + str(i) + '_s' + str(s + 1) + '_c' + c + '.csv')
                iDat_nonSort['trialNo'] = iDat_nonSort.index
                            
                getItemIDs = pd.read_csv(otherPath1 + '/' + 'forLMER_randEffectsVars_' + cartoonNames[int(c)-1] + '_init.csv')
                iDat_nonSort['itemID'] = getItemIDs['itemID']
                
                iDat = iDat_nonSort.copy()
                iDat = iDat.sort_values([' condition', 'trialNo'])
                
                # replace RT with nan for incorrect trials
                iDat.loc[(iDat['correct'] == 0), ' RT (ms)'] = np.nan
                
                if c == '1':
                    if len(dat_acc_c1) == 0:
                        dat_acc_c1 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_acc_c1[' condition'] = iDat[' condition'].copy()
                        dat_acc_c1['itemID'] = iDat['itemID'].copy()
                        dat_RT_c1 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_RT_c1[' condition'] = iDat[' condition'].copy()
                        dat_RT_c1['itemID'] = iDat['itemID'].copy()
                        
                    dat_acc_c1['subj' + str(i)] = iDat['correct'].copy()
                    dat_RT_c1['subj' + str(i)] = iDat[' RT (ms)'].copy()
                else:
                    #pdb.set_trace()
                    if len(dat_acc_c2) == 0:
                        dat_acc_c2 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_acc_c2[' condition'] = iDat[' condition'].copy()
                        dat_acc_c2['itemID'] = iDat['itemID'].copy()
                        dat_RT_c2 = pd.DataFrame(index=iDat['trialNo'].copy())
                        dat_RT_c2[' condition'] = iDat[' condition'].copy()
                        dat_RT_c2['itemID'] = iDat['itemID'].copy()
                        
                    dat_acc_c2['subj' + str(i)] = iDat['correct'].copy()
                    dat_RT_c2['subj' + str(i)] = iDat[' RT (ms)'].copy()
                
        if p == 'a':
            aDat_acc = [dat_acc_c1, dat_acc_c2]
            aDat_RT = [dat_RT_c1, dat_RT_c2]
        else:
            cDat_acc = [dat_acc_c1, dat_acc_c2]
            cDat_RT = [dat_RT_c1, dat_RT_c2]
                
    allDat_byTrial = {'aDat_acc_byCs': aDat_acc, 'aDat_RT_byCs': aDat_RT,
              'cDat_acc_byCs': cDat_acc, 'acDat_RT_byCs': cDat_RT,
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
