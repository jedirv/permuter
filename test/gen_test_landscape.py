'''
Created on Dec 31, 2013

@author: admin-jed
'''
import shutil
import os
#trials:2
#permute:number=1 3
#permute:letter=AAA,BBB
#permute:singleton_val=300
#permute:animal=dog,cat
#concise_print:animal,an
#concise_print:letter,l
#concise_print:singleton_val,s
#concise_print:resolution,res
#concise_print:AAA,aa
#concise_print:BBB,bb
#scores_permute:resolution=userDay,userMonth
def main():
    dir = '/nfs/stak/students/i/irvine/python/cluster/test/sample_results/unittest'
    if os.path.isdir(dir):
        shutil.rmtree(dir)
    trials = ['1','2']
    # rm for result_map
    rm = {}
    #userDay
    #    trial1
    #         animal
    rm['trial1_userDay_cat'] = '1'
    rm['trial1_userDay_dog'] = '2'
    #        letter
    rm['trial1_userDay_aa'] = '1'
    rm['trial1_userDay_bb'] = '2'
    #        number
    rm['trial1_userDay_1'] = '1'
    rm['trial1_userDay_2'] = '2'
    rm['trial1_userDay_3'] = '3'
    #        singleton_val
    rm['trial1_userDay_300'] = '1'
        
    #    trial2
    #        animal
    rm['trial2_userDay_cat'] = '5'
    rm['trial2_userDay_dog'] = '6'
    #        letter
    rm['trial2_userDay_aa'] = '1'
    rm['trial2_userDay_bb'] = '2'
    #        number
    rm['trial2_userDay_1'] = '1'
    rm['trial2_userDay_2'] = '2'
    rm['trial2_userDay_3'] = '3'
    #singleton_val
    rm['trial2_userDay_300'] = '1'
    
    #userMonth
    #    trial1
    #         animal
    rm['trial1_userMonth_cat'] = '3'
    rm['trial1_userMonth_dog'] = '4'
    #        letter
    rm['trial1_userMonth_aa'] = '1'
    rm['trial1_userMonth_bb'] = '2'
    #        number
    rm['trial1_userMonth_1'] = '1'
    rm['trial1_userMonth_2'] = '2'
    rm['trial1_userMonth_3'] = '3'
    #        singleton_val
    rm['trial1_userMonth_300'] = '1'
        
    #    trial2
    #        animal
    rm['trial2_userMonth_cat'] = '7'
    rm['trial2_userMonth_dog'] = '8'
    #        letter
    rm['trial2_userMonth_aa'] = '1'
    rm['trial2_userMonth_bb'] = '2'
    #        number
    rm['trial2_userMonth_1'] = '1'
    rm['trial2_userMonth_2'] = '2'
    rm['trial2_userMonth_3'] = '3'
    #        singleton_val
    rm['trial2_userMonth_300'] = '1'
    os.mkdir(dir)
    for trial in trials:
        trialdir =  "{0}/trial{1}".format(dir,trial)
        os.mkdir(trialdir)
        animals = ['cat','dog']
        letters = ['aa','bb']
        numbers =['1','2','3']
        singleton_values = ['300']
        for animal in animals:
            for letter in letters:
                for number in numbers:
                    for singleton_value in singleton_values:
                        permutation_dir = "{0}/an_{1}_l_{2}_number_{3}_s_{4}".format(trialdir,animal,letter,number, singleton_value)
                        os.mkdir(permutation_dir)
                        userDayPath = "{0}/userDay.csv".format(permutation_dir)
                        userMonthPath = "{0}/userMonth.csv".format(permutation_dir)
                        
                        userDayFile = open(userDayPath,'w')
                        #foo,auc,bar
                        userDayFile.write("foo,auc,bar\n")
                        #x,0.512,y'
                        animal_key = "trial{0}_userDay_{1}".format(trial, animal)
                        letter_key = "trial{0}_userDay_{1}".format(trial, letter)
                        number_key =  "trial{0}_userDay_{1}".format(trial, number)
                        singleton_key = "trial{0}_userDay_{1}".format(trial, singleton_value)
                        userDayFile.write("x,{0}{1}{2}{3},y\n".format(rm[animal_key],rm[letter_key],rm[number_key],rm[singleton_key],))
                        #na,nb,nc
                        userDayFile.write("na,nb,nc\n")
                        userDayFile.close()
                        
                        userMonthFile = open(userMonthPath,'w')
                        #foo,auc,bar
                        userMonthFile.write("foo,auc,bar\n")
                        #x,0.512,y'
                        animal_key = "trial{0}_userMonth_{1}".format(trial, animal)
                        letter_key = "trial{0}_userMonth_{1}".format(trial, letter)
                        number_key =  "trial{0}_userMonth_{1}".format(trial, number)
                        singleton_key = "trial{0}_userMonth_{1}".format(trial, singleton_value)
                        userMonthFile.write("x,{0}{1}{2}{3},y\n".format(rm[animal_key],rm[letter_key],rm[number_key],rm[singleton_key],))
                        #na,nb,nc
                        userMonthFile.write("na,nb,nc\n")
                        userMonthFile.close()
                        

    
if __name__ == '__main__':
    main()
    