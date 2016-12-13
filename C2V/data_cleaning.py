import regex #import this because it supports infinite window lookback

#FUNCTIONS FOR DATA CLEANING

def strip_html(dictionary):
    '''Ingets a dictionary that contains a 'text' key and alters the 'text' value
    to be a cleaned version of the text without the USPTO website junk. Returns a clean dictionary object'''
    #get the speakers name for the regex
    speaker = dictionary['speaker']
    name_pattern = regex.compile(r'(Mrs|Ms|Dr|Sr|Mr)\s([A-Z]*\s?[A-Z]*)') #matches title, optional first and mandatory last name
    name_match = name_pattern.match(speaker)
    
    #we don't assume that the match was successful
    if name_match: 
        title, name = name_match.groups()

    #use the regex groups returned from above to extract text
    text_pattern = regex.compile('(?:[^\(]'+ title +'\.?\s?'+ name +':?)(.*)(?:[_]*<\/pre>)')
    
    #run the regex after removing newline characters
    #NOTE: must use "re.search" because match only looks in the begning of a string
    text_match = text_pattern.search(dictionary['text'].replace('\n',''))
    if text_match:
        text = text_match.groups()[0] #should only return a single object of text 
        
    #in the chance that this doc actually didn't have a speach in it 
    try:
        dictionary['text'] = text
        
    except:
        print('#####LOG OF IGNORED#####',dictionary['text'],'#####END LOG OF IGNORED#####')
        dictionary['text'] = ''
        
    return dictionary

def detect_protocol(text):
    '''Ingets a string and returns whether or not the text is protocol speach'''
    #complie a regex that looks for protocol
    protocol_pattern = regex.compile(r'(H.R.\s[0-9]*.\s*Congress\s*has\s*the\s*power\s*to)') #matches title, optional first and mandatory last name
    protocol_match = protocol_pattern.search(text)
    
    if protocol_match:
        return True
    else:
        return False    

def strip_states(text):
    '''Ingets a string and returns a clean version of the text with the state/congress name stripped out'''
    #get list of US states/territories
    states = [str(state) for state in us.states.STATES_AND_TERRITORIES]
    #complie a regex
    state_pattern = regex.compile('|'.join(['([\s*\w]*of\s*'+state+'[:.])' for state in states]))
    
    new_text = state_pattern.sub('',text)
    
    if len(new_text) > 0:
        return new_text
    else:
        #this means we've cut out too much
        return text        

def replace_underscore(text):
    '''Strips out underscore from string'''
    #compile the underscore regex
    underscore_pattern = regex.compile(r'(_)')
    
    new_text = underscore_pattern.sub('',text)
    return new_text

def clean_numbers(text):
    '''Strips out underscore from string'''
    #compile pattern for stripping out page number from the text:
    page_n_pattern = regex.compile(r'(\[\[Page\s[a-zA-Z0-9]*\]\])')
    text = page_n_pattern.sub(' ',text)
    
    #take bill names and fix them as entities so that in the creation of the bag
    #of words they aren't turned in to numbers:        
    bill_pattern = regex.compile(r'H.R.\s[0-9]*.?')
    text = bill_pattern.sub(lambda x: ' HR' + x.group()[5:] + ' ', text)  
        
    hres_pattern = regex.compile(r'\sH.\s?Res.\s?(\d{1,}).?')
    text = hres_pattern.sub(lambda x: ' HRES' + x.group()[9:] + ' ', text)        
        
    #we also want to capture resolutions (Ex/H.J. Res. 43.)    
    hjres_pattern = regex.compile(r'(H.J.\sRes.)\s([0-9]*).?')
    text = hjres_pattern.sub(lambda x: ' HJRES' + x.group()[10:] + ' ', text)   
        
    #strip timestamp out of text:
    time_pattern = regex.compile(r'({time}\s*[0-9]{4})')
    text = time_pattern.sub(' ',text)
    
    #strip pagenumber 
    page_pattern = regex.compile(r'(pp.\s?[0-9]*\s?[0-9]{0,5})')
    text = page_pattern.sub(' ',text)    
    
    #replace any reference to dollar amount with MNY tag
    dollar_pattern = regex.compile(r'(\$\d*\.?\d+)')
    text = dollar_pattern.sub(' MNY ',text) 
    
    #replace any reference to years amount with YR tag
    year_pattern = regex.compile(r'\s([1-2][0-9]{3})\s?')
    text = year_pattern.sub(' YR ',text) 
    
    legis_pattern = regex.compile(r'(?<=[Aa]rticle|[Cc]lause|[Ss]ection)\s(\d|IX|IV|V?I{0,3})')
    text = legis_pattern.sub(' ', text)
        
    #capture left-over meaningless number junk and put into a single bucket:
    number_pattern = regex.compile(r'(\s\d*\.?-?\/?\d+)')
    #leave this in because one party might be more numbers-driven
    text = number_pattern.sub(' QNTY ',text) 
    
    return text

def clean_beginning(text):
    '''Noticed that there was a residual issue with the begining of some text strings. 
    This regex deals with the issue'''
    #compile pattern for stripping out page number from the text:
    beg_pattern = regex.compile(r'^(\s*[a-z][A-Z]{2,}[.:])')
    text = beg_pattern.sub('',text)
    return text    


