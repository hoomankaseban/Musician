# Programmer: Hooman Kaseban
# Step By Step of Goals...
# Code a program which takes a simple (in further steps, signatured scales) Scale Name and generates Suitable notes for creating Major (all scale forms) scale.
# ...takes the scale name, then generates all complete Cadances of it.
# ...takes the scale neme, then gererates all types of Cadances of it.
# finally, I can go for mapping the scales on guitar board.

# This takes a note and desired scale form then, returns its scale in the desired form. 
def scaler(scale,form):
    Cmaj=["C","D","E","F","G","A",'B'] # Cmajor chord notes (using in giving priorities).
    # Cmajor distances (natural distance between notes), crucial for finding distances in any scale.
    natural_pattern_prior={('C','D'):1 , ('D','E'):1 , ('E','F'):0.5 , ('F','G'):1 , ('G','A'):1 , ('A','B'):1 , ('B','C'):0.5 }
    # this dict will include the scale distances.
    natural_pattern={}
    # handling scales with signatures ('b's and '#'s).
    if len(scale)>1: 
        #Cmaj Update
        pure_note=scale[0]
        signature=scale[1]
        Cmaj[Cmaj.index(pure_note)]=scale    # a little trick :)
        # create a draft of scale distances based on standard distance pattern (Cmajor).
        # in further steps, it would be updated to the actual scale distances.
        for key,val in natural_pattern_prior.items():
            if key[0]==pure_note: # first note of tuple
                revised_scale_tuple=(key[0]+signature,key[1]) #create right appearence for that tuple
                # distance handling for signatures.
                if signature=='#': 
                    revised_tuple_distance=val-0.5
                else: # for 'b' signature...
                    revised_tuple_distance=val+0.5
                # fill the scale dict.
                natural_pattern[revised_scale_tuple]=revised_tuple_distance
            elif key[1]==pure_note: # second note of tuple
                revised_scale_tuple=(key[0],key[1]+signature) #create right appearence for that tuple
                if signature=='#': #distance handling for diez
                    revised_tuple_distance=val+0.5
                else: # for 'b' signature...
                    revised_tuple_distance=val-0.5
                # fill the scale dict.
                natural_pattern[revised_scale_tuple]=revised_tuple_distance
            else: #Nothings changed (exactly looks same as Cmaj distance)
                natural_pattern[key]=val
    else: #simple scale (without signatures)
        natural_pattern=natural_pattern_prior

    standard_major_distance=[1,1,0.5,1,1,1,0.5] # to create major form.
    natural_minor_distance=[1,0.5,1,1,0.5,1,1] # to create natural minor form.
    # harmonic_minor_distance=[1,0.5,1,1,0.5,1.5,1]
    # melodic_minor_distance=[1,0.5,1,1,1,1,0.5]

    # Decide which form should be used
    if form=='1':
        desired_form_pattern=standard_major_distance
    elif form=='2':
        desired_form_pattern=natural_minor_distance
    
    base_note_index=Cmaj.index(scale) 
    #Creating a draft of scale (sorted notes).
    scale_sorted_notes=Cmaj[base_note_index:].copy()
    scale_sorted_notes+=Cmaj[:base_note_index+1]
    #this loop works on finding the distance between the Note (it should be palced on the 1st location of the pattern) and the next one.
    #it finds the "Standard" pattern of distance
    #in further steps, code works on "actual" distance for desired form.
    natural_note_tuples=list(natural_pattern.keys())
    desired_scale={} # this is the answer! (wanted scale)
    for note_index in range(len(scale_sorted_notes)-1):
        current_note=scale_sorted_notes[note_index]
        next_note=scale_sorted_notes[note_index+1] #for further use in creating tuples...
        for pair_note in natural_note_tuples:
            #check if the note is 'lead' note in the tuple.
            if (current_note in pair_note) and (pair_note.index(current_note)==0):
                #create a draft of the scale distances based on the form pattern.
                desired_scale[(current_note,next_note)]=natural_pattern[pair_note] 
                break
            else:
                continue
    # Now I have a draft of scale distances based on the pattern on "desired_scale".
    # in the next step, I must adopt it...
    for tuples_priority_index in range(len(desired_form_pattern)):
        scale_note_tuples=list(desired_scale.keys()) # use list forms of dictionarys for making a loop on them. 
        current_tuple=scale_note_tuples[tuples_priority_index] # will be used for searching the scale distance in the dict    
        # "if" distances are equal : DO NOTHING
        # check wheather natural distance is equal with form distance.
        if desired_scale[current_tuple] == desired_form_pattern[tuples_priority_index]: 
            continue
        else: # have to use signatures
        # the change (signature move) is always append on the 2nd note and influences next tuple!
            difference = abs(desired_scale[current_tuple] - desired_form_pattern[tuples_priority_index])
            # check for # or b.
            if desired_scale[current_tuple] < desired_form_pattern[tuples_priority_index]:
                # add '#' to the 2nd note.
                desired_scale=update_scale(desired_scale,current_tuple,'#',tuples_priority_index,difference)
                
            else:
                # add "b" to the 2nd note.
                desired_scale=update_scale(desired_scale,current_tuple,'b',tuples_priority_index,difference)

    scale_notes=[]
    for tup in list(desired_scale.keys()):
        scale_notes.append(tup[0])
    return desired_scale,scale_notes # Now, it's complete!!
    


# function using in 'scaler' for applying #s and bs.
# this function returns signatured scale based on a mentioned tuple change.
def update_scale(scale_dict,current_tuple,signature,tuples_priority_index,difference): 
    scale_keys=list(scale_dict.keys())
    next_tuple=scale_keys[tuples_priority_index+1]
    updated_scale={} #the answer
    # process for 'b' signature
    if signature=='#':
        #first, update distances...
        scale_dict[current_tuple]+=difference
        scale_dict[next_tuple]-=difference
        # second, add '#' to the note
        alter_note=current_tuple[1] # select the 2nd note for making changes.
        difference=int(difference/0.5) #due to multiplying the number in signature sings (char type), I have to use integer.
        # this loop works on signature signs and applying them.
        for key,val in scale_dict.items(): 
            # only current tuple and the next would be updated by signatures
            # reminder: the note with signature is placed in 2nd and 1st of the current tuple and the next tuple respectively.
            if key==current_tuple: # check if it's turn to apply signature on the current tuple. (to update 'key')
                # transform to 'list' type for making changes.
                key=list(key) 
                # allow to insert multiple '#' if it needs! example: D#major
                key[1]=key[1]+'#'*difference 
                # in this stage, I wanna handle 'double diezes(##)' or 'multiple ones'
                # I don't know if this might cause a problem but, I didn't handle '#b' or inverse! 
                # hope to not face with that challenge :)
                if (len(key[1])==2) and (key[1][0]=='E' or key[1][0]=='B'): #check for B# and E#
                        if key[1][0]=='B':
                            key[1]='C'
                        else:
                            key[1]='F'
                # check for notes with "more" than 2 signatures. example: G##
                if len(key[1])>2:
                    Cmaj=['C','D','E','F','G','A','B']
                    complex_note=key[1]
                    pure_note=complex_note[0]
                    pure_note_index=Cmaj.index(pure_note)
                    signatures=complex_note[1:]
                    # for 'E' and 'B', by one #, the note goes 1 level up.
                    if pure_note=='E' or pure_note=='B':
                        signatures=signatures[:-1] #removing last signature. 
                        # replace by the higher note.
                        if pure_note=='B':
                            pure_note='C'
                        else:
                            pure_note='F'
                    else: # for other notes, by two #, the note goes 1 level up.
                        #removing two last signatures.
                        signatures=signatures[:-2] 
                        # replace by the higher note.
                        pure_note=Cmaj[pure_note_index+1]
                    #replace new shape of note. (optimized shape)
                    key[1]=pure_note+signatures
                #transform again to tuple for using in Dict (list type can't be placed as "key" in dict).
                key=tuple(key)
            elif key==next_tuple: # check if it's turn to apply signature on the next tuple. (to update 'key')
                # transform to 'list' type for making changes.
                key=list(key)
                # allow to insert multiple '#' if it needs! example: D#major
                key[0]=key[0]+'#'*difference
                # in this stage, I wanna handle 'double diezes(##)' or 'multiple ones'
                # I don't know if this might cause a problem but, I didn't handle '#b' or inverse! 
                # hope to not face with that challenge :)
                if len(key[0])==2 and (key[0][0]=='E' or key[0][0]=='B'): #check for B# and E#
                        if key[0][0]=='B':
                            key[0]='C'
                        else:
                            key[0]='F'
                # check for notes with "more" than 2 signatures. example: G##
                if len(key[0])>2:
                    Cmaj=['C','D','E','F','G','A','B']
                    complex_note=key[0]
                    pure_note=complex_note[0]
                    pure_note_index=Cmaj.index(pure_note)
                    signatures=complex_note[1:]
                    # for 'E' and 'B', by one #, the note goes 1 level up.
                    if pure_note=='E' or pure_note=='B': #removing last signature. 
                        # replace by the higher note.
                        signatures=signatures[:-1]
                        if pure_note=='B':
                            pure_note='C'
                        else:
                            pure_note='F'
                    else: # for other notes, by two #, the note goes 1 level up.
                        #removing two last signatures.
                        signatures=signatures[:-2]
                        # replace by the higher note.
                        pure_note=Cmaj[pure_note_index+1]
                    #replace new shape of note. (optimized shape)
                    key[0]=pure_note+signatures
                #transform again to tuple for using in Dict (list type can't be placed as "key" in dict).
                key=tuple(key)
            # at the end, fill the answer dict.
            updated_scale[key]=val 

    else: # process for 'b' signature
        #first, update distances...
        scale_dict[current_tuple]-difference
        scale_dict[next_tuple]+=difference #due to multiplying the number in signature sings (char type), I have to use integer.
        # this loop works on signature signs and applying them.
        difference=int(difference/0.5)
        # second, add 'b' to the note
        alter_note=current_tuple[1] # select the 2nd note for making changes.
        for key,val in scale_dict.items():
            # only current tuple and the next would be updated by signatures
            # reminder: the note with signature is placed in 2nd and 1st of the current tuple and the next tuple respectively.
            if key==current_tuple: # check if it's turn to apply signature on the current tuple. (to update 'key')
                # transform to 'list' type for making changes.
                key=list(key)
                # allow to insert multiple 'b' if it needs! example: Dbmajor
                key[1]=key[1]+'b'*difference
                # in this stage, I wanna handle 'double bemols(bb)' or 'multiple ones'
                # I don't know if this might cause a problem but, I didn't handle '#b' or inverse! 
                # hope to not face with that challenge :)
                if len(key[1])==2: #check for Cb and Fb
                        if key[1][0]=='C':
                            key[1]='B'
                        if key[1][0]=='F':
                            key[1]='E'
                # check for notes with "more" than 2 signatures. example: Gbb
                if len(key[1])>2:
                    Cmaj=['C','D','E','F','G','A','B']
                    complex_note=key[1]
                    pure_note=complex_note[0]
                    pure_note_index=Cmaj.index(pure_note)
                    signatures=complex_note[1:]
                    # for 'F' and 'C', by one b, the note goes 1 level down.
                    if pure_note=='F' or pure_note=='C':
                        #removing last signature. 
                        signatures=signatures[:-1] 
                        # replace by the lower note.
                        if pure_note=='C':
                            pure_note='B'
                        else:
                            pure_note='E'
                    else:
                        #removing two last signatures.
                        signatures=signatures[:-2]
                        # replace by the lower note.
                        pure_note=Cmaj[pure_note_index-1]
                    #replace new shape of note. (optimized shape)
                    key[1]=pure_note+signatures
                #transform again to tuple for using in Dict (list type can't be placed as "key" in dict).
                key=tuple(key)
            elif key==next_tuple: # check if it's turn to apply signature on the next tuple. (to update 'key')
                # transform to 'list' type for making changes.
                key=list(key)
                # allow to insert multiple 'b' if it needs! example: Dbmajor
                key[0]=key[0]+'b'*difference
                # in this stage, I wanna handle 'double diezes(##)' or 'multiple ones'
                # I don't know if this might cause a problem but, I didn't handle '#b' or inverse! 
                # hope to not face with that challenge :)
                if len(key[0])==2: #check for Cb and Fb
                        if key[0][0]=='C':
                            key[0]='B'
                        if key[0][0]=='F':
                            key[0]='E'
                # check for notes with "more" than 2 signatures. example: Gbb
                if len(key[0])>2:
                    Cmaj=['C','D','E','F','G','A','B']
                    complex_note=key[0]
                    pure_note=complex_note[0]
                    pure_note_index=Cmaj.index(pure_note)
                    signatures=complex_note[1:]
                    # for 'F' and 'C', by one b, the note goes 1 level down.
                    if pure_note=='F' or pure_note=='C':
                        #removing last signature. 
                        signatures=signatures[:-1]
                        # replace by the lower note.
                        if pure_note=='C':
                            pure_note='B'
                        else:
                            pure_note='E'
                    else:
                        #removing 2 last signatures. 
                        signatures=signatures[:-2]
                        # replace by the lower note.
                        pure_note=Cmaj[pure_note_index-1]
                    #replace new shape of note. (optimized shape)
                    key[0]=pure_note+signatures
                #transform again to tuple for using in Dict (list type can't be placed as "key" in dict).
                key=tuple(key)
            # at the end, fill the answer dict.
            updated_scale[key]=val
    return updated_scale

def display(desired_scale,scale_notes,scale_name,form):
    if form=='1':
        scale_form_name='Major'
    elif form=='2':
        scale_form_name='Minor'
    print(f'"{scale_name}" {scale_form_name} with distances is:\n {desired_scale}')
    #printing notes of the scale...
    print(f'{scale_name} Major notes would be:\n{scale_notes}')

def interface():
    scale= input('Please enter your desired note: \n')
    task= input('Please specify your desired scale: \n1-Major     2-Minor \n')
    scale_with_distance,scale_notes= scaler(scale,task)
    display(scale_with_distance,scale_notes,scale,task)
    
# With this function, I can find all chords of the scale.
def scale_harmonization():# for now, I don't insert any factors in the function call due to tests...
    scale_distances,scale_notes=scaler("D","1")
    # D major "scale_distances":
    # {('D', 'E'): 1, ('E', 'F#'): 1.0, ('F#', 'G'): 0.5, ('G', 'A'): 1, ('A', 'B'): 1, ('B', 'C#'): 1.0, ('C#', 'D'): 0.5}
    # D major "scale_notes":
    # ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']
    # create a list which contains difference of (standard thirds or fifth with real ones.)
    # this helps to specify the type of the chord (major,minor,aug,dim).
    thirds=[]
    fifth=[]
    # should put a loop over all notes from begain in sort.
    # in each time should create an scale dict using circular loop
    # (don't use "scaler" because I want prior distances) without any changes.
    # then I calculate differences of the distances and append them to the lists.
    
    # chord quality rule

    # by a circular loop, I want to calculate third and fifth degree distances of all notes of the scale (Music Theory!)
    for base_note in scale_notes:
        one_octave={} # it will contain an octave begain with the selected note. 
        #finding the starter tuple
        for key in scale_distances.keys():
            if base_note in key[0]:
                base_tup=key
                break
        # achieve the octave using circular loop
        tup_list=list(scale_distances.keys())
        i=tup_list.index(base_tup)
        while True:
            one_octave[tup_list[i]]=scale_distances[tup_list[i]]
            i = (i+1) % len(tup_list)
            if tup_list[i]==base_tup:
                break
    

    # hint!
    # use a function called "chord quality" which takes an octave
    # it returns wheather it's Major,Minor,etc.
        
scale_harmonization()

#this function should return the quality of the chord(Major,minor,augmented,and diminished)
def chord_qiality(octave):
    #tertian Harmony :
    # Major = major third + perfect fifth
    # Minor = minor third + perfect fifth
    # Augmented = major third + augmented fifth
    # Diminished = minor third + diminished 
    third={2:'major',2.5:'minor'}
    fifth={3.5:'perfect',3:'diminished',4:'augmented'}
    counter=0
    tone=0
    third_form=''
    fifth_form=''
    for dist in octave.val():
        tone+=dist
        #check for 'third degree'
        if counter==2:
            third_form=third[tone]
        #check for 'fifth degree'
        if counter==4:
            fifth_form=fifth[tone]
            break
        counter+=1
    # specify the quality of the chord
    quality={('major','perfect'):'maj',('minor','perfect'):'minor',('major','augmented'):'aug',('minor','diminished'):'dim'}
    chord_signature=quality[(third_form,fifth_form)]     
    return chord_signature   

        


        

    






        

 
#interface() 
# It's great! I handled multiple diezs(bemols) and diezed(bemoled) notes as scales
# I have handled multiple diezes and bemols for moving notes (if it's possible!) and have a standard shape of scale.
# but, I have to move forward!!!
# as the next stage, I can work on adding other forms of scales (such Minor, Harmonics or Melodics and etc.).
# I have SERIOUS probelms with "harmonic" and "melodic (should Consider DIMINISHED and AUGMENTED). (for now, I skipped)
# and in the further step, I can work on Cadences...
# for creating cadences, first I have to calculate each scales' chords then, I can go for cadences...

# a={'a':1,'b':2,'c':3}
# start='b'
# li=list(a.keys())
# i=li.index(start)
# while True:
#     print(a[li[i]])
#     i=(i+1) % len(li)

#     if (li[i]==start):
#         break

