# load packages 
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# load the master results as a global varaible 
# a global variable can be used anywhere in the script
results = pd.read_csv('C:\\Users\\walshn4\\Desktop\\Worldcuppool\\Master results.csv')

# to get the group results from the final table we first create an empty list
group_list = []
# we then iterate through the column headers for each group and append the team positions 
# in each  group to the list
for group in list(results)[:8]:
    for team_position in results[group].head(4):
        group_list.append(team_position) 
        
# We then convert the list to a pd series(column) so we can use it for bollean comparison 
group_final = pd.Series(group_list)
# We create a results table to enter the results of each entrant and set correct column types
results_table =  pd.DataFrame(dtype=np.int8, columns = ['Entrantname', 'GP Points', 'SR Points', 'Quarter Points', 'Semi Points','Final Points', 'Playoff Winner Points', 'Winner Points', 'Total Points'])
results_table['Entrantname'] = results_table['Entrantname'].astype(str)

# ------------------------------------------
# FUNCTION get file extension
# ------------------------------------------
def get_file_extension(file_name):
    # We get the size of a string
    size = len(file_name) - 1

    # We look for the position where the last point was placed
    found = False
    while found == False and size >= 0:
        if file_name[size] == '.':
            found = True
        else:
            size = size - 1
            
    # We collect the extension
    if found == True:
        extension = file_name[(size+1):(len(file_name))]
    else:
        extension = ''
        
    # We return the extension
    return extension

#------------------------------------------
# FUNCTION select_files_from_directory_with_real_extension
#------------------------------------------
def select_files_from_directory_with_real_extension(directory, extension):
    # We get the current directory and ask for all its elements
    os.chdir(directory)
    dir = os.getcwd()
    files = os.listdir(dir)

    # We create a list with all files we are interested at
    # Initially, the list is empty
    selected_files = []

    # We traverse the files of the directory to select the ones we are interested at
    for i in range(0, len(files)):
        name = files[i]
        # If the file is not a subdirectory and has csv extension then we pick it
        if os.path.isdir(name) == False and get_file_extension(name) == extension:
            selected_files.append(name)

    # We return the list of files
    return selected_files

# ------------------------------------------
# FUNCTION simulating_my_map
# ------------------------------------------
def get_results(directory, extension):
    #  We get the files to be processed
    input_files = select_files_from_directory_with_real_extension(directory, extension)
    
    # we split the input file name to get a list of entrant names
    names_list = [i.split('.')[0] for i in input_files]
    
    #create an empty list to store predicted winners
    final_winners = []
    playoff_winners = []
    
    #entrant = pd.read_csv("C:\\Users\\walshn4\\Desktop\\Worldcuppool\\Entrants\\Ian Mc Carthy.csv")
    #  We process them
    for i in range(0, len(input_files)):
        
        #  We convert the file to a pd dataframe
        entrant = pd.read_csv(input_files[i])
        # set rownum to be order of entrant files
        
        # append the predictied winner to winners list
        final_winners.append(entrant['final winner'].dropna().loc[0])
        playoff_winners.append(entrant['Playoff winner'].dropna().loc[0])
        rownum = i
        # enter the name into the corresponding cell
        results_table.at[rownum, 'Entrantname'] = names_list[i]
        # repeat of the results table group positions for each entrant table
        gplist = []
        for group in list(entrant)[:8]:
            for team_position in entrant[group].head(4):
                gplist.append(team_position)        
        gp_entrant = pd.Series(gplist)
        
        # to get the points for each allocation we must sum a boolean array and multiply it by the points 
        # .loc is used to select specific rows in a column
        # .iloc is used to select specific rows and columns in a dataframe
        #col_entrant = results.columns[8:]
        #col_results = results_table.columns[2:]
        
        # Group position
        results_table.at[rownum, 'GP Points'] = int(sum(group_final == gp_entrant) * 2)
        
        # Second Round
        sr_score = 0
        for team in entrant['Round 2']:
            if team in list(results['Round 2']):
                sr_score += 3     
        results_table.at[rownum, 'SR Points'] = sr_score
        
        # Quarter Finaln Points
        qf_score = 0
        for team in entrant['Quarter finals'].loc[:7]:
            if team in list(results['Quarter finals'].loc[:7]):
                qf_score += 4
        results_table.at[rownum, 'Quarter Points'] = qf_score
        
        # Semi Final Points
        semi_score = 0
        for team in entrant['Semi Finals'].loc[:3]:
            if team in list(results['Semi Finals'].loc[:3]):
                semi_score += 5
        results_table.at[rownum,'Semi Points'] = semi_score
        
        # Final Points
        final = 0
        for team in entrant['Final'].loc[:1]:
            if team in list(results['Final'].loc[:1]):
                final += 6
        results_table.at[rownum,'Final Points'] = final
        
        # Playoff Winner
        results_table.at[rownum, 'Playoff Winner Points'] = sum(entrant['Playoff winner'].loc[:0] == results['Playoff winner'].loc[:0]) * 6
        # Final Winner
        results_table.at[rownum, 'Winner Points'] = sum(entrant['final winner'].loc[:0] == results['final winner'].loc[:0]) * 10
        # Total Points
        results_table.at[rownum, 'Total Points'] = results_table.iloc[[rownum], 1:].sum(axis = 1) 
        
    # sort the table in descending order on total points 
    final_table = results_table.sort_values(by='Total Points', ascending=False)
    # export the final table to csv
    final_table.to_csv("C:\\Users\\walshn4\\Desktop\\Worldcuppool\\Results 16th july.csv", index = False)
    
    # plot the distribution of results
    plt.figure()   
    sns.distplot(final_table['GP Points'], kde = True,  hist = False, kde_kws={ "label": 'Group Position Points', 'color': 'red'})
    sns.distplot(final_table['SR Points'], kde = True, hist = False, kde_kws={ "label": 'Second Round Points', 'color': 'royalblue'})
    sns.distplot(final_table['Quarter Points'],   kde = True, hist = False, kde_kws={ "label": 'Quarter Final Points', 'color': 'green'})
    sns.distplot(final_table['Total Points'], kde = True, hist = False, kde_kws={ "label": 'Total Points', 'color': 'gold'} )
    plt.xlabel("Points")
    plt.ylabel("Density")
    plt.xticks(np.arange(0,140, 10))
    plt.title('Distribution of Results')
#    plt.savefig('C:\\Users\\walshn4\\Desktop\\Worldcuppool\\Distribution of Results 2.png', dpi = 300)
    
    
    # We convert the winnners list to a data frame and count values, then graph a bar plot
#    winners = pd.DataFrame( pd.Series(final_winners).value_counts().reset_index())
#    winners.columns = ['Team name', 'Count']
#    sns.barplot(x = 'Team name', y = 'Count', data = winners, palette = "RdYlBu")
#    plt.title('Winner Predictions')
#    plt.xlabel("")
#    plt.xticks(rotation=45)
#    plt.tight_layout()
 #   plt.savefig('C:\\Users\\walshn4\\Desktop\\Worldcuppool\\Winner Predictions.png', dpi = 300)
    
 
#    playoff_winners = pd.DataFrame( pd.Series(playoff_winners).value_counts().reset_index())
#    playoff_winners.columns = ['Team name', 'Count']
#    sns.barplot(x = 'Team name', y = 'Count', data = playoff_winners, palette = "RdYlBu")
#    plt.title('Playoff Winner Predictions')
#    plt.xlabel("")
#    plt.xticks(rotation=45)
#    plt.tight_layout()
    
def my_main():
    # Select the directory and the extension
    directory = "C:\\Users\\walshn4\\Desktop\\Worldcuppool\\Entrants"
    extension = "csv"

    # call hte function to get results
    get_results(directory, extension)

# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    my_main()

